# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Simple Odoo Debranding",
    "summary": "Hide Odoo and Odoo Enterprise from backend",
    "version": "16.0.1.0.1",
    "author": "Yiğit Budak",
    "license": "AGPL-3",
    "website": "https://github.com/yibudak/best-odoo-addons",
    "depends": ["base", "web", "website"],
    "data": [
        "views/webclient_templates.xml",
        # "security/res_users.xml",
    ],
    "installable": True,
    "assets": {
        "web.assets_backend": [
            "simple_odoo_debranding/static/src/js/user_menu_items.js",
            "simple_odoo_debranding/static/src/js/webclient.js",
        ],
    },
    # Odoo Apps Store Specific #
    # "images": ["static/description/banner.png"],
    "price": 20.00,
    "currency": "EUR",
    "category": "Website",
}
