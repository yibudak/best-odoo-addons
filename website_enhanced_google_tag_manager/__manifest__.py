# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Enhanced Google Tag Manager",
    "summary": "Enhanced Google Tag Manager for Odoo Website",
    "version": "16.0.1.0.1",
    "author": "Ahmet Yiğit Budak",
    "license": "AGPL-3",
    "website": "https://github.com/yibudak/best-odoo-addons",
    "depends": ["website", "website_sale"],
    "data": [
        "views/res_config_settings_view.xml",
        # TEMPLATE
        "templates/website.xml",
        "templates/website_sale.xml",
    ],
    "installable": True,
    # Odoo Apps Store Specific #
    "images": ["static/description/banner.png"],
    "price": 10.00,
    "currency": "EUR",
    "category": "Website",
}
