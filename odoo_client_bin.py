import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

import os, odoorpc, ssl, urllib.request, configparser

from lib import ModelData
from data.GeneralData import GeneralData
from data.UserData import UserData


class MainPage:
    def on_window1_destroy(self, object, data=None):
        Gtk.main_quit()

    def on_cancel_button_clicked(self, object, data=None):
        Gtk.main_quit()

    def on_about_activate(self, object, data=None):
        self.response = self.about_dialog.run()
        self.about_dialog.hide()

    def on_saleorder_forward_button_clicked(self, object, data=None):
        if self.saleorder_model.page_num != 0 and self.saleorder_model.current_page != self.saleorder_model.page_num:
            self.saleorder_model.current_page = self.saleorder_model.current_page + 1
            self.saleorder_model.update_data(self.saleorder_model.current_condition_lists)

    def on_saleorder_back_button_clicked(self, object, data=None):
        if self.saleorder_model.page_num != 0 and self.saleorder_model.current_page != 1:
            self.saleorder_model.current_page = self.saleorder_model.current_page - 1
            self.saleorder_model.update_data(self.saleorder_model.current_condition_lists)

    def on_saleorder_searchentry_activate(self, entry, data=None):
        self.saleorder_model.construct_condition_list(entry.get_text())
        self.saleorder_model.show_data(self.saleorder_model.current_condition_lists)

    def on_saleorder_print_button_clicked(self, object, data=None):
        ready = self.saleorder_model.prepare_document()
        if not ready:
            error_message = 'Error! Tidak ada dokumen yang dipilih.\nPilih salah satu dokumen terlebih dahulu'
            self.show_error_message(error_message)
        else:
            self.saleorder_model.send_print_job()

    def on_stockpicking_forward_button_clicked(self, object, data=None):
        if self.stockpicking_model.page_num != 0 and self.stockpicking_model.current_page != self.stockpicking_model.page_num:
            self.stockpicking_model.current_page = self.stockpicking_model.current_page + 1
            self.stockpicking_model.update_data(self.stockpicking_model.current_condition_lists)

    def on_stockpicking_back_button_clicked(self, object, data=None):
        if self.stockpicking_model.page_num != 0 and self.stockpicking_model.current_page != 1:
            self.stockpicking_model.current_page = self.stockpicking_model.current_page - 1
            self.stockpicking_model.update_data(self.stockpicking_model.current_condition_lists)

    def on_stockpicking_searchentry_activate(self, entry, data=None):
        self.stockpicking_model.construct_condition_list(entry.get_text())
        self.stockpicking_model.show_data(self.stockpicking_model.current_condition_lists)

    def on_stockpicking_print_button_clicked(self, object, data=None):
        ready = self.stockpicking_model.prepare_document()
        if not ready:
            error_message = 'Error! Tidak ada dokumen yang dipilih.\nPilih salah satu dokumen terlebih dahulu'
            self.show_error_message(error_message)
        else:
            self.stockpicking_model.send_print_job()

    def on_invoice_forward_button_clicked(self, object, data=None):
        if self.invoice_model.page_num != 0 and self.invoice_model.current_page != self.invoice_model.page_num:
            self.invoice_model.current_page = self.invoice_model.current_page + 1
            self.invoice_model.update_data(self.invoice_model.current_condition_lists)

    def on_invoice_back_button_clicked(self, object, data=None):
        if self.invoice_model.page_num != 0 and self.invoice_model.current_page != 1:
            self.invoice_model.current_page = self.invoice_model.current_page - 1
            self.invoice_model.update_data(self.invoice_model.current_condition_lists)

    def on_invoice_searchentry_activate(self, entry, data=None):
        self.invoice_model.construct_condition_list(entry.get_text())
        self.invoice_model.show_data(self.invoice_model.current_condition_lists)

    def on_invoice_print_button_clicked(self, object, data=None):
        ready = self.invoice_model.prepare_document()
        if not ready:
            error_message = 'Error! Tidak ada dokumen yang dipilih.\nPilih salah satu dokumen terlebih dahulu'
            self.show_error_message(error_message)
        else:
            self.invoice_model.send_print_job()

    def on_close_button_clicked(self, button, data=None):
        self.message_window_obj.hide()

    def on_username_entry_activate(self, button, data=None):
        self.on_okay_button_clicked(button, data)

    def on_password_entry_activate(self, button, data=None):
        self.on_okay_button_clicked(button, data)

    def on_okay_button_clicked(self, button, data=None):
        username = self.builder.get_object("username_entry").get_text()
        password = self.builder.get_object("password_entry").get_text()
        try:
            self.odoo.login(GeneralData.db_name, username, password)
            self.initiate_window()
        except odoorpc.error.RPCError as exc:
            self.builder.get_object("login_message").set_text('Login gagal!\nPastikan nama pengguna dan kata sandi\nAnda sudah benar\ndan server dalam keadaan aktif')

    def __init__(self):
        self.read_config()
        
        self.gladefile = "ui/main_page.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("main_window")
        self.login_window_obj = self.builder.get_object("password_input_dialog")
        self.message_window_obj = self.builder.get_object("error_messagedialog")
        self.about_dialog = self.builder.get_object("aboutdialog1")
        self.status_label = self.builder.get_object("status_label")

        self.odoo = self.prepare_odoo_instance()

        self.saleorder_model = ModelData.ModelData(
                self.odoo,
                'sale.order',
                'sale.order.line',
                self.builder.get_object("saleorder_treeview"),
                self.builder.get_object("saleorder_searchentry"),
                self.builder.get_object("saleorder_page_label"),
                self.builder.get_object("saleorder_back_button"),
                self.builder.get_object("saleorder_forward_button"),
                self.builder.get_object("saleorder_print_button"),
                self.builder.get_object("saleorder_statuslabel")
                )

        self.stockpicking_model = ModelData.ModelData(
                self.odoo,
                'stock.picking',
                'stock.move',
                self.builder.get_object("stockpicking_treeview"),
                self.builder.get_object("stockpicking_searchentry"),
                self.builder.get_object("stockpicking_page_label"),
                self.builder.get_object("stockpicking_back_button"),
                self.builder.get_object("stockpicking_forward_button"),
                self.builder.get_object("stockpicking_print_button"),
                self.builder.get_object("stockpicking_statuslabel")
                )

        self.invoice_model = ModelData.ModelData(
                self.odoo,
                'account.invoice',
                'account.invoice.line',
                self.builder.get_object("invoice_treeview"),
                self.builder.get_object("invoice_searchentry"),
                self.builder.get_object("invoice_page_label"),
                self.builder.get_object("invoice_back_button"),
                self.builder.get_object("invoice_forward_button"),
                self.builder.get_object("invoice_print_button"),
                self.builder.get_object("invoice_statuslabel")
                )

        Gtk.Widget.show(self.login_window_obj)

    def read_config(self):
        # Get config from file
        config = configparser.ConfigParser()
        try:
            config.read('data/config.ini')
            try:
                GeneralData.set_url(config['SERVER']['url'])
                GeneralData.set_port(config['SERVER']['port'])
                GeneralData.set_db_name(config['SERVER']['db_name'])
                GeneralData.set_page_limit(config['VIEW']['page_limit'])
            except KeyError:
                #TODO: show error of incorrect config file structure
                pass
        except FileNotFoundError:
            #TODO: show error of config file not found
            pass
        else:
            #TODO: show unknown error
            pass

    def prepare_odoo_instance(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
        return odoorpc.ODOO(GeneralData.url, protocol='jsonrpc+ssl', port=GeneralData.port, opener=opener)

    def initiate_window(self):
        self.check_groups()
        UserData.set_file_path(os.path.dirname(__file__))
        if UserData.sales_access:
            self.saleorder_model.show_data()
        else:
            self.saleorder_model.no_access_view()
        if UserData.stock_access:
            self.stockpicking_model.show_data()
        else:
            self.stockpicking_model.no_access_view()
        if UserData.invoice_access:
            self.invoice_model.show_data()
        else:
            self.invoice_model.no_access_view()

        self.login_window_obj.destroy()
        self.window.show()
        self.window.maximize()
        self.status_label.set_text('Log masuk sebagai : ' + self.odoo.env.user.name)

    def check_groups(self):
        groups = self.odoo.env.user.groups_id
        parsed_groups = []
        for group in groups:
            parsed_groups.append((group.full_name).split('/')[0])
        if any('Penjualan' in group for group in parsed_groups) and self.odoo.env['sale.order'].check_access_rights:
            UserData.give_sales_access()
        if any('Persediaan' in group for group in parsed_groups) and self.odoo.env['stock.picking'].check_access_rights:
            UserData.give_stock_access()
        if any('Akuntansi' in group for group in parsed_groups) or any('Penagihan' in group for group in parsed_groups) and self.odoo.env['account.invoice'].check_access_rights:
            UserData.give_invoice_access()

    def show_error_message(self, message):
        self.message_window_obj.set_markup(message)
        self.message_window_obj.show()

if __name__ == "__main__":
    main = MainPage()
    Gtk.main()