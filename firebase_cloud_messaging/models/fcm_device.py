# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields


class FCMDevices(models.Model):
    _name = "fcm.device"
    _description = "Firebase Cloud Messaging Device"

    # name = fields.Char("Name") # todo: make it compute with partner name + device name
    device_token = fields.Char("Device Token", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner")
    # sent_notification_ids = fields.One2many(
    #     "fcm.message", "device_id", string="Sent Notifications"
    # )