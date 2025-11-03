# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # @api.model
    # def default_get(self, fields_list):
    #     res = super().default_get(fields_list)
    #     if 'company_ids' in fields_list and not res.get('company_ids'):
    #         try:
    #             user = self.env.user
    #             if user.has_group('base.group_system'):
    #                 active_company = self.env.company
    #                 if active_company:
    #                     res['company_ids'] = [(6, 0, [active_company.id])]
    #                     _logger.info("Asignando company_ids desde la compañía activa (env.company) para administrador: %s", active_company.name)
    #                 else:
    #                     _logger.warning("No se pudo obtener la compañía activa desde env.company")
    #             else:
    #                 user_company = user.company_id
    #                 if user_company and user_company.id:
    #                     res['company_ids'] = [(6, 0, [user_company.id])]
    #                     _logger.info("Asignando company_ids desde la compañía del usuario (user.company_id): %s", user_company.name)
    #                 else:
    #                     _logger.warning("El usuario no tiene una compañía principal asignada")
    #         except Exception as e:
    #             _logger.warning("Error al asignar company_ids en default_get: %s", e)

    #     return res
    
    @api.model
    def create(self, vals):
        vals_list = vals if isinstance(vals, list) else [vals]
        for vals_item in vals_list:
            if not vals_item.get('company_ids'):
                try:
                    user = self.env.user if self.env.user.id != SUPERUSER_ID else self.env['res.users'].browse(SUPERUSER_ID)
                    company_id = user.company_id.id if not user.has_group('base.group_system') else self.env.company.id
                    if company_id:
                        vals_item['company_ids'] = [(6, 0, [company_id])]
                        _logger.info("Asignando company_ids en create para '%s': %s", vals_item.get('name'), company_id)
                except Exception as e:
                    _logger.warning("Error al asignar company_ids en create: %s", e)
        return super().create(vals_list if isinstance(vals, list) else vals_list[0])

    