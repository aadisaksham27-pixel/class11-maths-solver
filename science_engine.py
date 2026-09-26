# ============================================================
# KSHITIJ SCIENCE ENGINE
# Classes 8-10
# Physics + Chemistry + Biology
# ============================================================

import math
import re
from collections import Counter


# ============================================================
# BASIC HELPERS
# ============================================================

def get_numbers(text):
    text = text.replace(",", "")
    found = re.findall(
        r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)",
        text
    )
    return [float(x) for x in found]


def fmt(value):
    if isinstance(value, float):
        if abs(value - round(value)) < 1e-10:
            return str(int(round(value)))
        return f"{value:.8g}"
    return str(value)


def result(title, formula, steps, answer):
    lines = [
        f"### {title}",
        "",
        f"**Formula:** {formula}",
        "",
        "**Steps:**"
    ]

    for i, step in enumerate(steps, 1):
        lines.append(f"{i}. {step}")

    lines.extend([
        "",
        f"**Answer:** {answer}"
    ])

    return "\n".join(lines)


# ============================================================
# PHYSICS — MOTION
# ============================================================

def solve_motion(question):

    q = question.lower()
    nums = get_numbers(question)

    if not nums:
        return None

    if not any(word in q for word in [
        "speed",
        "velocity",
        "distance",
        "displacement",
        "acceleration",
        "motion"
    ]):
        return None

    # speed = distance / time
    if "speed" in q and len(nums) >= 2:

        distance, time = nums[:2]

        if time == 0:
            raise ValueError("Time cannot be zero.")

        speed = distance / time

        return result(
            "Speed",
            "Speed = Distance / Time",
            [
                f"Distance = {distance}",
                f"Time = {time}",
                f"Speed = {distance} / {time}"
            ],
            fmt(speed)
        )

    # velocity = displacement / time
    if "velocity" in q and len(nums) >= 2:

        displacement, time = nums[:2]

        if time == 0:
            raise ValueError("Time cannot be zero.")

        velocity = displacement / time

        return result(
            "Velocity",
            "Velocity = Displacement / Time",
            [
                f"Displacement = {displacement}",
                f"Time = {time}",
                f"Velocity = {displacement} / {time}"
            ],
            fmt(velocity)
        )

    # acceleration = change in velocity / time
    if "acceleration" in q and len(nums) >= 3:

        u, v, t = nums[:3]

        if t == 0:
            raise ValueError("Time cannot be zero.")

        acceleration = (v - u) / t

        return result(
            "Acceleration",
            "a = (v − u) / t",
            [
                f"Initial velocity u = {u}",
                f"Final velocity v = {v}",
                f"Time t = {t}",
                f"a = ({v} − {u}) / {t}"
            ],
            fmt(acceleration)
        )

    return None


# ============================================================
# MOTION EQUATIONS
# ============================================================

def solve_motion_equations(question):

    q = question.lower()
    nums = get_numbers(question)

    if len(nums) < 3:
        return None

    if not any(word in q for word in [
        "equation of motion",
        "motion equation",
        "final velocity",
        "distance travelled"
    ]):
        return None

    u, a, t = nums[:3]

    if "final velocity" in q:
        v = u + a * t

        return result(
            "Equation of Motion",
            "v = u + at",
            [
                f"u = {u}",
                f"a = {a}",
                f"t = {t}",
                f"v = {u} + ({a})({t})"
            ],
            fmt(v)
        )

    s = u * t + 0.5 * a * t ** 2

    return result(
        "Equation of Motion",
        "s = ut + ½at²",
        [
            f"u = {u}",
            f"a = {a}",
            f"t = {t}",
            f"s = ({u})({t}) + ½({a})({t})²"
        ],
        fmt(s)
    )


# ============================================================
# FORCE
# ============================================================

