/** @odoo-module **/
import {WebClient} from "@web/webclient/webclient";
import {patch} from "@web/core/utils/patch";

const rpc = require('web.rpc');

// Patch the WebClient to change the title
patch(WebClient.prototype, 'simple_odoo_debranding.webclient', {
    async setup() {
        await this._super(); // Call the original setup
        let customTitle = "Odoo";
        // Get the title from the website module
        const data = await rpc.query({
            fields: ['name'],
            domain: [],
            model: 'website',
            method: 'search_read',
            limit: 1,
        });
        if (data && data[0] && data[0].name) {
            customTitle = data[0].name;
        }
        this.title.setParts({ zopenerp: customTitle });
    },
});
