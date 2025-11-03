# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    @api.model
    def create(self, vals):
        vals_list = vals if isinstance(vals, list) else [vals]

        for vals_item in vals_list:
            if not vals_item.get('company_ids'):
                try:
                    company_id = self.env.company.id
                    if company_id:
                        vals_item['company_ids'] = [(6, 0, [company_id])]
                        _logger.info("Asignando company_ids en create para '%s': %s", vals_item.get('name'), company_id)
                except Exception as e:
                    _logger.warning("Error al asignar company_ids en create: %s", e)

        return super().create(vals_list if isinstance(vals, list) else vals_list[0])
