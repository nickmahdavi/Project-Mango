import sys


def log()
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return f"{exc_type.__name__} at line {exc_tb.tb_lineno}: {exc_obj}"