def solve_force(question):

    q = question.lower()
    nums = get_numbers(question)

    if len(nums) < 2:
        return None

    if not any(word in q for word in [
        "force",
        "newton"
    ]):
        return None

    mass, acceleration = nums[:2]

    force = mass * acceleration

    return result(
        "Force",
        "F = ma",
        [
            f"Mass = {mass}",
            f"Acceleration = {acceleration}",
            f"F = {mass} × {acceleration}"
        ],
        f"{fmt(force)} N"
    )


# ============================================================
# WEIGHT
# ============================================================

def solve_weight(question):

    q = question.lower()
    nums = get_numbers(question)

    if "weight" not in q or not nums:
        return None

    mass = nums[0]

    g = 9.8

    if len(nums) >= 2:
        g = nums[1]

    weight = mass * g

    return result(
        "Weight",
        "W = mg",
        [
            f"Mass = {mass} kg",
            f"g = {g} m/s²",
            f"W = {mass} × {g}"
        ],
        f"{fmt(weight)} N"
    )


# ============================================================
# WORK
# ============================================================

def solve_work(question):

    q = question.lower()
    nums = get_numbers(question)

    if "work" not in q or len(nums) < 2:
        return None

    force, distance = nums[:2]

    work = force * distance

    return result(
        "Work",
        "W = F × s",
        [
            f"Force = {force} N",
            f"Distance = {distance} m",
            f"W = {force} × {distance}"
        ],
        f"{fmt(work)} J"
    )


# ============================================================
# ENERGY
# ============================================================

def solve_energy(question):

    q = question.lower()
    nums = get_numbers(question)

    if not nums:
        return None

    if "kinetic energy" in q:

        if len(nums) < 2:
            return None

        mass, velocity = nums[:2]

        ke = 0.5 * mass * velocity ** 2

        return result(
            "Kinetic Energy",
            "KE = ½mv²",
            [
                f"m = {mass}",
                f"v = {velocity}",
                f"KE = ½ × {mass} × {velocity}²"
            ],
            f"{fmt(ke)} J"
        )

    if "potential energy" in q:

        if len(nums) < 2:
            return None

        mass, height = nums[:2]

        g = nums[2] if len(nums) >= 3 else 9.8

        pe = mass * g * height

        return result(
            "Potential Energy",
            "PE = mgh",
            [
                f"m = {mass}",
                f"g = {g}",
                f"h = {height}"
            ],
            f"{fmt(pe)} J"
        )

    return None


# ============================================================
# POWER
# ============================================================

def solve_power(question):

    q = question.lower()
    nums = get_numbers(question)

    if "power" not in q or len(nums) < 2:
        return None

    work, time = nums[:2]

    if time == 0:
        raise ValueError("Time cannot be zero.")

    power = work / time

    return result(
        "Power",
        "P = W / t",
        [
            f"Work = {work} J",
            f"Time = {time} s",
            f"P = {work} / {time}"
        ],
        f"{fmt(power)} W"
    )


# ============================================================
# PRESSURE
# ============================================================

def solve_pressure(question):

    q = question.lower()
    nums = get_numbers(question)

    if "pressure" not in q or len(nums) < 2:
        return None

    force, area = nums[:2]

    if area == 0:
        raise ValueError("Area cannot be zero.")

    pressure = force / area

    return result(
        "Pressure",
        "P = F / A",
        [
            f"Force = {force} N",
            f"Area = {area} m²",
            f"P = {force} / {area}"
        ],
        f"{fmt(pressure)} Pa"
    )


# ============================================================
# DENSITY
# ============================================================

def solve_density(question):

    q = question.lower()
    nums = get_numbers(question)

    if "density" not in q or len(nums) < 2:
        return None

    mass, volume = nums[:2]

    if volume == 0:
        raise ValueError("Volume cannot be zero.")

    density = mass / volume

    return result(
        "Density",
        "ρ = m / V",
        [
            f"Mass = {mass}",
            f"Volume = {volume}",
            f"ρ = {mass} / {volume}"
        ],
        f"{fmt(density)} kg/m³"
    )


