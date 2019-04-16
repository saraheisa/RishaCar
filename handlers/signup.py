import json
from bson import json_util
from bson.json_util import dumps
from handlers.base import BaseHandler
from lib.DBConnection import UserFunctions

import logging
logger = logging.getLogger('rishacar.' + __name__)

class SignupHandler(BaseHandler):
  async def post(self):
    if self.request.body:
      data = json.loads(self.request.body)
      # todo: validate the data
      userFunc = UserFunctions()
      res = await userFunc.insertUser(data)
      if res:
        token = super(SignupHandler, self).jwtEncode()
        self.encoded = token
        response = {'token': self.encoded.decode('ascii')}
        self.write(response)
      else:
        self.write({'message': 'error happened'})
    else:
      self.set_status(400)
      self.write({"message":"data is missing"})
      self.finish()