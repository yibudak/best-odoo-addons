# # Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import http
from odoo.http import request
from werkzeug.exceptions import Forbidden, NotFound
from odoo.addons.website_sale.controllers.main import WebsiteSale
import ast


class WebsiteSaleInherit(WebsiteSale):
    #     def checkout_values(self, **kw):
    #         """Inherited to add multiple billing addresses to checkout page."""
    #         res = super(WebsiteSaleInherit, self).checkout_values(**kw)
    #
    #         current_partner = http.request.env.user.partner_id
    #         if (
    #             current_partner.billing_address_ids
    #             and not http.request.website.is_public_user()
    #         ):
    #             res.update({"billing_address_ids": current_partner.billing_address_ids})
    #         elif res.get("order") and res["order"].partner_id:
    #             # This means request is coming from public user, add sale order partner
    #             # as billing address.
    #             res.update({"billing_address_ids": res["order"].partner_id})
    #
    #         return res
    #

    @http.route(
        ["/shop/address"],
        type="http",
        methods=["GET", "POST"],
        auth="public",
        website=True,
        sitemap=False,
    )
    def address(self, **kw):
        """Inherited to handle non-cart address edit or creations."""
        if kw.get("address_management"):
            return self.address_invoice(**kw)
        else:
            return super(WebsiteSaleInherit, self).address(**kw)

    @http.route(
        ["/my/address/manage"],
        type="http",
        methods=["GET", "POST"],
        auth="public",
        website=True,
        sitemap=False,
    )
    def address_invoice(self, **kw):
        Partner = request.env["res.partner"].with_context(show_address=1).sudo()
        current_partner = request.env.user.partner_id
        order = request.website.sale_get_order(force_create=True)
        # dummy_order = None
        # if not order:
        #     dummy_order = request.env["sale.order"].sudo().create(
        #         {"partner_id": current_partner.id}
        #     )
        #     order = dummy_order
        #     request.session.sale_order_id = order.id

        # redirection = self.checkout_redirection(order)
        # if redirection:
        #     return redirection

        mode = (False, False)
        can_edit_vat = False
        values, errors = {}, {}

        partner_id = int(kw.get("partner_id", -1))

        # IF PUBLIC ORDER
        if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
            mode = ("new", "billing")
            can_edit_vat = True
        # IF ORDER LINKED TO A PARTNER
        else:
            if partner_id > 0:
                if partner_id == order.partner_id.id:
                    mode = ("edit", "billing")
                    can_edit_vat = order.partner_id.can_edit_vat()
                else:
                    shippings = Partner.search(
                        [("id", "child_of", order.partner_id.commercial_partner_id.ids)]
                    )
                    if order.partner_id.commercial_partner_id.id == partner_id:
                        mode = ("new", "shipping")
                        partner_id = -1
                    elif partner_id in shippings.mapped("id"):
                        mode = ("edit", "shipping")
                    elif partner_id == current_partner.id:
                        mode = ("edit", "billing")
                        can_edit_vat = current_partner.can_edit_vat()
                    else:
                        # if dummy_order:
                        #     dummy_order.unlink()
                        return Forbidden()
                if mode and partner_id != -1:
                    values = Partner.browse(partner_id)
            elif partner_id == -1:
                mode = ("new", "shipping")
            else:  # no mode - refresh without post?
                return request.redirect("/my/address/manage")

        # IF POSTED
        if "submitted" in kw and request.httprequest.method == "POST":
            pre_values = self.values_preprocess(kw)
            errors, error_msg = self.checkout_form_validate(mode, kw, pre_values)
            post, errors, error_msg = self.values_postprocess(
                order, mode, pre_values, errors, error_msg
            )

            if errors:
                errors["error_message"] = error_msg
                values = kw
            else:
                # if mode[1] == 'shipping' and not post.get('parent_id'):
                #     post['parent_id'] = current_partner.id
                partner_id = self._checkout_form_save(mode, post, kw)
                # We need to validate _checkout_form_save return, because when partner_id not in shippings
                # it returns Forbidden() instead the partner_id
                if isinstance(partner_id, Forbidden):
                    return partner_id
                fpos_before = order.fiscal_position_id
                if mode[1] == "billing":
                    order.partner_id = partner_id
                    # This is the *only* thing that the front end user will see/edit anyway when choosing billing address
                    order.partner_invoice_id = partner_id
                    if not kw.get("use_same"):
                        kw["callback"] = kw.get("callback") or (
                            not order.only_services
                            and (
                                mode[0] == "edit"
                                and "/shop/checkout"
                                or "/shop/address"
                            )
                        )
                    # We need to update the pricelist(by the one selected by the customer), because onchange_partner reset it
                    # We only need to update the pricelist when it is not redirected to /confirm_order
                    if kw.get("callback", False) != "/shop/confirm_order":
                        request.website.sale_get_order(update_pricelist=True)
                elif mode[1] == "shipping":
                    order.partner_shipping_id = partner_id

                if order.fiscal_position_id != fpos_before:
                    order._recompute_taxes()

                # TDE FIXME: don't ever do this
                # -> TDE: you are the guy that did what we should never do in commit e6f038a
                order.message_partner_ids = [
                    (4, partner_id),
                    (3, request.website.partner_id.id),
                ]
                if not errors:
                    # if dummy_order:
                    #     dummy_order.unlink()
                    return request.redirect("/my/address")

        render_values = {
            "website_sale_order": order,
            "partner_id": partner_id,
            "mode": mode,
            "checkout": values,
            "can_edit_vat": can_edit_vat,
            "error": errors,
            "callback": kw.get("callback"),
            "only_services": order and order.only_services,
            "account_on_checkout": request.website.account_on_checkout,
            "is_public_user": request.website.is_public_user(),
            "address_management": True,
        }
        render_values.update(self._get_country_related_render_values(kw, render_values))
        return request.render("website_sale.address", render_values)
