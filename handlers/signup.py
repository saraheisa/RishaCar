import json
from bson import json_util
from bson.json_util import dumps
from bson import ObjectId
from handlers.base import BaseHandler
from lib.DBConnection import UserFunctions
from cryptography.fernet import Fernet
import logging

logger = logging.getLogger('rishacar.' + __name__)


class SignupHandler(BaseHandler):
  async def post(self):
    if self.request.body:
      data = json.loads(self.request.body)
      if self.verify_data(data):
        if not await self.email_exists(data['email']):
          key = b'i102LDEGa-8PLuZJ9kw-VR2VKCeYxOanZvM4KQAZLt8='
          cipher_password = self.encrypt(key, bytes(data['password'], 'utf-8'))
          data['password'] = cipher_password.decode("utf-8")
          userFunc = UserFunctions()
          res = await userFunc.insertUser(data)
          if res:
            _id = res.inserted_id
            token = super(SignupHandler, self).jwtEncode()
            self.encoded = token
            response = {'token': self.encoded.decode('ascii'), 'id': str(_id)}
            self.write(response)
          else:
            self.write({'message': 'error happened'})
        else:
          self.set_status(400)
          self.write({"message":"email exists"})
          self.finish()
      else:
        self.set_status(400)
        self.write({"message":"some data is missing"})
        self.finish()
    else:
      self.set_status(400)
      self.write({"message":"data is missing"})
      self.finish()

  def encrypt(self, key, text):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(text)
  
  def verify_data(self, data):
    return data['email'] and data['password'] and data['firstName'] and data['middleName'] and data['lastName'] and data['phoneNumber']

  async def email_exists(self, email):
    userFunc = UserFunctions()
    return await userFunc.getEmail(email)
