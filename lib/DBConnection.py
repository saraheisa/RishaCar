import motor.motor_tornado

# db = motor.motor_tornado.MotorClient('localhost', 27017).RichaCarDB
connection = motor.motor_tornado.MotorClient('mongodb://admin:aMtcr6Bi4xixhp2C4EK4mKerd@ds119996.mlab.com:19996/rishacar')
db  = connection.rishacar

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
    result = await db.users.delete_one({"id": int(id)})
    return result

  async def updateUser(self, id, user):
    global db
    result = await db.users.update_one({"id": int(id)}, {'$set': user}, False, True)
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
      user = await db.users.find_one({'id': int(id)})
      return user

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
    result = await db.drives.delete_one({"id":int(id)})
    return result
  
  async def getDrive(self, id):
    global db
    result = await db.drives.find_one({"id": int(id)})
    return result

  async def updateDrive(self, id, drive):
    global db
    result = await db.drives.update_one({"id": int(id)}, {'$set': drive}, False, True)
    return result

  async def getFilteredDrives(self, f):
    global db
    collection = db.drives 
    cursor = collection.find(f)
    drives = []
    for doc in await cursor.to_list(10):
      drives.append(doc)
    return drives
