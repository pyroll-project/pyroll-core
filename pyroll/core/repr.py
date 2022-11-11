import html
from abc import ABC, abstractmethod


class ReprMixin(ABC):
    @property
    @abstractmethod
    def __attrs__(self):
        raise NotImplementedError()

    def __str__(self):
        return type(self).__qualname__

    def __repr__(self):
        kwattrs = sorted(f"{name}={repr(value)}" for name, value in self.__attrs__.items())
        return f"{self.__class__.__name__}({', '.join(kwattrs)})"

    def _repr_pretty_(self, p, cycle):
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
        buf = [f"<table><tr><th colspan=2 style='text-align:center'>{html.escape(str(self), True)}</th></tr>"]

        for name, value in sorted(self.__attrs__.items()):
            if hasattr(value, "_repr_html_"):
                r = value._repr_html_()
            else:
                r = html.escape(repr(value), True)
            buf.append(f"<tr><td style='text-align:left'>{html.escape(name, True)}</td><td>{r}</td></tr>")

        buf.append("</table>")
        return ''.join(buf)
