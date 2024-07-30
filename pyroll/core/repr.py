import html
from abc import ABC, abstractmethod
from io import StringIO
from .config import Config
from .log import global_logger


class ReprMixin(ABC):
    """Mixin class providing common functionality for ``__repr__``, ``__str__``,
    ``_repr_pretty_`` and ``_repr_html_``."""

    @property
    @abstractmethod
    def __attrs__(self):
        raise NotImplementedError()

    def _plot_plotly_(self):
        raise NotImplementedError("Plotting using plotly not available on this type.")

    def _plot_matplotlib_(self):
        raise NotImplementedError("Plotting using matplotlib not available on this type.")

    def plot_plotly(self):
        """
        Create a plot of the current object using plotly.
        :return: a plotly figure object
        """
        plot = self._plot_plotly_()
        plot.update_layout(
            width=Config.PLOT_WIDTH,
            height=Config.PLOT_HEIGHT,
        )
        return plot

    def plot_matplotlib(self):
        """
        Create a plot of the current object using matplotlib.
        :return: a matplotlib figure object
        """
        plot = self._plot_matplotlib_()
        plot.set_size_inches(Config.PLOT_WIDTH / Config.PLOT_RESOLUTION,
                             Config.PLOT_HEIGHT / Config.PLOT_RESOLUTION)
        plot.set_dpi(Config.PLOT_RESOLUTION)
        return plot

    def plot(self):
        """
        Create a plot of the current object using an available backend.

        :returns: either a plotly or matplotlib figure object
        """

        try:
            return self.plot_plotly()
        except (NotImplementedError, ImportError):
            return self.plot_matplotlib()

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
            ns = type(plot).__module__.split(".", 1)[0]

            if ns == "matplotlib":
                import matplotlib.pyplot as plt
                with StringIO() as sio:
                    plot.savefig(sio, format="svg")
                    image = sio.getvalue()
                plt.close(plot)

            if ns == "plotly":
                from plotly.io import to_html
                image = to_html(
                    plot,
                    full_html=False,
                    include_plotlyjs="cdn",
                )

            return (
                    "<table>"
                    + "<tr><td style='text-align: center'>" + image + "</td></tr>"
                    + "<tr><td style='text-align: left'>" + table + "</td></tr>"
                    + "</table>"
            )

        except (NotImplementedError, ImportError, AttributeError, TypeError) as e:
            return table

    def __rich_repr__(self):
        """Pretty printing for Rich."""
        yield from sorted(self.__attrs__.items())
