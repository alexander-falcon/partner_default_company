# -*- coding: utf-8 -*-

from odoo import models, api, SUPERUSER_ID
import logging

_logger = logging.getLogger(__name__)

class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.model
    def create(self, vals):
        company = super().create(vals)
        try:
            partner = company.partner_id
            user = self.env.user if self.env.user.id != SUPERUSER_ID else self.env['res.users'].browse(SUPERUSER_ID)
            user_company = user.company_id
            company_ids = set()
            if company.id:
                company_ids.add(company.id)
            if user_company and user_company.id != company.id:
                company_ids.add(user_company.id)
            if partner and not partner.company_ids:
                partner.with_context(skip_company_check=True).sudo().write({
                    'company_ids': [(6, 0, list(company_ids))]
                })
                _logger.info("Asignando company_ids al partner '%s' desde res.company.create: %s", partner.name, list(company_ids))
        except Exception as e:
            _logger.warning("Error al asignar company_ids al partner desde res.company.create: %s", e)
        return company
