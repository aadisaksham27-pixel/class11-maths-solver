def moles_from_mass(mass, molar_mass):

    if molar_mass == 0:
        raise ValueError(
            "Molar mass cannot be zero."
        )

    return mass / molar_mass


def mass_from_moles(moles, molar_mass):

    return moles * molar_mass


def molarity(moles, volume_litres):

    if volume_litres == 0:
        raise ValueError(
            "Volume cannot be zero."
        )

    return moles / volume_litres


def moles_from_molarity(
    molarity_value,
    volume_litres
):

    return molarity_value * volume_litres


def density(mass, volume):

    if volume == 0:
        raise ValueError(
            "Volume cannot be zero."
        )

    return mass / volume


def percentage_composition(
    element_mass,
    total_mass
):

    if total_mass == 0:
        raise ValueError(
            "Total mass cannot be zero."
        )

    return (
        element_mass /
        total_mass
    ) * 100