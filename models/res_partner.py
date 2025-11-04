# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    @api.model_create_multi
    def create(self, vals_list):
        user = self.env.user

        if len(user.company_ids) > 1:
            active_company_id = self.env.company.id
        else:
            active_company_id = user.company_id.id

        for vals in vals_list:
            if active_company_id:
                vals['company_ids'] = [(6, 0, [active_company_id])]
                _logger.info("Asignando company_ids en create para '%s': %s", vals.get('name'), active_company_id)
            elif not active_company_id:
                _logger.warning("No se pudo determinar la compañía activa. Se omite la asignación de company_ids para '%s'.", vals.get('name'))

        return super().create(vals_list)