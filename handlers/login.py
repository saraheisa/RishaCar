import json
import base64
import logging
from cryptography.fernet import Fernet
from bson import json_util
from bson.json_util import dumps
from handlers.base import BaseHandler
from lib.DBConnection import UserFunctions

logger = logging.getLogger('rishacar.' + __name__)


class LoginHandler(BaseHandler):
  async def post(self):
    if self.request.body:
      data = json.loads(self.request.body)
      user = ''
      if ('password' in data) & ('username' in data):
        userFunc = UserFunctions()
        user = await userFunc.getUser(username=data['username'])
      elif ('password' in data) & ('email' in data):
        userFunc = UserFunctions()
        user = await userFunc.getUser(email=data['email'])
      if user:
        key = b'i102LDEGa-8PLuZJ9kw-VR2VKCeYxOanZvM4KQAZLt8='
        user['password'] = self.decrypt(key, bytes(user['password'], 'utf-8')).decode("utf-8")
        if user['password'] == data['password']:
          token = super(LoginHandler, self).jwtEncode()
          self.encoded = token
          response = {'token': self.encoded.decode('ascii'), 'id': str(user['_id'])}
          self.write(response)
        else:
          self.set_status(400)
          self.write({"message":"wrong password"})
          self.finish()
      else:
        self.set_status(400)
        self.write({"message":"wrong data"})
        self.finish()
    else:
      self.set_status(400)
      self.write({"message":"data is missing"})
      self.finish()
  
  def decrypt(self, key, text):
    cipher_suite = Fernet(key)
    return (cipher_suite.decrypt(text))
