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
            if partner:
                existing_ids = partner.company_ids.ids if partner.company_ids else []
                if company.id not in existing_ids:
                    updated_ids = list(set(existing_ids + [company.id]))
                    partner.sudo().write({
                        'company_ids': [(6, 0, updated_ids)]
                    })
                    _logger.info("Extendiendo company_ids del partner '%s' con la nueva compañía: %s", partner.name, company.name)
        except Exception as e:
            _logger.warning("Error al extender company_ids al partner desde res.company.create: %s", e)
        return company