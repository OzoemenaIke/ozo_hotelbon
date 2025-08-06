## Hotel Bon Aanpak

### Product

##### Add `is_voucher` field to `Products`. When `new` is clicked there should be a field you can select.

- Inherit `product_template.py` as a Model and add a boolean field `is_voucher`

- Create an XML `product_template_views.xml` 
- Find & Inherit the New Product form
- Add the field to the New Product form using `xpath`
- Add a unique code using `stock.lot`

- _Here I need to get the delivery date so I can calculate the expiration date of the voucher. It looks like its in sale_order. Not sure how to do this. I can only get the delivery date once the order has been made._
  -  Try: Inherit sale_order, when the order is being confirmed through `action_confirm` , check if `is_voucher` is true in the product.template. Does product appear in `sale_order` though?
  - If the sale_order is confirmed then add an `expiration` date


- These should only be added if the `is_voucher` boolean is true


- The expiration date should be the `delivery date` + 1 year


- The unique code is generated and managed by the `stock.lot`


- You should be able to buy multiple vouchers


----------------------------------------------------------------

- Unique code has been added through stock lots, by enabling tracking in products. This goes for every voucher

- Delivery date + expiration date? But if the delivery is to a company how does it work.


### Notes 8/6/25

Picking is like a receipt (5 pieces of bread, 2 eggs)

A Move is one line at the product level inside the picking
(5 pieces of bread) is 1st product
(2 eggs) is the 2nd product

Move line is the detailed row under a move unit

(5 pieces of bread)
(Bread 1, Bread 2, Bread 3, Bread 4, Bread 5) - This is a move_line!

(2 Eggs)
(Egg 1, Egg 2) - This is a move_line!
A voucher code should be set here

for each move_line, get delivery_date of picking and add that to the date


-- Questions:
Easier way to upgrade modules? maybe -U command

