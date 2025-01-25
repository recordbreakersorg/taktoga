"""Hold definitions for applications."""
import pyoload
import toga

# import inspect

# from . import pyodchecks
from atak.app import AppExit
from atak.app import AtakApplication
from atak.app import get_cmd

# from importlib import import_module
from typing import Any

# from typing import Callable
from dataclasses import dataclass


@dataclass
class CmdParams:
    """Command utility."""

    name: str
    app: "App"

    def view(self, widget, set=True):
        """Shortcut to view page from command."""
        (
            self.app.pagebrowser.set_page
            if set
            else self.app.pagebrowser.set_page
        )((self.name, widget))


@pyoload
class App(toga.App, AtakApplication):
    """Taktoga application."""

    def view_pageurl_now(self, url: str):
        """View the page in url."""
        self.main_window.content = get_cmd(url)

    def run(self) -> int:
        """Run the taktoga application."""
        try:
            toga.App.main_loop(self)
        except AppExit as e:
            print(e)
            return e.code
        return 0

    def run_cmd(self, __cmd: str, *args, **kw) -> Any:
        """Run the given command."""
        ret = get_cmd(__cmd)(
            CmdParams(name=__cmd, app=self),
            *args,
            **kw,
        )
        self.update_page()
        return ret

    def update_page(self):
        """Update the currently viewed page from browser."""
        self.main_window.content = self.pagebrowser.get_current()[-1]
