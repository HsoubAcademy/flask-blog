from flask import Blueprint
from blog.controllers.MainController import MainController

MainRouter = Blueprint("main_controller", __name__)

MainRouter.route("/")(MainController.home)
