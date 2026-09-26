from flask import Flask, request, render_template_string, jsonify

from solver import solve, detect_chapter
from curriculum import get_classes, get_chapters

from ai_tutor import solve_with_ai, solve_with_media

try:
    from math_engine import solve_math as unified_math_solve
except Exception:
    unified_math_solve = None

try:
    from school_math import solve_school_math
except Exception:
    solve_school_math = None

from physics import (
    speed,
    velocity,
    acceleration,
    final_velocity,
    displacement,
    final_velocity_squared,
    average_velocity,
    force,
    mass_from_force,
    acceleration_from_force,
    weight,
    normal_force,
    work,
    work_at_angle,
    kinetic_energy,
    potential_energy,
    mechanical_energy,
    power,
    power_from_force,
    momentum,
    velocity_from_momentum,
    impulse,
    change_in_momentum,
    total_momentum,
    final_velocity_after_sticking,
    gravitational_force,
    gravitational_acceleration,
    escape_velocity,
    pressure,
    force_from_pressure,
    area_from_pressure,
    density,
    mass_from_density,
    volume_from_density,
    liquid_pressure,
    buoyant_force,
    centripetal_force,
    centripetal_acceleration,
    angular_velocity,
    linear_velocity_from_angular,
    heat_energy,
    temperature_change,
    specific_heat_from_heat,
    latent_heat_energy,
    wave_speed,
    wavelength_from_speed,
    frequency_from_speed,
    frequency_from_period,
    period_from_frequency,
    ohms_law,
    electrical_power,
    electrical_power_from_resistance,
    electrical_power_from_voltage,
    electrical_energy,
    resistance_series,
    resistance_parallel,
    current_from_charge,
    charge_from_current,
    capacitance,
    capacitor_energy,
    kmh_to_ms,
    ms_to_kmh,
    celsius_to_kelvin,
    kelvin_to_celsius,
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
)


app = Flask(__name__)

CLASSES = get_classes()


# ============================================================
# PHYSICS CALCULATOR DATABASE
# ============================================================

