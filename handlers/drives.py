import json
from lib.auth import jwtauth
from bson import json_util
from bson.json_util import dumps
from handlers.base import BaseHandler
from lib.DBConnection import DriveFunctions

import logging
logger = logging.getLogger('rishacar.' + __name__)

@jwtauth
class DrivesHandler(BaseHandler):
  async def get(self, id):
    driveFunc = DriveFunctions()
    if id:
      result = await driveFunc.getDrive(id)
    elif self.request.body:
      data = json.loads(self.request.body)
      result = await driveFunc.getFilteredDrives(data)
    else:
      result = await driveFunc.getDrives()

    if result:
      self.write(json_util.dumps(result))
    else:
      self.set_status(500)
      self.write({"message":"database error"})
      self.finish()

  async def post(self,_):
    if self.request.body:
      data = json.loads(self.request.body)
      driveFunc = DriveFunctions()
      result = await driveFunc.insertDrive(data)
      print(result)
      if result:
        self.write({"message":"drive added successfully"})
      else:
        self.set_status(500)
        self.write({"message":"database error"})
        self.finish()
    else:
      self.set_status(400)
      self.write({"message":"missing data"})
      self.finish()

  async def delete(self, id):
    if id:
      driveFunc = DriveFunctions()
      result = await driveFunc.deleteDrive(id)
      print(result)
      if result:
        self.write({"message":"drive deleted successfully"})
      else:
        self.set_status(500)
        self.write({"message":"database error"})
        self.finish()
    else:
      self.set_status(400)
      self.write({"message":"missing data"})
      self.finish()

  async def put(self, id):
    if id:
      if self.request.body:
        data = json.loads(self.request.body)
        driveFunc = DriveFunctions()
        result = await driveFunc.updateDrive(id, data)
        if result:
          self.write({"message":"updated"})
        else:
          self.set_status(500)
          self.write({"message":"database error"})
          self.finish()
      else:
        self.set_status(400)
        self.write({"message":"missing data"})
        self.finish()
    else:
      self.set_status(400)
      self.write({"message":"missing data"})
      self.finish()
