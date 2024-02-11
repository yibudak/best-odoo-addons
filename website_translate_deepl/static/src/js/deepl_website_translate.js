/** @odoo-module */
import {patch} from "@web/core/utils/patch";

var WebsiteTranslator = require("@website/components/translator/translator");


// Burada websitetranslator'un en son çalışan fonksiyonlarından birini patchlicez.
patch(WebsiteTranslator.WebsiteTranslator.prototype, 'deepl', {
    markTranslatableNodes() {
        this._super();
        const self = this;
        this._editableElements().each(function () {
            var $node = $(this);
            $('<button class="oe-deepl-btn" data-no-translate="1"><i class="fa fa-globe"></i>Translate</button>').appendTo(this);
            // $node.on('click', function () {
            //
            // });
            // stopPropagation();
        });
    }
});