PHYSICS_CALCULATIONS = {

    "speed": {
        "name": "Speed",
        "category": "Motion",
        "formula": "v = distance / time",
        "unit": "m/s",
        "function": speed,
        "fields": [
            ("distance", "Distance", "m"),
            ("time", "Time", "s"),
        ],
    },

    "velocity": {
        "name": "Velocity",
        "category": "Motion",
        "formula": "v = displacement / time",
        "unit": "m/s",
        "function": velocity,
        "fields": [
            ("displacement", "Displacement", "m"),
            ("time", "Time", "s"),
        ],
    },

    "acceleration": {
        "name": "Acceleration",
        "category": "Motion",
        "formula": "a = change in velocity / time",
        "unit": "m/s²",
        "function": acceleration,
        "fields": [
            ("change_in_velocity", "Change in velocity", "m/s"),
            ("time", "Time", "s"),
        ],
    },

    "final_velocity": {
        "name": "Final Velocity",
        "category": "Motion",
        "formula": "v = u + at",
        "unit": "m/s",
        "function": final_velocity,
        "fields": [
            ("initial_velocity", "Initial velocity", "m/s"),
            ("acceleration_value", "Acceleration", "m/s²"),
            ("time", "Time", "s"),
        ],
    },

    "displacement": {
        "name": "Displacement",
        "category": "Motion",
        "formula": "s = ut + ½at²",
        "unit": "m",
        "function": displacement,
        "fields": [
            ("initial_velocity", "Initial velocity", "m/s"),
            ("time", "Time", "s"),
            ("acceleration_value", "Acceleration", "m/s²"),
        ],
    },

    "final_velocity_squared": {
        "name": "Final Velocity Squared",
        "category": "Motion",
        "formula": "v² = u² + 2as",
        "unit": "m²/s²",
        "function": final_velocity_squared,
        "fields": [
            ("initial_velocity", "Initial velocity", "m/s"),
            ("acceleration_value", "Acceleration", "m/s²"),
            ("displacement_value", "Displacement", "m"),
        ],
    },

    "average_velocity": {
        "name": "Average Velocity",
        "category": "Motion",
        "formula": "v = (u + v) / 2",
        "unit": "m/s",
        "function": average_velocity,
        "fields": [
            ("initial_velocity", "Initial velocity", "m/s"),
            ("final_velocity_value", "Final velocity", "m/s"),
        ],
    },

    "force": {
        "name": "Force",
        "category": "Force & Newton's Laws",
        "formula": "F = ma",
        "unit": "N",
        "function": force,
        "fields": [
            ("mass", "Mass", "kg"),
            ("acceleration_value", "Acceleration", "m/s²"),
        ],
    },

    "mass_from_force": {
        "name": "Mass from Force",
        "category": "Force & Newton's Laws",
        "formula": "m = F/a",
        "unit": "kg",
        "function": mass_from_force,
        "fields": [
            ("force_value", "Force", "N"),
            ("acceleration_value", "Acceleration", "m/s²"),
        ],
    },

    "acceleration_from_force": {
        "name": "Acceleration from Force",
        "category": "Force & Newton's Laws",
        "formula": "a = F/m",
        "unit": "m/s²",
        "function": acceleration_from_force,
        "fields": [
            ("force_value", "Force", "N"),
            ("mass", "Mass", "kg"),
        ],
    },

    "weight": {
        "name": "Weight",
        "category": "Force & Newton's Laws",
        "formula": "W = mg",
        "unit": "N",
        "function": weight,
        "fields": [
            ("mass", "Mass", "kg"),
            ("gravity", "Gravity", "m/s²"),
        ],
        "defaults": {"gravity": 9.8},
    },

    "normal_force": {
        "name": "Normal Force",
        "category": "Force & Newton's Laws",
        "formula": "N = mg",
        "unit": "N",
        "function": normal_force,
        "fields": [
            ("mass", "Mass", "kg"),
            ("gravity", "Gravity", "m/s²"),
        ],
        "defaults": {"gravity": 9.8},
    },

    "work": {
        "name": "Work",
        "category": "Work, Energy & Power",
        "formula": "W = Fd",
        "unit": "J",
        "function": work,
        "fields": [
            ("force_value", "Force", "N"),
            ("distance", "Distance", "m"),
        ],
    },

    "work_at_angle": {
        "name": "Work at an Angle",
        "category": "Work, Energy & Power",
        "formula": "W = Fd cosθ",
        "unit": "J",
        "function": work_at_angle,
        "fields": [
            ("force_value", "Force", "N"),
            ("distance", "Distance", "m"),
            ("angle_degrees", "Angle", "degrees"),
        ],
    },

    "kinetic_energy": {
        "name": "Kinetic Energy",
        "category": "Work, Energy & Power",
        "formula": "KE = ½mv²",
        "unit": "J",
        "function": kinetic_energy,
        "fields": [
            ("mass", "Mass", "kg"),
            ("velocity_value", "Velocity", "m/s"),
        ],
    },

    "potential_energy": {
        "name": "Potential Energy",
        "category": "Work, Energy & Power",
        "formula": "PE = mgh",
        "unit": "J",
        "function": potential_energy,
        "fields": [
            ("mass", "Mass", "kg"),
            ("gravity", "Gravity", "m/s²"),
            ("height", "Height", "m"),
        ],
        "defaults": {"gravity": 9.8},
    },

    "mechanical_energy": {
        "name": "Mechanical Energy",
        "category": "Work, Energy & Power",
        "formula": "E = KE + PE",
        "unit": "J",
        "function": mechanical_energy,
        "fields": [
            ("kinetic_energy_value", "Kinetic Energy", "J"),
            ("potential_energy_value", "Potential Energy", "J"),
        ],
    },

    "power": {
        "name": "Power",
        "category": "Work, Energy & Power",
        "formula": "P = W/t",
        "unit": "W",
        "function": power,
        "fields": [
            ("work_value", "Work", "J"),
            ("time", "Time", "s"),
        ],
    },

    "power_from_force": {
        "name": "Power from Force",
        "category": "Work, Energy & Power",
        "formula": "P = Fv",
        "unit": "W",
        "function": power_from_force,
        "fields": [
            ("force_value", "Force", "N"),
            ("velocity_value", "Velocity", "m/s"),
        ],
    },

    "momentum": {
        "name": "Momentum",
        "category": "Momentum & Collisions",
        "formula": "p = mv",
        "unit": "kg·m/s",
        "function": momentum,
        "fields": [
            ("mass", "Mass", "kg"),
            ("velocity_value", "Velocity", "m/s"),
        ],
    },

    "velocity_from_momentum": {
        "name": "Velocity from Momentum",
        "category": "Momentum & Collisions",
        "formula": "v = p/m",
        "unit": "m/s",
        "function": velocity_from_momentum,
        "fields": [
            ("momentum_value", "Momentum", "kg·m/s"),
            ("mass", "Mass", "kg"),
        ],
    },

    "impulse": {
        "name": "Impulse",
        "category": "Momentum & Collisions",
        "formula": "J = Ft",
        "unit": "N·s",
        "function": impulse,
        "fields": [
            ("force_value", "Force", "N"),
            ("time", "Time", "s"),
        ],
    },

    "change_in_momentum": {
        "name": "Change in Momentum",
        "category": "Momentum & Collisions",
        "formula": "Δp = pf - pi",
        "unit": "kg·m/s",
        "function": change_in_momentum,
        "fields": [
            ("final_momentum", "Final momentum", "kg·m/s"),
            ("initial_momentum", "Initial momentum", "kg·m/s"),
        ],
    },

    "total_momentum": {
        "name": "Total Momentum",
        "category": "Momentum & Collisions",
        "formula": "p = m₁v₁ + m₂v₂",
        "unit": "kg·m/s",
        "function": total_momentum,
        "fields": [
            ("mass1", "Mass 1", "kg"),
            ("velocity1", "Velocity 1", "m/s"),
            ("mass2", "Mass 2", "kg"),
            ("velocity2", "Velocity 2", "m/s"),
        ],
    },

    "final_velocity_after_sticking": {
        "name": "Sticking Collision",
        "category": "Momentum & Collisions",
        "formula": "v = (m₁v₁ + m₂v₂)/(m₁+m₂)",
        "unit": "m/s",
        "function": final_velocity_after_sticking,
        "fields": [
            ("mass1", "Mass 1", "kg"),
            ("velocity1", "Velocity 1", "m/s"),
            ("mass2", "Mass 2", "kg"),
            ("velocity2", "Velocity 2", "m/s"),
        ],
    },

    "gravitational_force": {
        "name": "Gravitational Force",
        "category": "Gravitation",
        "formula": "F = Gm₁m₂/r²",
        "unit": "N",
        "function": gravitational_force,
        "fields": [
            ("mass1", "Mass 1", "kg"),
            ("mass2", "Mass 2", "kg"),
            ("distance", "Distance", "m"),
        ],
    },

    "gravitational_acceleration": {
        "name": "Gravitational Acceleration",
        "category": "Gravitation",
        "formula": "g = GM/r²",
        "unit": "m/s²",
        "function": gravitational_acceleration,
        "fields": [
            ("mass", "Mass", "kg"),
            ("distance", "Distance", "m"),
        ],
    },

    "escape_velocity": {
        "name": "Escape Velocity",
        "category": "Gravitation",
        "formula": "v = √(2GM/R)",
        "unit": "m/s",
        "function": escape_velocity,
        "fields": [
            ("mass", "Mass", "kg"),
            ("radius", "Radius", "m"),
        ],
    },

    "pressure": {
        "name": "Pressure",
        "category": "Pressure & Fluids",
        "formula": "P = F/A",
        "unit": "Pa",
        "function": pressure,
        "fields": [
            ("force_value", "Force", "N"),
            ("area", "Area", "m²"),
        ],
    },

    "force_from_pressure": {
        "name": "Force from Pressure",
        "category": "Pressure & Fluids",
        "formula": "F = PA",
        "unit": "N",
        "function": force_from_pressure,
        "fields": [
            ("pressure_value", "Pressure", "Pa"),
            ("area", "Area", "m²"),
        ],
    },

    "area_from_pressure": {
        "name": "Area from Pressure",
        "category": "Pressure & Fluids",
        "formula": "A = F/P",
        "unit": "m²",
        "function": area_from_pressure,
        "fields": [
            ("force_value", "Force", "N"),
            ("pressure_value", "Pressure", "Pa"),
        ],
    },

    "density": {
        "name": "Density",
        "category": "Pressure & Fluids",
        "formula": "ρ = m/V",
        "unit": "kg/m³",
        "function": density,
        "fields": [
            ("mass", "Mass", "kg"),
            ("volume", "Volume", "m³"),
        ],
    },

    "mass_from_density": {
        "name": "Mass from Density",
        "category": "Pressure & Fluids",
        "formula": "m = ρV",
        "unit": "kg",
        "function": mass_from_density,
        "fields": [
            ("density_value", "Density", "kg/m³"),
            ("volume", "Volume", "m³"),
        ],
    },

    "volume_from_density": {
        "name": "Volume from Density",
        "category": "Pressure & Fluids",
        "formula": "V = m/ρ",
        "unit": "m³",
        "function": volume_from_density,
        "fields": [
            ("mass", "Mass", "kg"),
            ("density_value", "Density", "kg/m³"),
        ],
    },

    "liquid_pressure": {
        "name": "Liquid Pressure",
        "category": "Pressure & Fluids",
        "formula": "P = ρgh",
        "unit": "Pa",
        "function": liquid_pressure,
        "fields": [
            ("density_value", "Liquid density", "kg/m³"),
            ("gravity", "Gravity", "m/s²"),
            ("depth", "Depth", "m"),
        ],
        "defaults": {"gravity": 9.8},
    },

    "buoyant_force": {
        "name": "Buoyant Force",
        "category": "Pressure & Fluids",
        "formula": "Fb = ρgV",
        "unit": "N",
        "function": buoyant_force,
        "fields": [
            ("density_value", "Fluid density", "kg/m³"),
            ("gravity", "Gravity", "m/s²"),
            ("displaced_volume", "Displaced volume", "m³"),
        ],
        "defaults": {"gravity": 9.8},
    },

    "centripetal_force": {
        "name": "Centripetal Force",
        "category": "Circular Motion",
        "formula": "F = mv²/r",
        "unit": "N",
        "function": centripetal_force,
        "fields": [
            ("mass", "Mass", "kg"),
            ("velocity_value", "Velocity", "m/s"),
            ("radius", "Radius", "m"),
        ],
    },

    "centripetal_acceleration": {
        "name": "Centripetal Acceleration",
        "category": "Circular Motion",
        "formula": "a = v²/r",
        "unit": "m/s²",
        "function": centripetal_acceleration,
        "fields": [
            ("velocity_value", "Velocity", "m/s"),
            ("radius", "Radius", "m"),
        ],
    },

    "angular_velocity": {
        "name": "Angular Velocity",
        "category": "Circular Motion",
        "formula": "ω = θ/t",
        "unit": "rad/s",
        "function": angular_velocity,
        "fields": [
            ("angle_radians", "Angle", "rad"),
            ("time", "Time", "s"),
        ],
    },

    "linear_velocity_from_angular": {
        "name": "Linear Velocity from Angular Velocity",
        "category": "Circular Motion",
        "formula": "v = ωr",
        "unit": "m/s",
        "function": linear_velocity_from_angular,
        "fields": [
            ("angular_velocity_value", "Angular velocity", "rad/s"),
            ("radius", "Radius", "m"),
        ],
    },

    "heat_energy": {
        "name": "Heat Energy",
        "category": "Heat & Thermal",
        "formula": "Q = mcΔT",
        "unit": "J",
        "function": heat_energy,
        "fields": [
            ("mass", "Mass", "kg"),
            ("specific_heat", "Specific heat", "J/kg·K"),
            ("temperature_change", "Temperature change", "K"),
        ],
    },

    "temperature_change": {
        "name": "Temperature Change",
        "category": "Heat & Thermal",
        "formula": "ΔT = Tf - Ti",
        "unit": "K",
        "function": temperature_change,
        "fields": [
            ("final_temperature", "Final temperature", "K"),
            ("initial_temperature", "Initial temperature", "K"),
        ],
    },

    "specific_heat_from_heat": {
        "name": "Specific Heat",
        "category": "Heat & Thermal",
        "formula": "c = Q/(mΔT)",
        "unit": "J/kg·K",
        "function": specific_heat_from_heat,
        "fields": [
            ("heat", "Heat", "J"),
            ("mass", "Mass", "kg"),
            ("temperature_change_value", "Temperature change", "K"),
        ],
    },

    "latent_heat_energy": {
        "name": "Latent Heat Energy",
        "category": "Heat & Thermal",
        "formula": "Q = mL",
        "unit": "J",
        "function": latent_heat_energy,
        "fields": [
            ("mass", "Mass", "kg"),
            ("latent_heat", "Latent heat", "J/kg"),
        ],
    },

    "wave_speed": {
        "name": "Wave Speed",
        "category": "Waves",
        "formula": "v = fλ",
        "unit": "m/s",
        "function": wave_speed,
        "fields": [
            ("frequency", "Frequency", "Hz"),
            ("wavelength", "Wavelength", "m"),
        ],
    },

    "wavelength_from_speed": {
        "name": "Wavelength",
        "category": "Waves",
        "formula": "λ = v/f",
        "unit": "m",
        "function": wavelength_from_speed,
        "fields": [
            ("wave_speed_value", "Wave speed", "m/s"),
            ("frequency", "Frequency", "Hz"),
        ],
    },

    "frequency_from_speed": {
        "name": "Frequency",
        "category": "Waves",
        "formula": "f = v/λ",
        "unit": "Hz",
        "function": frequency_from_speed,
        "fields": [
            ("wave_speed_value", "Wave speed", "m/s"),
            ("wavelength", "Wavelength", "m"),
        ],
    },

    "frequency_from_period": {
        "name": "Frequency from Period",
        "category": "Waves",
        "formula": "f = 1/T",
        "unit": "Hz",
        "function": frequency_from_period,
        "fields": [
            ("period", "Period", "s"),
        ],
    },

    "period_from_frequency": {
        "name": "Period from Frequency",
        "category": "Waves",
        "formula": "T = 1/f",
        "unit": "s",
        "function": period_from_frequency,
        "fields": [
            ("frequency", "Frequency", "Hz"),
        ],
    },

    "ohms_voltage": {
        "name": "Ohm's Law — Voltage",
        "category": "Electricity",
        "formula": "V = IR",
        "unit": "V",
        "function": lambda current, resistance: ohms_law(
            current=current,
            resistance=resistance
        ),
        "fields": [
            ("current", "Current", "A"),
            ("resistance", "Resistance", "Ω"),
        ],
    },

    "ohms_current": {
        "name": "Ohm's Law — Current",
        "category": "Electricity",
        "formula": "I = V/R",
        "unit": "A",
        "function": lambda voltage, resistance: ohms_law(
            voltage=voltage,
            resistance=resistance
        ),
        "fields": [
            ("voltage", "Voltage", "V"),
            ("resistance", "Resistance", "Ω"),
        ],
    },

    "ohms_resistance": {
        "name": "Ohm's Law — Resistance",
        "category": "Electricity",
        "formula": "R = V/I",
        "unit": "Ω",
        "function": lambda voltage, current: ohms_law(
            voltage=voltage,
            current=current
        ),
        "fields": [
            ("voltage", "Voltage", "V"),
            ("current", "Current", "A"),
        ],
    },

    "electrical_power": {
        "name": "Electrical Power",
        "category": "Electricity",
        "formula": "P = VI",
        "unit": "W",
        "function": electrical_power,
        "fields": [
            ("voltage", "Voltage", "V"),
            ("current", "Current", "A"),
        ],
    },

    "electrical_power_resistance": {
        "name": "Electrical Power from Current",
        "category": "Electricity",
        "formula": "P = I²R",
        "unit": "W",
        "function": electrical_power_from_resistance,
        "fields": [
            ("current", "Current", "A"),
            ("resistance", "Resistance", "Ω"),
        ],
    },

    "electrical_power_voltage": {
        "name": "Electrical Power from Voltage",
        "category": "Electricity",
        "formula": "P = V²/R",
        "unit": "W",
        "function": electrical_power_from_voltage,
        "fields": [
            ("voltage", "Voltage", "V"),
            ("resistance", "Resistance", "Ω"),
        ],
    },

    "electrical_energy": {
        "name": "Electrical Energy",
        "category": "Electricity",
        "formula": "E = Pt",
        "unit": "J",
        "function": electrical_energy,
        "fields": [
            ("power_value", "Power", "W"),
            ("time", "Time", "s"),
        ],
    },

    "current_from_charge": {
        "name": "Current from Charge",
        "category": "Charge & Current",
        "formula": "I = Q/t",
        "unit": "A",
        "function": current_from_charge,
        "fields": [
            ("charge", "Charge", "C"),
            ("time", "Time", "s"),
        ],
    },

    "charge_from_current": {
        "name": "Charge from Current",
        "category": "Charge & Current",
        "formula": "Q = It",
        "unit": "C",
        "function": charge_from_current,
        "fields": [
            ("current", "Current", "A"),
            ("time", "Time", "s"),
        ],
    },

    "capacitance": {
        "name": "Capacitance",
        "category": "Capacitance",
        "formula": "C = Q/V",
        "unit": "F",
        "function": capacitance,
        "fields": [
            ("charge", "Charge", "C"),
            ("voltage", "Voltage", "V"),
        ],
    },

    "capacitor_energy": {
        "name": "Capacitor Energy",
        "category": "Capacitance",
        "formula": "E = ½CV²",
        "unit": "J",
        "function": capacitor_energy,
        "fields": [
            ("capacitance_value", "Capacitance", "F"),
            ("voltage", "Voltage", "V"),
        ],
    },

    "kmh_to_ms": {
        "name": "km/h → m/s",
        "category": "Unit Conversions",
        "formula": "m/s = km/h ÷ 3.6",
        "unit": "m/s",
        "function": kmh_to_ms,
        "fields": [
            ("speed_kmh", "Speed", "km/h"),
        ],
    },

    "ms_to_kmh": {
        "name": "m/s → km/h",
        "category": "Unit Conversions",
        "formula": "km/h = m/s × 3.6",
        "unit": "km/h",
        "function": ms_to_kmh,
        "fields": [
            ("speed_ms", "Speed", "m/s"),
        ],
    },

    "celsius_to_kelvin": {
        "name": "Celsius → Kelvin",
        "category": "Unit Conversions",
        "formula": "K = °C + 273.15",
        "unit": "K",
        "function": celsius_to_kelvin,
        "fields": [
            ("celsius", "Temperature", "°C"),
        ],
    },

    "kelvin_to_celsius": {
        "name": "Kelvin → Celsius",
        "category": "Unit Conversions",
        "formula": "°C = K - 273.15",
        "unit": "°C",
        "function": kelvin_to_celsius,
        "fields": [
            ("kelvin", "Temperature", "K"),
        ],
    },

    "celsius_to_fahrenheit": {
        "name": "Celsius → Fahrenheit",
        "category": "Unit Conversions",
        "formula": "°F = °C × 9/5 + 32",
        "unit": "°F",
        "function": celsius_to_fahrenheit,
        "fields": [
            ("celsius", "Temperature", "°C"),
        ],
    },

    "fahrenheit_to_celsius": {
        "name": "Fahrenheit → Celsius",
        "category": "Unit Conversions",
        "formula": "°C = (°F - 32) × 5/9",
        "unit": "°C",
        "function": fahrenheit_to_celsius,
        "fields": [
            ("fahrenheit", "Temperature", "°F"),
        ],
    },

    "resistance_series": {
        "name": "Resistance in Series",
        "category": "Electricity",
        "formula": "R = R₁ + R₂ + ...",
        "unit": "Ω",
        "function": resistance_series,
        "fields": [
            ("resistances", "Resistances", "Ω"),
        ],
    },

    "resistance_parallel": {
        "name": "Resistance in Parallel",
        "category": "Electricity",
        "formula": "1/R = 1/R₁ + 1/R₂ + ...",
        "unit": "Ω",
        "function": resistance_parallel,
        "fields": [
            ("resistances", "Resistances", "Ω"),
        ],
    },
}


