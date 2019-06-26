from handlers.login import LoginHandler
from handlers.home import HomeHandler
from handlers.loginWithFb import FBLoginHandler
from handlers.loginWithGoogle import GoogleLoginHandler
from handlers.signup import SignupHandler
from handlers.drives import DrivesHandler
from handlers.users import UsersHandler
from handlers.usersVerify import UsersVerifyHandler
from handlers.cars import CarsHandler
from handlers.drivesRequest import DrivesRequestHandler
from handlers.forgetPassword import ForgetPasswordHandler
from handlers.userProvider import UserProviderHandler
from handlers.driveFilter import DrivesFilterHandler
from handlers.resetPassword import ResetPasswordHandler
from handlers.changePassword import ChangePasswordHandler

url_patterns = [
    (r"/login", LoginHandler),
    (r"/", HomeHandler),
    (r"/auth/fb/", FBLoginHandler),
    (r"/auth/google/", GoogleLoginHandler),
    (r"/signup", SignupHandler),
    (r"/drives/([^/]+)?", DrivesHandler),
    (r"/drive/filter", DrivesFilterHandler),
    (r"/cars/([^/]+)?", CarsHandler),
    (r"/users/([^/]+)?", UsersHandler),
    (r"/users/verify/", UsersVerifyHandler),
    (r"/drives/request/", DrivesRequestHandler),
    (r"/forgetPassword", ForgetPasswordHandler),
    (r"/user/provider", UserProviderHandler),
    (r"/reset/password/([^/]+)", ResetPasswordHandler),
    (r"/changePassword", ChangePasswordHandler)
]
