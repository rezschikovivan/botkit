"""botkit
Ленивая инициализация компоненотов
"""
import sys
from types import ModuleType

__version__ = "1.0.0"

# import mapping to objects in other modules
all_by_module = {
    "botkit.core":["start_bots", "BaseComponent", "ClsHandler", "ClsComponenter", "CoreMeta", "set_cmpnts_registrator", "set_handlers_registrator"],
    "botkit.handle": ["Handler"],
    "botkit.message": ["BaseMsg", "Sender", "Keyboard", "Button", "MsgFactory"],
    "botkit.filter":["Filter", "ABCFilter"],
    "botkit.aiogram_component": ["AiogramComponent", "AiogramFilter", "AiogramMsger"],
    "botkit.vkbottle_component": ["VKBottleComponent", "VKFilter", "VKMsger"]
}

# modules that should be imported when accessed as attributes of werkzeug
attribute_modules = frozenset(["core" ])
#item:module
object_origins = {}
for Module, items in all_by_module.items():
    for item in items:
        object_origins[item] = Module


class Module(ModuleType):
    """Automatically import objects from the modules."""

    def __getattr__(self, name):
        if name in object_origins:
            module = __import__(object_origins[name], None, None, [name])
            for extra_name in all_by_module[module.__name__]:
                setattr(self, extra_name, getattr(module, extra_name))
            return getattr(module, name)
        elif name in attribute_modules:
            __import__("botkit." + name)
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

from botkit.message import BaseMsg, Sender, Keyboard, Button
from botkit.handle import Handler
from botkit.filter import Filter, BaseFilterImplementor
from botkit.core import start_bots, BaseComponent, ClsHandler, ClsComponenter, CoreMeta, set_cmpnts_registrator, set_handlers_registrator

# keep a reference to this module so that it's not garbage collected
old_module = sys.modules["botkit"]

# setup the new module and patch it into the dict of loaded modules
new_module = sys.modules["botkit"] = Module("botkit")
new_module.__dict__.update(
    {
        "__file__": __file__,
        "__package__": "botkit",
        "__path__": __path__,
        "__doc__": __doc__,
        "__version__": __version__,
        "__all__": tuple(object_origins) + tuple(attribute_modules) 
        #импортировать сразу
        + tuple([BaseComponent, ClsHandler, ClsComponenter, CoreMeta, set_cmpnts_registrator, set_handlers_registrator,start_bots, Filter, Handler, BaseFilterImplementor, BaseMsg, Sender, Keyboard, Button])
    }
)
