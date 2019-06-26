import json
import logging
from bson import json_util
from lib.auth import jwtauth
from handlers.base import BaseHandler
from lib.DBConnection import LinksFunctions

logger = logging.getLogger('rishacar.' + __name__)


class ResetPasswordHandler(BaseHandler):
  async def get(self, id):
    # make sure id in db
    if id:
      linkFuns = LinksFunctions()
      res = await linkFuns.getLink(id)
      if res:
        self.render('index.html', id = id)
        