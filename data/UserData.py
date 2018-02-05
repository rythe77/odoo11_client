class UserData:
    username = ""
    password = ""
    uid = 0
    sales_access = False
    stock_access = False
    invoice_access = False
    file_path = ''

    @classmethod
    def set_username(cls, username_input):
        cls.username = username_input
    @classmethod
    def set_password(cls, password_input):
        cls.password = password_input
    @classmethod
    def set_uid(cls, uid_input):
        cls.uid = uid_input
    @classmethod
    def give_sales_access(cls):
        cls.sales_access = True
    @classmethod
    def give_stock_access(cls):
        cls.stock_access = True
    @classmethod
    def give_invoice_access(cls):
        cls.invoice_access = True
    @classmethod
    def set_file_path(cls,path):
        cls.file_path = path
