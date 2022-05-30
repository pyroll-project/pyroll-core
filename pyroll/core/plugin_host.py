from typing import Set, Dict, Any, Callable, List

import numpy as np
import pluggy


def _full_name(cls: type):
    return f"{cls.__module__}.{cls.__qualname__}"


class HookspecMarker:
    """Wrapper around :py:class:`pluggy.HookspecMarker` with minified interface.
    Implicitly sets ``firstresult=True`` and ``historic=False``"""

    def __init__(self, cls):
        self._marker = pluggy.HookspecMarker(_full_name(cls))
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
        self._marker = pluggy.HookimplMarker(_full_name(cls))
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

    Not for direct uses but through :py:class:`PluginHost` base class.
    """

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

        cls.plugin_manager: pluggy.PluginManager = pluggy.PluginManager(_full_name(cls))
        """A :py:class:`pluggy.PluginManager` instance used to maintain the plugins on this class."""

        cls.hookspec: HookspecMarker = HookspecMarker(cls)
        """A wrapper around a :py:class:`pluggy.HookspecMarker` instance for defining new hook specifications. 
        Supports only a subset of the original arguments."""

        cls.hookimpl: HookimplMarker = HookimplMarker(cls)
        """A wrapper around a :py:class:`pluggy.HookimplMarker` instance for defining new hook implementations."""

        cls.root_hooks: Set[str] = set()
        """Set of hooks to call in every solution iteration."""


class PluginHost(metaclass=PluginHostMeta):
    """
    A base class providing plugin functionality using the :py:class:`PluginHostMeta` metaclass.

    The :py:meth:`get_from_hook` method is also callable through the attribute syntax (``.`` notation),
    where the key equals the attributes name.
    """

    def __init__(self, hook_args: Dict[str, Any]):
        """
        :param hook_args: keyword arguments to pass to hook calls
        """
        self.hook_args = hook_args
        """Keyword arguments to pass to hook calls."""

        self.hook_result_attributes: Set[str] = set()
        """Set remembering all hooks that were called on this class, used by :py:meth:`delete_hook_result_attributes`."""

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
        self_type = type(self)

        def enumerate_hooks_with_key():
            for t in self_type.__mro__:
                if hasattr(t, "plugin_manager") and hasattr(t.plugin_manager.hook, key):
                    yield getattr(t.plugin_manager.hook, key)

        hooks = list(enumerate_hooks_with_key())

        if not hooks:
            raise AttributeError(f"No hook '{key}' available on '{self_type.__name__}'.")

        result = None
        for hook in hooks:
            result = hook(**self.hook_args)

            if result is not None:
                break

        if result is None:
            raise AttributeError(f"Hook call for '{key}' on '{self}' resulted in None.")

        try:
            if not np.isfinite(result).all():
                raise ValueError(f"Hook call for '{key}' on '{self}' resulted in an infinite value.")
        except TypeError:
            pass  # only numeric types can be tested for finiteness, for others it is meaningless

        self.__dict__[key] = result
        self.hook_result_attributes.add(key)

        return result

    def __getattr__(self, key: str):
        """
        Call a hook through attribute syntax if there is no explicit attribute with that name
        by use of :py:meth:`get_from_hook`.
        """
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
        """
        Deletes the attributes created by :py:meth:`get_from_hook` calls, except those present in
        :py:attr:`root_hooks`.
        """

        for hook in self.hook_result_attributes:
            if hook in self.__dict__ and hook not in self.root_hooks:
                del self.__dict__[hook]

    def _enumerate_hooks(self):
        for t in type(self).__mro__:
            if hasattr(t, "plugin_manager"):
                yield from t.plugin_manager.hook.__dict__

    def __dir__(self):
        return list(
            set(self.__dict__).union(self._enumerate_hooks())
        )

    def _get_repr_attrs(self):
        return sorted(filter(
            lambda a: not a.startswith("_"),
            set(self.__dict__) - {"hook_args", "hook_result_attributes"} - set(PluginHost.__dict__)
        ))

    def __repr__(self):
        return (
                type(self).__qualname__
                + "("
                + ", ".join(f"{attr}={getattr(self, attr)}" for attr in self._get_repr_attrs())
                + ")"
        )

    def _repr_pretty_(self, p, cycle):
        if cycle:
            p.text(
                type(self).__qualname__ + "(...)"
            )
            return

        with p.group(4, type(self).__qualname__ + "(", ")"):
            p.break_()
            for attr in self._get_repr_attrs():
                p.text(attr)
                p.text("=")
                p.pretty(getattr(self, attr))
                p.text(",")
                p.breakable()
