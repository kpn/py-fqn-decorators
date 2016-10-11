import fqn_decorators


@fqn_decorators.Decorator
def my_test_func(a):
    return a


@fqn_decorators.Decorator()
class A(object):

    @fqn_decorators.Decorator
    def method(self, a):
        return a


class B(object):

    @fqn_decorators.Decorator
    def method(self, b):
        return b
