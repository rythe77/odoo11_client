import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

import math
import jinja2
import os

from docxtpl import DocxTemplate
from lib import Formatter
from lib import PrintJob
from data.UserData import UserData
from data.GeneralData import GeneralData


class ModelData:
    def __init__(self, odoo_instance, model_name, model_line_name, treeview, search_entry, page_label, back_button, forward_button, print_button, status_label, default_condition = -1):
        self.odoo = odoo_instance
        self.model_name = model_name
        self.model_line_name = model_line_name
        self.treeview = treeview
        self.search_entry = search_entry
        self.page_label = page_label
        self.back_button = back_button
        self.forward_button = forward_button
        self.print_button = print_button
        self.status_label = status_label
        
        treeview_col = self.treeview.get_columns()
        for col_num,col in enumerate(treeview_col):
            cell = Gtk.CellRendererText()
            col.pack_start(cell, True)
            col.add_attribute(cell, "text", col_num)
        
        if default_condition == -1:
            if self.model_name == 'sale.order':
                default_condition = GeneralData.saleorder_default_condition
            elif self.model_name == 'stock.picking':
                default_condition = GeneralData.stockpicking_default_condition
            elif self.model_name == 'account.invoice':
                default_condition = GeneralData.invoice_default_condition
        self.default_condition_lists = default_condition
        self.current_condition_lists = default_condition

        self.current_page = 0
        self.page_num = 0
        self.total_records = 0

    def no_access_view(self):
        self.treeview.hide()
        self.search_entry.hide()
        self.page_label.hide()
        self.back_button.hide()
        self.forward_button.hide()
        self.print_button.hide()
        if self.model_name == 'sale.order':
            document_name = 'Order Penjualan'
        elif self.model_name == 'stock.picking':
            document_name = 'Surat Jalan'
        elif self.model_name == 'account.invoice':
            document_name = 'Faktur'
        self.status_label.set_text('Anda tidak memiliki izin akses %s' % document_name)

    def show_data(self, condition_lists = -1):
        if condition_lists == -1:
            condition_lists = self.default_condition_lists

        self.count_page(condition_lists)
        if self.page_num != 0:
            self.current_page = 1
            self.update_data(condition_lists)

    def update_data(self, condition_lists = -1):
        if condition_lists == -1:
            condition_lists = self.default_condition_lists

        self.prepare_label()
        if self.model_name == 'sale.order':
            fields = GeneralData.saleorder_fields
            data_lists = self.prepare_saleorder_data(fields, condition_lists)
            self.liststore = Gtk.ListStore(str, str, str, str, str, str)
        elif self.model_name == 'stock.picking':
            fields = GeneralData.stockpicking_fields
            data_lists = self.prepare_stockpicking_data(fields, condition_lists)
            self.liststore = Gtk.ListStore(str, str, str, str, str, str)
        elif self.model_name == 'account.invoice':
            fields = GeneralData.invoice_fields
            data_lists = self.prepare_invoice_data(fields, condition_lists)
            self.liststore = Gtk.ListStore(str, str, str, str, str, str)
        else:
            data_lists = []
            self.liststore = Gtk.ListStore()
    
        # append the values in the model
        for data_list in data_lists:
            self.liststore.append(data_list)
        self.treeview.set_model(self.liststore)

    def count_page(self, conditions):
        num = self.odoo.env[self.model_name].search_count(conditions)
        self.total_records = num
        self.page_num = math.ceil(num/GeneralData.page_limit)

    def prepare_label(self):
        # Set page label
        if self.current_page*GeneralData.page_limit < self.total_records:
            self.page_label.set_text('%d - %d / %d' % ((self.current_page - 1)*GeneralData.page_limit + 1, self.current_page*GeneralData.page_limit, self.total_records))
        else:
            self.page_label.set_text('%d - %d / %d' % ((self.current_page - 1)*GeneralData.page_limit + 1, self.total_records, self.total_records))
        # Set page button label
        if self.current_page == 1 or self.current_page == 0:
            self.back_button.hide()
        else:
            self.back_button.show()
        if self.current_page == self.page_num:
            self.forward_button.hide()
        else:
            self.forward_button.show()

    def prepare_saleorder_data(self, fields, condition_lists):
        # Return appropriate data for this page view
        offset = (self.current_page-1)*GeneralData.page_limit
        order = fields[0] + ' desc'
        records = self.odoo.env[self.model_name].search_read(condition_lists, fields=fields, limit=GeneralData.page_limit, offset=offset, order=order, context={'lang': "id_ID"})
        data_list = []
        for record in records:
            data_list.append([
                Formatter.format_odoo_field(Formatter.format_date(record.get(GeneralData.saleorder_fields[0]), treeview_format=True)),
                Formatter.format_odoo_field(record.get(GeneralData.saleorder_fields[1])),
                Formatter.format_odoo_field(record.get(GeneralData.saleorder_fields[2])),
                Formatter.format_odoo_field(record.get(GeneralData.saleorder_fields[3])),
                Formatter.format_odoo_field(record.get(GeneralData.saleorder_fields[4])),
                Formatter.format_odoo_field(str(record.get(GeneralData.saleorder_fields[5]))),
                ])
        return data_list

    def prepare_stockpicking_data(self, fields, condition_lists):
        # Return appropriate data for this page view
        offset = (self.current_page-1)*GeneralData.page_limit
        order = fields[0] + ' desc'
        records = self.odoo.env[self.model_name].search_read(condition_lists, fields=fields, limit=GeneralData.page_limit, offset=offset, order=order, context={'lang': "id_ID"})
        data_list = []
        for record in records:
            data_list.append([
                Formatter.format_odoo_field(Formatter.format_date(record.get(GeneralData.stockpicking_fields[0]), treeview_format=True)),
                Formatter.format_odoo_field(record.get(GeneralData.stockpicking_fields[1])),
                Formatter.format_odoo_field(record.get(GeneralData.stockpicking_fields[2])),
                Formatter.format_odoo_field(record.get(GeneralData.stockpicking_fields[3])),
                Formatter.format_odoo_field(Formatter.map_stockpicking_status(record.get(GeneralData.stockpicking_fields[4]))),
                Formatter.format_odoo_field(str(record.get(GeneralData.stockpicking_fields[5]))),
                ])
        return data_list

    def prepare_invoice_data(self, fields, condition_lists):
        # Return appropriate data for this page view
        offset = (self.current_page-1)*GeneralData.page_limit
        order = fields[0] + ' desc'
        records = self.odoo.env[self.model_name].search_read(condition_lists, fields=fields, limit=GeneralData.page_limit, offset=offset, order=order, context={'lang': "id_ID"})
        data_list = []
        for record in records:
            data_list.append([
                Formatter.format_odoo_field(Formatter.format_date(record.get(GeneralData.invoice_fields[0]), date_only=True, treeview_format=True)),
                Formatter.format_odoo_field(Formatter.format_date(record.get(GeneralData.invoice_fields[1]), date_only=True, treeview_format=True)),
                Formatter.format_odoo_field(record.get(GeneralData.invoice_fields[2])),
                Formatter.format_odoo_field(record.get(GeneralData.invoice_fields[3])),
                Formatter.format_odoo_field(record.get(GeneralData.invoice_fields[4])),
                Formatter.format_odoo_field(str(record.get(GeneralData.invoice_fields[5]))),
                ])
        return data_list

    def construct_condition_list(self, entry_text):
        conditions = []
        for default_condition in self.default_condition_lists:
            conditions.append(default_condition)
        text_list = entry_text.split('&')
        if len(text_list) > 1:
            conditions.append('&')
            conditions.append(['partner_id', 'ilike', text_list[0]])
            conditions.append(['name', 'ilike', text_list[1]])
        else:
            conditions.append(['partner_id', 'ilike', text_list[0]])
        self.current_condition_lists = conditions

    def prepare_document(self):
        model = self.treeview.get_selection().get_selected()
        if model[1]:
            rowval = model[0].get_value(model[1],5)
            ids = [int(rowval)]
        else:
            return False
        if self.model_name == 'sale.order':
            fields = GeneralData.saleorder_detail_fields
            line_fields = GeneralData.saleorder_line_fields
            self.prepare_saleorder_document(ids, fields, line_fields)
            return True
        elif self.model_name == 'stock.picking':
            fields = GeneralData.stockpicking_detail_fields
            line_fields = GeneralData.stockpicking_line_fields
            self.prepare_stockpicking_document(ids, fields, line_fields)
            return True
        elif self.model_name == 'account.invoice':
            fields = GeneralData.invoice_detail_fields
            line_fields = GeneralData.invoice_line_fields
            self.prepare_invoice_document(ids, fields, line_fields)
            return True

    def prepare_saleorder_document(self, ids, fields, line_fields):
        saleorder_data = self.odoo.env[self.model_name].read(ids, fields=fields)[0]
        partner_data = self.odoo.env['res.partner'].read(saleorder_data.get('partner_id')[0], fields=GeneralData.partner_fields)[0]
        for field in fields:
            if field != 'order_line':
                saleorder_data[field] = Formatter.format_odoo_field(saleorder_data.get(field))
            if 'date' in field:
                saleorder_data[field] = Formatter.format_date(saleorder_data.get(field))
        for field in GeneralData.partner_fields:
            partner_data[field] = Formatter.format_odoo_field(partner_data.get(field))
        saleorder_line_data = self.odoo.env[self.model_line_name].read(saleorder_data.get('order_line'), fields=line_fields)
        for data in saleorder_line_data:
            for field in GeneralData.saleorder_line_fields:
                data[field] = Formatter.format_odoo_field(data.get(field))
        doc = DocxTemplate("template/sale_order.docx")
        context = saleorder_data
        context.update(partner_data)
        context.update({'items':saleorder_line_data})
        jinja_env = jinja2.Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=False
            )
        doc.render(context, jinja_env)
        doc.save("tmp/saleorder.docx")

    def prepare_stockpicking_document(self, ids, fields, line_fields):
        stockpicking_data = self.odoo.env[self.model_name].read(ids, fields=fields)[0]
        partner_data = self.odoo.env['res.partner'].read(stockpicking_data.get('partner_id')[0], fields=GeneralData.partner_fields)[0]
        for field in fields:
            if field != 'move_lines':
                stockpicking_data[field] = Formatter.format_odoo_field(stockpicking_data.get(field))
            if 'date' in field:
                stockpicking_data[field] = Formatter.format_date(stockpicking_data.get(field))
        for field in GeneralData.partner_fields:
            partner_data[field] = Formatter.format_odoo_field(partner_data.get(field))
        stockpicking_line_data = self.odoo.env[self.model_line_name].read(stockpicking_data.get('move_lines'), fields=line_fields)
        for data in stockpicking_line_data:
            for field in GeneralData.stockpicking_line_fields:
                data[field] = Formatter.format_odoo_field(data.get(field))
        doc = DocxTemplate("template/stock_picking.docx")
        context = stockpicking_data
        context.update(partner_data)
        context.update({'items':stockpicking_line_data})
        jinja_env = jinja2.Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=False
            )
        doc.render(context, jinja_env)
        doc.save("tmp/stockpicking.docx")

    def prepare_invoice_document(self, ids, fields, line_fields):
        invoice_data = self.odoo.env[self.model_name].read(ids, fields=fields)[0]
        partner_data = self.odoo.env['res.partner'].read(invoice_data.get('partner_id')[0], fields=GeneralData.partner_fields)[0]
        for field in GeneralData.invoice_detail_fields:
            if field != 'invoice_line_ids':
                invoice_data[field] = Formatter.format_odoo_field(invoice_data.get(field))
            if 'date' in field:
                invoice_data[field] = Formatter.format_date(invoice_data.get(field), date_only=True)
        for field in GeneralData.partner_fields:
            partner_data[field] = Formatter.format_odoo_field(partner_data.get(field))
        invoice_line_data = self.odoo.env[self.model_line_name].read(invoice_data.get('invoice_line_ids'), fields=line_fields)
        for data in invoice_line_data:
            for field in GeneralData.invoice_line_fields:
                data[field] = Formatter.format_odoo_field(data.get(field))
        doc = DocxTemplate("template/account_invoice.docx")
        context = invoice_data
        context.update(partner_data)
        context.update({'items':invoice_line_data})
        jinja_env = jinja2.Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=False
            )
        doc.render(context, jinja_env)
        doc.save("tmp/accountinvoice.docx")

    def send_print_job(self):
        if self.model_name == 'sale.order':
            filename = "tmp/saleorder.docx"
        if self.model_name == 'stock.picking':
            filename = "tmp/stockpicking.docx"
        if self.model_name == 'account.invoice':
            filename = "tmp/invoice.docx"

        filename = os.path.join(UserData.file_path, filename)
        PrintJob.print_job(filename)
        os.remove(filename)
