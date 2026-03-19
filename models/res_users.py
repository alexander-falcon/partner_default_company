# -*- coding: utf-8 -*-

from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def default_get(self, fields_list):
        """Valores por defecto al crear usuario"""
        try:
            res = super(ResUsers, self.sudo()).default_get(fields_list)
            _logger.info(
                "[users.default_get] Obtenidos defaults para creación de usuario"
            )
            return res
        except Exception as e:
            _logger.exception("[users.default_get] Error: %s", e)
            return super().default_get(fields_list)

    @api.model_create_multi
    def create(self, vals_list):
        """Crear usuarios con sudo() para evitar problemas de permisos"""
        try:
            users = super(ResUsers, self.sudo()).create(vals_list)
            
            _logger.info(
                "[users.create] Creados %d usuarios con sudo para %s",
                len(users), self.env.user.login
            )
            
            return users
            
        except Exception as e:
            _logger.exception("[users.create] Error: %s", e)
            raise