# ============================================================
# HEAT
# ============================================================

def solve_heat(question):

    q = question.lower()
    nums = get_numbers(question)

    if not any(word in q for word in [
        "heat",
        "specific heat",
        "temperature"
    ]):
        return None

    if len(nums) < 3:
        return None

    mass, specific_heat, temperature_change = nums[:3]

    heat = (
        mass
        * specific_heat
        * temperature_change
    )

    return result(
        "Heat Energy",
        "Q = mcΔT",
        [
            f"m = {mass}",
            f"c = {specific_heat}",
            f"ΔT = {temperature_change}",
            f"Q = {mass} × {specific_heat} × {temperature_change}"
        ],
        f"{fmt(heat)} J"
    )


# ============================================================
# ELECTRICITY
# ============================================================

def solve_electricity(question):

    q = question.lower()
    nums = get_numbers(question)

    if not any(word in q for word in [
        "ohm",
        "voltage",
        "current",
        "resistance",
        "electricity"
    ]):
        return None

    if len(nums) < 2:
        return None

    a, b = nums[:2]

    # V = IR
    if "voltage" in q or "potential difference" in q:

        current = a
        resistance = b

        voltage = current * resistance

        return result(
            "Ohm's Law",
            "V = IR",
            [
                f"I = {current} A",
                f"R = {resistance} Ω",
                f"V = {current} × {resistance}"
            ],
            f"{fmt(voltage)} V"
        )

    # I = V/R
    if "current" in q:

        voltage = a
        resistance = b

        if resistance == 0:
            raise ValueError(
                "Resistance cannot be zero."
            )

        current = voltage / resistance

        return result(
            "Electric Current",
            "I = V / R",
            [
                f"V = {voltage} V",
                f"R = {resistance} Ω",
                f"I = {voltage} / {resistance}"
            ],
            f"{fmt(current)} A"
        )

    # R = V/I
    if "resistance" in q:

        voltage = a
        current = b

        if current == 0:
            raise ValueError(
                "Current cannot be zero."
            )

        resistance = voltage / current

        return result(
            "Resistance",
            "R = V / I",
            [
                f"V = {voltage} V",
                f"I = {current} A"
            ],
            f"{fmt(resistance)} Ω"
        )

    return None


# ============================================================
# ELECTRICAL POWER
# ============================================================

def solve_electrical_power(question):

    q = question.lower()
    nums = get_numbers(question)

    if (
        "electrical power" not in q
        and "electric power" not in q
    ):
        return None

    if len(nums) < 2:
        return None

    voltage, current = nums[:2]

    power = voltage * current

    return result(
        "Electrical Power",
        "P = VI",
        [
            f"V = {voltage} V",
            f"I = {current} A",
            f"P = {voltage} × {current}"
        ],
        f"{fmt(power)} W"
    )


# ============================================================
# SOUND
# ============================================================

def solve_sound(question):

    q = question.lower()
    nums = get_numbers(question)

    if not any(word in q for word in [
        "sound",
        "frequency",
        "wavelength"
    ]):
        return None

    if len(nums) < 2:
        return None

    speed, frequency = nums[:2]

    if frequency == 0:
        raise ValueError(
            "Frequency cannot be zero."
        )

    wavelength = speed / frequency

    return result(
        "Sound Wave",
        "v = fλ",
        [
            f"v = {speed} m/s",
            f"f = {frequency} Hz",
            f"λ = v/f"
        ],
        f"{fmt(wavelength)} m"
    )


# ============================================================
# LIGHT — MIRROR
# ============================================================

def solve_mirror(question):

    q = question.lower()
    nums = get_numbers(question)

    if "mirror" not in q:
        return None

    if len(nums) < 2:
        return None

    u, v = nums[:2]

    if u == 0 or v == 0:
        raise ValueError(
            "Object and image distances cannot be zero."
        )

    f = (u * v) / (u + v)

    return result(
        "Mirror Formula",
        "1/f = 1/u + 1/v",
        [
            f"u = {u}",
            f"v = {v}",
            f"f = uv/(u+v)"
        ],
        fmt(f)
    )


