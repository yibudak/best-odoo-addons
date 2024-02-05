
![Odoo Version](https://img.shields.io/badge/maturity-production/stable-green)  ![Odoo Version](https://img.shields.io/badge/odoo_version-12.0-blue)  ![Licence](https://img.shields.io/badge/licence-LGPL--3-lightgrey) 

You can purchase this module from Odoo Apps Store to support our work and maintenance.

[![Odoo Apps Store](https://img.shields.io/badge/Odoo%20Apps%20Store-714b67?style=for-the-badge)](https://apps.odoo.com/apps/modules/12.0/web_translate_deepl/)

![Odoo DeepL Translation](./static/description/usage.png)

# Web DeepL Translate

This module adds new features to web_translate_dialog module. It allows you to translate all the fields using DeepL API.

## Features:

- Translate all the languages with a single click.
- Translate specific language.
- Glossary support.
- Set base field for translation. (e.g. use English for Japanese translation, use French for German translation etc.)
- Use context and formality settings for translation.
- Translate all kind of fields. (e.g. Char, Text, HTML, etc.)

## Installation:

1. Clone this repository.
2. Add this directory to your addons path (e.g. `--addons-path=addons,path/to/this/repo`).
3. Install the module `web_translate_deepl`.
4. Go to `Settings > Technical > DeepL Account` and set your DeepL API key.
5. Set default DeepL account for company.
6. Set base language for translation in `Settings > Translations > Languages`.

## Dependencies:
1. [web_translate_dialog](https://odoo-community.org/shop/web-translate-dialog-2813#attr=7720)

## Known Issues / Roadmap:
1. This module can translate html fields, but the field is not rendered again in the interface, so it looks like it was never translated until you save it.

## Authors:

- [Ahmet Yiğit Budak](https://github.com/yibudak)

## Contribution:

We welcome your contributions to our project.

- This project is licensed under LGPL-3. Your contributions will be under the same license.
- We aim to adhere to **OCA quality standards** for all modules and content in this project.
- General information on contributing can be found on the [Contribute to OCA](https://odoo-community.org/page/Contribute) page.
- General rules for adding modules can be accessed at https://github.com/OCA/maintainer-tools/blob/master/CONTRIBUTING.md
- Quality control can be simplified using [OCA's quality control tools](https://github.com/OCA/maintainer-quality-tools).
