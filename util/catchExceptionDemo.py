import sys, traceback

try:
    3/0
except Exception:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback,limit=100, file=sys.stdout)