# odoo11_client
Simple odoo 11 client for printing on dot matrix printer.

Printing document on dot matrix printer from odoo is problematic because odoo by default output PDF document. Other reporting engine may output document on text format, such as odt, but this create another problem for my implementation. Downloading text document on odt format will allow user to easily change document's content before printing, which is not desirable for me.

Therefore I create this simple python program to fetch data from odoo server through JSON-RPC, create docx documents and send it directly to client system's default printer (which is set to a dot matrix printer).
