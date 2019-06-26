import json
import base64
import logging
import hashlib
from cryptography.fernet import Fernet
from bson import json_util
from bson.json_util import dumps
from handlers.base import BaseHandler
from lib.DBConnection import UserFunctions
from lib.DBConnection import LinksFunctions
from tornado import gen
from email.message import EmailMessage
from tornado_smtp.client import TornadoSMTP

logger = logging.getLogger('rishacar.' + __name__)


class ForgetPasswordHandler(BaseHandler):
  async def post(self):
    if self.request.body:
      data = json.loads(self.request.body)
      if data['email']:
        # check if email exists in db
        if await self.email_exists(data['email']):
          userFunc = UserFunctions()
          user = await userFunc.getUser(email=data['email'])
          # create email id from user id
          userID = str(user['_id'])
          linkID = hashlib.md5(userID.encode()).hexdigest()
          
          link = {"userID": userID, "linkID": linkID}
          linksFunc = LinksFunctions()
          result = await linksFunc.insertLink(link)

          # send email
          link = "https://rishacar.herokuapp.com/reset/password/" + linkID

          self.send_email(data['email'], link)

          self.set_status(200)
          self.write({"message":"ok"})
          self.finish()
        else:
          self.set_status(400)
          self.write({"message":"wrong email"})
          self.finish()
      else:
        self.set_status(400)
        self.write({"message":"missing email"})
        self.finish()
    else:
      self.set_status(400)
      self.write({"message":"data is missing"})
      self.finish()
  
  def encrypt(self, key, text):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(text)

  async def email_exists(self, email):
    userFunc = UserFunctions()
    return await userFunc.getEmail(email)

  @gen.coroutine
  def send_email(self, email, link):
    smtp = TornadoSMTP('smtp-mail.outlook.com')
    yield smtp.starttls()
    yield smtp.login('existed_user@outlook.com', 'eo%Y0pOTmJ%8lG$F9qfT')

    msg = EmailMessage()
    msg['Subject'] = 'Reset Password for RISHA CAR'
    msg['To']      = email
    msg['From']    = 'existed_user@outlook.com'
    msg.set_content('reset your password:\n ' + link)
    smtp.send_message(msg)
    print('done')
