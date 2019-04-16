from handlers.login import LoginHandler
from handlers.home import HomeHandler
from handlers.loginWithFb import FBLoginHandler
from handlers.loginWithGoogle import GoogleLoginHandler
from handlers.signup import SignupHandler
from handlers.drives import DrivesHandler
from handlers.users import UsersHandler

url_patterns = [
    (r"/login", LoginHandler),
    (r"/", HomeHandler),
    (r"/auth/fb/", FBLoginHandler),
    (r"/auth/google/", GoogleLoginHandler),
    (r"/signup", SignupHandler),
    (r"/drives/([^/]+)?", DrivesHandler),
    (r"/users/([^/]+)?", UsersHandler)
]
