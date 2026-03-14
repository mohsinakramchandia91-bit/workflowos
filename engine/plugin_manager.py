import os
import importlib


class PluginManager:
    def __init__(self, logger, plugins_path):
        self.logger = logger
        self.plugins_path = plugins_path
        self.plugins = {}
        self._load_plugins()

    def _load_plugins(self):
        for folder in os.listdir(self.plugins_path):

            if folder.startswith("_"):
                continue

            full_path = os.path.join(self.plugins_path, folder)
            if not os.path.isdir(full_path):
                continue

            try:
                module = importlib.import_module(f"plugins.{folder}.plugin")

                for attr in dir(module):
                    obj = getattr(module, attr)

                    if isinstance(obj, type) and hasattr(obj, "name"):
                        self.plugins[obj.name] = obj
                        self.logger.info(f"Loaded plugin: {obj.name}")

            except Exception as e:
                self.logger.error(f"Failed loading plugin {folder}: {e}")

    def get_plugin(self, name):
        return self.plugins.get(name)