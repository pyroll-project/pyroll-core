import inspect
import logging
import weakref
from abc import ABCMeta
from functools import partial
from typing import overload, TypeVar, Generic, List, Generator, Union

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

    def __init__(self, func, hook, tryfirst=False, trylast=False):
        """
        :param func: the function
        :param hook: the associated hook
        :param tryfirst: whether to use this function with the highest priority
        :param trylast: whether to use this function with the lowest priority
        """
        self.function = func
        """The underlying function."""

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

        self._tryfirst = tryfirst
        self._trylast = trylast

    @property
    def tryfirst(self):
        """Whether to use this function with the highest priority."""
        return self._tryfirst

    @property
    def trylast(self):
        """Whether to use this function with the lowest priority."""
        return self._trylast

    def __call__(self, instance):
        """Call the function as it were a method the provided instance."""

        extra_args = self._determine_extra_args()
        self.cycle = True
        try:
            result = self.function(instance, **extra_args)
        finally:
            self.cycle = False
        return result

    def __repr__(self):
        return f"<{self.__str__()}>"

    def __str__(self):
        return f"HookFunction {self.module}.{self.qualname}"

    def _determine_extra_args(self):
        extra_args = {}
        pars = inspect.signature(self.function).parameters
        if "cycle" in pars:
            extra_args["cycle"] = self.cycle

        return extra_args


class Hook(Generic[T]):
    """
    Descriptor yielding the value of a hook attribute if called on instance,
    or itself if called on class.
    """

    def __init__(self, name=None, owner=None):
        self.name = name
        """The name of the hook."""

        self.owner = owner
        """The owner class of the hook instance."""

        self._first_functions: List[HookFunction] = []

        self._last_functions: List[HookFunction] = []

        self._functions: List[HookFunction] = []

    def __set_name__(self, owner, name):
        self.name = name
        self.owner = owner

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

    def _yield_functions_from(self, attr: str):
        for s in self.owner.__mro__:
            h = getattr(s, self.name, None)
            funcs = getattr(h, attr, None)
            if funcs:
                yield from reversed(funcs)

    @property
    def functions_gen(self) -> Generator[HookFunction, None, None]:
        """
        Generator listing functions stored in this instance and equally named instances in superclasses of its owner.
        """

        yield from self._yield_functions_from("_first_functions")
        yield from self._yield_functions_from("_functions")
        yield from self._yield_functions_from("_last_functions")

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

    def add_function(self, func, tryfirst=False, trylast=False):
        """
        Add the given function to the internal function store.

        :return: the created HookFunction object
        """
        if isinstance(func, HookFunction):
            func = func.function

        hf = HookFunction(func, self, trylast=trylast, tryfirst=tryfirst)

        if tryfirst:
            self._first_functions.append(hf)
        elif trylast:
            self._last_functions.append(hf)
        else:
            self._functions.append(hf)

        return hf

    def __call__(self, func=None, tryfirst=False, trylast=False):
        if func is None:
            return partial(self.add_function, tryfirst=tryfirst, trylast=trylast)
        return self.add_function(func, tryfirst=tryfirst, trylast=trylast)

    def remove_function(self, func: HookFunction):
        """
        Remove a function from the internal function store.

        :return: the underlying function object
        """
        self._functions.remove(func)
        return func.function

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

    @classmethod
    @property
    def __hooks__(cls):
        """Return a set of all hook names defined on this class and all superclasses."""

        hooks = set()
        for s in cls.__mro__:
            hooks = hooks.union([
                name for name, value in s.__dict__.items()
                if not name.startswith("_")
                if isinstance(value, Hook)
            ])
        return hooks

    @classmethod
    def extension_class(cls, source: type):
        """
        Class decorator for adding new hook definitions to an existing HookHost.

        :return: the extended class (the reference to the source class is discarded)
        :raises TypeError: if the source class is itself derived from HookHost (error-prone)
        """

        for name, value in source.__dict__.items():
            if isinstance(value, Hook) and name not in cls.__dict__:
                setattr(cls, name, value)
        return cls

    @property
    def __attrs__(self):
        return {
            n: v
            for n, v in (self.__dict__ | self.__cache__).items()
            if not n.startswith("_") and not isinstance(v, weakref.ref)
        }

    def evaluate_and_set_hooks(self):
        """Evaluate functions of root hooks and set the results explicitly as attributes."""

        def _gen():
            for h in root_hooks:
                if issubclass(type(self), h.owner):
                    h = getattr(type(self), h.name)
                    result = h.get_result(self)

                    if result is None:
                        continue

                    setattr(self, h.name, result)

                    try:
                        arr = np.array(result)
                        yield from arr[np.isfinite(arr)].flat
                    except TypeError:  # yield only numeric values
                        continue

        return list(_gen())


root_hooks = set()  # filled in __init__.py due to circular imports
"""
Set of hooks to call explicitly in each solution iteration.
Their values will be treated as explicitly set but reevaluated in every iteration.
They will not be deleted during cache clearing.
They serve as root for the calling tree and persistent iterational variables.
"""
