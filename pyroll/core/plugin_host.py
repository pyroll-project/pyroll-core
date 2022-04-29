from typing import Set, Dict, Any

import numpy as np
import pluggy


class HookspecMarker:
    """Wrapper around :py:class:`pluggy.HookspecMarker` with minified interface.
    Implicitly sets ``firstresult=True`` and ``historic=False``"""

    def __init__(self, cls):
        self._marker = pluggy.HookspecMarker(f"pyroll_{cls.__name__}")
        self.plugin_host = cls

    def __call__(self, function=None, warn_on_impl=None):
        """
        Decorator for defining hook specifications.

        :param function: the function to apply the decorator directly to, if None a decorator is returned
        :param warn_on_impl: raise a warning if an implementation of this hook is registered, useful for deprecation warnings
        :returns: if ``function`` is not ``None``, the modified function, else, the decorator
        """
        func = self._marker.__call__(function, True, False, warn_on_impl)
        func.plugin_host = self.plugin_host
        return func


class HookimplMarker:
    """Wrapper around :py:class:`pluggy.HookimplMarker` with minified interface."""

    def __init__(self, cls):
        self._marker = pluggy.HookimplMarker(f"pyroll_{cls.__name__}")
        self.plugin_host = cls

    def __call__(
            self,
            function=None,
            hookwrapper=False,
            optionalhook=False,
            tryfirst=False,
            trylast=False,
            specname=None,
    ):
        """
        Decorator for defining hook implementations.

        :param function: the function to apply the decorator directly to, if None a decorator is returned
        :param hookwrapper: whether the implementation is a hook wrapper
        :param optionalhook: whether to raise no error if no corresponding spec exists
        :param tryfirst: whether to run this implementation as early as possible
        :param trylast: whether to run this implementation as late as possible
        :param specname: define a specname other than the function name, useful to avoid naming collisions of several implementations of the same hook in one namespace
        :returns: if ``function`` is not ``None``, the modified function, else, the decorator
        """
        func = self._marker.__call__(function, hookwrapper, optionalhook, tryfirst, trylast, specname)
        func.plugin_host = self.plugin_host
        return func


class PluginHostMeta(type):
    """
    Metaclass that provides plugin functionality to a class.

    Adds the following members to a class:

    ``plugin_host`` - a :py:class:`pluggy.PluginManager` instance used to maintain the plugins on this class.

    ``hookspec`` - a wrapper around a :py:class:`pluggy.HookspecMarker` instance for defining new hook specifications.
    Supports only a subset of the original arguments.

    ``hookimpl`` - a wrapper around a :py:class:`pluggy.HookimplMarker` instance for defining new hook implementations.
    """

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

        cls.plugin_manager = pluggy.PluginManager(f"pyroll_{cls.__name__}")
        """A :py:class:`pluggy.PluginManager` instance used to maintain the plugins on this class."""

        cls.hookspec = HookspecMarker(cls)
        """A wrapper around a :py:class:`pluggy.HookspecMarker` instance for defining new hook specifications. 
        Supports only a subset of the original arguments."""

        cls.hookimpl = HookimplMarker(cls)
        """A wrapper around a :py:class:`pluggy.HookimplMarker` instance for defining new hook implementations."""

        cls.root_hooks: Set[str] = set()
        """Set of hooks to call in every solution iteration."""

        cls._hook_result_attributes: Set[str] = set()
        """List remembering all hooks that were called on this class, used by :py:meth:`delete_hook_result_attributes`."""


class PluginHost(metaclass=PluginHostMeta):
    """
    A base class providing plugin functionality using the :py:class:`PluginHostMeta` metaclass.
    """

    def __init__(self, hook_args: Dict[str, Any]):
        """
        :param hook_args: keyword arguments to pass to hook calls
        """
        self.hook_args = hook_args
        """Keyword arguments to pass to hook calls."""

    def get_hook(self, key: str):
        """
        Search a hook on the class of this instance or its superclasses of the name specied by ``key``.

        :param str key: the name of the hook to get
        """
        self_type = type(self)

        for t in self_type.__mro__:
            if hasattr(t, "plugin_manager") and hasattr(t.plugin_manager.hook, key):
                return getattr(t.plugin_manager.hook, key)

        raise AttributeError(
            f"No hook '{key}' available on '{self_type.__name__}'.")

    def get_from_hook(self, key: str):
        """
        Explicitly tries to get a value from a hook specified on this class.
        Returns and caches the result of the hook call as attribute.
        Use `clear_hook_results()` to clear the cache.
        Hook calls done by this function are not cleared, only those by attribute syntax.

        If the plugin manager does not know a hook of name `key`,
        the function dispatches to eventual base classes.

        :param str key: the hook name to call

        :raises AttributeError: if the hook call resulted in None
        :raises AttributeError: if the hook name is not known to this class, nor to base classes
        :raises ValueError: if the hook call resulted in an infinite value
        """

        hook = self.get_hook(key)
        result = hook(**self.hook_args)

        if result is None:
            raise AttributeError(f"Hook call for '{key}' on '{self}' resulted in None.")

        try:
            if not np.isfinite(result).any():
                raise ValueError(f"Hook call for '{key}' on '{self}' resulted in an infinite value.")
        except TypeError:
            pass  # only numeric types can be tested for finiteness, for others it is meaningless

        self.__dict__[key] = result
        self._hook_result_attributes.add(key)

        return result

    def __getattr__(self, key: str):
        return self.get_from_hook(key)

    def get_root_hook_results(self):
        """
        Call necessary root hooks of this instance and return an array of their results.
        """
        results = []
        for key in self.root_hooks:
            result = self.get_from_hook(key)
            try:
                results.append(float(result))
            except TypeError:
                pass  # only add numeric values, since they are used for loop control

        return np.asarray(results)

    def delete_hook_result_attributes(self):
        """Recalls all hooks that have been called by :py:meth:`get_from_hook` so far on this instance."""
        self_type = type(self)

        for hook in self_type._hook_result_attributes:
            if hook in self.__dict__ and hook not in self_type.root_hooks:
                del self.__dict__[hook]
