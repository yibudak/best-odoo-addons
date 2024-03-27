odoo.define('website_address_management.address_management', function (require) {
    "use strict";
    var core = require('web.core');
    var _t = core._t;
    var publicWidget = require('web.public.widget');
    var VariantMixin = require('website_sale.VariantMixin');
    var wSaleUtils = require('website_sale.utils');
    const cartHandlerMixin = wSaleUtils.cartHandlerMixin;
    publicWidget.registry.WebsiteAddressManagement = publicWidget.Widget.extend(VariantMixin,
        cartHandlerMixin, {
            selector: '.oe_website_sale',
            events: _.extend({}, VariantMixin.events || {}, {
                'click .a-delete': '_onClickDelete',
            }),
            init: function () {
                this._super.apply(this, arguments);
                this.isWebsite = true;

            },
            /**
             * @private
             * @param {Event} ev
             */
            _onClickDelete: function (ev) {
                ev.preventDefault();
                var $el = $(ev.currentTarget);
                var address_id = $el.parents('.one_kanban').find('input[name=partner_id]').val();
                if (window.confirm(_t("Are you sure you want to delete this address?"))) {
                    this._rpc({
                        route: "/my/address/delete",
                        params: {
                            'address_id': parseInt(address_id),
                        },
                    }).then(function (data) {
                        location.reload();
                    });
                }
            },
        });

    // Disable to change shipping address on 'address management page',
    // It can cause the error when the user wants to edit the address,
    // but it changes the delivery address on the cart page.
    publicWidget.registry.websiteSaleCart.include({
        _onClickChangeShipping: function (ev) {
            let $address_management = $(ev.currentTarget).parent('div.one_kanban').find("input[name='address_management']");
            if ($address_management.length && $address_management.val() === '1') {
                return;
            }
            this._super.apply(this, arguments);
        },
    });

    return {
        WebsiteAddressManagement: publicWidget.registry.WebsiteAddressManagement,
    };

});
