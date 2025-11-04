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
                    _logger.info("Extendiendo company_ids del partner '%s' con la nueva compañía: %s", partner.name, company.name)
            except Exception as e:
                _logger.warning("Error al extender company_ids al partner desde res.company.create: %s", e)

        return companies