# ============================================================
# LIGHT — LENS
# ============================================================

def solve_lens(question):

    q = question.lower()
    nums = get_numbers(question)

    if "lens" not in q:
        return None

    if len(nums) < 2:
        return None

    u, v = nums[:2]

    if u == 0 or v == 0:
        raise ValueError(
            "Object and image distances cannot be zero."
        )

    f = (u * v) / (u + v)

    return result(
        "Lens Formula",
        "1/f = 1/v − 1/u",
        [
            f"u = {u}",
            f"v = {v}",
            "Using the supplied magnitudes:",
            f"f = uv/(u+v)"
        ],
        fmt(f)
    )


# ============================================================
# CHEMISTRY — MOLE
# ============================================================

def solve_mole(question):

    q = question.lower()
    nums = get_numbers(question)

    if not any(word in q for word in [
        "mole",
        "moles",
        "molar mass"
    ]):
        return None

    if len(nums) < 2:
        return None

    mass, molar_mass = nums[:2]

    if molar_mass == 0:
        raise ValueError(
            "Molar mass cannot be zero."
        )

    moles = mass / molar_mass

    return result(
        "Moles",
        "n = m/M",
        [
            f"Mass = {mass} g",
            f"Molar mass = {molar_mass} g/mol",
            f"n = {mass}/{molar_mass}"
        ],
        f"{fmt(moles)} mol"
    )


# ============================================================
# CHEMISTRY — MOLECULAR MASS
# ============================================================

ATOMIC_MASSES = {
    "H": 1.008,
    "C": 12.011,
    "N": 14.007,
    "O": 15.999,
    "Na": 22.990,
    "Mg": 24.305,
    "Al": 26.982,
    "Cl": 35.45,
    "K": 39.098,
    "Ca": 40.078,
    "Fe": 55.845,
    "Cu": 63.546,
    "Zn": 65.38,
    "Ag": 107.868,
    "I": 126.904,
    "S": 32.06,
    "P": 30.974,
}


def molecular_mass(formula):

    tokens = re.findall(
        r"([A-Z][a-z]?)(\d*)",
        formula
    )

    if not tokens:
        return None

    total = 0

    for element, count in tokens:

        if element not in ATOMIC_MASSES:
            return None

        multiplier = int(count) if count else 1

        total += (
            ATOMIC_MASSES[element]
            * multiplier
        )

    return total


def solve_molecular_mass(question):

    q = question.lower()

    if not any(word in q for word in [
        "molecular mass",
        "molar mass"
    ]):
        return None

    # Find simple chemical formula.
    match = re.search(
        r"\b(?:H|C|N|O|Na|Mg|Al|Cl|K|Ca|Fe|Cu|Zn|Ag|I|S|P)"
        r"(?:[a-z]?\d*)+\b",
        question
    )

    if not match:
        return None

    formula = match.group()

    mass = molecular_mass(formula)

    if mass is None:
        return None

    return result(
        "Molecular Mass",
        "Add the atomic masses of all atoms",
        [
            f"Formula = {formula}",
            f"Molecular mass = {mass:.4g} u"
        ],
        f"{mass:.4g} u"
    )


# ============================================================
# CHEMISTRY — CONCENTRATION
# ============================================================

def solve_concentration(question):

    q = question.lower()
    nums = get_numbers(question)

    if not any(word in q for word in [
        "concentration",
        "mass percent"
    ]):
        return None

    if len(nums) < 2:
        return None

    solute, solution = nums[:2]

    if solution == 0:
        raise ValueError(
            "Solution mass/volume cannot be zero."
        )

    concentration = (
        solute / solution
    ) * 100

    return result(
        "Concentration",
        "Concentration % = Solute / Solution × 100",
        [
            f"Solute = {solute}",
            f"Solution = {solution}",
            f"Concentration = ({solute}/{solution}) × 100"
        ],
        f"{fmt(concentration)}%"
    )


