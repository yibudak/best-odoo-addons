# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import http


class WebsiteSaleClearCart(http.Controller):
    @http.route(
        ["/shop/cart/empty"],
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def clear_cart(self):
        order = http.request.website.sale_get_order()
        for line in order.order_line:
            line.unlink()
        return http.request.redirect("/shop/cart")
