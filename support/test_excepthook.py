import sys

debug = False

def print_stderr(message):
    print(message, file=sys.stderr)


def new_excepthook(exception_type, exception, traceback, debug_hook=sys.__excepthook__):
    '''print_stderr user friendly error messages normally, full traceback if DEBUG on.
       Adapted from http://stackoverflow.com/questions/27674602/hide-traceback-unless-a-debug-flag-is-set
    '''
    if debug:
        print_stderr('\n*** Error:')
        # raise
        debug_hook(exception_type, exception, traceback)
    else:
        print_stderr("\tnew_excepthook: %s: %s" % (exception_type.__name__, exception))


sys.excepthook = new_excepthook

def raise_it():
    print_stderr("BEGIN raise_it")
    print_stderr("debug == %s" % debug)
    # try:
    raise Exception("intentionally raised")
    # except Exception as e:
    #     print_stderr("In exception handler")
    print_stderr("END raise_it")


if __name__ == '__main__':
    debug = True
    print_stderr("BEGIN inline 1")
    print_stderr("debug == %s" % debug)
    try:
        raise Exception("intentionally raised 1")
    except Exception as e:
        print_stderr("In exception handler 1")
    print_stderr("END inline 1")

    debug = True
    print_stderr("BEGIN inline 2")
    print_stderr("debug == %s" % debug)
    try:
        raise Exception("intentionally raised 2")
    except Exception as e:
        print_stderr("In exception handler 2")
    print_stderr("END inline 2")

    # debug = False
    # raise_it()
    # debug = True
    # raise_it()

