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
from . import custom_models
from openerp import fields, api, exceptions, _


class CowCount(custom_models.HistoricalModel):

    _name = 'cow.count'
    _order = 'sequence desc'

    sequence = fields.Integer('sequence', default=0)
    partner_id = fields.Many2one('res.partner', 'Partner',
                                 states={'current': [('readonly', False)],
                                         'history': [('readonly', True)]})
    date = fields.Date('Date', states={'current': [('readonly', False)],
                                       'history': [('readonly', True)]})
    user_id = fields.Many2one('res.users', 'User', states={'current': [('readonly', False)],
                                                           'history': [('readonly', True)]})
    heifer_0_3 = fields.Integer('Heifer 0-3 months')
    heifer_3_12 = fields.Integer('Heifer 3-12 months')
    heifer_plus_12 = fields.Integer('Heifer >12 months')
    milk_cow = fields.Integer('Milk cows')
    dry_cow = fields.Integer('Dry cows')
    state = fields.Selection(
        (('current', 'Current'), ('history', 'History')), 'State', default='current')