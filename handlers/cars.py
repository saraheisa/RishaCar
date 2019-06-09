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
      self.finish()
    # get filtered cars
    elif self.request.body:
      data = json.loads(self.request.body)
      result = await carFunc.getFilteredCars(data)
    # get all cars
    else:
      result = await carFunc.getCar()
    if result:
      self.write(json_util.dumps(super(CarsHandler, self).listToDict(result)))
    else:
      self.set_status(500)
      self.write({"message":"database error"})
      self.finish()

  async def post(self, _):
    if self.request.body:
      data = json.loads(self.request.body)
      if self.verify_data(data):
        carFunc = carFunctions()
        result = await carFunc.insertcar(data)
        if result:
          self.write({"message":"car added successfully"})
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
          carFunc = CarFunctions()
          result = await carFunc.getcar(id)
          if result:
            if result['userId'] == data['userId']:
              result = await carFunc.deleteCar(id)
              if result:
                self.write({"message":"car was deleted successfully"})
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
            self.write({"message":"car not found"})
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
      self.write({"message":"missing car id"})
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
            self.write({"message":"car not found"})
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
      self.write({"message":"missing car id"})
      self.finish()

  def verify_data(self, data):
    return data['userId'] and data['carModel'] and data['carMake'] and data['carColor'] and data['carPlateNumber'] and data['isVerfifiedCar'] and data['carLisenceNumber']
