# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields
from pyfcm import FCMNotification


class FCMServer(models.Model):
    _name = "fcm.server"
    _description = "Firebase Cloud Messaging Server"

    name = fields.Char(string="Name", required=True)
    server_key = fields.Char(string="Server Key", required=True)
    sender_id = fields.Char(string="Sender ID", required=True)

    def _send_notification(self, device_ids, title, body, data=None):
        """
        Base method to send notification to devices
        """
        push_service = FCMNotification(api_key=self.server_key)
        result = push_service.notify_multiple_devices(
            registration_ids=device_ids,
            message_title=title,
            message_body=body,
            data_message=data,
        )
        return result
