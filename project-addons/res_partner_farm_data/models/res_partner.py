# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Comunitea All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@comunitea.com>$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api, exceptions, _


class ResPartner(models.Model):

    _inherit = 'res.partner'

    _sql_constraints = [
        ('vat_uniq', 'unique (vat)',
         _('Error! Specified VAT Number already exists for any other registered partner.'))
    ]

    farm = fields.Boolean('Farm')
    farm_group = fields.Boolean('Is farm group', compute='_get_farm_group', store=True)
    partner_of = fields.Char('Partner of')
    exploitation_technician = fields.Many2one('res.users',
                                              'Exploitation technician')
    secondary_technician = fields.Many2one('res.users', 'Secondary technician')
    barn_type = fields.Selection((('free', 'Free'), ('stuck', 'Stuck'),
                                  ('mixed', 'Mixed')), 'Barn type')
    dairy_company = fields.Many2one('res.partner', 'Dairy company')
    bed_suppliers = fields.Many2many('res.partner', 'farm_bed_supplier_rel',
                                     'farm_id', 'bed_supplier_id',
                                     'Bed suppliers',
                                     domain=[('supplier', '=', True)])
    production_orientation = fields.Selection(
        (('milk', 'Milk'), ('meat', 'Meat'), ('mixed', 'Mixed'),
         ('orchard', 'Orchard'), ('other', 'Other')), 'Production orientation')
    cornadizas = fields.Integer('Cornadizas quantity')
    electric_power = fields.Integer('Electric power')
    average_annual_consumption = fields.Integer('Average annual consumption')
    pickup_frequency = fields.Integer('Pickup frequency')
    milk_tank_liter = fields.Integer('Milk tank liter')
    supplies_technician = fields.Many2one('res.users', 'Supplies technician')
    lactating_cows = fields.Many2one('product.product', 'Lactating cows')
    dry_cows = fields.Many2one('product.product', 'Dry cows')
    heifers = fields.Many2one('product.product', 'Heifers')
    bait = fields.Many2one('product.product', 'Bait')
    feeding_supplier = fields.Many2one('res.partner', 'Feeding supplier',
                                       domain=[('supplier', '=', True)])
    milk_quality_supplier = fields.Many2one('res.partner',
                                            'Milk quality supplier',
                                            domain=[('supplier', '=', True)])
    counselling_supplier = fields.Many2one('res.partner',
                                           'Counselling supplier',
                                           domain=[('supplier', '=', True)])
    clinic_supplier = fields.Many2one('res.partner', 'Clinic supplier',
                                      domain=[('supplier', '=', True)])
    mixer_truck_supplier = fields.Many2one('res.partner',
                                           'Mixer truck supplier',
                                           domain=[('supplier', '=', True)])
    replacement_supplier = fields.Many2one('res.partner',
                                           'Replacement supplier',
                                           domain=[('supplier', '=', True)])
    reproduction_supplier = fields.Many2one('res.partner',
                                            'Reproduction supplier',
                                            domain=[('supplier', '=', True)])
    adsg_certification_supplier = fields.Many2one(
        'res.partner', 'ADSG certification supplier',
        domain=[('supplier', '=', True)])
    special_mix = fields.Integer('Special mix')
    dry_mix = fields.Integer('Dry mix')
    mh = fields.Integer('mh')
    standard_fodder = fields.Integer('Standard fodder')
    concentrate_capacity = fields.Integer('concentrate capacity')
    forage_silos = fields.Integer('Forage silos')
    manure_pit = fields.Integer('Manure pit')
    manure_pit_outdoor = fields.Integer('Manure pit outdoor')
    trailer_access = fields.Boolean('Trailer access')
    temporary = fields.Boolean('Temporary')

    @api.one
    @api.depends('farm', 'company_id', 'company_id.child_ids')
    def _get_farm_group(self):
        if self.farm and self.company_id.child_ids:
            self.farm_group = True
        else:
            self.farm_group = False

    @api.model
    def create(self, vals):
        if self._context.get('company_partner', False):
            vals['farm'] = True
        res = super(ResPartner, self).create(vals)
        if vals.get('exploitation_technician', False):
            res.message_subscribe([res.exploitation_technician.partner_id.id])
        if vals.get('secondary_technician', False):
            res.message_subscribe([res.secondary_technician.partner_id.id])
        return res

    @api.multi
    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        for partner in self:
            if vals.get('exploitation_technician', False):
                partner.message_subscribe(
                    [partner.exploitation_technician.partner_id.id])
            if vals.get('secondary_technician', False):
                partner.message_subscribe(
                    [partner.secondary_technician.partner_id.id])
        return res

    @api.multi
    def action_account_assets(self):
        return {
            'domain': "[('company_id','=',[" + str(self.company_id.id) + "])]",
            'name': _('Assets'),
            'view_mode': 'tree,form',
            'view_type': 'form',
            'context': {'tree_view_ref':
                        'account_asset.view_account_asset_asset_tree'},
            'res_model': 'account.asset.asset',
            'type': 'ir.actions.act_window',
        }
