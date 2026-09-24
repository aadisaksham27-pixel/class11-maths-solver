# ============================================================
# KSHITIJ PHYSICS CALCULATOR ENGINE
# ============================================================

import math


# ============================================================
# BASIC MOTION
# ============================================================

def speed(distance, time):
    if time == 0:
        raise ValueError("Time cannot be zero.")
    return distance / time


def velocity(displacement, time):
    if time == 0:
        raise ValueError("Time cannot be zero.")
    return displacement / time


def acceleration(change_in_velocity, time):
    if time == 0:
        raise ValueError("Time cannot be zero.")
    return change_in_velocity / time


def final_velocity(initial_velocity, acceleration_value, time):
    return initial_velocity + acceleration_value * time


def displacement(
    initial_velocity,
    time,
    acceleration_value
):
    return (
        initial_velocity * time
        + 0.5 * acceleration_value * time ** 2
    )


def final_velocity_squared(
    initial_velocity,
    acceleration_value,
    displacement_value
):
    return (
        initial_velocity ** 2
        + 2 * acceleration_value * displacement_value
    )


def average_velocity(initial_velocity, final_velocity_value):
    return (
        initial_velocity + final_velocity_value
    ) / 2


# ============================================================
# NEWTON'S LAWS / FORCE
# ============================================================

def force(mass, acceleration_value):
    return mass * acceleration_value


def mass_from_force(force_value, acceleration_value):
    if acceleration_value == 0:
        raise ValueError("Acceleration cannot be zero.")
    return force_value / acceleration_value


def acceleration_from_force(force_value, mass):
    if mass == 0:
        raise ValueError("Mass cannot be zero.")
    return force_value / mass


def weight(mass, gravity=9.8):
    return mass * gravity


def normal_force(mass, gravity=9.8):
    return mass * gravity


# ============================================================
# WORK, ENERGY AND POWER
# ============================================================

def work(force_value, distance):
    return force_value * distance


def work_at_angle(
    force_value,
    distance,
    angle_degrees
):
    angle_radians = math.radians(angle_degrees)

    return (
        force_value
        * distance
        * math.cos(angle_radians)
    )


def kinetic_energy(mass, velocity_value):
    return 0.5 * mass * velocity_value ** 2


def potential_energy(
    mass,
    gravity,
    height
):
    return mass * gravity * height


def mechanical_energy(
    kinetic_energy_value,
    potential_energy_value
):
    return (
        kinetic_energy_value
        + potential_energy_value
    )


def power(work_value, time):
    if time == 0:
        raise ValueError("Time cannot be zero.")

    return work_value / time


def power_from_force(
    force_value,
    velocity_value
):
    return force_value * velocity_value


# ============================================================
# MOMENTUM
# ============================================================

def momentum(mass, velocity_value):
    return mass * velocity_value


def velocity_from_momentum(
    momentum_value,
    mass
):
    if mass == 0:
        raise ValueError("Mass cannot be zero.")

    return momentum_value / mass


def impulse(force_value, time):
    return force_value * time


def change_in_momentum(
    final_momentum,
    initial_momentum
):
    return final_momentum - initial_momentum


# ============================================================
# COLLISIONS
# ============================================================

def total_momentum(
    mass1,
    velocity1,
    mass2,
    velocity2
):
    return (
        mass1 * velocity1
        + mass2 * velocity2
    )


def final_velocity_after_sticking(
    mass1,
    velocity1,
    mass2,
    velocity2
):
    total_mass = mass1 + mass2

    if total_mass == 0:
        raise ValueError(
            "Total mass cannot be zero."
        )

    return (
        mass1 * velocity1
        + mass2 * velocity2
    ) / total_mass


# ============================================================
# GRAVITATION
# ============================================================

GRAVITATIONAL_CONSTANT = 6.67430e-11


def gravitational_force(
    mass1,
    mass2,
    distance
):
    if distance == 0:
        raise ValueError(
            "Distance cannot be zero."
        )

    return (
        GRAVITATIONAL_CONSTANT
        * mass1
        * mass2
        / distance ** 2
    )


def gravitational_acceleration(
    mass,
    distance
):
    if distance == 0:
        raise ValueError(
            "Distance cannot be zero."
        )

    return (
        GRAVITATIONAL_CONSTANT
        * mass
        / distance ** 2
    )


def escape_velocity(
    mass,
    radius
):
    if radius == 0:
        raise ValueError(
            "Radius cannot be zero."
        )

    return math.sqrt(
        2
        * GRAVITATIONAL_CONSTANT
        * mass
        / radius
    )


# ============================================================
# PRESSURE / DENSITY / FLUIDS
# ============================================================

def pressure(force_value, area):
    if area == 0:
        raise ValueError(
            "Area cannot be zero."
        )

    return force_value / area


def force_from_pressure(
    pressure_value,
    area
):
    return pressure_value * area


def area_from_pressure(
    force_value,
    pressure_value
):
    if pressure_value == 0:
        raise ValueError(
            "Pressure cannot be zero."
        )

    return force_value / pressure_value


def density(mass, volume):
    if volume == 0:
        raise ValueError(
            "Volume cannot be zero."
        )

    return mass / volume


def mass_from_density(
    density_value,
    volume
):
    return density_value * volume


def volume_from_density(
    mass,
    density_value
):
    if density_value == 0:
        raise ValueError(
            "Density cannot be zero."
        )

    return mass / density_value


