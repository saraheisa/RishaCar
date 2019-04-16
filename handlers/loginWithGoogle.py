from tornado.auth import GoogleOAuth2Mixin
from handlers.base import BaseHandler
from settings import settings

import logging
logger = logging.getLogger('rishacar.' + __name__)


class GoogleLoginHandler(BaseHandler, GoogleOAuth2Mixin):
  async def get(self):
    if self.get_argument('code', False):
      user = await self.get_authenticated_user(
        redirect_uri='http://localhost:5000/auth/google',
        code=self.get_argument('code'))
    else:
      await self.authorize_redirect(
        redirect_uri='http://localhost:5000//auth/google',
        client_id=self.settings["google_client_id"],
        scope=['profile', 'email'],
        response_type='code',
        extra_params={'approval_prompt': 'auto'})
