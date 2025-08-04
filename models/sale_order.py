from odoo import models, api
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # def action_confirm(self):
    #     res = super().action_confirm()
    #
    #
    #     return res