# ============================================================
# HTML
# ============================================================

HTML = r"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Kshitij Class 8-12 Study Solver</title>

<style>

* {
    box-sizing: border-box;
}

.answer {
    white-space: pre-wrap;
}

body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: #0b1020;
    color: #eef2ff;
}

.container {
    max-width: 1100px;
    margin: auto;
    padding: 18px;
}

header {
    padding: 10px 0 20px;
}

header h1 {
    margin: 0;
    font-size: 30px;
}

.subtitle {
    color: #9aa7bd;
    margin-top: 7px;
}

.card {
    background: #151c2e;
    border: 1px solid #27324a;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 16px;
}

.section-title {
    font-size: 21px;
    font-weight: bold;
    margin-bottom: 14px;
}

.grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 9px;
}

.grid3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
}

button {
    border: 1px solid #34415d;
    background: #1d2639;
    color: #eef2ff;
    border-radius: 11px;
    padding: 12px;
    cursor: pointer;
    font-size: 15px;
}

button:hover {
    border-color: #668cff;
}

.active {
    background: #3157b7 !important;
    border-color: #6f91ff !important;
}

.tabs {
    display: flex;
    gap: 9px;
    flex-wrap: wrap;
}

.tool {
    display: none;
}

.active-tool {
    display: block;
}

