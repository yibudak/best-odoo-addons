# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, api, fields, _
import logging

_logger = logging.getLogger(__name__)


class WebsiteMenu(models.Model):
    _inherit = "website.menu"

    def deepl_translate_menu(
        self,
        deepl_account_id,
        source_lang_id,
        target_lang_id,
        translation_override=False,
    ):
        """
        Translate all fields of the view with DeepL API
        :param deepl_account_id: deepl.account
        :param target_lang_id: res.lang
        """
        self.ensure_one()

        def _translate_name(model):
            translations = model.get_field_translations(
                "name", langs={target_lang_id.code}
            )[0]
            if not translations:
                return

            updated_fields = {target_lang_id.code: {}}
            for translation in translations:
                if translation["value"] and not translation_override:
                    continue
                try:
                    source_text = translation["source"] or model.name
                    if source_text:
                        translated_text = deepl_account_id.translate(
                            text=source_text,
                            source_lang_code=source_lang_id.code,
                            target_lang_code=target_lang_id.code,
                        )
                        updated_fields[target_lang_id.code] = translated_text
                except Exception as e:
                    _logger.error(
                        "Error while translating field '%s' in view %s [%s]: %s",
                        translation["source"],
                        model.name,
                        model.id,
                        e,
                    )
                    continue
            if updated_fields[target_lang_id.code]:
                model.update_field_translations("name", updated_fields)
                model.env.cr.commit()

        def _translate_content(model):
            model.ensure_one()
            fields = model.get_field_translations(
                "mega_menu_content", langs={target_lang_id.code}
            )
            field_list = fields[0]

            if not field_list:
                return

            updated_fields = {target_lang_id.code: {}}
            for field in field_list:
                # We're only working on single language but double check for safety
                if field["lang"] != target_lang_id.code:
                    continue

                # Skip translated fields
                if field["value"] and not translation_override:
                    continue

                try:
                    translated_text = deepl_account_id.translate(
                        text=field["source"],
                        source_lang_code=source_lang_id.code,
                        target_lang_code=target_lang_id.code,
                    )
                    updated_fields[field["lang"]].update(
                        {
                            field["source"]: translated_text,
                        },
                    )
                except Exception as e:
                    _logger.error(
                        "Error while translating field '%s' in view %s [%s]: %s",
                        field["source"],
                        model.name,
                        model.id,
                        e,
                    )
                    continue

            # Update the fields with the translated texts
            if updated_fields[target_lang_id.code]:
                model.update_field_translations("mega_menu_content", updated_fields)

            model.env.cr.commit()
            return True

        # Website menu is a special case, it has a name and a content
        _translate_name(self)
        _translate_content(self)

        return True
