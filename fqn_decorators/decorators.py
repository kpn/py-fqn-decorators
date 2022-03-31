import functools
import sys


def get_fqn(obj):
    """
    This function tries to determine the fully qualified name (FQN) of the callable that is provided.
    It only works for classes, methods and functions.
    It is unable to properly determine the FQN of class instances, static methods and class methods.
    """
    im_self = getattr(obj, "__self__", None)
    im_class = getattr(im_self, "__class__", None)
    if im_self and im_class:
        path = [
            getattr(im_class, "__module__", None),
            getattr(im_class, "__name__", None),
            getattr(obj, "__name__", None),
        ]
    else:
        path = [
            getattr(obj, "__module__", None),
            getattr(obj, "__qualname__", "").replace("<locals>.", ""),
        ]
    return ".".join(filter(None, path))


class Decorator:
    """
    A base class to easily create decorators.
    """

    def __init__(self, func=None, _initialized=False, **params):
        if func:
            functools.update_wrapper(self, func)

        self._initialized = _initialized
        """Special flag that indicates we are in a separate decorator instance during a function call"""

        self.func = func
        """The callable that is being decorated"""

        self.fqn = None
        """The fully qualified name of the callable"""

        self.args = ()
        """The non-keyworded arguments with which the callable will be called"""

        self.kwargs = {}
        """The keyword arguments with which the callable will be called"""

        self.params = params
        """The keyword arguments provided to the decorator on init"""

        self.result = None
        """The result of the execution of the callable"""

        self.exc_info = None
        """Exception information in case of an exception"""

    def _ensure_decorator_instance(self, *args, **kwargs):
        """
        Makes sure that a separate decorator class instance is created for each decorated function call.
        Otherwise all function decorator attributes will be shared across all calls.

        NB: to be called only from the __call__() method

        Returns: tuple(object, bool) : where bool is a flag whether the object must be returned to the caller
        """
        if not self._initialized:
            if not self.func:
                # Decorator was initialized with arguments
                return self.__class__(args[0], **self.params), True

            # The `self.func` at the caller site is replaced with the `self` decorator instance.
            # Should a user override `fqn` on it, the «inner» decorator created for the particular
            # function call will still see the FQN as returned by the global `get_fqn()` function.
            # In particular, that'd prevent an inherited decorator from seeing the overridden FQN
            # since it'd be lost in the «outer» decorator instance.
            inner_decorator = self.__class__(self.func, _initialized=True, **self.params)
            inner_decorator.fqn = self.get_fqn()
            return inner_decorator(*args, **kwargs), True

        self.fqn = self.get_fqn()
        self.args = args
        self.kwargs = kwargs
        return None, False

    def __call__(self, *args, **kwargs):
        return_value, should_return = self._ensure_decorator_instance(*args, **kwargs)
        if should_return:
            return return_value

        self.before()
        try:
            self.result = self.func(*self.args, **self.kwargs)
        except:  # noqa: E722
            self.exc_info = sys.exc_info()
            self.exception()
            raise
        finally:
            self.after()

        return self.result

    def __getattr__(self, attr):
        if hasattr(self.func, attr):
            return getattr(self.func, attr)
        raise AttributeError("'{}' object has no attribute {}".format(self, attr))

    def __get__(self, obj, type=None):
        return self.__class__(self.func.__get__(obj, type), **self.params)

    def get_fqn(self):
        """Allow overriding the fqn and also change functionality to determine fqn."""
        return self.fqn or get_fqn(self.func)

    def before(self):
        """Allow performing an action before the function is called."""
        pass

    def after(self):
        """Allow performing an action after the function is called."""
        pass

    def exception(self):
        """Allow exception processing (note that the exception will still be raised after processing."""
        pass


class ChainedDecorator(Decorator):
    """
    Simple decorator which allows you to combine regular decorators and decorators based on Decorator.
    It will preserve the FQN for those based on Decorator.
    """

    def __init__(self, func=None, decorators=None, **params):
        """Override the init just to make the decorators argument more visible"""
        params["decorators"] = decorators
        super(ChainedDecorator, self).__init__(func, **params)

    def before(self):
        for decorator in self.params.get("decorators", []):
            self.func = decorator(self.func)
            if hasattr(self.func, "fqn"):
                setattr(self.func, "fqn", self.fqn)


chained_decorator = ChainedDecorator
