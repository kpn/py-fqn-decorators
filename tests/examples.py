import fqn_decorators


@fqn_decorators.Decorator
def my_test_func(a):
    return a


@fqn_decorators.Decorator()
class A:
    @fqn_decorators.Decorator
    def method(self, a):
        return a


class B:
    @fqn_decorators.Decorator
    def method(self, b):
        return b
