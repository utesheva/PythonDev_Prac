#!/usr/bin/env python3
"""
Example graduate project calendar task.

- Real project should be larger
- Real project should do something useful)
"""
import tkinter as tk
import tkinter.font as tkfont
import gettext
import locale
import os
import pyfiglet
from . import Model, View, Control

locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())
_podir = os.path.join(os.path.dirname(__file__), "po")
translation = gettext.translation("DateTime", _podir, fallback=True)
_, ngettext = translation.gettext, translation.ngettext


class AppView(View):
    """Calendar task."""

    def createWidgets(self):
        """Calendar layout."""
        self.Date = self._(tk.Label, self, "0+2/NEW", font=tkfont.Font(family="fixed"), text="Date\nDate")
        self._DCtl = self._(tk.LabelFrame, self, "0.0:1.1", text=_("Date"))
        self._CCtl = self._(tk.LabelFrame, self, "1.0:1.1", text=_("Calendar"))
        self._Filler = self._(tk.Frame, self, "2:1")
        self.sCaltype = tk.IntVar()
        self.caltypes = 1, 3, 12
        self.Caltype = self._(tk.OptionMenu, self._CCtl, "0+1:0.0/W", self.sCaltype, *self.caltypes)
        self.sMonth = tk.StringVar()
        self.sCaltype.trace_add("write", self.update_months)
        self.Months = self._(tk.Label, self._CCtl, "0+1:1.0/W", textvariable=self.sMonth)
        self.sCaltype.set(self.caltypes[0])
        self.sStart = tk.IntVar()
        self.sStart.set(1)
        self.Monday = self._(tk.Radiobutton, self._CCtl, "0:2/NW", variable=self.sStart, text=_("Monday"), value=1)
        self.Sunday = self._(tk.Radiobutton, self._CCtl, "1:2/NW", variable=self.sStart, text=_("Sunday"), value=7)
        self.formats = "%c", "%F", "%D"
        self.sFormat = tk.StringVar()
        self.Format = self._(tk.OptionMenu, self._DCtl, "0:0.0", self.sFormat, *self.formats)
        self.sFormat.set(self.formats[0])
        self.Manual = self._(tk.Entry, self._DCtl, "0:1", textvariable=self.sFormat)

        self.LFont = self._(tk.Label, self._DCtl, "1:0.0", text=_("Font"))
        self.fonts = [font for font in pyfiglet.FigletFont.getFonts()
                if "cyrillic" in pyfiglet.FigletFont.infoFont(font).lower()]
        self.sFont = tk.StringVar()
        self.Font = self._(tk.OptionMenu, self._DCtl, "1:1.0", self.sFont, *self.fonts)
        self.sFont.set(self.fonts[0])
        self.Calendar = self._(tk.Label, self, "3:0.0+1", text="Cal\nCal")
        self.Quit = self._(tk.Button, self, "3:1/SE", text=_("Quit"), command=self.quit)

    def assingbindings(self):
        """Watch s-variables and initiate control events."""
        self._varbind(self.sFormat, self.control.dateformat)
        self._varbind(self.sFont, self.control.fonttype)
        self._varbind(self.sCaltype, self.control.caltype)
        self._varbind(self.sStart, self.control.calstart)

    def update_months(self, var, param, reason):
        """Update montth label."""
        self.sMonth.set(ngettext("month", "months", self.sCaltype.get()))


class AppControl(Control):
    """Simple control: no view → model translation."""

    def dateformat(self, val):
        """Date format changed."""
        self.model.datechanged()

    def fonttype(self, val):
        """Different font selected."""
        self.model.datechanged()

    def caltype(self, val):
        """Calendar type changed."""
        self.model.calchanged()

    def calstart(self, val):
        """Calendar start date changed."""
        self.model.calchanged()

    def setup(self):
        """Ask model to calculate initial values."""
        self.model.datechanged()
        self.model.calchanged()


class AppModel(Model):
    """Calendar app logic: model → view connection is too strong."""

    import time
    import subprocess

    def datechanged(self):
        """Get date according to format."""
        try:
            txt = self.time.strftime(self.view.sFormat.get())
        except Exception as E:
            txt = f"{E}"
        f = pyfiglet.Figlet(font=self.view.sFont.get())
        self.view.Date["text"] = f.renderText(txt)

    def calchanged(self):
        """Get calendar according to type and start day."""
        t, s = self.view.sCaltype.get(), self.view.sStart.get()
        self.view.Calendar["text"] = self._getcal(t, s)

    def _getcal(self, ctype, cstart):
        """Run 'cal' with appropriate options."""
        res = self.subprocess.run(["cal",
            ctype == 3 and "-3" or ctype == 12 and "-y" or "-1",
            str(cstart) == "1" and "-m" or "-s"], capture_output=True)
        return (res.stderr if res.returncode else res.stdout).decode()


def main():
    """Call main application."""
    import locale
    locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())
    view = AppView(title=_("Calendar and date"))
    model = AppModel(view)
    control = AppControl(model)
    model(control)
