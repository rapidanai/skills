from importlib import import_module


def load_plugin(name):
    return import_module(f"plugins.{name}")