label {
    display: block;
    margin-top: 12px;
    margin-bottom: 6px;
    font-weight: bold;
}

select,
input,
textarea {
    width: 100%;
    background: #0d1322;
    color: #eef2ff;
    border: 1px solid #34415d;
    border-radius: 10px;
    padding: 12px;
    font-size: 15px;
}

textarea {
    min-height: 140px;
    resize: vertical;
}

.primary {
    background: #3157b7;
    color: white;
    border: none;
    font-weight: bold;
    width: 100%;
    margin-top: 12px;
}

.primary:hover {
    background: #416bd0;
}

.answer {
    background: #0d1322;
    border-radius: 10px;
    padding: 15px;
    white-space: pre-wrap;
    overflow-x: auto;
    margin-top: 14px;
    line-height: 1.6;
}

.notice {
    padding: 12px;
    border-radius: 10px;
    background: #10182a;
    color: #b9c7df;
    margin-top: 10px;
}

.small {
    font-size: 13px;
    color: #9aa7bd;
}

.calc-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
}

.calc-card {
    background: #10182a;
    border: 1px solid #293650;
    border-radius: 12px;
    padding: 15px;
}

.calc-card h3 {
    margin-top: 0;
}

.physics-layout {
    display: grid;
    grid-template-columns: 280px 1fr;
    gap: 15px;
}

.physics-menu {
    background: #10182a;
    border-radius: 12px;
    padding: 12px;
    max-height: 650px;
    overflow-y: auto;
}

.physics-menu button {
    width: 100%;
    text-align: left;
    margin-bottom: 7px;
}

.physics-category {
    color: #8da9ff;
    font-size: 13px;
    font-weight: bold;
    padding: 10px 7px 5px;
    text-transform: uppercase;
}

.physics-workspace {
    background: #10182a;
    border-radius: 12px;
    padding: 18px;
}

.field-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
}

.formula-box {
    background: #151f34;
    border-radius: 9px;
    padding: 12px;
    margin: 12px 0;
    color: #c5d4f5;
}

.result-big {
    font-size: 22px;
    font-weight: bold;
    color: #7fa1ff;
}

@media (max-width: 750px) {

    .grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .calc-grid {
        grid-template-columns: 1fr;
    }

    .physics-layout {
        grid-template-columns: 1fr;
    }

    .field-grid {
        grid-template-columns: 1fr;
    }

    header h1 {
        font-size: 24px;
    }

}

</style>

</head>

<body>

<div class="container">

<header>

<h1>KSHITIJ CLASS 8-12 STUDY SOLVER</h1>

<div class="subtitle">
Mathematics • Physics • Chemistry • Calculator
</div>

</header>


<!-- CLASS -->

<div class="card">

<div class="section-title">
1. Select Class
</div>

<div class="grid" id="class_buttons">

{% for cls in classes %}

<button
    type="button"
    class="class-btn {% if cls == 'Class 11' %}active{% endif %}"
    data-value="{{ cls }}"
>
{{ cls }}
</button>

{% endfor %}

</div>

<div class="notice">
Selected:
<strong id="class_label">Class 11</strong>
</div>

</div>


<!-- SUBJECT -->

<div class="card">

<div class="section-title">
2. Choose Subject / Tool
</div>

<div class="tabs">

<button
    type="button"
    class="subject-btn active"
    data-tool="math"
>
Mathematics
</button>

<button
    type="button"
    class="subject-btn"
    data-tool="physics"
>
Physics
</button>

<button
    type="button"
    class="subject-btn"
    data-tool="chemistry"
>
Chemistry
</button>

<button
    type="button"
    class="subject-btn"
    data-tool="calculator"
>
Scientific Calculator
</button>

<button
    type="button"
    class="subject-btn"
    data-tool="ai_assistant"
>
AI Study Assistant
</button>

</div>

</div>


<!-- MATHEMATICS -->

<div id="math" class="card tool active-tool">

<div class="section-title">
Mathematics Solver
</div>

<div class="small" style="margin-bottom:10px;">
Chapter selection is not required. The solver automatically detects the topic/chapter from your question.
</div>

<label>Question</label>

<textarea
    id="math_question"
    placeholder="Example: Solve x^2 - 5*x + 6 = 0"
></textarea>

<button
    type="button"
    class="primary"
    id="solve_math_button"
>
SOLVE
</button>

<div id="math_result" class="answer">
Your solution will appear here.
</div>

</div>


<!-- PHYSICS -->

<div id="physics" class="card tool">

<div class="section-title">
Physics Calculator
</div>

<p class="small">
Choose a physics calculation and enter the required values.
</p>

<div class="physics-layout">

<div class="physics-menu">

<div id="physics_menu">
Loading...
</div>

</div>

<div class="physics-workspace">

<h2 id="physics_title">
Select a calculation
</h2>

<div id="physics_formula" class="formula-box">
Choose a calculation from the left.
</div>

<div id="physics_fields" class="field-grid">
</div>

<button
    type="button"
    class="primary"
    id="calculate_physics_button"
>
CALCULATE
</button>

<div id="physics_result" class="answer">
Your result will appear here.
</div>

</div>

</div>

</div>


<!-- CHEMISTRY -->

<div id="chemistry" class="card tool">

<div class="section-title">
Chemistry Calculator
</div>

<div class="calc-grid">

<div class="calc-card">

<h3>Moles</h3>

<p class="small">
n = mass / molar mass
</p>

<label>Mass (g)</label>

<input id="moles_mass" type="number" step="any">

<label>Molar mass (g/mol)</label>

<input id="moles_molar_mass" type="number" step="any">

<button type="button" class="primary" id="moles_button">
Calculate
</button>

</div>


<div class="calc-card">

<h3>Molarity</h3>

<p class="small">
M = moles / volume
</p>

<label>Moles</label>

<input id="molarity_moles" type="number" step="any">

<label>Volume (L)</label>

<input id="molarity_volume" type="number" step="any">

<button type="button" class="primary" id="molarity_button">
Calculate
</button>

</div>


<div class="calc-card">

<h3>Density</h3>

<p class="small">
Density = mass / volume
</p>

<label>Mass</label>

<input id="chem_density_mass" type="number" step="any">

<label>Volume</label>

<input id="chem_density_volume" type="number" step="any">

<button type="button" class="primary" id="chem_density_button">
Calculate
</button>

</div>

</div>

<div id="chem_result" class="answer">
Your chemistry result will appear here.
</div>

</div>


<!-- AI STUDY ASSISTANT -->
<div id="ai_assistant" class="card tool">
<div class="section-title">AI Study Assistant</div>
<p class="small">Ask a maths question normally, or upload a photo/video of a question on paper. The AI can read the problem and automatically detect the likely topic.</p>
<textarea id="ai_question" rows="4" placeholder="Ask your maths question in your own words..."></textarea>
<div class="small" style="margin-top:10px;">Photo / paper question / short clip</div>
<input id="ai_media" type="file" accept="image/*,application/pdf,video/*">
<button type="button" id="ai_remove_media" style="margin-top:8px;">REMOVE PHOTO / FILE</button>
<div class="small" style="margin-top:8px;">If you upload a page/photo, you can leave the question box empty. The AI will look for every visible maths question.</div>
<button class="primary" type="button" id="ai_solve_button">ASK AI &amp; SOLVE</button>
<div id="ai_status" class="small"></div>
<div id="ai_result" class="answer">Your AI solution will appear here.</div>
</div>


<!-- SCIENTIFIC CALCULATOR -->

<div id="calculator" class="card tool">

<div class="section-title">
Scientific Calculator
</div>

<p class="small">
Examples: 2+3*5, sqrt(25), sin(30), 5^2, pi*2
</p>

<input
    id="calc_expression"
    placeholder="Enter expression"
>

<button
    type="button"
    class="primary"
    id="calculate_expression_button"
>
CALCULATE
</button>

<div id="calc_result" class="answer">
Your result will appear here.
</div>

</div>


<!-- FORMULAS -->

<div class="card">

