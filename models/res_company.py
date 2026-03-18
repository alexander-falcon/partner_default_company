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
                if partner:
                    partner.sudo().write({
                        'company_ids': [(6, 0, [company.id])]
                    })
                    _logger.info(
                        "[company.create] Asignado company_ids del partner '%s' a compañía: %s (ID: %s)",
                        partner.name, company.name, company.id
                    )
            except Exception as e:
                _logger.exception(
                    "[company.create] Error al asignar company_ids al partner de compañía %s: %s",
                    company.name, e
                )

        return companies