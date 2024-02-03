odoo.define('web_translate_deepl.web_translate_dialog_deepl', function (require) {
    "use strict";

    var translate_dialog = require('web_translate_dialog.translate_dialog');
    var rpc = require('web.rpc');

    translate_dialog.TranslateDialog.include({

        init: function (parent, options) {
            this._super.apply(this, arguments);
            var self = this;
            this.company_id = null;
            this.deepl_enabled = false;
            // Company Field
            this.company_fields_loaded = $.Deferred();
            this._getCompanyFields().then(this.on_company_fields_loaded);
            this._open_dialog_wait_for.push(this.company_fields_loaded);
            // New languages set
            this.new_languages_loaded = $.Deferred();
            this.lang_data.read_slice(['code', 'name', 'tr_base_lang_id']).then(this.on_new_languages_loaded);
            this._open_dialog_wait_for.push(this.new_languages_loaded);
        },

        _getCompanyFields: function () {
            return rpc.query({
                model: 'deepl.account',
                method: 'rpc_get_current_company_lang',
                args: [false],
            });
        },

        on_new_languages_loaded: function (lang_data) {
            this.languages = lang_data;
            this.new_languages_loaded.resolve();
        },

        on_company_fields_loaded: function (company_fields) {
            this.user_lang = company_fields.user_lang;
            this.deepl_enabled = company_fields.deepl_enabled;
            this.company_id = company_fields.company_id;
            this.company_fields_loaded.resolve();
        },

        start: function () {
            this._super.apply(this, arguments);
            // Add translateDeepl function on each button
            this.$el.find('.oe_translate_btn').click(this._onSingleBtnTranslateDeepl.bind(this));
            // Multi translate button
            this.$el.find('.oe_translate_all_btn').click(this._multiBtnTranslate.bind(this));
        },

        _multiBtnTranslate: function (ev) {
            var $translate_btns = this.$el.find('.oe_translate_btn');
            // Filter out english.
            var index = 1; // Keep track of the current button index

            var translateNext = () => {
                if (index < $translate_btns.length) {
                    var btn = $translate_btns[index];
                    $(btn).click();
                    index++; // Move to the next button
                } else {
                    // Remove the event listener once all translations are done
                    $(document).off('translationCompleted', translateNext);
                }
            };

            // Listen for the custom event to trigger the next translation
            $(document).on('translationCompleted', translateNext);

            // Start the first translation
            translateNext();
        },

        _onSingleBtnTranslateDeepl: function (ev) {
            var $btn = $(ev.currentTarget);
            let inputType = "input"
            // html and text fields are rendered as textarea
            if (['html', 'text'].includes($btn.data('field-type'))) {
                inputType = "textarea"
            }
            var $currentInput = $btn.closest('tr').find(inputType);
            if ($currentInput.val() && this.deepl_enabled) {
                $btn.addClass('disabled');
                this._translateDeepl($currentInput, inputType);
                $btn.removeClass('disabled');
            }
        },

        _translateDeepl: function ($currentInput, inputType) {
            /**
             * @param {Object} $currentInput - The jQuery object of the input field containing the text to be translated.
             * @param {String} inputType - The type of input field. Can be 'input' or 'textarea'
             */
            let target_lang = $currentInput.data('lang');
            let source_lang = $currentInput.data('base-tr-lang');
            if (!source_lang) {
                console.error('Base translation language not found');
                return;
            }
            let $source_input = $currentInput.closest('table').find(inputType + '[data-lang="' + source_lang + '"]');

            rpc.query({
                model: 'deepl.account',
                method: 'rpc_translate',
                args: [false, this.company_id, target_lang, $source_input.val()],
            }).then(function (result) {
                if (result) {
                    $currentInput.val(result);
                    $currentInput.toggleClass('touched', true);
                    $currentInput.css('color', 'green');
                }
                // Emit custom event to indicate translation completion
                $(document).trigger('translationCompleted');
            });
        },

    });


});
