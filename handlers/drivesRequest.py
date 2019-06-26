import json
import logging
from bson import json_util
from lib.auth import jwtauth
from handlers.base import BaseHandler
from lib.DBConnection import DriveFunctions

logger = logging.getLogger('rishacar.' + __name__)

@jwtauth
class DrivesRequestHandler(BaseHandler):
  async def get(self, id):
    pass

  async def post(self, _):
    pass

  async def delete(self, id):
    pass

  async def put(self, id):
    pass

  def verify_data(self, data):
    return 'userId' in data and 'to' in data and 'from' in data and 'rideStatus' in data and 'date' in data and 'time' in data and 'carId' in data and 'proposal' in data
