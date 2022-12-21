import inspect
import logging
import weakref
from abc import ABCMeta
from typing import overload, Iterable, TypeVar, Generic, List, Generator, Union

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
        """The module the function originates from."""

        self.qualname = func.__qualname__
        """The qualified name of the function."""

        self.name = func.__name__
        """The name of the function."""

        self.hook = hook
        """The hook the function is defined for."""

        self.cycle = False
        """Cycle detection."""

    def __call__(self, instance):
        """Call the function as it were a method the provided instance."""

        extra_args = self._determine_extra_args()
        self.cycle = True
        try:
            result = self._func(instance, **extra_args)
        finally:
            self.cycle = False
        return result

    def __repr__(self):
        return f"<{self.__str__()}>"

    def __str__(self):
        return f"HookFunction {self.module}.{self.qualname}"

    def _determine_extra_args(self):
        extra_args = {}
        pars = inspect.signature(self._func).parameters
        if "cycle" in pars:
            extra_args["cycle"] = self.cycle

        return extra_args


class Hook(Generic[T]):
    """
    Descriptor yielding the value of a hook attribute if called on instance,
    or itself if called on class.
    """

    def __set_name__(self, owner, name):
        self.name = name
        """The name of the hook."""

        self.owner = owner
        """The owner class of the hook instance."""

        self._functions = []
        """The functions connected to this hook and owner."""

    @overload
    def __get__(self, instance: None, owner: type) -> 'Hook[T]':
        ...

    @overload
    def __get__(self, instance: 'HookHost', owner: type) -> T:
        ...

    def __get__(self, instance: 'HookHost', owner: type) -> Union[T, 'Hook[T]']:
        """
        Get the value of the hook if called on instance or the descriptor itself if called on class.

        Hook value resolution is done in the following order:
        1. explicit values (in ``__dict__``)
        2. cached values (in ``__cache__``)
        3. from hook functions.

        Saves the value in ``__cache__`` if the value was determined from functions.

        :raises AttributeError: if no value could be provided or if a RecursionError occurred during hook function calling
        :raises ValueError: if the resulting value was infinite (only for numeric values)
        """

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
        """Saves a value to the ``__dict__`` of the instance."""
        instance.__dict__[self.name] = value

    def __delete__(self, instance: object) -> None:
        """
        Deletes the value from the ``__dict__`` of the instance.
        Does not raise, if the value is not in the ``__dict__``.
        """
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

    def get_result(self, instance) -> Union[T, None]:
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

        :return: the given function
        """
        self._functions.append(HookFunction(func, self))
        return func

    def __call__(self, func):
        """
        Add the given function to the internal function store.

        :return: the created HookFunction object
        """
        hf = HookFunction(func, self)
        self._functions.append(hf)
        return hf

    def __repr__(self):
        return f"<{self.__str__()}>"

    def __str__(self):
        return f"Hook {self.owner.__qualname__}.{self.name}"


class _HookHostMeta(ABCMeta):
    """
    Metaclass that provides plugin functionality to a class.

    Not for direct use but through :py:class:`PluginHost` base class.
    """

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

    def __setattr__(self, key, value):
        if isinstance(value, Hook):
            value.__set_name__(self, key)
        super().__setattr__(key, value)


class HookHost(ReprMixin, metaclass=_HookHostMeta):
    """
    A base class providing plugin functionality and some related convenience methods to a derived class.
    """

    def __init__(self):
        self.__cache__ = dict()

    def clear_hook_cache(self):
        """
        Clears the cache of hook function results.
        """
        self.__cache__.clear()

    def has_set(self, name: str):
        """Checks whether a value is explicitly set for the hook `name`."""
        return name in self.__dict__

    def has_cached(self, name: str):
        """Checks whether a value is cached for the hook `name`."""
        return name in self.__cache__

    def has_set_or_cached(self, name: str):
        """Checks whether a value is explicitly set or cached for the hook `name`."""
        return self.has_set(name) or self.has_cached(name)

    def has_value(self, name: str):
        """Checks whether a value is available for the hook `name`."""
        return hasattr(self, name)

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
