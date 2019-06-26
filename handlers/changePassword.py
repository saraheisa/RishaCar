import json
import logging
from bson import json_util
from lib.auth import jwtauth
from handlers.base import BaseHandler
from cryptography.fernet import Fernet
from lib.DBConnection import LinksFunctions
from lib.DBConnection import UserFunctions

logger = logging.getLogger('rishacar.' + __name__)


class ChangePasswordHandler(BaseHandler):
  async def post(self):
    data = self.request.body_arguments
    linkID = data['id'][0].decode("utf-8")
    password = data['password'][0].decode("utf-8")
    linkFuncs = LinksFunctions()
    link = await linkFuncs.getLink(linkID)
    userFuncs = UserFunctions()
    key = b'i102LDEGa-8PLuZJ9kw-VR2VKCeYxOanZvM4KQAZLt8='
    cipher_password = self.encrypt(key, bytes(password, 'utf-8'))
    user = {'password': cipher_password.decode("utf-8")}
    res = await userFuncs.updateUser(link['userID'], user)
    if res:
      result = await linkFuncs.deleteLink(linkID)
      self.set_status(200)
      self.write({"message":"password changed"})
      self.finish()

  def encrypt(self, key, text):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(text)
