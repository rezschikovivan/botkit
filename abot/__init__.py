"""
"""
#код ленивой инициализации модулей повзаимствован с https://github.com/pallets/werkzeug/tree/71eab19be2c83fb476de51275e2f9bdf69d5cc10
import sys
from types import ModuleType

__version__ = "0.0.0"

# import mapping to objects in other modules
all_by_module = {
    "abot.core":["start_bots", "BaseComponent", "ClsHandler", "ClsComponenter", "CoreMeta", "set_cmpnts_registrator", "set_handlers_registrator"],
    "abot.handle": ["Handler"],
    "abot.message": ["BaseMsg", "Sender", "Keyboard", "Button", "MsgFactory"],
    "abot.filter":["Filter", "ABCFilter"],
    "abot.aiogram_component": ["AiogramComponent", "AiogramFilter", "AiogramMsger"],
    "abot.vkbottle_component": ["VKBottleComponent", "VKFilter", "VKMsger"]
}

# modules that should be imported when accessed as attributes of werkzeug
attribute_modules = frozenset(["core" ])
#item:module
object_origins = {}
for module, items in all_by_module.items():
    for item in items:
        object_origins[item] = module


class module(ModuleType):
    """Automatically import objects from the modules."""

    def __getattr__(self, name):
        if name in object_origins:
            module = __import__(object_origins[name], None, None, [name])
            for extra_name in all_by_module[module.__name__]:
                setattr(self, extra_name, getattr(module, extra_name))
            return getattr(module, name)
        elif name in attribute_modules:
            __import__("abot." + name)
        return 

    def __dir__(self):
        """Just show what we want to show."""
        result = list(new_module.__all__)
        result.extend(
            (
                "__file__",
                "__doc__",
                "__all__",
                "__docformat__",
                "__name__",
                "__path__",
                "__package__",
                "__version__",
            )
        )
        return result

from abot.message import BaseMsg, Sender, Keyboard, Button
from abot.handle import Handler
from abot.filter import Filter, BaseFilterImplementor
from abot.core import start_bots, BaseComponent, ClsHandler, ClsComponenter, CoreMeta, set_cmpnts_registrator, set_handlers_registrator

# keep a reference to this module so that it's not garbage collected
old_module = sys.modules["abot"]

# setup the new module and patch it into the dict of loaded modules
new_module = sys.modules["abot"] = module("abot")
new_module.__dict__.update(
    {
        "__file__": __file__,
        "__package__": "abot",
        "__path__": __path__,
        "__doc__": __doc__,
        "__version__": __version__,
        "__all__": tuple(object_origins) + tuple(attribute_modules) 
        #импортировать сразу
        + tuple([BaseComponent, ClsHandler, ClsComponenter, CoreMeta, set_cmpnts_registrator, set_handlers_registrator,start_bots, Filter, Handler, BaseFilterImplementor, BaseMsg, Sender, Keyboard, Button])
    }
)
