from exceptions import PipeTypeException, PipeMethodException


def pipe_to_cls_method(target_class):
    """
    Wraps a function and passes its arguments to method of the same name
    defined in the given parent class.
    
    :param target_class: Class type/object
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
                method = self.data['function'].__name__
                # Check if method exists.
                self._method_exists(other, method)
                # Pass arguments to the given instance and method.
                return getattr(other, method)(*self.data['args'], **self.data['kwargs'])

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

        return Pipe
    return wrapper


class AttrPipeMixin(object):

    def __init__(self, type_attr_map):
        self.type_attr_map = type_attr_map

    def __rrshift__(self, other):
        """
        Override the '>>' operator in order to allow for 'piping' in of...

        """
        pass

