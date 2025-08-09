# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import uuid, hashlib
import traceback

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _generate_test_code(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        raw = f"{now}-{uuid.uuid4()}"
        h = hashlib.sha256(raw.encode()).hexdigest()
        return ''.join(filter(str.isdigit, h))[:12]

    def _calc_valid_till(self):
        return datetime.today() + relativedelta(years=1)

    def _ensure_move_lines(self, move):
        if move.move_line_ids:
            return move.move_line_ids
        if not move.product_uom_qty:
            raise UserError(_("No quantity to deliver on move for %s.") % move.product_id.display_name)
        vals = {
            'move_id': move.id,
            'location_id': move.location_id.id,
            'location_dest_id': move.location_dest_id.id,
            'product_id': move.product_id.id,
            'product_uom_id': move.product_uom.id,
            'quantity': move.product_uom_qty,
        }
        mls = self.env['stock.move.line'].create(vals)
        print(f"Created 1 move line for {move.product_id.display_name} (quantity={move.product_uom_qty}).")
        return mls

    def button_validate(self):
        print("Started button_validate")
        for picking in self:
            print(f"Voucher auto-assign: start (picking: {picking.name}, type: {picking.picking_type_code}).")
            if picking.picking_type_code != 'outgoing':
                print("Skipped: picking is not outgoing.")
                continue
            total_assigned = 0
            total_skipped_has_lot = 0
            total_non_voucher = 0
            try:
                for move in picking.move_ids:
                    product = move.product_id
                    if not getattr(product, 'is_voucher', False):
                        total_non_voucher += 1
                        print(f"Move {product.display_name} skipped (not a voucher).")
                        continue
                    print(f"Processing voucher move: {product.display_name} (qty={move.product_uom_qty}).")
                    tracking = product.tracking
                    if tracking == 'serial':
                        move_lines = self.env['stock.move.line']
                    else:
                        move_lines = self._ensure_move_lines(move)
                    def _unique_code():
                        for _ in range(6):
                            code = self._generate_test_code()
                            if not self.env['stock.lot'].search_count([
                                ('name', '=', code),
                                ('product_id', '=', product.id),
                                ('company_id', '=', picking.company_id.id),
                            ]):
                                return code
                        raise UserError(_("Couldn't generate a unique serial."))
                    def _create_lot(code, expiry):
                        return self.env['stock.lot'].create({
                            'name': code,
                            'product_id': product.id,
                            'company_id': picking.company_id.id,
                            'expiration_date': expiry,
                        })
                    if tracking == 'serial':
                        total = int(move.product_uom_qty)
                        already = len(move.move_line_ids.filtered(lambda l: l.lot_id))
                        to_create = max(0, total - already)
                        for ml in move.move_line_ids:
                            if not ml.lot_id and not ml.lot_name and (getattr(ml, 'quantity', 0.0) or 0.0) == 0:
                                ml.unlink()
                        for _ in range(to_create):
                            code = _unique_code()
                            expiry = self._calc_valid_till()
                            lot = _create_lot(code, expiry)
                            self.env['stock.move.line'].create({
                                'move_id': move.id,
                                'location_id': move.location_id.id,
                                'location_dest_id': move.location_dest_id.id,
                                'product_id': product.id,
                                'product_uom_id': move.product_uom.id,
                                'lot_id': lot.id,
                                'quantity': 1.0,
                            })
                            print(f"Created serial {code}; expires {expiry.date()}")
                    elif tracking == 'lot':
                        target = move.move_line_ids[:1] or self._ensure_move_lines(move)
                        ml = target[0]
                        if not ml.lot_id:
                            code = _unique_code()
                            expiry = self._calc_valid_till()
                            lot = _create_lot(code, expiry)
                            ml.write({'lot_id': lot.id})
                            print(f"Created lot {code}; expires {expiry.date()}")
                    else:
                        pass
            except Exception as e:
                tb = traceback.format_exc()
                print(f"Error during voucher assignment: {str(e)}")
                print(tb)
            print(f"Voucher auto-assign: done. Assigned={total_assigned}, already_had_lot={total_skipped_has_lot}, non_voucher_moves={total_non_voucher}.")
            for ml in picking.move_line_ids:
                qty_val = getattr(ml, 'quantity', None)
                print(
                    f"Move line {ml.id}: quantity={qty_val}, lot_name={ml.lot_name}, "
                    f"lot_id={ml.lot_id and ml.lot_id.name}, product={ml.product_id.display_name}, "
                    f"tracking={ml.product_id.tracking}"
                )
        return super().button_validate()
