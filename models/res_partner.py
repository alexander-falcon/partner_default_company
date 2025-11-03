# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID
import logging

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'company_ids' in fields_list and not res.get('company_ids'):
            try:
                user_company = self.env.user.company_id
                if user_company:
                    res['company_ids'] = [(6, 0, [user_company.id])]
            except Exception as e:
                _logger.warning("Failed to set default company: %s", e)
        return res
    
    @api.model
    def create(self, vals):
        if not vals.get('company_ids'):
            try:
                user = self.env.user if self.env.user and self.env.user.id != SUPERUSER_ID else self.env['res.users'].browse(SUPERUSER_ID)
                user_company = user.company_id
                if user_company:
                    vals['company_ids'] = [(6, 0, [user_company.id])]
            except Exception as e:
                _logger.warning("Failed to set default company in create: %s", e)
        return super().create(vals)
    
    def write(self, vals):
        if 'company_ids' in vals and not vals['company_ids']:
            try:
                user_company = self.env.user.company_id
                if user_company:
                    vals['company_ids'] = [(6, 0, [user_company.id])]
            except Exception as e:
                _logger.warning("Failed to restore company_ids in write: %s", e)
        return super().write(vals)
    