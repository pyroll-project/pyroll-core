from pathlib import Path
from typing import Any

import pytask
from schemdraw import Drawing
from schemdraw.elements import ElementCompound
from schemdraw.flow import Box, Arrow
from schemdraw.util import Point


class Block(ElementCompound):
    def __init__(self, title: str, content: list[str], width: float, *d, **kwargs):
        super().__init__(*d, **kwargs)

        self.right()

        t = self.add(Box(h=1, w=width).anchor("N").at([0, 0]).label(title).fill(color="lightgray"))

        if content:
            content_height = len(content) / 2 + 0.5
            c = self.add(Box(h=content_height, w=width).anchor("N").at(t.S).label(
                "\n".join(content)
            ))
        else:
            c = t

        bbox = self.get_bbox()
        center_x = (bbox.xmax + bbox.xmin) / 2
        center_y = (bbox.ymax + bbox.ymin) / 2
        self.anchors = dict(
            N=t.N,
            S=c.S,
            E=(bbox.xmax, center_y),
            W=(bbox.xmin, center_y),
            center=(center_x, center_y),
            NW=(bbox.xmin, bbox.ymax),
            NE=(bbox.xmax, bbox.ymax),
            SW=(bbox.xmin, bbox.ymin),
            SE=(bbox.xmax, bbox.ymin)
        )

        self.drop("S")


@pytask.mark.produces("chart_influence.svg")
def task_chart_influence(produces: dict[Any, Path]):
    d = Drawing()

    material_prop = d.add(Block(
        "Werkstoffeigenschaften",
        ["Fließspannung", "Verfestigung", "Entfestigung", "Ausscheidung", "Phasenumwandlung", "Anisotropie"],
        5.5
    ).anchor("center").at([0, 0]))

    temperature = d.add(Block(
        "Temperaturentwicklung",
        ["Erwärmung", "Kühlung", "Walzenkontakt", "Strahlung", "Umformwärme"],
        5.5
    ).anchor("center").at([-7, 0]))

    material_flow = d.add(Block(
        "Werkstoffluss",
        ["Breitung", "Streckung", "Geschwindigkeit", "Umformgrad", "Umformgeschwindigkeit"],
        5.5
    ).anchor("center").at([0, 5]))

    groove_design = d.add(Block(
        "Kalibrierung",
        ["Kaliberfolge", "Kaliberform", "Kalibergröße", "Max. Streckgrad", "Walzspalt", "Walzenradius"],
        5.5
    ).anchor("center").at([-7, 5]))

    force = d.add(Block(
        "Walzkraft/-moment",
        ["Gedrückte Fläche", "Reibung", "Scherung"],
        5.5
    ).anchor("center").at([7, 0]))

    stand = d.add(Block(
        "Anlagenelastik, Verschleiß",
        ["Walzenwerkstoff", "Walzengeometrie", "Gerüststeifigkeit"],
        6
    ).anchor("center").at([7, 5]))

    d += Arrow(double=True).at(temperature.E).to(material_prop.W)
    d += Arrow(double=True).at(groove_design.E).to(material_flow.W)
    d += Arrow(double=True).at(material_flow.S).to(material_prop.N)
    d += Arrow(double=True).at(material_flow.E).to(stand.W)

    d += Arrow().at(material_flow.SE).to(force.NW)
    d += Arrow().at(material_prop.E).to(force.W)
    d += Arrow().at(force.N).to(stand.S)
    d += Arrow().at(material_flow.SW).to(temperature.NE)

    d.save((str(produces)))
