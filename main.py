from abc import ABC, abstractmethod

class Plugin(ABC):
    @abstractmethod
    def _run(self, data):
        """
        process data in the plugin
            NOTE: the leading underscore, this should only be used in System,
            and is an abstractmethod because it must be defined in Plugins
        :param data: string data
        :return: processed data
        """
        pass

class System(object):
    plugins = dict()

    def __init__(self, data):
        self.data = data

    def install_plugin(self, plugin_id, plugin):
        self.plugins[plugin_id] = plugin

    def uninstall_plugin(self, plugin_id):
        if plugin_id not in self.plugins.keys():
            raise Exception("no such plugin in system")
        del self.plugins[plugin_id]

    def execute(self):
        for plugin in self.plugins.values():
            self.data = plugin._run(self.data)

    def execute_plugin(self, plugin_id):
        if plugin_id not in self.plugins.keys():
            raise Exception("no such plugin in system")
        self.data = self.plugins[plugin_id]._run(self.data)

class Multiplier(Plugin):
    def __init__(self, multiplier):
        self.multiplier = multiplier
    def _run(self, data):
        return self.multiplier * data

class Printer(Plugin):
    def __init__(self, wrapper=" "):
        self.wrapper = wrapper
    def _run(self, data):
        """
        NOTE: this doesn't change the data
        """
        formatting = {"wrapper": self.wrapper, "data": data}
        print("{wrapper}{data}{wrapper}".format(**formatting))
        return data

def main():
    system = System("<0>")

    multiplier = Multiplier(2)
    print("plugin block")
    system.install_plugin("multiplier", multiplier)
    print(f"main() print >>> data:{system.data}")
    # system.execute()
    try:
        system.execute_plugin("multiplier")
    except:
        pass
    print(f"main() print >>> data:{system.data}")

    print("plugin block")
    printer = Printer(wrapper="##")
    system.install_plugin("printer", printer)
    print(f"main() print >>> data:{system.data}")
    # system.execute()
    try:
        system.execute_plugin("printer")
    except Exception:
        print("printer was not installed")
    system.uninstall_plugin("printer")
    try:
        system.execute_plugin("printer")
    except Exception:
        print("printer was not installed")
    print(f"main() print >>> data:{system.data}")

if __name__ == "__main__":
    main()
