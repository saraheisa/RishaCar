import json
import logging
from bson import json_util
from lib.auth import jwtauth
from handlers.base import BaseHandler
from lib.DBConnection import DriveFunctions

logger = logging.getLogger('rishacar.' + __name__)

@jwtauth
class DrivesHandler(BaseHandler):
  async def get(self, id):
    driveFunc = DriveFunctions()
    # get a drive by id
    if id:
      result = await driveFunc.getDrive(id)
      result['_id'] = str(result['_id'])
      self.write(json_util.dumps(result))
      self.finish()
    # get filtered rides
    elif self.request.body:
      data = json.loads(self.request.body)
      result = await driveFunc.getFilteredDrives(data)
    # get all rides
    else:
      result = await driveFunc.getDrives()
    if result:
      self.write(json_util.dumps(super(DrivesHandler, self).listToDict(result)))
    else:
      self.set_status(500)
      self.write({"message":"database error"})
      self.finish()

  async def post(self, _):
    if self.request.body:
      data = json.loads(self.request.body)
      if self.verify_data(data):
        driveFunc = DriveFunctions()
        result = await driveFunc.insertDrive(data)
        if result:
          self.write({"message":"drive added successfully"})
        else:
          self.set_status(500)
          self.write({"message":"database error"})
          self.finish()
      else:
        self.set_status(400)
        self.write({"message":"missing some data"})
        self.finish()
    else:
      self.set_status(400)
      self.write({"message":"missing data"})
      self.finish()

  async def delete(self, id):
    if id:
      if self.request.body:
        data = json.loads(self.request.body)
        if 'userId' in data:
          driveFunc = DriveFunctions()
          result = await driveFunc.getDrive(id)
          if result:
            if result['userId'] == data['userId']:
              result = await driveFunc.deleteDrive(id)
              if result:
                self.write({"message":"drive deleted successfully"})
              else:
                self.set_status(500)
                self.write({"message":"database error"})
                self.finish()
            else:
              self.set_status(400)
              self.write({"message":"wrong userId"})
              self.finish()
          else:
            self.set_status(400)
            self.write({"message":"drive not found"})
            self.finish()
        else:
          self.set_status(400)
          self.write({"message":"missing userId"})
          self.finish()
      else:
        self.set_status(400)
        self.write({"message":"missing data"})
        self.finish()
    else:
      self.set_status(400)
      self.write({"message":"missing drive id"})
      self.finish()

  async def put(self, id):
    if id:
      if self.request.body:
        data = json.loads(self.request.body)
        if data['userId']:
          driveFunc = DriveFunctions()
          # making sure of the userId so not anyone update the drive but its owner
          result = await driveFunc.getDrive(id)
          # if there is no result then the drive doesn't exist
          if result:
            if result['userId'] == data['userId']:
              result = await driveFunc.updateDrive(id, data)
              if result:
                self.write({"message":"updated"})
              else:
                self.set_status(500)
                self.write({"message":"database error"})
                self.finish()
            else:
              self.set_status(400)
              self.write({"message":"wrong userId"})
              self.finish()
          else:
            self.set_status(400)
            self.write({"message":"drive not found"})
            self.finish()
        else:
          self.set_status(400)
          self.write({"message":"missing userId"})
          self.finish()
      else:
        self.set_status(400)
        self.write({"message":"missing data"})
        self.finish()
    else:
      self.set_status(400)
      self.write({"message":"missing drive id"})
      self.finish()

  def verify_data(self, data):
    return data['userId'] and data['to'] and data['from'] and data['rideStatus'] and data['date'] and data['time'] and data['carId'] and data['proposal']
