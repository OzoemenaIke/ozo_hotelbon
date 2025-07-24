from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class StockLot(models.Model):
    _inherit = 'stock.lot'
    isused = fields.Boolean(string='Is Used?')
    validity_date = fields.Date(string='Validity Date')


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'validity_date' not in vals:
                vals['validity_date'] = (fields.Datetime.now() + relativedelta(years=1)).date()

        return super().create(vals_list)
