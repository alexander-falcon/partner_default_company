# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError
from odoo import SUPERUSER_ID


@tagged('post_install', 'standard')
class TestResPartnerCompanyIds(TransactionCase):

    def setUp(self):
        super().setUp()
        self.ResPartner = self.env['res.partner']
        self.ResCompany = self.env['res.company']
        self.AdminUser = self.env.ref('base.user_admin')
        self.NormalUser = self.env.ref('base.user_demo')
        self.DefaultCompany = self.env.company

    def test_default_get_admin(self):
        """Verifica que default_get asigne env.company si el usuario es administrador"""
        self.env.user = self.AdminUser
        values = self.ResPartner.default_get(['company_ids'])
        self.assertIn('company_ids', values)
        self.assertEqual(values['company_ids'][0][2], [self.env.company.id])

    def test_default_get_normal_user(self):
        """Verifica que default_get asigne user.company_id si el usuario no es administrador"""
        self.env.user = self.NormalUser
        values = self.ResPartner.default_get(['company_ids'])
        self.assertIn('company_ids', values)
        self.assertEqual(values['company_ids'][0][2], [self.NormalUser.company_id.id])

    def test_create_partner_as_company(self):
        """Verifica que no se asignen company_ids si el partner representa una compañía"""
        partner = self.ResPartner.create({
            'name': 'Empresa X',
            'is_company': True
        })
        self.assertFalse(partner.company_ids)

    def test_create_partner_normal_user(self):
        """Verifica que se asignen company_ids al crear un partner normal"""
        self.env.user = self.NormalUser
        partner = self.ResPartner.create({
            'name': 'Cliente Y',
            'is_company': False
        })
        self.assertIn(self.NormalUser.company_id, partner.company_ids)

    def test_write_restores_company_ids(self):
        """Verifica que write restaure company_ids si está vacío y no es compañía"""
        self.env.user = self.NormalUser
        partner = self.ResPartner.create({
            'name': 'Cliente Z',
            'is_company': False,
            'company_ids': [(6, 0, [self.NormalUser.company_id.id])]
        })
        # Vaciar company_ids usando contexto para evitar restricción
        partner.with_context(skip_company_check=True).write({'company_ids': [(5, 0, 0)]})
        # Ejecutar write para restaurar
        partner.write({'name': 'Cliente Z actualizado'})
        self.assertIn(self.NormalUser.company_id, partner.company_ids)

    def test_write_skips_if_is_company(self):
        """Verifica que write no restaure company_ids si el partner representa una compañía"""
        partner = self.ResPartner.create({
            'name': 'Empresa W',
            'is_company': True,
            'company_ids': [(5, 0, 0)]
        })
        partner.write({'name': 'Empresa W actualizada'})
        self.assertFalse(partner.company_ids)

    def test_constraint_company_ids_required(self):
        """Verifica que se lance ValidationError si company_ids está vacío y no es compañía"""
        with self.assertRaises(ValidationError):
            self.ResPartner.create({
                'name': 'Cliente sin compañía',
                'is_company': False,
                'company_ids': [(5, 0, 0)]
            })

    def test_company_creation_assigns_partner_company_ids(self):
        """Verifica que al crear una compañía, su partner recibe correctamente el campo company_ids"""
        self.env.user = self.AdminUser
        company = self.ResCompany.create({
            'name': 'Compañía Nueva',
        })
        partner = company.partner_id
        self.assertIn(company.id, partner.company_ids.ids)
        self.assertIn(self.AdminUser.company_id.id, partner.company_ids.ids)

    def test_company_creation_does_not_duplicate_company_ids(self):
        """Verifica que no se duplican company_ids si el partner ya tiene asignaciones"""
        self.env.user = self.AdminUser
        company = self.ResCompany.create({
            'name': 'Compañía Duplicada',
        })
        partner = company.partner_id
        # Simular que ya tiene company_ids
        partner.write({'company_ids': [(6, 0, [company.id])]})
        # Forzar reescritura desde create (no debería duplicar)
        company2 = self.ResCompany.create({
            'name': 'Compañía Repetida',
        })
        self.assertEqual(len(set(partner.company_ids.ids)), len(partner.company_ids.ids))

    def test_company_creation_with_superuser(self):
        """Verifica que el superusuario puede crear una compañía sin errores"""
        self.env.user = self.env['res.users'].browse(SUPERUSER_ID)
        company = self.ResCompany.create({
            'name': 'Compañía Superusuario',
        })
        partner = company.partner_id
        self.assertIn(company.id, partner.company_ids.ids)

    def test_partner_company_ids_restored_if_missing(self):
        """Verifica que un partner no empresarial restaura company_ids si se vacía"""
        self.env.user = self.AdminUser
        partner = self.ResPartner.create({
            'name': 'Cliente sin compañía',
            'is_company': False,
            'company_ids': [(6, 0, [self.AdminUser.company_id.id])]
        })
        partner.with_context(skip_company_check=True).write({'company_ids': [(5, 0, 0)]})
        partner.write({'name': 'Cliente actualizado'})
        self.assertTrue(partner.company_ids)


