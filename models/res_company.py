# -*- coding: utf-8 -*-

from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.model_create_multi
    def create(self, vals_list):
        companies = super().create(vals_list)

        for company in companies:
            try:
                partner = company.partner_id
                 
                if not partner:
                    _logger.warning(
                        "[company.create] La compañía %s (ID: %s) no tiene partner asociado",
                        company.name, company.id
                    )
                    continue
                
                partner_vals = {}

                current_ids = partner.company_ids.ids or []
                if company.id not in current_ids:
                    new_ids = current_ids + [company.id]
                    partner_vals['company_ids'] = [(6, 0, new_ids)]
                    _logger.info(
                        "[company.create] Actualizado company_ids del partner '%s': %s",
                        partner.name, new_ids
                    )

                if partner_vals:
                    partner.sudo().write(partner_vals)
                    partner._compute_company_id()

                if not partner.is_system_partner:
                    partner.sudo().write({'is_system_partner': True})
                    _logger.info(
                        "[company.create] Marcado partner '%s' como partner del sistema",
                        partner.name
                    )

            except Exception as e:
                _logger.exception(
                    "[company.create] Error al actualizar partner de compañía %s (ID: %s): %s",
                    company.name, company.id, e
                )

        return companies