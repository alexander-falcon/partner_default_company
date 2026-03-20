# -*- coding: utf-8 -*-

from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model_create_multi
    def create(self, vals_list):
        users = super().create(vals_list)
        
        for user in users:
            try:
                if user.partner_id and not user.partner_id.is_system_partner:
                    user.partner_id.sudo().write({'is_system_partner': True})
                    _logger.info(
                        "[users.create] Marcado partner del usuario %s como partner del sistema",
                        user.login
                    )
            except Exception as e:
                _logger.exception(
                    "[users.create] Error al marcar partner: %s", e
                )
        
        return users

    def write(self, vals):
        result = super().write(vals)
        
        if 'company_ids' in vals or 'company_id' in vals:
            for user in self:
                if user.partner_id and not user.partner_id.is_system_partner:
                    user.partner_id.sudo().write({'is_system_partner': True})
                    _logger.info(
                        "[users.write] Marcado partner del usuario %s como partner del sistema",
                        user.login
                    )
        
        return result