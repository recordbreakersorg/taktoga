# from efus.types import Binding
from efus.types import ENil as Nil
from efus.types import ENilType as NilT
from efus.types import ESize

import toga

from ..component import TogaComponent
from ..component import TogaLayout


class Box(TogaLayout):
    class ParamsClass:
        pass

    widget_config = ()
    widget_config_aliasses: dict[str, str] = {}

    WidgetClass = toga.Box


class ImageView(TogaComponent):
    class ParamsClass:
        image: str | NilT

    widget_config = ()
    widget_config_aliasses: dict[str, str] = {}

    WidgetClass = toga.ImageView
