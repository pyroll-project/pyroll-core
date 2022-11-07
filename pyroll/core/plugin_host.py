from typing import Any, overload, Iterable

import numpy as np


class HookCaller:
    """
    Class able to retrieve a value from subsequent function results, where the first not ``None`` value is returned.
    """

    def __init__(self, name: str, owner: type):
        self._functions = []
        self.name = name
        self._caller_name = f"_{name}_hook_caller"
        self.owner = owner

    @property
    def functions(self):
        """
        Generator listing functions stored in this instance and equally named instances in superclasses of its owner.
        """
        yield from reversed(self._functions)

        for s in self.owner.__mro__[1:]:
            h = getattr(s, self._caller_name, None)

            if hasattr(h, "functions"):
                yield from h.functions

    def get_result(self, instance):
        """
        Get the first not ``None`` result of the functions in ``self.functions`` or the cached value..
        """

        for f in self.functions:
            result = f(instance)
            if result is not None:
                return result

        raise ValueError(f"Hook call for '{self.name}' on '{instance}' resulted in None.")

    def add_function(self, func):
        """
        Add the given function to the internal function store.
        """
        self._functions.append(func)
        return func

    def __call__(self, func):
        """
        Add the given function to the internal function store.
        """
        self.add_function(func)


class HookDescriptor:
    """
    Descriptor yielding the value of a hook attribute if called on instance,
    or the respective HookCaller if called on class.
    """

    def __set_name__(self, owner, name):
        self.name = name
        self._caller_name = f"_{name}_hook_caller"
        self._cache_name = f"_{name}_hook_cache"

    @overload
    def __get__(self, instance: None, owner: type) -> HookCaller:
        ...

    @overload
    def __get__(self, instance: object, owner: type) -> Any:
        ...

    def __get__(self, instance, owner) -> HookCaller | Any:
        caller = owner.__dict__.get(self._caller_name, None)

        if caller is None:
            # create associated HookCaller on first get
            caller = HookCaller(self.name, owner)
            setattr(owner, self._caller_name, caller)

        if instance is None:
            return caller

        # try to get value explicitly set by user
        result = instance.__dict__.get(self.name, None)
        if result is not None:
            return result

        # try to get cached value
        result = instance.__dict__.get(self._cache_name, None)
        if result is not None:
            return result

        # try to get value from hook caller
        result = caller.get_result(instance)

        try:
            if not np.isfinite(result).all():
                raise ValueError(f"Hook call for '{self.name}' on '{instance}' resulted in an infinite value.")
        except TypeError:
            pass  # only numeric types can be tested for finiteness, for others it is meaningless

        instance.__dict__[self._cache_name] = result

        return result

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class PluginHostMeta(type):
    """
    Metaclass that provides plugin functionality to a class.

    Not for direct uses but through :py:class:`PluginHost` base class.
    """

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

    def __setattr__(self, key, value):
        if isinstance(value, HookDescriptor):
            value.__set_name__(self, key)
        super().__setattr__(key, value)


class PluginHost(metaclass=PluginHostMeta):
    """
    A base class providing plugin functionality using the :py:class:`PluginHostMeta` metaclass.

    The :py:meth:`get_from_hook` method is also callable through the attribute syntax (``.`` notation),
    where the key equals the attributes name.
    """

    def clear_hook_cache(self):
        """
        Clears the cache of hook function results.
        """

        for key in self.__dict__:
            if key.endswith("_hook_cache"):
                del self.__dict__[key]


def evaluate_and_pin_hooks(instance: object, hooks: Iterable[HookCaller]):
    def _gen():
        for h in hooks:
            if issubclass(type(instance), h.owner):
                result = h.get_result(instance)
                setattr(instance, h.name, result)
                yield result

    return list(_gen())
