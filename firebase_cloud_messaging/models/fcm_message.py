# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class FCMMessage(models.Model):
    _name = "fcm.message"
    _description = "Firebase Cloud Messaging Message"

    title = fields.Char(string="Title", required=True)
    body = fields.Char(string="Body", required=True)

    def action_send_message(self):
        """
        Action to send message to devices
        """
        self.ensure_one()
        if not self.env.user.company_id.fcm_server_id:
            raise UserError(_("Please define a FCM Server for this company."))
        device_ids = (
            self.env["fcm.device"]
            .search([("partner_id", "!=", False)])
            .mapped("device_token")
        )
        self.env.user.company_id.fcm_server_id._send_notification(
            device_ids=device_ids,
            title=self.title,
            body=self.body,
        )
