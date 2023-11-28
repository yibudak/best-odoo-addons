/** @odoo-module **/
/*
* Yiğit Budak 2023
* This file removes Odoo links from user menu
* */

require("@web/webclient/user_menu/user_menu_items");
import { registry } from "@web/core/registry";

let menu_items = registry.category("user_menuitems");
menu_items.remove("documentation");
menu_items.remove("support");
menu_items.remove("odoo_account");