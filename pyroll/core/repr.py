import html
from abc import ABC, abstractmethod
from io import StringIO


class ReprMixin(ABC):
    """Mixin class providing common functionality for ``__repr__``, ``__str__``,
    ``_repr_pretty_`` and ``_repr_html_``."""

    @property
    @abstractmethod
    def __attrs__(self):
        raise NotImplementedError()

    def plot(self, **kwargs):
        """
        Returns a matplotlib figure visualizing this instance.
        It is not required to implement this method.
        :param kwargs: keyword arguments passed to the figure constructor

        :raises RuntimeError: if matplotlib is not importable
        :raises TypeError: if the current type does not support plotting
        """
        raise TypeError("This type does not support plotting.")

    def __str__(self):
        return type(self).__qualname__

    def __repr__(self):
        kwattrs = sorted(f"{name}={repr(value)}" for name, value in self.__attrs__.items())
        return f"{self.__class__.__name__}({', '.join(kwattrs)})"

    def _repr_pretty_(self, p, cycle):
        """Pretty printing for IPython."""

        if cycle:
            p.text(f"{type(self).__name__}(...)")
        else:
            with p.group(4, f"{type(self).__name__}(", ")"):
                p.break_()
                for name, value in sorted(self.__attrs__.items()):
                    p.text(name + "=")
                    p.pretty(value)
                    p.text(",")
                    p.breakable()

    # noinspection PyProtectedMember
    def _repr_html_(self):
        """HTML repr for IPython."""

        buf = [f"<details><summary style='font-weight:bold'>{html.escape(str(self), True)}</summary><table>"]

        for name, value in sorted(self.__attrs__.items()):
            if hasattr(value, "_repr_html_"):
                r = value._repr_html_()
            elif isinstance(value, list) or isinstance(value, set):
                item_reprs = (
                    item._repr_html_() if hasattr(item, "_repr_html_") else html.escape(repr(item), True)
                    for item in value
                )
                r = f"<table style='margin:0'>{''.join(f'<tr><td>{item}</td></tr>' for item in item_reprs)}</table>"
            else:
                r = html.escape(repr(value), True)
            buf.append(f"<tr><td style='text-align:left'>{html.escape(name, True)}</td><td>{r}</td></tr>")

        buf.append("</table></details>")

        table = ''.join(buf)

        try:
            plot = self.plot()

            from pyroll.core import PLOTTING_BACKEND

            if PLOTTING_BACKEND == "matplotlib":
                import matplotlib.pyplot as plt
                with StringIO() as sio:
                    plot.savefig(sio, format="svg")
                    svg = sio.getvalue()
                plt.close(plot)

            if PLOTTING_BACKEND == "plotly":
                from plotly.io import to_image
                svg = to_image(
                    plot,
                    format="svg",
                    width=600,
                    height=400
                ).decode("utf-8")

            return (
                    "<table>"
                    + "<tr><td style='text-align: center'>" + svg + "</td></tr>"
                    + "<tr><td style='text-align: left'>" + table + "</td></tr>"
                    + "</table>"
            )

        except (NotImplementedError, ImportError, AttributeError, TypeError) as e:
            return table

    def __rich_repr__(self):
        """Pretty printing for Rich."""
        yield from sorted(self.__attrs__.items())
