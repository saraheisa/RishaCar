import logging
import tornado
import tornado.template
import os
from tornado.options import define, options

import environment
import logconfig

# Make filepaths relative to settings.
path = lambda root,*a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

define("port", help="run on the given port", type=int)
define("config", default=None, help="tornado config file")
define("debug", default=True, help="debug mode")
define("facebook_api_key", default="1047153442161077", help="your Facebook application API key", type=str)
define("facebook_secret", default="3c91af752dee7f06969c17d7d421a7e5", help="your Facebook application secret", type=str)
define("google_client_id", default="491858733778-78kv83qc0folfb5b7ppck9aoq44a2v77.apps.googleusercontent.com", help="your Google application API key", type=str)
define("google_secret", default="if5kw7wiWUDxb6O4odGNT_Kb", help="your Google application secret key", type=str)
tornado.options.parse_command_line()

MEDIA_ROOT = path(ROOT, 'media')
TEMPLATE_ROOT = path(ROOT, 'templates')

# Deployment Configuration

class DeploymentType:
  PRODUCTION = "PRODUCTION"
  DEV = "DEV"
  SOLO = "SOLO"
  STAGING = "STAGING"
  dict = {
    SOLO: 1,
    PRODUCTION: 2,
    DEV: 3,
    STAGING: 4
  }

if 'DEPLOYMENT_TYPE' in os.environ:
  DEPLOYMENT = os.environ['DEPLOYMENT_TYPE'].upper()
else:
  DEPLOYMENT = DeploymentType.SOLO

settings = {}
settings['debug'] = DEPLOYMENT != DeploymentType.PRODUCTION or options.debug
settings['static_path'] = MEDIA_ROOT
settings['cookie_secret'] = "your-cookie-secret"
# settings['xsrf_cookies'] = True
settings['template_loader'] = tornado.template.Loader(TEMPLATE_ROOT)
settings['facebook_api_key'] = options.facebook_api_key
settings['google_client_id'] = options.google_client_id
settings['facebook_secret'] = options.facebook_secret
settings['google_secret'] = options.google_secret

SYSLOG_TAG = "rishacar"
SYSLOG_FACILITY = logging.handlers.SysLogHandler.LOG_LOCAL2

# See PEP 391 and logconfig for formatting help.  Each section of LOGGERS
# will get merged into the corresponding section of log_settings.py.
# Handlers and log levels are set up automatically based on LOG_LEVEL and DEBUG
# unless you set them here.  Messages will not propagate through a logger
# unless propagate: True is set.
LOGGERS = {
  'loggers': {
    'rishacar': {},
  },
}

if settings['debug']:
  LOG_LEVEL = logging.DEBUG
else:
  LOG_LEVEL = logging.INFO
USE_SYSLOG = DEPLOYMENT != DeploymentType.SOLO

logconfig.initialize_logging(SYSLOG_TAG, SYSLOG_FACILITY, LOGGERS,
        LOG_LEVEL, USE_SYSLOG)

if options.config:
  tornado.options.parse_config_file(options.config)
