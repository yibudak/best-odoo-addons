# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, api, fields, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    def deepl_translate_all_fields(
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
        fields = self.get_field_translations("arch_db", langs={target_lang_id.code})
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
                    self.name,
                    self.id,
                    e,
                )
                continue

        # Update the fields with the translated texts
        if updated_fields[target_lang_id.code]:
            self.update_field_translations("arch_db", updated_fields)

        self.env.cr.commit()
        return True
