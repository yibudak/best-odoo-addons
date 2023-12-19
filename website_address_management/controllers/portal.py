# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request


class PortalAccount(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "address_count" in counters:
            partner = request.env.user.partner_id
            address_count = (
                len(partner.shipping_address_ids)
                if request.env["res.partner"].check_access_rights(
                    "read", raise_exception=False
                )
                else 0
            )
            values["address_count"] = address_count
        return values
