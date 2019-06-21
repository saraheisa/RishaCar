import json
from lib.auth import jwtauth
from bson import json_util
from bson.json_util import dumps
from handlers.base import BaseHandler
from lib.DBConnection import UserFunctions
from cryptography.fernet import Fernet

import logging
logger = logging.getLogger('rishacar.' + __name__)

@jwtauth
class UsersHandler(BaseHandler):
  async def get(self, id):
    # get other users' data
    if id:
      userFunc = UserFunctions()
      result = await userFunc.getUser(id=id)
      if result:
        result['_id'] = str(result['_id'])
        del result['password']
        self.write(json_util.dumps(result))
        self.set_header('Content-Type', 'application/json')
        self.finish()
      else:
        self.set_status(500)
        self.write({"message":"database error"})
        self.finish()
    # get the user's data
    else:
      if self.request.body:
        data = json.loads(self.request.body)
        if data['id']:
          id = data['id']
          userFunc = UserFunctions()
          result = await userFunc.getUser(id=id)
          if result:
            result['_id'] = str(result['_id'])
            del result['password']
            self.write(json_util.dumps(result))
            self.set_header('Content-Type', 'application/json')
            self.finish()
          else:
            self.set_status(500)
            self.write({"message":"database error"})
            self.finish()
        else:
          self.set_status(400)
          self.write({"message":"missing id"})
          self.finish()
      else:
        self.set_status(400)
        self.write({"message":"missing id"})
        self.finish()
  
  async def put(self, id):
    if self.request.body:
      data = json.loads(self.request.body)
      if data['id']:
        id = data['id']
        userFunc = UserFunctions()
        del data['id']
        result = await userFunc.updateUser(id, data)
        if result:
          self.write({"message":"user updated"})
        else:
          self.set_status(500)
          self.write({"message":"database error"})
          self.finish()
      else:
        self.set_status(400)
        self.write({"message":"missing id"})
        self.finish()
    else:
      self.set_status(400)
      self.write({"message":"missing data"})
      self.finish()

  async def delete(self, id):
    if self.request.body:
      data = json.loads(self.request.body)
      if 'id' in data:
        if 'password' in data:
          id = data['id']
          password = data['password']
          userFunc = UserFunctions()
          user = await userFunc.getUser(id=id)
          key = b'i102LDEGa-8PLuZJ9kw-VR2VKCeYxOanZvM4KQAZLt8='
          user['password'] = self.decrypt(key, bytes(user['password'], 'utf-8')).decode("utf-8")
          if user['password'] == data['password']:
            result = await userFunc.deleteUser(id)
            if result:
              self.write({"message":"user deleted"})
            else:
              self.set_status(500)
              self.write({"message":"database error"})
              self.finish()
          else:
            self.set_status(400)
            self.write({"message":"wrong password"})
            self.finish()
        else:
          self.set_status(400)
          self.write({"message":"missing password"})
          self.finish()
      else:
        self.set_status(400)
        self.write({"message":"missing id"})
        self.finish()
    else:
      self.set_status(400)
      self.write({"message":"missing data"})
      self.finish()

  def decrypt(self, key, text):
    cipher_suite = Fernet(key)
    return (cipher_suite.decrypt(text))