def liquid_pressure(
    density_value,
    gravity,
    depth
):
    return (
        density_value
        * gravity
        * depth
    )


def buoyant_force(
    density_value,
    gravity,
    displaced_volume
):
    return (
        density_value
        * gravity
        * displaced_volume
    )


# ============================================================
# CIRCULAR MOTION
# ============================================================

def centripetal_force(
    mass,
    velocity_value,
    radius
):
    if radius == 0:
        raise ValueError(
            "Radius cannot be zero."
        )

    return (
        mass
        * velocity_value ** 2
        / radius
    )


def centripetal_acceleration(
    velocity_value,
    radius
):
    if radius == 0:
        raise ValueError(
            "Radius cannot be zero."
        )

    return velocity_value ** 2 / radius


def angular_velocity(
    angle_radians,
    time
):
    if time == 0:
        raise ValueError(
            "Time cannot be zero."
        )

    return angle_radians / time


def linear_velocity_from_angular(
    angular_velocity_value,
    radius
):
    return angular_velocity_value * radius


# ============================================================
# HEAT / THERMAL
# ============================================================

def heat_energy(
    mass,
    specific_heat,
    temperature_change
):
    return (
        mass
        * specific_heat
        * temperature_change
    )


def temperature_change(
    final_temperature,
    initial_temperature
):
    return final_temperature - initial_temperature


def specific_heat_from_heat(
    heat,
    mass,
    temperature_change_value
):
    if mass == 0:
        raise ValueError(
            "Mass cannot be zero."
        )

    if temperature_change_value == 0:
        raise ValueError(
            "Temperature change cannot be zero."
        )

    return (
        heat
        / (
            mass
            * temperature_change_value
        )
    )


def latent_heat_energy(
    mass,
    latent_heat
):
    return mass * latent_heat


# ============================================================
# WAVES
# ============================================================

def wave_speed(frequency, wavelength):
    return frequency * wavelength


def wavelength_from_speed(
    wave_speed_value,
    frequency
):
    if frequency == 0:
        raise ValueError(
            "Frequency cannot be zero."
        )

    return wave_speed_value / frequency


def frequency_from_speed(
    wave_speed_value,
    wavelength
):
    if wavelength == 0:
        raise ValueError(
            "Wavelength cannot be zero."
        )

    return wave_speed_value / wavelength


def frequency_from_period(period):
    if period == 0:
        raise ValueError(
            "Period cannot be zero."
        )

    return 1 / period


def period_from_frequency(frequency):
    if frequency == 0:
        raise ValueError(
            "Frequency cannot be zero."
        )

    return 1 / frequency


# ============================================================
# ELECTRICITY
# ============================================================

def ohms_law(
    voltage=None,
    current=None,
    resistance=None
):

    supplied = sum(
        x is not None
        for x in [
            voltage,
            current,
            resistance
        ]
    )

    if supplied != 2:
        raise ValueError(
            "Provide exactly two of voltage, "
            "current and resistance."
        )

    if voltage is None:

        return current * resistance

    if current is None:

        if resistance == 0:
            raise ValueError(
                "Resistance cannot be zero."
            )

        return voltage / resistance

    if resistance is None:

        if current == 0:
            raise ValueError(
                "Current cannot be zero."
            )

        return voltage / current


def electrical_power(
    voltage,
    current
):
    return voltage * current


def electrical_power_from_resistance(
    current,
    resistance
):
    return current ** 2 * resistance


def electrical_power_from_voltage(
    voltage,
    resistance
):
    if resistance == 0:
        raise ValueError(
            "Resistance cannot be zero."
        )

    return voltage ** 2 / resistance


def electrical_energy(
    power_value,
    time
):
    return power_value * time


def resistance_series(*resistances):
    return sum(resistances)


def resistance_parallel(*resistances):

    if not resistances:
        raise ValueError(
            "At least one resistance is required."
        )

    if any(r == 0 for r in resistances):
        return 0

    reciprocal_sum = sum(
        1 / r
        for r in resistances
    )

    return 1 / reciprocal_sum


# ============================================================
# CHARGE / CURRENT
# ============================================================

def current_from_charge(
    charge,
    time
):
    if time == 0:
        raise ValueError(
            "Time cannot be zero."
        )

    return charge / time


def charge_from_current(
    current,
    time
):
    return current * time


# ============================================================
# CAPACITANCE
# ============================================================

def capacitance(
    charge,
    voltage
):
    if voltage == 0:
        raise ValueError(
            "Voltage cannot be zero."
        )

    return charge / voltage


def capacitor_energy(
    capacitance_value,
    voltage
):
    return (
        0.5
        * capacitance_value
        * voltage ** 2
    )


# ============================================================
# SIMPLE UNIT CONVERSIONS
# ============================================================

def kmh_to_ms(speed_kmh):
    return speed_kmh / 3.6


def ms_to_kmh(speed_ms):
    return speed_ms * 3.6


def celsius_to_kelvin(celsius):
    return celsius + 273.15


def kelvin_to_celsius(kelvin):
    return kelvin - 273.15


def celsius_to_fahrenheit(celsius):
    return (
        celsius * 9 / 5
        + 32
    )


def fahrenheit_to_celsius(fahrenheit):
    return (
        (fahrenheit - 32)
        * 5 / 9
    )