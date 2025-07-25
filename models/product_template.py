from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Add line is_voucher as boolean
    is_voucher = fields.Boolean('Is a Voucher')
