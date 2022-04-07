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


class PluginHost(type):
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

        project_name = f"pyroll_{cls.__name__}"

        cls.plugin_manager = pluggy.PluginManager(project_name)
        """A :py:class:`pluggy.PluginManager` instance used to maintain the plugins on this class."""

        cls.hookspec = HookspecMarker(cls)
        """A wrapper around a :py:class:`pluggy.HookspecMarker` instance for defining new hook specifications. 
        Supports only a subset of the original arguments."""

        cls.hookimpl = HookimplMarker(cls)
        """A wrapper around a :py:class:`pluggy.HookimplMarker` instance for defining new hook implementations."""

        cls._hook_results_to_clear = set()
        """Internal memory of called hook names to clear when running :py:meth:`clear_hook_results`"""

        def get_from_hook(self, key):
            """
            Explicitly tries to get a value from a hook specified on this class.
            Returns and caches the result of the hook call as attribute.
            Use `clear_hook_results()` to clear the cache.
            Hook calls done by this function are not cleared, only those by attribute syntax.

            If the plugin manager does not know a hook of name `key`,
            the function dispatches to eventual base classes.

            :param key: the hook name to call

            :raises AttributeError: if the hook call resulted in None
            :raises AttributeError: if the hook name is not known to this class, nor to base classes
            """

            if hasattr(cls.plugin_manager.hook, key):
                hook = getattr(cls.plugin_manager.hook, key)
                result = hook(**self.hook_args)

                if result is None:
                    raise AttributeError(f"Hook call for '{key}' on '{self}' resulted in None.")

                self.__dict__[key] = result

                return result

            # try to get from super class
            s = super(cls, self)
            if hasattr(s, "get_from_hook"):
                return s.get_from_hook(key)

            raise AttributeError(
                f"No hook '{key}' available on '{self}'.")

        cls.get_from_hook = get_from_hook

        def __getattr__(self, key):
            cls._hook_results_to_clear.add(key)
            return self.get_from_hook(key)

        cls.__getattr__ = __getattr__

        def clear_hook_results(self):
            """Delete the attributes created by hook calls using attribute syntax."""
            for key in cls._hook_results_to_clear:
                if key in self.__dict__:
                    delattr(self, key)

            s = super(cls, self)
            if hasattr(s, "clear_hook_results"):
                s.clear_hook_results()

        cls.clear_hook_results = clear_hook_results
