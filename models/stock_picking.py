from odoo import models, api
import logging
logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def print_has_vouchers(self):
        for picking in self:
            # 1) Has vouchers?
            has_vouchers = any(
                m.state != 'cancel' and m.product_id.product_tmpl_id.is_voucher
                for m in picking.move_ids
            )
            msg = f"{picking.name} has vouchers: {has_vouchers}"
            print(msg)
            logger.info(msg)

            # 2) Print all products on this picking
            if picking.move_ids:
                lines = []
                for m in picking.move_ids:
                    if m.state == 'cancel':
                        continue
                    planned = m.product_uom_qty or 0.0
                    lines.append(f"- {m.product_id.display_name} (planned: {planned:g})")
                prod_msg = f"{picking.name} products:\n" + ("\n".join(lines) if lines else "(none)")
            else:
                prod_msg = f"{picking.name} products: (none)"

            print(prod_msg)
            logger.info(prod_msg)
            # If you also want to see it in the UI, uncomment:
            # picking.message_post(body=f"{msg}<br/>{prod_msg.replace('\n','<br/>')}")


    def button_validate(self):
        # This runs when you click "Check Availability" (reserve).
        for picking in self:
            # 1) Has vouchers?
            has_vouchers = any(
                m.state != 'cancel' and m.product_id.product_tmpl_id.is_voucher
                for m in picking.move_ids
            )
            msg = f"{picking.name} has vouchers: {has_vouchers}"
            print(msg)
            logger.info(msg)

            for move in picking.move_ids:
                names = sorted(move._fields.keys())
                print("FIELDS on stock.move:", ", ".join(names))
                break  # just show once


            for move in picking.move_ids:
                print(move.move_lines_count) # why does this print 0???? there should be move_lines
                for ml in move.move_line_ids:
                    print("hi, entered")
                    print( f"  line -> qty_done={ml.qty_done:g}, lot={ml.lot_id.name or ml.lot_name or ''}")
                line = f"- {move.product_id.display_name} (planned: {move.product_uom_qty:g})"
                print(line)
                logger.info(line)


        res = super().button_validate()
        return res