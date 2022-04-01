import pluggy


class PluginHost(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

        project_name = f"pyroll_{cls.__name__}"

        cls.plugin_manager = pluggy.PluginManager(project_name)
        cls.hookspec = pluggy.HookspecMarker(project_name)(firstresult=True)
        cls.hookimpl = pluggy.HookimplMarker(project_name)

        cls._hook_results_to_clear = set()

        def get_from_hook(self, key):
            if hasattr(cls.plugin_manager.hook, key):
                hook = getattr(cls.plugin_manager.hook, key)
                result = hook(**self.hook_args)

                if result is None:
                    raise AttributeError(f"Hook call for '{key}' on '{self}' resulted in None.")

                self.__dict__[key] = result
                cls._hook_results_to_clear.add(key)

                return result

            # try to get from super class
            s = super(cls, self)
            if hasattr(s, "get_from_hook"):
                return s.get_from_hook(key)

            raise AttributeError(
                f"No hook '{key}' available on '{self}'.")

        cls.get_from_hook = get_from_hook

        def __getattr__(self, key):
            return self.get_from_hook(key)

        cls.__getattr__ = __getattr__

        def clear_hook_results(self):
            for key in cls._hook_results_to_clear:
                if key in self.__dict__:
                    delattr(self, key)

            s = super(cls, self)
            if hasattr(s, "clear_hook_results"):
                s.clear_hook_results()

        cls.clear_hook_results = clear_hook_results
