import locale
import datetime

def format_integer(amount):
    locale.setlocale(locale.LC_ALL, '')
    rounded = locale.format("%d", round(amount), grouping=True)
    string_amount = swap_separator(rounded)
    return string_amount

def swap_separator(amount):
    string_amount = str(amount).replace('.', '_(temp)_').replace(',', '.').replace('_(temp)_', ',')
    return string_amount

def format_date(date_string, date_only=False, treeview_format=False):
    if not date_only:
        input_format = '%Y-%m-%d %H:%M:%S'
        if not treeview_format:
            output_format = '%d/%m/%Y'
        else:
            output_format = '%Y-%m-%d %H:%M:%S'
    else:
        input_format = '%Y-%m-%d'
        if not treeview_format:
            output_format = '%d/%m/%Y'
        else:
            output_format = '%Y-%m-%d'
    if date_string == False:
        date_formatted = date_string
    else:
        date_formatted = (datetime.datetime.strptime(date_string, input_format) + datetime.timedelta(hours=8)).strftime(output_format)
    return date_formatted

def format_odoo_field(field):
    if type(field) is list:
        return field[len(field)-1]
    elif type(field) is bool:
        if field == False:
            return ''
        else:
            return 'True'
    elif type(field) is float:
        if field == 0.0:
            return ''
        elif field == round(field):
            return format_integer(field)
        else:
            return swap_separator(field)
    else:
        return field

def map_stockpicking_status(status_input):
    dictionary = {
        'draft': 'Rancangan',
        'waiting': 'Menunggu Operasi',
        'confirmed': 'Menunggu',
        'partially_available': 'Tersedia Sebagian',
        'assigned': 'Tersedia',
        'waiting_validation': 'Menunggu Validasi',
        'done': 'Selesai',
        'cancel': 'Dibatalkan'
        }
    status = dictionary.get(status_input)
    return status

if __name__ == "__main__":
    print(format_currency(22300.4))
