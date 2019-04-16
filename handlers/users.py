import json
from lib.auth import jwtauth
from bson import json_util
from bson.json_util import dumps
from handlers.base import BaseHandler
from lib.DBConnection import UserFunctions

import logging
logger = logging.getLogger('rishacar.' + __name__)

@jwtauth
class UsersHandler(BaseHandler):
  async def get(self, id):
    if id:
      userFunc = UserFunctions()
      result = await userFunc.getUser(id = id)
      if result:
        self.write(json_util.dumps(result))
      else:
        self.set_status(500)
        self.write({"message":"database error"})
        self.finish()
    else:
      self.set_status(400)
      self.write({"message":"missing id"})
      self.finish()
  
  async def put(self, id):
    if id:
      if self.request.body:
        data = json.loads(self.request.body)
        userFunc = UserFunctions()
        result = await userFunc.updateUser(id, data)
        self.write({"message":"user updated"})
      else:
        self.set_status(400)
        self.write({"message":"missing data"})
        self.finish()
    else:
      self.set_status(400)
      self.write({"message":"missing id"})
      self.finish()

  async def delete(self, id):
    if id:
      userFunc = UserFunctions()
      result = await userFunc.deleteUser(id)
      self.write({"message":"user deleted"})
    else:
      self.set_status(400)
      self.write({"message":"missing id"})
      self.finish()
