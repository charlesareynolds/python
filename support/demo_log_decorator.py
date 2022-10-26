def decorator1(func):
    """Decorator, returning a wrapped function
    """
    def wrapper(*args, **kwargs):
        """The wrapped function (self is included in args*)
        """
        print("Start {}".format(func.__name__))
        func(*args, **kwargs)
        print("End {}".format(func.__name__))
    return wrapper

@decorator1
def bar1(parm):
    print(parm)

@decorator1
def bat1(parm):
    print(parm)


bar1("parm1")
bat1("parm2")

class SomeClass1:
    @decorator1
    def bar11(self, parm):
        print(parm)

    @decorator1
    def bat11(self, parm):
        print(parm)

test = SomeClass1()
test.bar11("parm11")
test.bat11("parm22")

class SomeClass2(object):

    def write_begin_end(message):
        """Decorator factory, returning a begin-end decorator with the desired message.
        Note: Not a class method, just hidden in the class namespace
        """

        def decorator2(func_to_be_wrapped):
            """Decorator, returning a wrapped function
            Note: Not a class method, just hidden in the class namespace
            """
            def wrapper(self, *args, **kwargs):
                """The wrapped function (self is included in args*)
                """
                print("Start {}".format(message))
                func_to_be_wrapped(self, *args, **kwargs)
                print("End {}".format(message))
            return wrapper
        return decorator2

    @write_begin_end("this")
    def bar2(self, parm):
        print(parm)

    @write_begin_end("that")
    def bat2(self, parm):
        print(parm)


test = SomeClass2()
test.bar2("parm3")
test.bat2("parm4")

