import json
import logging
from bson import json_util
from lib.auth import jwtauth
from handlers.base import BaseHandler
from lib.DBConnection import DriveFunctions

logger = logging.getLogger('rishacar.' + __name__)

@jwtauth
class DrivesFilterHandler(BaseHandler):
  async def post(self):
    driveFunc = DriveFunctions()
    # get filtered rides
    if self.request.body:
      data = json.loads(self.request.body)
      result = await driveFunc.getFilteredDrives(data)
      if result:
        self.write(json_util.dumps(super(DrivesFilterHandler, self).listToDict(result)))
        self.set_header('Content-Type', 'application/json')
        self.finish()
      else:
        self.set_status(500)
        self.write({"message":"database error"})
        self.finish()
    else:
      self.set_status(500)
      self.write({"message":"missing data"})
      self.finish()
