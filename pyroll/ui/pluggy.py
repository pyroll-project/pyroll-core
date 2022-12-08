import pluggy

plugin_manager = pluggy.PluginManager("pyroll")
hookspec = pluggy.HookspecMarker("pyroll")
hookimpl = pluggy.HookimplMarker("pyroll")
