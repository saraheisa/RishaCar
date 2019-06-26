import json
import logging
from bson import json_util
from handlers.base import BaseHandler
from lib.DBConnection import DriveFunctions
from lib.DBConnection import UserFunctions

logger = logging.getLogger('rishacar.' + __name__)


class UserProviderHandler(BaseHandler):
  async def post(self):
    if self.request.body:
      data = json.loads(self.request.body)
      if 'email' in data:
        if await self.email_exists(data['email']):
          userFunc = UserFunctions()
          user = await userFunc.getUser(email=data['email'])
          if user:
            res = {"isExist":True, "provider":user['provider']}
            self.set_status(200)
            self.write(res)
            self.finish()
          else:
            self.set_status(500)
            self.write({"message":"database error"})
            self.finish()
        else:
          res = {"isExist":False}
          self.set_status(200)
          self.write(res)
          self.finish()
      else:
        self.set_status(400)
        self.write({"message":"missing email"})
        self.finish()
    else:
      self.set_status(400)
      self.write({"message":"missing data"})
      self.finish()

        
  async def email_exists(self, email):
    userFunc = UserFunctions()
    return await userFunc.getEmail(email)