<div class="section-title">
Quick Formula Reference
</div>

<div class="calc-grid">

<div class="calc-card">

<h3>Physics</h3>

<p>v = d/t</p>
<p>F = ma</p>
<p>KE = ½mv²</p>
<p>PE = mgh</p>
<p>W = Fd</p>
<p>P = W/t</p>
<p>p = mv</p>
<p>V = IR</p>

</div>

<div class="calc-card">

<h3>Chemistry</h3>

<p>n = m/M</p>
<p>M = n/V</p>
<p>Density = m/V</p>

</div>

<div class="calc-card">

<h3>Mathematics</h3>

<p>a² − b² = (a − b)(a + b)</p>
<p>(a + b)² = a² + 2ab + b²</p>
<p>(a − b)² = a² − 2ab + b²</p>
<p>sin²θ + cos²θ = 1</p>

</div>

</div>

</div>


<!-- DEFINITIONS -->

<div class="card">

<div class="section-title">
Quick Definitions
</div>

<div class="calc-grid">

<div class="calc-card">
<h3>Speed</h3>
<p>Distance travelled per unit time.</p>
</div>

<div class="calc-card">
<h3>Force</h3>
<p>An interaction that can change the motion of an object.</p>
</div>

<div class="calc-card">
<h3>Mole</h3>
<p>A unit used to measure amount of substance.</p>
</div>

<div class="calc-card">
<h3>Function</h3>
<p>A relation in which every input has exactly one output.</p>
</div>

</div>

</div>

<div style="text-align:center; margin-top:20px; margin-bottom:10px;">
<a href="/privacy" style="color:#9aa7bd; text-decoration:none; font-size:14px;">Privacy Policy</a>
</div>

</div>


<script>

