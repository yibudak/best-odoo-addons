# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Address Management",
    "summary": "Manage all the addresses in a single window.",
    "version": "16.0.1.0.1",
    "author": "Yiğit Budak",
    "license": "AGPL-3",
    "website": "https://github.com/yibudak/best-odoo-addons",
    "depends": ["website", "website_sale"],
    "data": [
        "views/templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "/website_address_management/static/src/js/address_management.js",
        ],
    },
    "installable": True,
    # Odoo Apps Store Specific #
    "images": ["static/description/banner.png"],
    "price": 10.00,
    "currency": "EUR",
    "category": "Website",
}
