# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Improved Sale Schema",
    "summary": "Google Search Console Schema Markup for Product Page",
    "version": "16.0.1.0.1",
    "author": "Ahmet Yiğit Budak",
    "license": "AGPL-3",
    "website": "https://github.com/yibudak/best-odoo-addons",
    "depends": ["website", "website_sale"],
    "data": [
        # TEMPLATE
        "templates/product_schema_markup.xml",
        "views/website_views.xml",
    ],
    "installable": True,
    # Odoo Apps Store Specific #
    "images": ["static/description/banner.png"],
    "price": 10.00,
    "currency": "EUR",
    "category": "Website",
}
