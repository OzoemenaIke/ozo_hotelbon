from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

class StockLot(models.Model):
    _inherit = 'stock.lot'

    @api.model
    def create(self, vals):
        lot = super().create(vals)
        # Kijk of het product een voucher is
        product = lot.product_id or lot.product_tmpl_id.product_variant_ids[:1]
        if product and product.is_voucher:

            seq = self.env['ir.sequence'].next_by_code('hotel.voucher')
            lot.lot_name = seq

            today = fields.Date.context_today(self)
            lot.expiration_date = today + relativedelta(years=1)
        return lot