(function () {

    "use strict";

    let currentClass = "Class 11";
    let currentSubject = "Mathematics";
    let selectedPhysicsCalculation = null;


    /* ========================================================
       CLASS
    ======================================================== */

    function selectClass(className) {

        currentClass = className;

        document.querySelectorAll(".class-btn").forEach(function (button) {

            button.classList.toggle(
                "active",
                button.dataset.value === className
            );

        });

        document.getElementById("class_label").textContent = className;

        updateChapters();
    }


    /* ========================================================
       TOOL
    ======================================================== */

    function showTool(toolName) {

        document.querySelectorAll(".tool").forEach(function (tool) {

            tool.classList.remove("active-tool");

        });

        const selectedTool = document.getElementById(toolName);

        if (selectedTool) {
            selectedTool.classList.add("active-tool");
        }

        document.querySelectorAll(".subject-btn").forEach(function (button) {

            button.classList.toggle(
                "active",
                button.dataset.tool === toolName
            );

        });


        if (toolName === "math") {

            currentSubject = "Mathematics";

            updateChapters();

        }
        else if (toolName === "physics") {

            currentSubject = "Physics";

            loadPhysicsMenu();

        }
        else if (toolName === "chemistry") {

            currentSubject = "Chemistry";

            updateChapters();

        }
        else if (toolName === "calculator") {

            currentSubject = "Mathematics";

        }
        else if (toolName === "ai_assistant") {

            currentSubject = "Mathematics";

        }

    }


    /* ========================================================
       CHAPTERS
    ======================================================== */

    async function updateChapters() {

        const select =
            document.getElementById("chapter_select");

        if (!select) {
            return;
        }

        select.innerHTML = "";

        const loadingOption =
            document.createElement("option");

        loadingOption.textContent = "Loading...";

        select.appendChild(loadingOption);

        try {

            const response = await fetch(
                "/api/chapters?class_name=" +
                encodeURIComponent(currentClass) +
                "&subject=" +
                encodeURIComponent(currentSubject)
            );

            if (!response.ok) {
                throw new Error("Chapter request failed");
            }

            const data = await response.json();

            select.innerHTML = "";

            if (!data.chapters || data.chapters.length === 0) {

                const option =
                    document.createElement("option");

                option.textContent = "No chapters available";

                select.appendChild(option);

                return;
            }


            data.chapters.forEach(function (chapter) {

                const option =
                    document.createElement("option");

                option.value = chapter;
                option.textContent = chapter;

                select.appendChild(option);

            });

        }
        catch (error) {

            select.innerHTML = "";

            const option =
                document.createElement("option");

            option.textContent = "Unable to load chapters";

            select.appendChild(option);

            console.error("Chapter loading error:", error);
        }

    }


    /* ========================================================
       MATHEMATICS
    ======================================================== */

    async function solveMath() {

        const question =
            document.getElementById("math_question").value.trim();

        const result =
            document.getElementById("math_result");


        if (!question) {

            result.textContent =
                "Please enter a mathematics question.";

            return;
        }


        result.textContent = "Solving...";


        try {

            const body =
                "question=" +
                encodeURIComponent(question) +
                "&class_name=" +
                encodeURIComponent(currentClass);


            const response = await fetch(
                "/solve",
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/x-www-form-urlencoded"
                    },
                    body: body
                }
            );


            const data = await response.json();


            if (data.success) {
                if (data.ai) {
                    renderAIResult(data.ai);
                    const aiStatus = document.getElementById("ai_status");
                    if (aiStatus) aiStatus.textContent = "Local solver could not safely handle this, so AI solved it automatically.";
                } else {
                    result.textContent =
                        "Detected Topic / Chapter: " +
                        data.detected_chapter +
                        "\n\n" +
                        data.solution;
                }
            }
            else {

                result.textContent =
                    data.error ||
                    "Unable to solve.";

            }

        }
        catch (error) {

            console.error("Math error:", error);

            result.textContent =
                "Could not connect to the solver.";

        }

    }


    /* ========================================================
       AI STUDY ASSISTANT
       ======================================================== */

    function renderAIResult(payload) {
        const result = document.getElementById("ai_result");
        if (!result) return;
        result.innerHTML = "";

        const questions = Array.isArray(payload.questions) ? payload.questions : [];

        if (payload.overall_message) {
            const message = document.createElement("div");
            message.className = "small";
            message.textContent = payload.overall_message;
            result.appendChild(message);
        }

        if (payload.page_summary) {
            const summary = document.createElement("div");
            summary.className = "small";
            summary.style.marginBottom = "14px";
            summary.textContent = payload.page_summary;
            result.appendChild(summary);
        }

        if (!questions.length) {
            const empty = document.createElement("div");
            empty.textContent = "No reliable mathematics question was detected. Try a clearer photo or type the question.";
            result.appendChild(empty);
            return;
        }

        questions.forEach(function (q, index) {
            const card = document.createElement("div");
            card.style.padding = "14px";
            card.style.marginTop = "12px";
            card.style.border = "1px solid rgba(128,128,128,.25)";
            card.style.borderRadius = "12px";

            const heading = document.createElement("div");
            heading.style.fontWeight = "700";
            heading.style.marginBottom = "8px";
            heading.textContent = "Question " + (index + 1);
            card.appendChild(heading);

            const topic = document.createElement("div");
            topic.className = "small";
            topic.textContent = "Detected topic: " + (q.chapter || "Auto detected");
            card.appendChild(topic);

            if (q.question_read) {
                const read = document.createElement("div");
                read.style.whiteSpace = "pre-wrap";
                read.style.marginTop = "10px";
                read.textContent = "Question: " + q.question_read;
                card.appendChild(read);
            }

            if (q.needs_clarification) {
                const clarification = document.createElement("div");
                clarification.style.marginTop = "10px";
                clarification.style.whiteSpace = "pre-wrap";
                clarification.textContent = "Need a clearer question: " + (q.clarification || "Please upload a clearer image.");
                card.appendChild(clarification);
            }

            if (q.answer) {
                const answer = document.createElement("div");
                answer.style.marginTop = "10px";
                answer.style.whiteSpace = "pre-wrap";
                answer.textContent = q.answer;
                card.appendChild(answer);
            }

            if (Array.isArray(q.steps) && q.steps.length) {
                const stepsTitle = document.createElement("div");
                stepsTitle.style.fontWeight = "700";
                stepsTitle.style.marginTop = "12px";
                stepsTitle.textContent = "Step-by-step solution";
                card.appendChild(stepsTitle);

                const list = document.createElement("ol");
                list.style.marginTop = "6px";
                list.style.paddingLeft = "22px";

                q.steps.forEach(function (step) {
                    const li = document.createElement("li");
                    li.style.whiteSpace = "pre-wrap";
                    li.style.marginBottom = "5px";
                    li.textContent = step;
                    list.appendChild(li);
                });
                card.appendChild(list);
            }

            if (q.final_answer) {
                const finalBox = document.createElement("div");
                finalBox.style.marginTop = "12px";
                finalBox.style.fontWeight = "700";
                finalBox.style.whiteSpace = "pre-wrap";
                finalBox.textContent = "Final answer: " + q.final_answer;
                card.appendChild(finalBox);
            }

            result.appendChild(card);
        });
    }

    async function askAIStudyAssistant() {
        const questionInput = document.getElementById("ai_question");
        const mediaInput = document.getElementById("ai_media");
        const status = document.getElementById("ai_status");
        const result = document.getElementById("ai_result");
        const button = document.getElementById("ai_solve_button");

        const question = questionInput ? questionInput.value.trim() : "";
        const media = mediaInput && mediaInput.files.length ? mediaInput.files[0] : null;

        if (!question && !media) {
            status.textContent = "Type a maths question or upload a photo/PDF/video of the question.";
            return;
        }

        button.disabled = true;
        status.textContent = media
            ? "Reading the uploaded material and finding every visible maths question..."
            : "Understanding the question and detecting the topic...";
        result.textContent = "Working...";

        try {
            let response;

            if (media) {
                const form = new FormData();
                form.append("media", media);
                form.append("question", question);
                form.append("class_name", "Class 11");
                response = await fetch("/api/ai/solve-media", { method: "POST", body: form });
            } else {
                response = await fetch("/api/ai/solve", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ question: question, class_name: "Class 11" })
                });
            }

            // Read the raw response first. This prevents the confusing
            // "Unexpected token '<'" error when a proxy/server returns HTML
            // instead of JSON, and gives a useful error message.
            const rawResponse = await response.text();
            let data;

            try {
                data = JSON.parse(rawResponse);
            } catch (parseError) {
                console.error("AI endpoint returned non-JSON:", {
                    status: response.status,
                    contentType: response.headers.get("content-type"),
                    bodyPreview: rawResponse.slice(0, 1000)
                });

                throw new Error(
                    `AI server returned an invalid response (HTTP ${response.status}). ` +
                    "Please refresh the page and try again."
                );
            }

            if (!response.ok || !data.success) {
                throw new Error(data.error || `The AI server returned HTTP ${response.status}.`);
            }

            status.textContent = "Done — topic detected automatically and question(s) processed.";
            renderAIResult(data.ai || {});
        }
        catch (error) {
            console.error("AI Study Assistant error:", error);
            status.textContent = error.message || "AI request failed.";
            result.textContent = "Try again with a clearer question or image.";
        }
        finally {
            button.disabled = false;
        }
    }

    const aiButton = document.getElementById("ai_solve_button");
    if (aiButton) {
        aiButton.addEventListener("click", askAIStudyAssistant);
    }

    const removeMediaButton = document.getElementById("ai_remove_media");
    if (removeMediaButton) {
        removeMediaButton.addEventListener("click", function () {
            const input = document.getElementById("ai_media");
            const status = document.getElementById("ai_status");
            const result = document.getElementById("ai_result");
            if (input) input.value = "";
            if (status) status.textContent = "Photo/file removed.";
            if (result) result.textContent = "Your AI solution will appear here.";
        });
    }


    async function loadPhysicsMenu() {

        const menu =
            document.getElementById("physics_menu");


        menu.textContent =
            "Loading physics calculations...";


        try {

            const response =
                await fetch("/api/physics/calculations");


            if (!response.ok) {
                throw new Error("Physics list request failed");
            }


            const data =
                await response.json();


            menu.innerHTML = "";


            let currentCategory = "";


            data.calculations.forEach(function (item) {

                if (item.category !== currentCategory) {

                    currentCategory = item.category;


                    const category =
                        document.createElement("div");

                    category.className =
                        "physics-category";

                    category.textContent =
                        currentCategory;

                    menu.appendChild(category);

                }


                const button =
                    document.createElement("button");

                button.type = "button";

                button.textContent =
                    item.name;


                button.addEventListener(
                    "click",
                    function () {

                        selectPhysicsCalculation(item.id);

                    }
                );


                menu.appendChild(button);

            });

        }
        catch (error) {

            console.error("Physics menu error:", error);

            menu.textContent =
                "Unable to load physics calculations.";

        }

    }


    /* ========================================================
       PHYSICS SELECTION
    ======================================================== */

    async function selectPhysicsCalculation(id) {

        selectedPhysicsCalculation = id;


        try {

            const response =
                await fetch(
                    "/api/physics/calculation/" +
                    encodeURIComponent(id)
                );


            const data =
                await response.json();


            if (!data.success) {
                return;
            }


            document.getElementById(
                "physics_title"
            ).textContent = data.name;


            document.getElementById(
                "physics_formula"
            ).textContent =
                data.formula +
                " | Unit: " +
                data.unit;


            const fields =
                document.getElementById(
                    "physics_fields"
                );


            fields.innerHTML = "";


            data.fields.forEach(function (field) {

                const wrapper =
                    document.createElement("div");


                const label =
                    document.createElement("label");

                label.textContent =
                    field.label +
                    " (" +
                    field.unit +
                    ")";


                const input =
                    document.createElement("input");

                input.type = "number";
                input.step = "any";

                input.id =
                    "physics_" +
                    field.name;


                if (
                    data.defaults &&
                    data.defaults[field.name] !== undefined
                ) {

                    input.value =
                        data.defaults[field.name];

                }


                wrapper.appendChild(label);
                wrapper.appendChild(input);

                fields.appendChild(wrapper);

            });


            document.getElementById(
                "physics_result"
            ).textContent =
                "Enter the values and press CALCULATE.";

        }
        catch (error) {

            console.error(
                "Physics selection error:",
                error
            );

            document.getElementById(
                "physics_result"
            ).textContent =
                "Unable to load this calculation.";

        }

    }


    /* ========================================================
       PHYSICS CALCULATE
    ======================================================== */

    async function calculatePhysics() {

        const result =
            document.getElementById(
                "physics_result"
            );


        if (!selectedPhysicsCalculation) {

            result.textContent =
                "Please select a physics calculation.";

            return;
        }


        try {

            const calculationResponse =
                await fetch(
                    "/api/physics/calculation/" +
                    encodeURIComponent(
                        selectedPhysicsCalculation
                    )
                );


            const calculation =
                await calculationResponse.json();


            if (!calculation.success) {

                result.textContent =
                    "Unable to load calculation.";

                return;
            }


            const values = {};


            for (
                const field of calculation.fields
            ) {

                const input =
                    document.getElementById(
                        "physics_" +
                        field.name
                    );


                if (!input) {
                    continue;
                }


                if (
                    input.value === "" &&
                    calculation.defaults &&
                    calculation.defaults[field.name] !== undefined
                ) {

                    values[field.name] =
                        calculation.defaults[field.name];

                }
                else {

                    values[field.name] =
                        input.value;

                }

            }


            result.textContent =
                "Calculating...";


            const response =
                await fetch(
                    "/api/physics/calculate",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type":
                                "application/json"
                        },
                        body: JSON.stringify({
                            calculation:
                                selectedPhysicsCalculation,
                            values:
                                values
                        })
                    }
                );


            const data =
                await response.json();


            if (!data.success) {

                result.textContent =
                    data.error ||
                    "Calculation failed.";

                return;
            }


            result.innerHTML =
                "<div class='result-big'>" +
                escapeHtml(data.result) +
                " " +
                escapeHtml(data.unit) +
                "</div>" +
                "<br>" +
                "Formula: " +
                escapeHtml(data.formula);

        }
        catch (error) {

            console.error(
                "Physics calculation error:",
                error
            );

            result.textContent =
                "Could not connect to the physics engine.";

        }

    }


    /* ========================================================
       CHEMISTRY
    ======================================================== */

    function chemMoles() {

        const mass =
            parseFloat(
                document.getElementById(
                    "moles_mass"
                ).value
            );


        const molarMass =
            parseFloat(
                document.getElementById(
                    "moles_molar_mass"
                ).value
            );


        if (
            !Number.isFinite(mass) ||
            !Number.isFinite(molarMass) ||
            molarMass === 0
        ) {

            document.getElementById(
                "chem_result"
            ).textContent =
                "Enter valid values.";

            return;
        }


        document.getElementById(
            "chem_result"
        ).textContent =
            "Moles = " +
            (mass / molarMass) +
            " mol";

    }


    function chemMolarity() {

        const moles =
            parseFloat(
                document.getElementById(
                    "molarity_moles"
                ).value
            );


        const volume =
            parseFloat(
                document.getElementById(
                    "molarity_volume"
                ).value
            );


        if (
            !Number.isFinite(moles) ||
            !Number.isFinite(volume) ||
            volume === 0
        ) {

            document.getElementById(
                "chem_result"
            ).textContent =
                "Enter valid values.";

            return;
        }


        document.getElementById(
            "chem_result"
        ).textContent =
            "Molarity = " +
            (moles / volume) +
            " mol/L";

    }


    function chemDensity() {

        const mass =
            parseFloat(
                document.getElementById(
                    "chem_density_mass"
                ).value
            );


        const volume =
            parseFloat(
                document.getElementById(
                    "chem_density_volume"
                ).value
            );


        if (
            !Number.isFinite(mass) ||
            !Number.isFinite(volume) ||
            volume === 0
        ) {

            document.getElementById(
                "chem_result"
            ).textContent =
                "Enter valid values.";

            return;
        }


        document.getElementById(
            "chem_result"
        ).textContent =
            "Density = " +
            (mass / volume);

    }


    /* ========================================================
       SCIENTIFIC CALCULATOR
    ======================================================== */

    async function calculateExpression() {

        const expression =
            document.getElementById(
                "calc_expression"
            ).value.trim();


        const result =
            document.getElementById(
                "calc_result"
            );


        if (!expression) {

            result.textContent =
                "Please enter an expression.";

            return;
        }


        result.textContent =
            "Calculating...";


        try {

            const response =
                await fetch(
                    "/api/calculate",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type":
                                "application/json"
                        },
                        body: JSON.stringify({
                            expression:
                                expression
                        })
                    }
                );


            const data =
                await response.json();


            if (data.success) {

                result.textContent =
                    data.result;

            }
            else {

                result.textContent =
                    data.error ||
                    "Calculation failed.";

            }

        }
        catch (error) {

            console.error(
                "Calculator error:",
                error
            );

            result.textContent =
                "Calculator error.";

        }

    }


    /* ========================================================
       ESCAPE HTML
    ======================================================== */

    function escapeHtml(value) {

        return String(value)
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");

    }


    /* ========================================================
       EVENT LISTENERS
    ======================================================== */

    document.querySelectorAll(".class-btn").forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    selectClass(
                        button.dataset.value
                    );

                }
            );

        }
    );


    document.querySelectorAll(".subject-btn").forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    showTool(
                        button.dataset.tool
                    );

                }
            );

        }
    );


    document.getElementById(
        "solve_math_button"
    ).addEventListener(
        "click",
        solveMath
    );


    document.getElementById(
        "calculate_physics_button"
    ).addEventListener(
        "click",
        calculatePhysics
    );


    document.getElementById(
        "moles_button"
    ).addEventListener(
        "click",
        chemMoles
    );


    document.getElementById(
        "molarity_button"
    ).addEventListener(
        "click",
        chemMolarity
    );


    document.getElementById(
        "chem_density_button"
    ).addEventListener(
        "click",
        chemDensity
    );


    document.getElementById(
        "calculate_expression_button"
    ).addEventListener(
        "click",
        calculateExpression
    );


    /* ========================================================
       START
    ======================================================== */

    updateChapters();

})();

