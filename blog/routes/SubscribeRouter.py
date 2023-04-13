from flask import Blueprint

from blog.controllers.SubscribeController import SubscribeController

SubscribeRouter = Blueprint("subscribe_controller", __name__)

SubscribeRouter.route("/subscription", methods=["GET"])(SubscribeController.subscription)
SubscribeRouter.route("/create-subscription", methods=["GET", "POST"])(SubscribeController.subscription_create)
SubscribeRouter.route("/public-key", methods=["GET"])(SubscribeController.get_publishable_key)
SubscribeRouter.route("/webhook", methods=["POST"])(SubscribeController.webhook_received)
SubscribeRouter.route("/subscription-success", methods=["GET"])(SubscribeController.subscription_success)
SubscribeRouter.route("/upgrade-verifying/<price_id>", methods=["GET"])(SubscribeController.upgrade_verifying)
SubscribeRouter.route("/upgrade-subscription/<price_id>", methods=["GET"])(SubscribeController.subscription_upgrade)
SubscribeRouter.route("/create-setup-intent", methods=["POST"])(SubscribeController.create_setup_intent)
SubscribeRouter.route("/update-payment", methods=["GET"])(SubscribeController.change_payment_method)
SubscribeRouter.route("/cancel-subscription/<is_canceled>", methods=["GET"])(SubscribeController.subscription_cancel)
