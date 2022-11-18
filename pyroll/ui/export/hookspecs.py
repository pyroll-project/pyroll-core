from ..pluggy import hookspec


@hookspec(firstresult=True)
def export_convert(name: str, value: object):
    """"""
