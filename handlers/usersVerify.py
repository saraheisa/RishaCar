import json
import re
from lib.auth import jwtauth
from bson import json_util
from bson.json_util import dumps
from handlers.base import BaseHandler
from lib.DBConnection import UserFunctions

import logging
logger = logging.getLogger('rishacar.' + __name__)

nationalIDPattern = '(2|3)[0-9][1-9][0-1][1-9][0-3][1-9](01|02|03|04|11|12|13|14|15|16|17|18|19|21|22|23|24|25|26|27|28|29|31|32|33|34|35|88)\d\d\d\d\d'

@jwtauth
class UsersVerifyHandler(BaseHandler):
  async def post(self):
    if self.request.body:
      data = json.loads(self.request.body)
      if self.verify_data(data):
        if re.match(nationalIDPattern, data['nationalID']) is not None:
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
          self.write({"message":"national id is wrong"})
          self.finish()
      else:
        self.set_status(400)
        self.write({"message":"some data is missing"})
        self.finish()
    else:
      self.set_status(400)
      self.write({"message":"data is missing"})
      self.finish()

  def verify_data(self, data):
    return 'id' in data and 'nationalID' in data and 'nationalIdImage' in data
