from math import pi
import diagrams

k_c = 4  # based on four simply supported edges and an a/b of >3
root_chord = 6.86  # m
tip_chord = 1.85  # m
wingbox_root_length = root_chord * 0.45  # m
wingbox_tip_length = tip_chord * 0.45  # m
half_span = 43.58 / 2  # m
skin_thickness_1 = 0.01  # m
skin_thickness_2 = 0.021  # m
skin_thickness_3 = 0.01  # m
t_over_c = 7.96
wingbox_root_thickness = root_chord * t_over_c / 100  # m
wingbox_tip_thickness = tip_chord * t_over_c / 100  # m
E = 6.89e10  # Pa
nu = 0.33
shear_modulus = 2.6e10  # Pa
I_skin = 0.0001  # m^4


def chord_at_span(span):
    return wingbox_root_length - (wingbox_root_length - wingbox_tip_length) * (
        span / half_span
    )


def thickness_at_span(span):
    return wingbox_root_thickness - (wingbox_root_thickness - wingbox_tip_thickness) * (
        span / half_span
    )


def stringer_spacing(span, stringers):
    return chord_at_span(span) / stringers


stringer_spacing_1 = [
    stringer_spacing(0, 50),
    stringer_spacing(half_span * 0.4, 40),
    stringer_spacing(half_span * 0.65, 20),
]
stringer_spacing_2 = [
    stringer_spacing(0, 10),
    stringer_spacing(half_span * 0.4, 10),
    stringer_spacing(half_span * 0.65, 10),
]
stringer_spacing_3 = [
    stringer_spacing(0, 30),
    stringer_spacing(half_span * 0.4, 20),
    stringer_spacing(half_span * 0.65, 10),
]

critical_spacing = [
    max(stringer_spacing_1),
    max(stringer_spacing_2),
    max(stringer_spacing_3),
]
print(critical_spacing)

moment = diagrams.moment_calc(
    0.908, [diagrams.engine_mass], [diagrams.wing_mass], 3.75, 8328.245793
)


def critical_buckling_stress(thickness, width):
    return pi**2 * k_c * E / (12 * (1 - nu**2)) * (thickness / width) ** 2


print(
    f"{critical_buckling_stress(skin_thickness_1, max(stringer_spacing_1))/1e6:.2f} MPa with {max(stringer_spacing_1):.2f} m stringer spacing"
)
print(
    f"{critical_buckling_stress(skin_thickness_2, max(stringer_spacing_2))/1e6:.2f} MPa with {max(stringer_spacing_2):.2f} m stringer spacing"
)
print(
    f"{critical_buckling_stress(skin_thickness_3, max(stringer_spacing_3))/1e6:.2f} MPa with {max(stringer_spacing_3):.2f} m stringer spacing"
)
