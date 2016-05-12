==============
Advanced Usage
==============
.. py:currentmodule:: fqn_decorators.decorators

.. note::
    It is possible to decorate static and class methods but you have to ensure that the order of decorators is right.
    The `@staticmethod` and `@classmethod` decorators should always be on top.::

        @staticmethod
        @my_decorator
        def my_static_method():
            pass


.. warning::
    The fully qualified name of a method cannot be properly determined for static methods and class methods.

.. warning::
    The fully qualified name of a method or function cannot be properly determined in case they are already decorated.
    This only applies to decorators that aren't using :class:`Decorator`


Decorators can be used in three different ways.::

     @my_decorator
     @my_decorator()
     @my_decorator(my_argument=True)
     def my_function():
        pass

Decorators can be used on all callables so you can decorator functions, (new style) classes and methods.::

    @my_decorator
    def my_function():
        pass

    @my_decorator
    class MyClass(object):
        @my_decorator
        def my_method():
            pass

Combining decorators
--------------------

Combining decorators is as simple as just stacking them on a function definition.

.. important::
    The :meth:`~Decorator.before` and :meth:`~Decorator.after` methods of the decorators are in different orders.
    In the example below the :meth:`~Decorator.before` methods of step2 and step1 are executed and then the method itself.
    The :meth:`~Decorator.after` method is called for step1 and then step2 after the method is executed.
    So the call stack becomes
    
    * step2.before()
    * step1.before()
    * my_process()
    * step1.after()
    * step2.after()

::

    @step2
    @step1
    def my_process():
        pass

If you want to create a decorator that combines decorators you can do that like this::

    class process(decorators.Decorator):
        """Combines step1 and step2 in a single decorator"""

        def before(self):
            self.func = step2(step1(self.func))

.. _usage_advanced_non_keyword_decorators:

Non-keyworded decorators
------------------------

Although not supported out of the box, it is possible to create decorators with non-keyworded or positional arguments::

    import fqn_decorators

    class arg_decorator(fqn_decorators.Decorator):

        def __init__(self, func=None, *args, **kwargs):
            self._args = args
            super(arg_decorator, self).__init__(func, **kwargs)

        def __call__(self, *args, **kwargs):
            if not self.func:
                # Decorator initialized without providing the function
                return self.__class__(args[0], *self._args, **self.params)
            return super(arg_decorator, self).__call__(*args, **kwargs)

        def __get__(self, obj, type=None):
            return self.__class__(self.func.__get__(obj, type), *self._args, **self.params)

        def before(self):
            print self._args


    @arg_decorator(None, 1, 2)
    def my_function():
        pass

    >>>my_function()
    (1, 2)

