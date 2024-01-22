# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    "name": "Firebase Cloud Messaging",
    "summary": "Send push notifications to customers with FCM.",
    "description": """
    This module allows users to send push notifications to customers with FCM.
    """,
    "version": "16.0.1.0.0",
    "author": "Ahmet Yiğit Budak",
    "website": "https://github.com/yibudak/best-odoo-addons",
    "license": "LGPL-3",
    "depends": [
        "base",
    ],
    "external_dependencies": {"python": ["pyfcm"]},
    "data": [
        "data/security.xml",
        "security/ir.model.access.csv",
        "views/fcm_message_views.xml",
        "views/fcm_device_views.xml",
        "views/fcm_server_views.xml",
        "views/res_partner_views.xml",
        "views/res_company_views.xml",
        "views/menus.xml",
    ],
    "installable": True,
    # Odoo Apps Store Specific #
    # Todo: enable
    # "images": ["static/description/banner.png"],
    "price": 10.00,
    "currency": "EUR",
    "category": "Tools",
}
