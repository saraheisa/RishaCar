import json
import base64
# from Crypto.Cipher import AES
# from Crypto.Hash import SHA256
# from Crypto import Random
from bson import json_util
from bson.json_util import dumps
from handlers.base import BaseHandler
from lib.DBConnection import UserFunctions

import logging
logger = logging.getLogger('rishacar.' + __name__)

class LoginHandler(BaseHandler):
  async def post(self):
    if (self.request.body):
      data = json.loads(self.request.body)
      # print(encrypt(""))
      user = ''
      if ( ('password' in data) & ('username' in data) ):
        userFunc = UserFunctions()
        user = await userFunc.getUser(username = data['username'])
      elif (('password' in data) & ('email' in data)):
        userFunc = UserFunctions()
        user = await userFunc.getUser(email= data['email'])
      if user:
        if (user['password'] == data['password']):
          token = super(LoginHandler, self).jwtEncode()
          self.encoded = token
          response = {'token': self.encoded.decode('ascii')}
          self.write(response)
        else:
          self.set_status(400)
          self.write({"message":"wrong password"})
          self.finish()
      else:
        self.set_status(400)
        self.write({"message":"wrong data"})
        self.finish()
    else:
      self.set_status(400)
      self.write({"message":"data is missing"})
      self.finish()
  
  # def encrypt(self, key, source, encode=True):
  #   key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
  #   IV = Random.new().read(AES.block_size)  # generate IV
  #   encryptor = AES.new(key, AES.MODE_CBC, IV)
  #   padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
  #   source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
  #   data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
  #   return base64.b64encode(data).decode("latin-1") if encode else data

  # def decrypt(self, key, source, decode=True):
  #   if decode:
  #       source = base64.b64decode(source.encode("latin-1"))
  #   key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
  #   IV = source[:AES.block_size]  # extract the IV from the beginning
  #   decryptor = AES.new(key, AES.MODE_CBC, IV)
  #   data = decryptor.decrypt(source[AES.block_size:])  # decrypt
  #   padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
  #   if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
  #     raise ValueError("Invalid padding...")
  #   return data[:-padding]  # remove the padding
