# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import http
from odoo.http import request


class WebsiteAddressManagement(http.Controller):
    @http.route("/my/address", type="http", auth="user", website=True)
    def my_addresses(self, **kw):
        partner = request.env.user.partner_id
        return request.render(
            "website_address_management.my_addresses",
            {
                "partner_id": partner,
                # "billing_address_ids": partner.billing_address_ids,
                "shipping_address_ids": partner.shipping_address_ids,
            },
        )

    @http.route(
        "/my/address/delete",
        type="json",
        auth="public",
        website=True,
    )
    def delete_address(self, **kw):
        address_id = kw.get("address_id")
        if address_id and isinstance(address_id, int):
            partner = request.env.user.partner_id
            address = request.env["res.partner"].browse(address_id)
            if address in partner.shipping_address_ids and address != partner:
                address.sudo().write({"active": False})
                # Set the first address as shipping address
                # if deleted address is the current shipping address.
                order = request.website.sale_get_order()
                if order and order.partner_shipping_id == address:
                    order.partner_shipping_id = partner.id
            return True
        else:
            return False
