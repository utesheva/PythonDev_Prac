#!/usr/bin/env python3
# noqa: D205 D400
"""
AppBase.py
~~~~~~~~~~

Skeleton MVC application module.

Provides three base classes for application build.

:copyright: (c) 2021 by Fr. Br. George
:license: MIT, see COPYING for more details.
"""
import tkinter as tk
import re


class View(tk.Frame):
    """
    Sample tkinter View class.

    :param master: master window (tkinter root if None)
    :param title: application window title
    :param control: the Control part of MVC framework
    """

    sepGeom = "", r"\.", r"\+", ":", r"\.", r"\+"
    reGeom = re.compile("".join((f"(?:{f}([0-9]*))?" for f in sepGeom)) + "(?:/([NEWSnews]+))?")

    def __init__(self, master=None, title="<application>", control=None, **kwargs):
        """Create root window with frame, tune weight and resize."""
        self.control = control
        super().__init__(master, ** kwargs)
        if not master:
            self.master.title(title)
            self.master.columnconfigure(0, weight=1)
            self.master.rowconfigure(0, weight=1)
            self.grid(sticky="NEWS")
        self.createWidgets()

    def _(self, cls, master, geom=":", *args, **kwargs):
        """
        Create a widget, set up geometry and adjust master's column/row weights.

        :param cls: widget class
        :param master: master widget to embed
        :param geom: geometry string
        :param args: positional arguments tuple for ``cls()`` call
        :param kwargs: named arguments tuple for ``cls()`` call

        Geometry string may (not) include any of the following fields:

        ::

            row+span.weight:row+column.weight/gravity

        :column, row:
          Master's grid column and row to place the widget. Default is 0.

        :span:
          Additional colunm or row to span. Default is 0.

        :weight:
          Master's grid colunm or row weight (last definition wins). Default is 1.

        :gravity:
          Widget gravity in tkinter standard form. Default is ``NEWS``.


        E. g. ``3.0:+2`` is equivalent to ``3.0+0:0.1+2``, column number 3,
        with zero (fixed) weight, spanned from row number zero to 2,
        with default weght of 1.
        """
        ret = cls(master, * args, ** kwargs)
        A = self.reGeom.match(geom or ":").groups()
        B = 0, 1, 0, master.grid_size()[0], 1, 0, "NEWS"
        y, wy, dy, x, wx, dx, s = (b if a in ('', None) else a for a, b in zip(A, B))
        ret.grid(column=x, columnspan=int(dx) + 1, row=y, rowspan=int(dy) + 1, sticky=s)
        master.rowconfigure(y, weight=wy)
        master.columnconfigure(x, weight=wx)
        # print(f"{master} row {y}+{dy} [{wy}], col {x}+{dx} [{wx}] {s} {ret}")
        return ret

    def createWidgets(self):
        """Create all the widgets."""

    def assingbindings(self):
        """Assign controller bindings."""

    def __call__(self, control=None):
        """Start an application.

        :param control: Control part of MVC framework
        """
        self.control = control
        self.assingbindings()
        self.mainloop()
        del self.control

    def _varbind(self, var, callback, *args):
        """Bind control callback to a tk.variable var."""
        var.trace_add("write", lambda v, p, rw: callback(var.get(), * args))


class Model:
    """
    Trivial program logic.

    :param view: View part of MVC framework
    """

    def __init__(self, view):
        """Set up view instance field."""
        self.view = view

    def __call__(self, control=None):
        """
        Initialize view instance.

        :param control: Control part of MVC framework
        """
        if control:
            control.setup()
        self.view(control)

    def _dump(self, *args, **kwargs):
        """Just print all agruments."""
        print("MODEL:", args, kwargs)


class Control:
    """
    Trivial program controller.

    :param model: Model part of MVC framework
    """

    def __init__(self, model):
        """Set up model instance field."""
        self.model = model

    def _dump(self, *args, **kwargs):
        """Just print all agruments."""
        print("CONTROL:", args, kwargs)

    def setup(self):
        """Command Model to set up stuff."""
