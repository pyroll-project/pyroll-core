import logging
import weakref
from abc import ABCMeta
from typing import overload, Iterable, TypeVar, Generic, List, Generator

import numpy as np

from pyroll.core.repr import ReprMixin

T = TypeVar("T")

_log = logging.getLogger(__name__)


class HookFunction:
    """
    Class wrapping a function used to yield the value of hooks.
    Instantiated commonly by use of a `Hook` instance as decorator on a function.
    You should not instantiate it yourself.
    """

    def __init__(self, func, hook):
        self._func = func
        self.module = func.__module__
        self.qualname = func.__qualname__
        self.name = func.__name__
        self.hook = hook

    def __call__(self, instance):
        return self._func(instance)

    def __repr__(self):
        return f"<{self.__str__()}>"

    def __str__(self):
        return f"HookFunction {self.module}.{self.qualname}"


class Hook(Generic[T]):
    """
    Descriptor yielding the value of a hook attribute if called on instance,
    or the respective HookCaller if called on class.
    """

    def __set_name__(self, owner, name):
        self.name = name
        self.owner = owner
        self._functions = []

    @overload
    def __get__(self, instance: None, owner: type) -> 'Hook[T]':
        ...

    @overload
    def __get__(self, instance: 'HookHost', owner: type) -> T:
        ...

    def __get__(self, instance: 'HookHost', owner: type) -> T | 'Hook[T]':

        if self.owner != owner:
            # create distinct instance on subclass
            hook = Hook()
            setattr(owner, self.name, hook)
            return hook.__get__(instance, owner)

        if instance is None:
            return self

        # try to get value explicitly set by user
        result = instance.__dict__.get(self.name, None)
        if result is not None:
            return result

        # try to get cached value
        result = instance.__cache__.get(self.name, None)
        if result is not None:
            return result

        # try to get value from hook caller
        try:
            result = self.get_result(instance)
        except RecursionError as e:
            raise AttributeError(f"Hook call for '{self.name}' on '{instance}' resulted in a RecursionError. "
                                 f"This may have one of the following reasons: missing data, interference of plugins. "
                                 f"Double check if you have provided all necessary input data.") from e

        if result is None:
            raise AttributeError(f"Hook call for '{self.name}' on '{instance}' could not provide a value.")

        try:
            if not np.isfinite(result).all():
                raise ValueError(f"Hook call for '{self.name}' on '{instance}' resulted in an infinite value.")
        except TypeError:
            pass  # only numeric types can be tested for finiteness, for others it is meaningless

        instance.__cache__[self.name] = result

        return result

    def __set__(self, instance: object, value: T) -> None:
        instance.__dict__[self.name] = value

    def __delete__(self, instance: object) -> None:
        instance.__dict__.pop(self.name, None)

    @property
    def functions_gen(self) -> Generator[HookFunction, None, None]:
        """
        Generator listing functions stored in this instance and equally named instances in superclasses of its owner.
        """
        yield from reversed(self._functions)

        for s in self.owner.__mro__[1:]:
            h = getattr(s, self.name, None)

            if hasattr(h, "_functions"):
                # noinspection PyProtectedMember
                yield from h._functions

    @property
    def functions(self) -> List[HookFunction]:
        """
        List of functions stored in this instance and equally named instances in superclasses of its owner.
        """
        return list(self.functions_gen)

    def get_result(self, instance) -> T | None:
        """
        Get the first not ``None`` result of the functions in ``self.functions`` or the cached value.
        """
        for f in self.functions_gen:
            result = f(instance)
            if result is not None:
                return result

    def add_function(self, func):
        """
        Add the given function to the internal function store.
        """
        self._functions.append(HookFunction(func, self))
        return func

    def __call__(self, func):
        """
        Add the given function to the internal function store.
        """
        hf = HookFunction(func, self)
        self._functions.append(hf)
        return hf

    def __repr__(self):
        return f"<{self.__str__()}>"

    def __str__(self):
        return f"Hook {self.owner.__qualname__}.{self.name}"


class HookHostMeta(ABCMeta):
    """
    Metaclass that provides plugin functionality to a class.

    Not for direct uses but through :py:class:`PluginHost` base class.
    """

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

    def __setattr__(self, key, value):
        if isinstance(value, Hook):
            value.__set_name__(self, key)
        super().__setattr__(key, value)


class HookHost(ReprMixin, metaclass=HookHostMeta):
    """
    A base class providing plugin functionality using the :py:class:`PluginHostMeta` metaclass.

    The :py:meth:`get_from_hook` method is also callable through the attribute syntax (``.`` notation),
    where the key equals the attributes name.
    """

    def __init__(self):
        self.__cache__ = dict()

    def clear_hook_cache(self):
        """
        Clears the cache of hook function results.
        """
        self.__cache__.clear()

    @property
    def __attrs__(self):
        return {
            n: v
            for n, v in (self.__dict__ | self.__cache__).items()
            if not n.startswith("_") and not isinstance(v, weakref.ref)
        }

    def evaluate_and_set_hooks(self, hooks: Iterable[Hook]):
        """Evaluate functions of root hooks and set the results explicitly as attributes."""
        def _gen():
            for h in hooks:
                if issubclass(type(self), h.owner):
                    result = h.get_result(self)
                    setattr(self, h.name, result)

                    try:
                        if np.isfinite(result).all():
                            yield result  # yield only numeric values
                    except TypeError:
                        continue

        return list(_gen())