# ============================================================
# CHEMISTRY — BALANCING BASIC EQUATIONS
# ============================================================

def balance_equation(question):

    q = question.lower()

    if not any(word in q for word in [
        "balance",
        "balanced equation"
    ]):
        return None

    # Basic common equations.
    equations = {

        "h2 + o2": "2H₂ + O₂ → 2H₂O",

        "hydrogen oxygen":
            "2H₂ + O₂ → 2H₂O",

        "na + cl":
            "2Na + Cl₂ → 2NaCl",

        "sodium chlorine":
            "2Na + Cl₂ → 2NaCl",

        "mg + o2":
            "2Mg + O₂ → 2MgO",

        "magnesium oxygen":
            "2Mg + O₂ → 2MgO",

        "c + o2":
            "C + O₂ → CO₂",

        "carbon oxygen":
            "C + O₂ → CO₂",
    }

    for key, balanced in equations.items():

        if key in q:
            return result(
                "Balanced Chemical Equation",
                "Atoms must be conserved on both sides",
                [
                    "Count atoms on both sides.",
                    "Adjust coefficients.",
                    "Verify that each element has equal atom counts."
                ],
                balanced
            )

    return (
        "I can currently balance several common school equations. "
        "For an unsupported equation, please write the complete "
        "chemical equation."
    )


# ============================================================
# BIOLOGY — BASIC DEFINITIONS
# ============================================================

BIOLOGY_KNOWLEDGE = {

    "cell": (
        "The cell is the basic structural and functional unit "
        "of living organisms."
    ),

    "tissue": (
        "A tissue is a group of similar cells performing "
        "a specific function."
    ),

    "photosynthesis": (
        "Photosynthesis is the process by which green plants "
        "use light energy to make food from carbon dioxide "
        "and water, releasing oxygen."
    ),

    "respiration": (
        "Cellular respiration is the process by which cells "
        "release energy from food."
    ),

    "digestion": (
        "Digestion is the breakdown of complex food into "
        "simpler substances that can be absorbed."
    ),

    "ecosystem": (
        "An ecosystem consists of living organisms and "
        "their physical environment interacting with each other."
    ),

    "food chain": (
        "A food chain shows the transfer of food and energy "
        "from one organism to another."
    ),

    "force": (
        "Force is a push or pull that can change the state "
        "of motion or shape of an object."
    ),

    "friction": (
        "Friction is a force that opposes relative motion "
        "between surfaces in contact."
    ),

    "pressure": (
        "Pressure is force acting per unit area."
    ),

    "sound": (
        "Sound is produced by vibrating objects and travels "
        "through a material medium."
    ),

    "electric current": (
        "Electric current is the rate of flow of electric charge."
    ),

    "reflection": (
        "Reflection is the bouncing back of light from a surface."
    ),

    "refraction": (
        "Refraction is the change in direction of light when "
        "it passes from one transparent medium to another."
    ),
}


def solve_biology_definition(question):

    q = question.lower()

    definition_words = [
        "what is",
        "define",
        "meaning of",
        "explain"
    ]

    if not any(word in q for word in definition_words):
        return None

    for key, definition in BIOLOGY_KNOWLEDGE.items():

        if key in q:

            return (
                f"### {key.title()}\n\n"
                f"**Answer:** {definition}"
            )

    return None


# ============================================================
# BIOLOGY — SIMPLE FACTUAL ANSWERS
# ============================================================

BIOLOGY_FACTS = {

    "powerhouse of the cell":
        "Mitochondria are commonly described as the powerhouse of the cell.",

    "control centre of the cell":
        "The nucleus controls many activities of the cell and contains genetic material.",

    "green pigment":
        "Chlorophyll is the green pigment involved in photosynthesis.",

    "functional unit of kidney":
        "The nephron is the structural and functional unit of the kidney.",

    "functional unit of nervous system":
        "The neuron is the basic functional unit of the nervous system.",

    "largest organ":
        "The skin is the largest organ of the human body.",
}