</script>

</body>
</html>
"""




# ============================================================
# PRIVACY POLICY
# ============================================================

PRIVACY_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Privacy Policy - Kshitij Class 8-12 Study Solver</title>
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: #0b1020;
    color: #eef2ff;
    line-height: 1.7;
}
.container {
    max-width: 900px;
    margin: auto;
    padding: 20px;
}
.card {
    background: #151c2e;
    border: 1px solid #27324a;
    border-radius: 16px;
    padding: 24px;
}
h1 { margin-top: 0; }
h2 { margin-top: 28px; }
p { color: #d7deec; }
.updated { color: #9aa7bd; font-size: 14px; }
a { color: #8da9ff; }
.back {
    display: inline-block;
    margin-top: 20px;
    padding: 10px 15px;
    background: #1d2639;
    border-radius: 9px;
    text-decoration: none;
}
</style>
</head>
<body>
<div class="container">
<div class="card">

<h1>Privacy Policy</h1>

<p class="updated">Last updated: September 25, 2026</p>

<p>
Kshitij Class 8-12 Study Solver is an educational web application
providing mathematics solving, physics calculations, chemistry
calculations, and a scientific calculator.
</p>

<h2>1. Information We Collect</h2>

<p>
The application does not require users to create an account and
does not intentionally ask users to provide personal information
such as their name, phone number, home address, or password in
order to use the study tools.
</p>

<p>
Users may enter questions, mathematical expressions, or values into
the study tools. These inputs are processed to provide the requested
calculation or solution.

The AI Study Assistant also allows users to submit questions and, when
the feature is used, photos or videos containing mathematics problems.
These inputs are sent to the configured AI service so it can read,
understand, classify, and explain the mathematics problem. Users should
avoid uploading documents or images containing personal or sensitive
information.
</p>

<h2>2. How Information Is Used</h2>

<p>
Information entered into the study tools is used to calculate or
process the requested result and display that result to the user.
</p>

<h2>3. Personal Information</h2>

<p>
The application does not intentionally request personal information
for an account or user profile. Users should avoid entering sensitive
personal information into questions or calculator fields.
</p>

<h2>4. Data Sharing</h2>

<p>
We do not intentionally sell users' personal information. The
application itself does not provide a feature for creating or
sharing user profiles.
</p>

<p>
The application is hosted using third-party internet infrastructure.
Technical information such as requests and server logs may be
processed by the hosting infrastructure provider as necessary to
operate, secure, and maintain the service.
</p>

<h2>5. Students and Children</h2>

<p>
This application is designed for educational use by students.
The application does not intentionally request personal information
from children or students.
</p>

<h2>6. Third-Party Services</h2>

<p>
The application uses third-party hosting infrastructure to make the
web application available online. Those providers may process
technical information according to their own applicable privacy
policies and terms.
</p>

<p>
When the AI Study Assistant is used, submitted text, images, or videos
may be processed by the configured AI provider (currently Google Gemini)
to understand the question and generate a response. The application does
not intentionally use these uploads to create a personal profile. The
AI provider's own privacy policy, data handling practices, and terms also
apply to that processing.
</p>

<h2>7. Data Security</h2>

<p>
Reasonable measures are used to operate the application securely.
However, no internet service can guarantee absolute security.
</p>

<h2>8. Data Retention</h2>

<p>
The application does not intentionally maintain a personal user
account or personal profile. Technical server information may be
retained by hosting infrastructure providers according to their
operational, security, and legal requirements.
</p>

<h2>9. Changes to This Privacy Policy</h2>

<p>
This Privacy Policy may be updated when the application or its data
practices change. The latest version will be published on this page.
</p>

<h2>10. Contact</h2>

<p>
For privacy questions, users may contact the developer using the
developer contact information shown on the application's Google Play
listing.
</p>

<a class="back" href="/">← Back to Study Solver</a>

</div>
</div>
</body>
</html>
"""


@app.route("/privacy")
def privacy():
    return render_template_string(PRIVACY_HTML)


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return render_template_string(
        HTML,
        classes=CLASSES
    )


# ============================================================
# MATHEMATICS SOLVER
# ============================================================

@app.route("/api/ai/solve", methods=["POST"])
def api_ai_solve():
    try:
        data = request.get_json(silent=True) or {}
        question = str(data.get("question", "")).strip()
        class_name = str(data.get("class_name", "Class 11")).strip() or "Class 11"
        if not question:
            return jsonify({"success": False, "error": "Please enter a maths question."}), 400
        chapters = get_chapters(class_name, "Mathematics")
        ai = solve_with_ai(question, class_name, chapters)
        return jsonify({"success": True, "ai": ai})
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 500


