from pyroll.core import Config, PlottingBackend, Profile


def test_plot_preferred_matplotlib(monkeypatch):
    import matplotlib.pyplot as plt

    monkeypatch.setattr(Config, "PREFERRED_PLOTTING_BACKEND", PlottingBackend.MATPLOTLIB)
    p = Profile.round(1)
    plot = p.plot()
    assert isinstance(plot, plt.Figure)


def test_plot_preferred_plotly(monkeypatch):
    import plotly.graph_objects as go

    monkeypatch.setattr(Config, "PREFERRED_PLOTTING_BACKEND", PlottingBackend.PLOTLY)
    p = Profile.round(1)
    plot = p.plot()
    assert isinstance(plot, go.Figure)


def test_plot_preferred_matplotlib_block_import(monkeypatch):
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go

    def mock_fn(*args, **kwargs):
        raise ImportError()

    monkeypatch.setattr(plt.Figure, "__init__", mock_fn)

    monkeypatch.setattr(Config, "PREFERRED_PLOTTING_BACKEND", PlottingBackend.MATPLOTLIB)
    p = Profile.round(1)
    plot = p.plot()
    assert isinstance(plot, go.Figure)


def test_plot_preferred_plotly_block_import(monkeypatch):
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go

    def mock_fn(*args, **kwargs):
        raise ImportError()

    monkeypatch.setattr(go.Figure, "__init__", mock_fn)

    monkeypatch.setattr(Config, "PREFERRED_PLOTTING_BACKEND", PlottingBackend.PLOTLY)
    p = Profile.round(1)
    plot = p.plot()
    assert isinstance(plot, plt.Figure)


def test_plot_preferred_matplotlib_block_impl(monkeypatch):
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go

    def mock_fn(*args, **kwargs):
        raise NotImplementedError()

    monkeypatch.setattr(plt.Figure, "__init__", mock_fn)

    monkeypatch.setattr(Config, "PREFERRED_PLOTTING_BACKEND", PlottingBackend.MATPLOTLIB)
    p = Profile.round(1)
    plot = p.plot()
    assert isinstance(plot, go.Figure)


def test_plot_preferred_plotly_block_impl(monkeypatch):
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go

    def mock_fn(*args, **kwargs):
        raise NotImplementedError()

    monkeypatch.setattr(go.Figure, "__init__", mock_fn)

    monkeypatch.setattr(Config, "PREFERRED_PLOTTING_BACKEND", PlottingBackend.PLOTLY)
    p = Profile.round(1)
    plot = p.plot()
    assert isinstance(plot, plt.Figure)
