import numpy as np
from ..laying_head import LayingHead


@LayingHead.number_of_windings
def number_of_windings(self: LayingHead):
    return self.in_profile.length / self.winding_diameter


@LayingHead.duration
def duration(self: LayingHead):
    return self.number_of_windings * np.pi * self.winding_diameter / self.in_profile.velocity


@LayingHead.characteristic_layer_section_length
def characteristic_layer_section_length(self: LayingHead):
    return np.pi * self.winding_diameter * (self.stelmor_conveyor_velocity / self.in_profile.velocity)


@LayingHead.layer_packing_height
def layer_packing_height(self: LayingHead):
    equivalent_diameter = self.in_profile.equivalent_radius * 2
    return equivalent_diameter * self.in_profile.velocity / (np.pi * self.stelmor_conveyor_velocity)


@LayingHead.layer_vertical_distance
def layer_vertical_distance(self: LayingHead):
    equivalent_diameter = self.in_profile.equivalent_radius * 2
    return (1 / equivalent_diameter ** 2 - 1 / self.characteristic_layer_section_length ** 2) ** (-0.5)


@LayingHead.stelmor_layer_distribution
def stelmor_layer_distribution(self: LayingHead):

    laying_time = np.linspace(0, self.duration, 10000)
    winding_radius = self.winding_diameter / 2
    winding_angle = 2 * (self.in_profile.velocity / self.winding_diameter) * laying_time

    x = winding_radius * np.cos(winding_angle)
    y = winding_radius * np.sin(winding_angle) + self.stelmor_conveyor_velocity * laying_time
    z = 0.5 * self.layer_packing_height * np.sin(winding_angle)

    return x, y, z


@LayingHead.layer_mass_distribution
def layer_mass_distribution(self: LayingHead):
    winding_radius = self.winding_diameter / 2

    x_coords = self.stelmor_layer_distribution[0]
    mask = x_coords > 0
    x = x_coords[mask]

    x = np.clip(x, -0.99 * winding_radius, 0.99 * winding_radius)

    return 2 / self.characteristic_layer_section_length * (1 - (x / winding_radius) ** 2) ** (-0.5)


@LayingHead.layer_horizontal_distance
def layer_horizontal_distance(self: LayingHead):
    winding_radius = self.winding_diameter / 2
    x_coords = self.stelmor_layer_distribution[0]
    mask = x_coords > 0
    x = x_coords[mask]

    x = np.clip(x, -0.999 * winding_radius, 0.999 * winding_radius)

    z_abs = 0.5 * self.layer_packing_height * (1 - (x / winding_radius) ** 2) ** 0.5
    term = 1 - 4 * (z_abs - self.layer_vertical_distance) ** 2 / self.layer_packing_height ** 2
    term = np.maximum(term, 0)

    return winding_radius * term ** 0.5 - x


@LayingHead.void_ratio
def void_ratio(self: LayingHead):
    equivalent_diameter = self.in_profile.equivalent_radius * 2


    return 1 - 0.25 * np.pi * equivalent_diameter / (
                self.layer_horizontal_distance * (1 + self.layer_vertical_distance / equivalent_diameter))


@LayingHead.wire_length_in_characteristic_layer_section_length
def wire_length_in_characteristic_layer_section_length(self: LayingHead):
    return np.pi * self.winding_diameter / 2
