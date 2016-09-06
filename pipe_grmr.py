# --------------------------------------
# pipe_grmr.py

# Package for creating 'pipe-able' class methods.

__author__ = "Peter Woyzbun"


# ======================================
# Exceptions
# --------------------------------------

class PipeException(Exception):
    """ Generic pipe exception. """
    pass


class PipeTypeException(PipeException):
    """ Wrong class type exception. """
    pass


class PipeOutputException(PipeTypeException):
    """ Pipe output of wrong type exception. """
    pass


class PipeMethodException(PipeException):
    """ Class pipe method exception. """
    pass


# ======================================
# Pipe Class Decorator
# --------------------------------------

def add_pipe(klass):
    """
    Passes __rshift__ operator behaviour/method to wrapped class.

    """
    def __rshift__(self, other):
        return other >> self
    return type(klass.__name__, (klass,), {'__rshift__': __rshift__})


# ======================================
# Pipe Function Decorator
# --------------------------------------

def pipe_to_cls_method(target_class, method_name=None):
    """
    Wraps a function and passes its arguments to method of the same name
    defined in the given parent class.

    :param target_class: Class type/object
    :param method_name: Optional. If no method_name is given, the class
    target class method is assumed to have the same name as the wrapped
    function.

    :return: Output of target class method
    """
    def wrapper(fcn):
        class Pipe(object):

            data = {'function': fcn}

            def __init__(self, *args, **kwargs):
                """
                Parameters
                ----------

                :param args: Arguments from wrapped function.
                :param kwargs: Keyword arguments from wrapped function.
                """

                self.data['args'] = args
                self.data['kwargs'] = kwargs

            def __rrshift__(self, other):
                """
                Override the '>>' operator and...

                :param other: class instance
                :return: class instance
                """
                # Check if piped in class object is of correct instance.
                self._is_instance(other)
                # Get the function name.
                if method_name is None:
                    method = self.data['function'].__name__
                else:
                    method = method_name
                # Check if method exists.
                self._method_exists(other, method)
                # Pass arguments to the given instance and method.
                output = getattr(other, method)(*self.data['args'], **self.data['kwargs'])
                if not isinstance(output, target_class):
                    raise PipeOutputException("Output of piped method is not of type %s"
                                              % target_class.__name__)
                else:
                    return output

            def __rshift__(self, other):
                """
                Override the 'left-side' '>>' operator using same behaviour as the
                'right-side' '>>' operator (__rrshift__).

                """
                return self.__rrshift__(other)

            @staticmethod
            def _is_instance(other):
                """ Raise an exception if the piped in instance is not the correct type. """
                if not isinstance(other, target_class):
                    raise PipeTypeException("First argument is not an '%s' instance."
                                                     % target_class.__class__.__name__)

            @staticmethod
            def _method_exists(other, method):
                """ Raise an exception if the piped instance class method is not defined. """
                if not hasattr(other, method):
                    raise PipeMethodException("Method '%s' is not defined." % method)

            @staticmethod
            def _valid_output(output):
                """ Raise exception if output type of pipe is not of given target class type. """
                if not isinstance(output, target_class):
                    raise PipeOutputException("Output of piped method is not of type %s"
                                              % target_class.__name__)

        return Pipe
    return wrapper
