from __future__ import print_function
import json
import base64
import logging
import hashlib
import pickle
import os.path
from cryptography.fernet import Fernet
from bson import json_util
from bson.json_util import dumps
from handlers.base import BaseHandler
from lib.DBConnection import UserFunctions
from lib.DBConnection import LinksFunctions
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


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

          print(link)
          self.set_status(200)
          self.write({"message":"done"})
          self.finish()
          # send email
          SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
          creds = None
          if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
              creds = pickle.load(token)
          if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
              creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
          
          service = build('gmail', 'v1', credentials=creds)

          # Call the Gmail API
          results = service.users().labels().list(userId='me').execute()
          labels = results.get('labels', [])

          if not labels:
            print('No labels found.')
          else:
            print('Labels:')
            for label in labels:
                print(label['name'])


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
