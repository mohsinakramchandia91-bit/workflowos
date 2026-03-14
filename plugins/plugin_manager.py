import os
import importlib
import inspect


class PluginManager:
    def __init__(self, plugins_path: str, logger):
        self.plugins_path = plugins_path
        self.logger = logger
        self.plugins = {}

        self._load_plugins()

    def _load_plugins(self):
        if not os.path.exists(self.plugins_path):
            self.logger.warning(f"Plugins path not found: {self.plugins_path}")
            return

        for folder in os.listdir(self.plugins_path):

            if folder.startswith("_"):
                continue

            folder_path = os.path.join(self.plugins_path, folder)

            if os.path.isdir(folder_path):
                try:
                    module_path = f"plugins.{folder}.plugin"
                    module = importlib.import_module(module_path)

                    plugin_class = None
                    for name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and hasattr(obj, "execute"):
                            plugin_class = obj
                            break

                    if not plugin_class:
                        raise Exception("No valid plugin class found")

                    plugin_instance = plugin_class()

                    self.plugins[plugin_instance.name] = plugin_instance

                    self.logger.info(f"Loaded plugin: {plugin_instance.name}")

                except Exception as e:
                    self.logger.error(f"Failed loading plugin {folder}: {e}")

    def get_plugin(self, name: str):
        return self.plugins.get(name)