@app.route("/api/ai/solve-media", methods=["POST"])
def api_ai_solve_media():
    try:
        import traceback

        print("=== AI MEDIA REQUEST START ===", flush=True)

        media = request.files.get("media")
        question = request.form.get("question", "").strip()
        class_name = request.form.get("class_name", "Class 11").strip() or "Class 11"

        print(f"AI media received: {media is not None}", flush=True)
        print(f"Question provided: {bool(question)}", flush=True)
        print(f"Class: {class_name}", flush=True)

        if media is None:
            print("ERROR: No media file was uploaded.", flush=True)
            return jsonify({
                "success": False,
                "error": "Please upload a photo, PDF, or video."
            }), 400

        print(f"Media filename: {media.filename}", flush=True)
        print(f"Media type: {media.mimetype}", flush=True)

        chapters = get_chapters(class_name, "Mathematics")
        print(f"Chapters loaded: {len(chapters)}", flush=True)
        print("Calling solve_with_media()...", flush=True)

        ai = solve_with_media(media, question, class_name, chapters)

        print("solve_with_media() completed successfully.", flush=True)
        print("=== AI MEDIA REQUEST SUCCESS ===", flush=True)

        return jsonify({"success": True, "ai": ai})

    except Exception as error:
        import traceback

        print("=== AI MEDIA REQUEST FAILED ===", flush=True)
        print(f"ERROR TYPE: {type(error).__name__}", flush=True)
        print(f"ERROR MESSAGE: {error}", flush=True)
        traceback.print_exc()
        print("=== END AI MEDIA ERROR ===", flush=True)

        return jsonify({
            "success": False,
            "error": "AI media processing failed: " + str(error)
        }), 500


@app.route("/solve", methods=["POST"])
def solve_question():
    """Main automatic mathematics solver. Local engines run first; AI is fallback."""
    question = request.form.get("question", "").strip()
    class_name = request.form.get("class_name", "Class 11").strip() or "Class 11"

    if not question:
        return jsonify({"success": False, "error": "Please enter a question."})

    # 1) Unified SymPy engine: equations, expressions, calculus, common word problems.
    if unified_math_solve is not None:
        try:
            result = unified_math_solve(question)
            if result.get("success"):
                steps = result.get("steps", [])
                solution_lines = [
                    "Step-by-step solution:",
                    *[f"{i}. {step}" for i, step in enumerate(steps, 1)],
                    "",
                    f"Final Answer: {result.get('final_answer', '')}",
                ]
                if result.get("decimal_answer"):
                    solution_lines.append(f"Decimal form: {result['decimal_answer']}")
                if result.get("verified"):
                    solution_lines.append("Verification: ✓")
                return jsonify({
                    "success": True,
                    "class": class_name,
                    "selected_chapter": result.get("topic", "Auto detected"),
                    "detected_chapter": result.get("topic", "Auto detected"),
                    "solution": "\n".join(solution_lines),
                    "source": "local-unified-engine",
                })
        except Exception:
            pass

    # 2) Existing school curriculum engine (Classes 8-10).
    if solve_school_math is not None:
        try:
            solution = solve_school_math(question, "Auto Detect")
            if solution and "could not" not in str(solution).lower() and "unable to" not in str(solution).lower():
                detected = "Auto detected"
                if unified_math_solve is not None:
                    try:
                        detected = unified_math_solve(question).get("topic", detected)
                    except Exception:
                        pass
                return jsonify({
                    "success": True,
                    "class": class_name,
                    "selected_chapter": detected,
                    "detected_chapter": detected,
                    "solution": str(solution),
                    "source": "school-math-engine",
                })
        except Exception:
            pass

    # 3) Legacy solver remains as compatibility fallback.
    try:
        detected = detect_chapter(question)
        solution = solve(question, detected)
        if solution:
            return jsonify({
                "success": True,
                "class": class_name,
                "selected_chapter": detected,
                "detected_chapter": detected,
                "solution": str(solution),
                "source": "legacy-engine",
            })
    except Exception:
        pass

    # 4) AI fallback for natural-language/advanced word problems.
    try:
        chapters = get_chapters(class_name, "Mathematics")
        ai = solve_with_ai(question, class_name, chapters)
        return jsonify({
            "success": True,
            "class": class_name,
            "selected_chapter": "AI auto detected",
            "detected_chapter": (ai.get("questions") or [{}])[0].get("chapter", "AI auto detected"),
            "solution": "AI Study Assistant result",
            "ai": ai,
            "source": "gemini-ai",
        })
    except Exception as error:
        return jsonify({
            "success": False,
            "error": "The question could not be solved automatically. " + str(error),
        })


# ============================================================
# CHAPTER API
# ============================================================

@app.route("/api/chapters")
def api_chapters():

    class_name = request.args.get(
        "class_name",
        "Class 11"
    )

    subject = request.args.get(
        "subject",
        "Mathematics"
    )


    try:

        chapters = get_chapters(
            class_name,
            subject
        )

    except Exception:

        chapters = []


    return jsonify({

        "success": True,

        "class": class_name,

        "subject": subject,

        "chapters": chapters

    })


# ============================================================
# SCIENTIFIC CALCULATOR API
# ============================================================

@app.route(
    "/api/calculate",
    methods=["POST"]
)
def api_calculate():

    from calculator import calculate


    try:

        data = request.get_json(
            silent=True
        ) or {}


        expression = data.get(
            "expression",
            ""
        )


        if not expression:

            return jsonify({

                "success": False,

                "error":
                    "Enter a calculator expression."

            })


        result = calculate(
            expression
        )


        return jsonify({

            "success": True,

            "result": str(result)

        })


    except Exception as error:

        return jsonify({

            "success": False,

            "error": str(error)

        })


# ============================================================
# PHYSICS LIST API
# ============================================================

@app.route(
    "/api/physics/calculations"
)
def physics_calculations():

    calculations = []


    for calculation_id, data in PHYSICS_CALCULATIONS.items():

        calculations.append({

            "id": calculation_id,

            "name": data["name"],

            "category": data["category"],

            "formula": data["formula"],

            "unit": data["unit"]

        })


    return jsonify({

        "success": True,

        "calculations": calculations

    })


# ============================================================
# PHYSICS INFORMATION API
# ============================================================

@app.route(
    "/api/physics/calculation/<calculation_id>"
)
def physics_calculation_info(calculation_id):

    data = PHYSICS_CALCULATIONS.get(
        calculation_id
    )


    if data is None:

        return jsonify({

            "success": False,

            "error":
                "Physics calculation not found."

        }), 404


    fields = []


    for name, label, unit in data["fields"]:

        fields.append({

            "name": name,

            "label": label,

            "unit": unit

        })


    return jsonify({

        "success": True,

        "id": calculation_id,

        "name": data["name"],

        "category": data["category"],

        "formula": data["formula"],

        "unit": data["unit"],

        "fields": fields,

        "defaults":
            data.get(
                "defaults",
                {}
            )

    })


# ============================================================
# PHYSICS CALCULATE API
# ============================================================

@app.route(
    "/api/physics/calculate",
    methods=["POST"]
)
def api_physics_calculate():

    try:

        data = request.get_json(
            silent=True
        ) or {}


        calculation_id = data.get(
            "calculation"
        )


        values = data.get(
            "values",
            {}
        )


        if not calculation_id:

            return jsonify({

                "success": False,

                "error":
                    "Please select a calculation."

            })


        calculation = PHYSICS_CALCULATIONS.get(
            calculation_id
        )


        if calculation is None:

            return jsonify({

                "success": False,

                "error":
                    "Unknown physics calculation."

            })


        final_values = {}


        for name, label, unit in calculation["fields"]:

            value = values.get(
                name
            )


            if value is None or value == "":

                defaults = calculation.get(
                    "defaults",
                    {}
                )


                if name in defaults:

                    value = defaults[name]

                else:

                    return jsonify({

                        "success": False,

                        "error":
                            "Please enter " +
                            label +
                            "."

                    })


            try:

                final_values[name] = float(value)

            except (TypeError, ValueError):

                return jsonify({

                    "success": False,

                    "error":
                        "Invalid value for " +
                        label +
                        "."

                })


        result = calculation["function"](
            **final_values
        )


        formatted_result = format_number(
            result
        )


        return jsonify({

            "success": True,

            "result":
                formatted_result,

            "unit":
                calculation["unit"],

            "formula":
                calculation["formula"]

        })


    except ZeroDivisionError:

        return jsonify({

            "success": False,

            "error":
                "Cannot divide by zero."

        })


    except ValueError as error:

        return jsonify({

            "success": False,

            "error":
                str(error)

        })


    except Exception as error:

        return jsonify({

            "success": False,

            "error":
                "Physics calculation failed: " +
                str(error)

        })


# ============================================================
# FORMAT NUMBER
# ============================================================

def format_number(value):

    value = float(value)


    if abs(value) < 1e-12:

        value = 0.0


    if value.is_integer():

        return str(
            int(value)
        )


    return f"{value:.10g}"


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )