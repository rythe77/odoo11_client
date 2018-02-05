# chose an implementation, depending on os
import platform
if platform.system() == 'Windows': #sys.platform == 'win32':
    import win32api
    import win32print
elif platform.system() == 'Linux':
    import subprocess
else:
    raise Exception("Sorry: no implementation for your platform ('%s') available" % platform.system())

def print_job(filename):
    if platform.system() == 'Windows':
        do_print_windows(filename)
    if platform.system() == 'Linux':
        do_print_linux(filename)

def do_print_windows(filename):
    win32api.ShellExecute (
        0,
        "print",
        filename,
        #
        # If this is None, the default printer will
        # be used anyway.
        #
        '/d:"%s"' % win32print.GetDefaultPrinter (),
        ".",
        0
    )

def do_print_linux(filename):
    #os.system('lpr -Pnama_printer %s' % filename)
    lpr =  subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
    lpr.stdin.write(filename)