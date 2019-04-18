import json
import logging
from bson import json_util
from lib.auth import jwtauth
from handlers.base import BaseHandler

logger = logging.getLogger('rishacar.' + __name__)

@jwtauth
class HomeHandler(BaseHandler):
  def get(self):
    self.write("suggestions in progress")
  def post(self):
    self.write({'message': json.loads(self.request.body)})
