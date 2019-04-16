import json
from tornado.auth import FacebookGraphMixin
from bson import json_util
from bson.json_util import dumps
from handlers.base import BaseHandler
from settings import settings
import tornado.escape
import os.path
import tornado.escape

import logging
logger = logging.getLogger('rishacar.' + __name__)

class FBLoginHandler(BaseHandler, FacebookGraphMixin):
  async def get(self):
    my_url = (
      self.request.protocol
      + "://"
      + self.request.host
      + "/auth/login?next="
      + tornado.escape.url_escape(self.get_argument("next", "/"))
    )
    if self.get_argument("code", False):
      user = await self.get_authenticated_user(
          redirect_uri=my_url,
          client_id=self.settings["facebook_api_key"],
          client_secret=self.settings["facebook_secret"],
          code=self.get_argument("code"),
      )
      token = super(FBLoginHandler, self).jwtEncode()
      self.encoded = token
      response = {'token': self.encoded.decode('ascii')}
      self.write(response)
      self.redirect(self.get_argument("next", "/"))
      return
    self.authorize_redirect(
      redirect_uri=my_url,
      client_id=self.settings["facebook_api_key"],
      extra_params={"scope": "user_posts"},
    )
