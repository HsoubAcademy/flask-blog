from flask import Blueprint
from blog.controllers.auth.UserController import UserController
from blog.controllers.auth.AdminController import AdminController


AuthRouter = Blueprint("auth_controller", __name__)
# Admin Router
AuthRouter.route("/register", methods=["GET", "POST"])(UserController.user_register)
AuthRouter.route("/login", methods=["GET", "POST"])(UserController.user_login)
AuthRouter.route("/logout")(UserController.user_logout)
AuthRouter.route('/reset_password', methods=["GET", "POST"])(UserController.reset_request)
AuthRouter.route('/reset_password/<token>', methods=["GET", "POST"])(UserController.reset_pass)
AuthRouter.route("/account")(UserController.user_account)
# Admin Router
AuthRouter.route("/sub-panel/users-control")(AdminController.users_control)
AuthRouter.route("/sub-panel/role-grant/<int:user_id>")(AdminController.role_grant)
AuthRouter.route("/sub-panel/role-revoke/<int:user_id>")(AdminController.role_revoke)
AuthRouter.route("/sub-panel/statistics")(AdminController.sub_panel)
