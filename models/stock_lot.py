from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class StockLot(models.Model):
    _inherit = 'stock.lot'
