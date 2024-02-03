# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    "name": "DeepL Translate",
    "summary": "Translate any fields in web dialog.",
    "description": """
    This module allows you to translate any fields in web dialog using DeepL API.
    """,
    "version": "12.0.1.0.0",
    "author": "Yiğit Budak",
    "website": "https://github.com/yibudak/best-odoo-addons",
    "license": "LGPL-3",
    "depends": ["web_translate_dialog"],
    "external_dependencies": {"python": ["requests"]},
    "data": [
        "security/deepl_account.xml",
        "views/deepl_account_view.xml",
        "views/menus.xml",
        "views/res_company_view.xml",
        "views/res_lang_view.xml",
        "views/web_translate.xml",
    ],
    "qweb": [
        "static/src/xml/inherit.xml",
    ],
    "installable": True,
    # Odoo Apps Store Specific #
    "images": ["static/description/banner.png"],
    "price": 10.00,
    "currency": "EUR",
    "category": "Tools",
}
