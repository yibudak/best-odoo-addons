# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    "name": "Website Translate DeepL",
    "summary": "Translate all texts in website pages.",
    "description": """
    This module allows you to translate all texts in website pages.
    """,
    "version": "12.0.1.0.0",
    "author": "Ahmet Yiğit Budak",
    "website": "https://github.com/yibudak/best-odoo-addons",
    "license": "AGPL-3",
    "depends": ["website", "queue_job"],
    "external_dependencies": {"python": ["requests"]},
    "data": [
        "security/security.xml",
        "views/deepl_account_view.xml",
        "views/deepl_glossary_view.xml",
        "views/website_view.xml",
        "views/menus.xml",
        # "views/res_company_view.xml",
        "wizards/website_translate_wizard_view.xml",
        # "views/web_translate.xml",
    ],
    # "qweb": [
    #     "static/src/xml/inherit.xml",
    # ],
    # Todo:
    # "assets": {
    #     "website.assets_editor": [
    #         "website_translate_deepl/static/src/js/deepl_website_translate.js",
    #     ],
    #     "website.assets_frontend": [
    #         "website_translate_deepl/static/src/scss/deepl_frontend.scss",
    #     ],
    # },
    "installable": True,
    # Odoo Apps Store Specific #
    "images": ["static/description/banner.png"],
    "price": 10.00,
    "currency": "EUR",
    "category": "Website",
}
