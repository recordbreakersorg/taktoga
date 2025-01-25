from efus.component import CompParams
from efus.component import Component as Component
from typing import Optional

import pyoload

from efus.namespace import Namespace
from efus.types import ENil as ENil
from efus.types import ENilType as ENilT
from efus.types import EObject


class TogaComponent(Component):
    """Base for building conponents for toga."""

    def __init_subclass__(cls):
        if hasattr(cls, "ParamsClass"):
            cls.params = CompParams.from_class(cls.ParamsClass, cls.__name__)

    def prerender(self):
        """Create the widget before component renders."""
        self.outlet = self.inlet = self.widget = self.WidgetClass(
            **self.filter_widget_config()
        )
        if self.parent is not None:
            assert isinstance(
                self.parent, TogaLayout
            ), "Parent can only be layout"
        print("created widget", self.widget)
        return self.widget

    def filter_widget_config(self):
        try:
            return {
                k: v
                for k, v in self.args.items()
                if k in self.widget_config and v is not ENil
            } | {
                a: self.args[k]
                for k, a in self.widget_config_aliasses.items()
                if self.args[k] is not ENil
            }
        except KeyError as e:
            raise KeyError(
                f"Key {e!s} not found. Please check {type(self).__name__}'s"
                + " configs and aliasses and make sure they are in the "
                + "ClassParams."
            ) from e

    @classmethod
    @pyoload
    def create(
        cls,
        np: Namespace,
        attrs: dict[str, EObject],
        pc: Optional[Component],
    ) -> Component:
        return cls(np, cls.params.bind(attrs, np), pc)

    def update(self):
        raise NotImplementedError()


class TogaLayout(Component):
    """Base for building conponents for toga."""

    def __init_subclass__(cls):
        if hasattr(cls, "ParamsClass"):
            cls.params = CompParams.from_class(cls.ParamsClass, cls.__name__)

    def filter_widget_config(self):
        try:
            return {
                k: v
                for k, v in self.args.items()
                if k in self.widget_config and v is not ENil
            } | {
                a: self.args[k]
                for k, a in self.widget_config_aliasses.items()
                if self.args[k] is not ENil
            }
        except KeyError as e:
            raise KeyError(
                f"Key {e!s} not found. Please check {type(self).__name__}'s"
                + " configs and aliasses and make sure they are in the "
                + "ClassParams."
            ) from e

    @classmethod
    @pyoload
    def create(
        cls,
        np: Namespace,
        attrs: dict[str, EObject],
        pc: Optional[Component],
    ) -> Component:
        return cls(np, cls.params.bind(attrs, np), pc)

    def update(self):
        raise NotImplementedError()

    def render(self):
        children = []
        for child in self.children:
            if child is not None:
                w = child.render()
                if w is not None:
                    children.append(w)
        self.widget = self.inlet = self.outlet = self.WidgetClass(
            children=children,
        )
        print("returning box", self.widget, children)
        return self.widget
