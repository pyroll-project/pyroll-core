import numpy as np

from ..spooler import Spooler


@Spooler.duration
def duration(self: Spooler):
    if self.has_set_or_cached("finished_coil_weight"):
        length = self.finished_coil_weight / self.in_profile.density
        return length / self.velocity
    else:
        return self.in_profile.length / self.velocity


@Spooler.windings_per_layer
def windings_per_layer(self: Spooler):
    equivalent_diameter = self.in_profile.equivalent_radius * 2
    return np.round(self.mandrel_width / equivalent_diameter)


@Spooler.finished_coil_radius
def finished_coil_radius(self: Spooler):
    return self.coil_layer_radii[-1]


@Spooler.coil_layer_bending_stresses
def coil_layer_bending_stresses(self: Spooler):
    equivalent_diameter = self.in_profile.equivalent_radius * 2
    bending_stresses = []

    for layer_radius in self.coil_layer_radii:
        stress = self.in_profile.elastic_modulus * equivalent_diameter / (2 * layer_radius)
        bending_stresses.append(stress)

    return np.array(bending_stresses)


@Spooler.coil_layer_bending_torques
def coil_layer_bending_torques(self: Spooler):
    equivalent_diameter = self.in_profile.equivalent_radius * 2

    section_modulus = np.pi * equivalent_diameter**3 / 32

    bending_torques = []

    for bending_stress in self.coil_layer_bending_stresses:
        torque = bending_stress * section_modulus
        bending_torques.append(torque)

    return np.array(bending_torques)


@Spooler.coil_layer_radii
def coil_layer_radii(self: Spooler):
    layer_radii = []
    layer_number = 1
    cumulative_weight = 0
    cumulative_length = 0
    equivalent_diameter = self.in_profile.equivalent_radius * 2

    while cumulative_weight < self.finished_coil_weight and cumulative_length < self.in_profile.length:
        outer_radius_current_layer = self.mandrel_radius + layer_number * equivalent_diameter
        layer_radii.append(outer_radius_current_layer)

        mean_radius_current_layer = self.mandrel_radius + (layer_number - 0.5) * equivalent_diameter
        wire_length_current_layer = self.windings_per_layer * 2 * np.pi * mean_radius_current_layer

        wire_volume_current_layer = wire_length_current_layer * self.in_profile.cross_section.area
        weight_current_layer = wire_volume_current_layer * self.in_profile.density

        weight_ok = cumulative_weight + weight_current_layer <= self.finished_coil_weight
        length_ok = cumulative_length + wire_length_current_layer <= self.in_profile.length

        if weight_ok and length_ok:
            cumulative_weight += weight_current_layer
            cumulative_length += wire_length_current_layer
            layer_number += 1
        else:
            if not weight_ok:
                remaining_weight = self.finished_coil_weight - cumulative_weight
                partial_layer_fraction = remaining_weight / weight_current_layer
            else:
                remaining_length = self.in_profile.length - cumulative_length
                partial_layer_fraction = remaining_length / wire_length_current_layer

            final_radius = self.mandrel_radius + (layer_number - 1 + partial_layer_fraction) * equivalent_diameter
            layer_radii[-1] = final_radius
            break

    return np.array(layer_radii)
