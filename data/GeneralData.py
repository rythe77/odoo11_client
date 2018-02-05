class GeneralData:
    url = 'localhost'
    port = '8069'
    db_name = 'test'
    page_limit = 50

    partner_fields = ['street', 'street2', 'city', 'country_id', 'phone']
    
    saleorder_fields = ['date_order', 'user_id', 'name', 'partner_id', 'amount_total', 'id']
    saleorder_detail_fields = ['confirmation_date', 'user_id', 'name', 'partner_id', 'amount_total', 'id', 'payment_term_id', 'order_line', 'note', 'x_transporter_id']
    saleorder_line_fields = ['product_id', 'product_uom_qty', 'product_uom', 'price_unit', 'discount', 'price_subtotal']
    saleorder_default_condition = [['state', '=', 'sale']]
    
    stockpicking_fields = ['scheduled_date', 'origin', 'name', 'partner_id', 'state', 'id']
    stockpicking_detail_fields = ['scheduled_date', 'origin', 'name', 'partner_id', 'state', 'id', 'move_lines', 'x_vehicle_notes', 'x_notes', 'x_transporter_id']
    stockpicking_line_fields = ['product_id', 'x_picking_notes', 'product_uom_qty', 'product_uom']
    stockpicking_default_condition = [['partner_id', 'ilike', '']]
    
    invoice_fields = ['date_invoice', 'date_due', 'number', 'partner_id', 'amount_total', 'id']
    invoice_detail_fields = ['date_invoice', 'date_due', 'number', 'partner_id', 'amount_total', 'id', 'invoice_line_ids', 'user_id', 'origin']
    invoice_line_fields = ['product_id', 'quantity', 'uom_id', 'price_unit', 'discount', 'price_subtotal']
    invoice_default_condition = ['&',['type', '=', 'out_invoice'],'|',['state', '=', 'open'],['state', '=', 'paid']]

    @classmethod
    def set_url(cls, url_input):
        cls.url = url_input
    @classmethod
    def set_port(cls, port_input):
        cls.port = port_input
    @classmethod
    def set_db_name(cls, db_name_input):
        cls.db_name = db_name_input
    @classmethod
    def set_page_limit(cls,page_limit_input):
        cls.page_limit = int(page_limit_input)
