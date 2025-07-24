from odoo import models, fields

class SalesOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super().action_confirm()

        for order in self:
            for line in order.order_line:
                product = line.product_id


