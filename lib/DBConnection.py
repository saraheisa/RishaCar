import motor.motor_tornado
from bson import ObjectId

db = motor.motor_tornado.MotorClient('localhost', 27017).RichaCarDB

class UserFunctions:
  async def getUsers(self):
    global db
    collection = db.users
    cursor = collection.find()
    users = []
    for doc in await cursor.to_list():
      users.append(doc)
    return users

  async def insertUser(self, user):
    global db
    result = await db.users.insert_one(user)
    return result

  async def deleteUser(self, id):
    global db
    result = await db.users.delete_one({'_id': ObjectId(id)})
    return result

  async def updateUser(self, id, user):
    global db
    result = await db.users.update_one({'_id': ObjectId(id)}, {'$set': user}, False, True)
    return result

  async def getUser(self, username = '', email = '', id = ''):
    global db
    if username != '':
      user = await db.users.find_one({'username': username})
      return user
    elif email != '':
      user = await db.users.find_one({'email': email})
      return user
    else:
      user = await db.users.find_one({'_id': ObjectId(id)})
      return user

  async def getEmail(self, email):
    global db
    user = await db.users.find_one({'email': email})
    if user:
      return True
    else:
      return False


class DriveFunctions:
  async def getDrives(self):
    global db
    collection = db.drives
    cursor = collection.find()
    drives = []
    for doc in await cursor.to_list(10):
      drives.append(doc)
    return drives
  
  async def insertDrive(self, drive):
    global db
    result = await db.drives.insert_one(drive)
    return result
  
  async def deleteDrive(self, id):
    global db
    result = await db.drives.delete_one({'_id': ObjectId(id)})
    return result
  
  async def getDrive(self, id):
    global db
    result = await db.drives.find_one({'_id': ObjectId(id)})
    return result

  async def updateDrive(self, id, drive):
    global db
    result = await db.drives.update_one({'_id': ObjectId(id)}, {'$set': drive}, False, True)
    return result

  async def getFilteredDrives(self, f):
    global db
    collection = db.drives 
    cursor = collection.find(f)
    drives = []
    for doc in await cursor.to_list(10):
      drives.append(doc)
    return drives


class CarFunctions:
  async def getCars(self):
    global db
    collection = db.cars
    cursor = collection.find()
    cars = []
    for doc in await cursor.to_list(10):
      cars.append(doc)
    return cars
  
  async def insertCar(self, car):
    global db
    result = await db.cars.insert_one(car)
    return result
  
  async def deleteCar(self, id):
    global db
    result = await db.cars.delete_one({'_id': ObjectId(id)})
    return result
  
  async def getCar(self, id):
    global db
    result = await db.cars.find_one({'_id': ObjectId(id)})
    return result

  async def updateCar(self, id, car):
    global db
    result = await db.cars.update_one({'_id': ObjectId(id)}, {'$set': car}, False, True)
    return result

  async def getFilteredCars(self, f):
    global db
    collection = db.cars 
    cursor = collection.find(f)
    cars = []
    for doc in await cursor.to_list(10):
      cars.append(doc)
    return cars


class LinksFunctions:
  async def getLink(self, id):
    global db
    result = await db.forgetPasswordLinks.find_one({'linkID': id})
    return result
  
  async def insertLink(self, link):
    global db
    result = await db.forgetPasswordLinks.insert_one(link)
    return result
  
  async def deleteLink(self, id):
    global db
    result = await db.forgetPasswordLinks.delete_one({'linkID': id})
    return result
