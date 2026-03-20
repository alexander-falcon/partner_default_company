# -*- coding: utf-8 -*-

from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model_create_multi
    def create(self, vals_list):
        users = super(ResUsers, self.with_context(skip_system_partner_compute=True)).create(vals_list)
        
        for user in users:
            try:
                if user.partner_id:
                    user.partner_id.with_context(skip_system_partner_compute=False)._compute_is_system_partner()
                    _logger.info(
                        "[users.create] Recalculado is_system_partner para partner del usuario %s",
                        user.login
                    )
            except Exception as e:
                _logger.exception(
                    "[users.create] Error al recalcular is_system_partner para usuario %s: %s",
                    user.login, e
                )
        
        return users

    def write(self, vals):
        result = super().write(vals)
        if 'company_ids' in vals or 'company_id' in vals:
            for user in self:
                if user.partner_id:
                    user.partner_id.with_context(skip_system_partner_compute=False)._compute_is_system_partner()
                    _logger.info(
                        "[users.write] Recalculado is_system_partner para partner del usuario %s",
                        user.login
                    )
        
        return result