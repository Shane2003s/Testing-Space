# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
#################################################################################
from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    pos_logo = fields.Binary()
    show_logo_on_receipt = fields.Boolean(
        string="Show Logo on Receipt", default=True)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_pos_logo = fields.Binary(
        related='pos_config_id.pos_logo', readonly=False)
    pos_show_logo_on_receipt = fields.Boolean(
        related='pos_config_id.show_logo_on_receipt', readonly=False)
