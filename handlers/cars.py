import json
import logging
from bson import json_util
from lib.auth import jwtauth
from handlers.base import BaseHandler
from lib.DBConnection import CarFunctions

logger = logging.getLogger('rishacar.' + __name__)

@jwtauth
class CarsHandler(BaseHandler):
  async def get(self, id):
    carFunc = CarFunctions()
    # get a car by id
    if id:
      result = await carFunc.getCar(id)
      result['_id'] = str(result['_id'])
      self.write(json_util.dumps(result))
      self.set_header('Content-Type', 'application/json')
      self.finish()
    # get filtered cars
    elif self.request.body:
      data = json.loads(self.request.body)
      result = await carFunc.getFilteredCars(data)
    # get all cars
    else:
      result = await carFunc.getCars()
    if result:
      self.write(json_util.dumps(super(CarsHandler, self).listToDict(result)))
      self.set_header('Content-Type', 'application/json')
      self.finish()
    else:
      self.set_status(500)
      self.write({"message":"database error"})
      self.set_header('Content-Type', 'application/json')
      self.finish()

  async def post(self, _):
    if self.request.body:
      data = json.loads(self.request.body)
      if self.verify_data(data):
        carFunc = CarFunctions()
        result = await carFunc.insertCar(data)
        if result:
          self.write({"message":"car added successfully"})
          self.set_header('Content-Type', 'application/json')
          self.finish()
        else:
          self.set_status(500)
          self.write({"message":"database error"})
          self.set_header('Content-Type', 'application/json')
          self.finish()
      else:
        self.set_status(400)
        self.write({"message":"missing some data"})
        self.set_header('Content-Type', 'application/json')
        self.finish()
    else:
      self.set_status(400)
      self.write({"message":"missing data"})
      self.set_header('Content-Type', 'application/json')
      self.finish()

  async def delete(self, id):
    if id:
      if self.request.body:
        data = json.loads(self.request.body)
        if 'userId' in data:
          carFunc = CarFunctions()
          result = await carFunc.getCar(id)
          if result:
            if result['userId'] == data['userId']:
              result = await carFunc.deleteCar(id)
              if result:
                self.write({"message":"car was deleted successfully"})
                self.set_header('Content-Type', 'application/json')
                self.finish()
              else:
                self.set_status(500)
                self.write({"message":"database error"})
                self.set_header('Content-Type', 'application/json')
                self.finish()
            else:
              self.set_status(400)
              self.write({"message":"wrong userId"})
              self.set_header('Content-Type', 'application/json')
              self.finish()
          else:
            self.set_status(400)
            self.write({"message":"car not found"})
            self.set_header('Content-Type', 'application/json')
            self.finish()
        else:
          self.set_status(400)
          self.write({"message":"missing userId"})
          self.set_header('Content-Type', 'application/json')
          self.finish()
      else:
        self.set_status(400)
        self.write({"message":"missing data"})
        self.set_header('Content-Type', 'application/json')
        self.finish()
    else:
      self.set_status(400)
      self.write({"message":"missing car id"})
      self.set_header('Content-Type', 'application/json')
      self.finish()

  async def put(self, id):
    if id:
      if self.request.body:
        data = json.loads(self.request.body)
        if data['userId']:
          carFunc = CarFunctions()
          # making sure of the userId so not anyone update the car but its owner
          result = await carFunc.getCar(id)
          # if there is no result then the car doesn't exist
          if result:
            if result['userId'] == data['userId']:
              result = await carFunc.updateCar(id, data)
              if result:
                self.write({"message":"updated"})
                self.set_header('Content-Type', 'application/json')
                self.finish()
              else:
                self.set_status(500)
                self.write({"message":"database error"})
                self.set_header('Content-Type', 'application/json')
                self.finish()
            else:
              self.set_status(400)
              self.write({"message":"wrong userId"})
              self.set_header('Content-Type', 'application/json')
              self.finish()
          else:
            self.set_status(400)
            self.write({"message":"car not found"})
            self.set_header('Content-Type', 'application/json')
            self.finish()
        else:
          self.set_status(400)
          self.write({"message":"missing userId"})
          self.set_header('Content-Type', 'application/json')
          self.finish()
      else:
        self.set_status(400)
        self.write({"message":"missing data"})
        self.set_header('Content-Type', 'application/json')
        self.finish()
    else:
      self.set_status(400)
      self.write({"message":"missing car id"})
      self.set_header('Content-Type', 'application/json')
      self.finish()

  def verify_data(self, data):
    return 'userId' in data and 'carModel' in data and 'carMake' in data and 'carColor' in data and 'carPlateNumber' in data and 'isVerfifiedCar' in data and 'carLisenceNumber' in data
