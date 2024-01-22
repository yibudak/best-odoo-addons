# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit = "res.company"

    fcm_server_id = fields.Many2one(
        "fcm.server",
        string="FCM Server",
        help="Firebase Cloud Messaging Server",
        # compute="_compute_fcm_server_id",
    )

    # def _compute_fcm_server_id(self):
    #     for rec in self:
    #         fcm_server = self.env["fcm.server"].search(
    #             [("company_id", "=", rec.id)], limit=1
    #         )
    #         if not fcm_server:
    #             raise UserError(_("Please define a FCM Server for this company."))