def solve_biology_fact(question):

    q = question.lower()

    for key, value in BIOLOGY_FACTS.items():

        if key in q:
            return (
                f"### Biology\n\n"
                f"**Answer:** {value}"
            )

    return None


# ============================================================
# UNIT CONVERSIONS
# ============================================================

def solve_conversion(question):

    q = question.lower()
    nums = get_numbers(question)

    if not nums:
        return None

    value = nums[0]

    # km/h → m/s
    if "km/h" in q and "m/s" in q:

        answer_value = value * 5 / 18

        return result(
            "Speed Conversion",
            "m/s = km/h × 5/18",
            [f"{value} × 5/18"],
            fmt(answer_value) + " m/s"
        )

    # m/s → km/h
    if "m/s" in q and "km/h" in q:

        answer_value = value * 18 / 5

        return result(
            "Speed Conversion",
            "km/h = m/s × 18/5",
            [f"{value} × 18/5"],
            fmt(answer_value) + " km/h"
        )

    # Celsius → Kelvin
    if "celsius" in q and "kelvin" in q:

        answer_value = value + 273.15

        return result(
            "Temperature Conversion",
            "K = °C + 273.15",
            [f"{value} + 273.15"],
            fmt(answer_value) + " K"
        )

    # Celsius → Fahrenheit
    if "celsius" in q and "fahrenheit" in q:

        answer_value = (
            value * 9 / 5
            + 32
        )

        return result(
            "Temperature Conversion",
            "°F = (°C × 9/5) + 32",
            [],
            fmt(answer_value) + " °F"
        )

    return None


# ============================================================
# MAIN SCIENCE ROUTER
# ============================================================

def solve_science(
    question,
    chapter="Auto Detect"
):

    if not question or not question.strip():
        return "Please enter a science question."

    engines = [

        # Biology
        solve_biology_definition,
        solve_biology_fact,

        # Chemistry
        solve_molecular_mass,
        solve_mole,
        solve_concentration,
        balance_equation,

        # Physics
        solve_conversion,
        solve_motion_equations,
        solve_motion,
        solve_force,
        solve_weight,
        solve_work,
        solve_energy,
        solve_power,
        solve_pressure,
        solve_density,
        solve_heat,
        solve_electricity,
        solve_electrical_power,
        solve_sound,
        solve_mirror,
        solve_lens,
    ]

    for engine in engines:

        try:

            output = engine(question)

            if output is not None:
                return output

        except Exception as error:

            return (
                f"Unable to solve this question: {error}"
            )

    return (
        "I could not confidently solve this science question yet. "
        "Please write the question with the required values "
        "or the complete question text."
    )


# ============================================================
# SUPPORTED SCIENCE CHAPTERS
# ============================================================

SCIENCE_CHAPTERS = {

    # Class 8
    "Crop Production and Management",
    "Microorganisms: Friend and Foe",
    "Coal and Petroleum",
    "Combustion and Flame",
    "Conservation of Plants and Animals",
    "Reproduction in Animals",
    "Reaching the Age of Adolescence",
    "Force and Pressure",
    "Friction",
    "Sound",
    "Chemical Effects of Electric Current",
    "Some Natural Phenomena",
    "Light",
    "Stars and the Solar System",
    "Pollution of Air and Water",

    # Class 9
    "Matter - Its Nature and Behaviour",
    "Organization in Living Organisms",
    "Motion",
    "Force and Work",
    "Food Production",

    # Class 10
    "Chemical Substances - Nature and Behaviour",
    "World of Living",
    "Natural Phenomena",
    "Effects of Current",
    "Natural Resources",
}


def is_science_chapter(chapter):

    return chapter in SCIENCE_CHAPTERS