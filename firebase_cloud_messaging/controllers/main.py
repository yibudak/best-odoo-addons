# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import logging
from odoo.http import route, request, Controller

_logger = logging.getLogger(__name__)


class FirebaseCloudMessaging(Controller):
    _register_token = "/FCM/Api/RegisterToken"

    @route(
        _register_token,
        auth="public",
        type="json",
        cors="*",
        methods=["POST"],
        csrf=False,
        save_session=False,
    )
    def register_token(self):
        """
        Required parameters:
            - registration_token: string
            - sender_id: string
            - partner_id: integer
        """
        jsonrequest = request.get_json_data()
        if not jsonrequest:
            return {"error": "No JSON data provided."}

        # Parameters
        registration_token = jsonrequest.get("registration_token")
        sender_id = jsonrequest.get("sender_id")
        user_id = jsonrequest.get("user_id")

        # Models sudo
        FCMServer = request.env["fcm.server"].sudo()
        User = request.env["res.users"].sudo()
        FCMDevice = request.env["fcm.device"].sudo()

        local_fcm_server = FCMServer.search(
            [
                ("sender_id", "=", sender_id),
            ],
            limit=1,
        )
        local_user = User.browse(user_id)

        if not (local_fcm_server and local_user):
            return {"error": "Token registration failed."}

        local_fcm_device = FCMDevice.search(
            [
                ("device_token", "=", registration_token),
                ("partner_id", "=", local_user.partner_id.id),
            ],
            limit=1,
        )
        # Create a new device if it does not exist
        if not local_fcm_device:
            FCMDevice.create(
                {
                    "device_token": registration_token,
                    "partner_id": local_user.partner_id.id,
                }
            )

        return {"success": "Token registered successfully."}
