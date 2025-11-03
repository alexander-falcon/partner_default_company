# -*- coding: utf-8 -*-
from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import ValidationError
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
                _logger.warning("Failed to set default company in default_get: %s", e)
        return res

    @api.model
    def create(self, vals):
        if not vals.get('company_ids'):
            try:
                if self.env.context.get('create_company') and vals.get('is_company') and vals.get('name'):
                    company = self.env['res.company'].search(
                        [('name', '=', vals['name']), ('active', '=', True)],
                        order='create_date desc',
                        limit=1
                    )
                    if company:
                        vals['company_ids'] = [(6, 0, [company.id])]
                        _logger.info("Asignado company_ids al partner '%s' desde la compañía '%s'", vals['name'], company.name)
                    else:
                        _logger.warning("No se encontró compañía coincidente para el partner '%s'", vals['name'])
                else:
                    user = self.env.user if self.env.user and self.env.user.id != SUPERUSER_ID else self.env['res.users'].browse(SUPERUSER_ID)
                    user_company = user.company_id
                    if user_company:
                        vals['company_ids'] = [(6, 0, [user_company.id])]
            except Exception as e:
                _logger.warning("Error al asignar company_ids en create: %s", e)
        return super().create(vals)

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            if not record.company_ids:
                try:
                    user_company = self.env.user.company_id
                    if user_company:
                        record.company_ids = [(6, 0, [user_company.id])]
                        _logger.info("company_ids restaurado automáticamente en write para %s", record.name)
                except Exception as e:
                    _logger.warning("Error al restaurar company_ids en write: %s", e)
        return res

    @api.constrains('company_ids')
    def _check_company_ids(self):
        for record in self:
            if not record.company_ids:
                raise ValidationError("No se puede dejar el campo 'company_ids' vacío.")


