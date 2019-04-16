import json
from lib.auth import jwtauth
from bson import json_util
from bson.json_util import dumps
from handlers.base import BaseHandler

import logging
logger = logging.getLogger('rishacar.' + __name__)

@jwtauth
class HomeHandler(BaseHandler):
  def get(self):
    self.write("suggestions in progress")
  def post(self):
    self.write({'message': json.loads(self.request.body)})
