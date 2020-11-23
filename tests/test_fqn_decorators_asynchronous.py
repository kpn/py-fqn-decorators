import asyncio

import mock
import pytest

from fqn_decorators import get_fqn
from fqn_decorators.asynchronous import AsyncDecorator


class CustomException(Exception):
    pass


class TestFqnAsync:
    def test_class_async(self):
        assert get_fqn(AsyncDecorator) == "fqn_decorators.asynchronous.AsyncDecorator"

    def test_method_async(self):
        assert get_fqn(AsyncDecorator().before) == "fqn_decorators.asynchronous.AsyncDecorator.before"

    def test_decorated_method_async(self):
        assert get_fqn(AsyncDecorator().before) == "fqn_decorators.asynchronous.AsyncDecorator.before"

    def test_decorated_method(self):
        class User:
            @AsyncDecorator
            async def method(self, a):
                return a

        assert get_fqn(User().method) == "tests.test_fqn_decorators_asynchronous.User.method"


@pytest.mark.asyncio
class TestAsyncDecorator:
    async def test_getattr_async(self):
        class Decorator(AsyncDecorator):
            pass

        @Decorator
        async def my_method():
            pass

        with pytest.raises(AttributeError):
            assert my_method.doesnotexists is False

    async def test_function_decoration_async(self):
        class Decorator(AsyncDecorator):
            def after(self):
                self.result = True

        @Decorator
        async def return_false():
            return False

        assert await return_false() is True

    async def test_method_decoration_async(self):
        class Decorator(AsyncDecorator):
            def after(self):
                if self.result != "root":
                    raise Exception("Not root")

        class User:
            def __init__(self, username):
                self.username = username

            @Decorator
            async def get_username(self):
                return self.username

        assert await User(username="root").get_username() == "root"
        with pytest.raises(Exception):
            await User(username="admin").get_username()

    async def test_static_method_decoration_async(self):
        class Decorator(AsyncDecorator):
            def after(self):
                self.result = False

        class User:
            @staticmethod
            @Decorator
            async def staticmethod():
                return True

        assert await User().staticmethod() is False

    async def test_class_method_decoration_async(self):
        class Decorator(AsyncDecorator):
            def after(self):
                self.result = False

        class User:
            @classmethod
            @Decorator
            async def classmethod(cls):
                return True

        assert await User.classmethod() is False

    async def test_exception_async(self):
        class User:
            @AsyncDecorator
            def check_permission(self):
                raise RuntimeError("Permission denied")

        with mock.patch("fqn_decorators.asynchronous.AsyncDecorator.exception") as mocked_method:
            with pytest.raises(RuntimeError):
                await User().check_permission()
            assert mocked_method.called is True

        with pytest.raises(RuntimeError):
            await User().check_permission()

    async def test_function_parametrized_decoration_expected(self):
        class Decorator(AsyncDecorator):
            def after(self):
                if "decorator_param" not in self.params:
                    raise CustomException("No decorator param")
                self.result = self.params["decorator_param"]

        @Decorator
        async def return_decorator_value():
            return False

        with pytest.raises(CustomException):
            await return_decorator_value()

    async def test_function_parametrized_decoration(self):
        class Decorator(AsyncDecorator):
            def after(self):
                if "decorator_param" not in self.params:
                    raise CustomException("No decorator param")
                self.result = self.params["decorator_param"]

        @Decorator(decorator_param="hello")
        async def return_decorator_value():
            return False

        assert await return_decorator_value() == "hello"

    async def test_parallel_independent_execution(self):
        class Decorator(AsyncDecorator):
            def after(self):
                self.result = self.kwargs["a"]

        @Decorator
        async def return_decorator_value(a=None):
            return 0

        params = list(range(5))
        results = await asyncio.gather(*[return_decorator_value(a=x) for x in params], return_exceptions=True)
        assert sorted(results) == params
