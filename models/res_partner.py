# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def default_get(self, fields_list):
        """Valores por defecto al crear partner"""
        res = super().default_get(fields_list)

        if 'company_ids' in fields_list and not res.get('company_ids'):
            try:
                user = self.env.user
                company = (
                    self.env.company if len(user.company_ids) > 1
                    else user.company_id
                )
                
                if company:
                    context_company = self.env.context.get('default_company_ids')
                    if not context_company:
                        company_sudo = company.sudo()
                        res['company_ids'] = [(6, 0, [company_sudo.id])]
                        _logger.info(
                            "[default_get] Asignado company_ids='%s' (%s) a partner por defecto (usuario: %s)",
                            company_sudo.id, company_sudo.name, user.login
                        )
                    else:
                        _logger.info(
                            "[default_get] Se respeta compañía del contexto: %s",
                            context_company
                        )
                else:
                    _logger.warning(
                        "[default_get] No se pudo determinar compañía activa para partner"
                    )
            except Exception as e:
                _logger.exception("[default_get] Error inesperado: %s", e)
                
        return res
    
    @api.model_create_multi
    def create(self, vals_list):
        user = self.env.user
        company = (
            self.env.company if len(user.company_ids) > 1
            else user.company_id
        )
        
        processed_vals_list = []
        
        for vals in vals_list:
            try:
                new_vals = vals.copy()
                partner_name = vals.get('name', 'Sin nombre')

                if 'company_ids' not in vals and company:
                    company_sudo = company.sudo()
                    new_vals['company_ids'] = [(6, 0, [company_sudo.id])]
                    _logger.info(
                        "[create] Asignado company_ids='%s' (%s) al partner '%s' (origen: %s)",
                        company_sudo.id, company_sudo.name, partner_name,
                        self._context.get('params', {}).get('model', 'desconocido')
                    )
                elif 'company_ids' in vals:
                    _logger.info(
                        "[create] Partner '%s' ya tenía company_ids definido, se respeta: %s",
                        partner_name, vals['company_ids']
                    )
                else:
                    _logger.warning(
                        "[create] No hay compañía activa para asignar al partner '%s'",
                        partner_name
                    )
                    
                processed_vals_list.append(new_vals)
                
            except Exception as e:
                _logger.exception(
                    "[create] Error procesando partner '%s': %s",
                    vals.get('name', 'Sin nombre'), e
                )
                processed_vals_list.append(vals)

        partners = super(ResPartner, self.sudo()).create(processed_vals_list)

        _logger.info(
            "[create] Creados %d partners para usuario %s",
            len(partners), user.login
        )
        
        return partners
