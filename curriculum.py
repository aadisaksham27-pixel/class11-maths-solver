"""
KSHITIJ CURRICULUM
CBSE / NCERT-aligned curriculum structure for the 2026-27 app build.

Classes IX-XII use the official CBSE 2026-27 structure.
Class VIII is an NCERT-aligned foundation because the current CBSE
curriculum publication covers IX-XII as the formal secondary/senior-secondary
syllabus.
"""

CURRICULUM_SESSION = "2026-27"

CURRICULUM = {
    "Class 8": {
        "Mathematics": [
            "Rational Numbers",
            "Linear Equations in One Variable",
            "Understanding Quadrilaterals",
            "Practical Geometry",
            "Data Handling",
            "Squares and Square Roots",
            "Cubes and Cube Roots",
            "Comparing Quantities",
            "Algebraic Expressions and Identities",
            "Visualising Solid Shapes",
            "Exponents and Powers",
            "Direct and Inverse Proportions",
            "Factorisation",
            "Introduction to Graphs",
            "Mensuration",
        ],
        "Science": [
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
        ],
    },

    "Class 9": {
        "Mathematics": [
            "Number System",
            "Introduction to Polynomials",
            "Sequences and Progressions",
            "Exploring Algebraic Identities",
            "Linear Equations in Two Variables",
            "Coordinate Geometry",
            "Introduction to Euclid's Geometry: Axioms and Postulates",
            "Lines and Angles",
            "Triangles - Congruence Theorems",
            "4-gons (Quadrilaterals)",
            "Circles",
            "Area and Perimeter",
            "Surface Area and Volume",
            "Statistics",
            "Introduction to Probability",
        ],
        "Science": [
            "Matter - Its Nature and Behaviour",
            "Organization in Living Organisms",
            "Motion, Force and Work",
            "Food Production",
        ],
    },

    "Class 10": {
        "Mathematics": [
            "Real Numbers",
            "Polynomials",
            "Pair of Linear Equations in Two Variables",
            "Quadratic Equations",
            "Arithmetic Progressions",
            "Coordinate Geometry",
            "Triangles",
            "Circles",
            "Introduction to Trigonometry",
            "Some Applications of Trigonometry",
            "Areas Related to Circles",
            "Surface Areas and Volumes",
            "Statistics",
            "Probability",
        ],
        "Science": [
            "Chemical Substances - Nature and Behaviour",
            "World of Living",
            "Natural Phenomena",
            "Effects of Current",
            "Natural Resources",
        ],
    },

    "Class 11": {
        "Mathematics": [
            "Sets",
            "Relations and Functions",
            "Trigonometric Functions",
            "Complex Numbers and Quadratic Equations",
            "Linear Inequalities",
            "Permutations and Combinations",
            "Binomial Theorem",
            "Sequences and Series",
            "Straight Lines",
            "Conic Sections",
            "Introduction to Three Dimensional Geometry",
            "Limits and Derivatives",
            "Statistics",
            "Probability",
        ],
        "Physics": [
            "Units and Measurements",
            "Motion in a Straight Line",
            "Motion in a Plane",
            "Laws of Motion",
            "Work, Energy and Power",
            "System of Particles and Rotational Motion",
            "Gravitation",
            "Mechanical Properties of Solids",
            "Mechanical Properties of Fluids",
            "Thermal Properties of Matter",
            "Thermodynamics",
            "Kinetic Theory",
            "Oscillations",
            "Waves",
        ],
        "Chemistry": [
            "Some Basic Concepts of Chemistry",
            "Structure of Atom",
            "Classification of Elements and Periodicity in Properties",
            "Chemical Bonding and Molecular Structure",
            "Chemical Thermodynamics",
            "Equilibrium",
            "Redox Reactions",
            "Organic Chemistry: Some Basic Principles and Techniques",
            "Hydrocarbons",
        ],
    },

    "Class 12": {
        "Mathematics": [
            "Relations and Functions",
            "Inverse Trigonometric Functions",
            "Matrices",
            "Determinants",
            "Continuity and Differentiability",
            "Application of Derivatives",
            "Integrals",
            "Application of Integrals",
            "Differential Equations",
            "Vector Algebra",
            "Three Dimensional Geometry",
            "Linear Programming",
            "Probability",
        ],
        "Physics": [
            "Electric Charges and Fields",
            "Electrostatic Potential and Capacitance",
            "Current Electricity",
            "Moving Charges and Magnetism",
            "Magnetism and Matter",
            "Electromagnetic Induction",
            "Alternating Current",
            "Electromagnetic Waves",
            "Ray Optics and Optical Instruments",
            "Wave Optics",
            "Dual Nature of Radiation and Matter",
            "Atoms",
            "Nuclei",
            "Semiconductor Electronics: Materials, Devices and Simple Circuits",
        ],
        "Chemistry": [
            "Solutions",
            "Electrochemistry",
            "Chemical Kinetics",
            "d- and f-Block Elements",
            "Coordination Compounds",
            "Haloalkanes and Haloarenes",
            "Alcohols, Phenols and Ethers",
            "Aldehydes, Ketones and Carboxylic Acids",
            "Amines",
            "Biomolecules",
        ],
    },
}


def get_classes():
    return list(CURRICULUM.keys())


def get_subjects(class_name):
    return list(CURRICULUM.get(class_name, {}).keys())


def get_chapters(class_name, subject):
    return list(CURRICULUM.get(class_name, {}).get(subject, []))


def has_class(class_name):
    return class_name in CURRICULUM


def has_subject(class_name, subject):
    return subject in CURRICULUM.get(class_name, {})


def has_chapter(class_name, subject, chapter):
    return chapter in get_chapters(class_name, subject)


def find_chapter(chapter_name):
    results = []
    if not isinstance(chapter_name, str):
        return results

    target = chapter_name.strip().lower()

    for class_name, subjects in CURRICULUM.items():
        for subject, chapters in subjects.items():
            for chapter in chapters:
                if chapter.lower() == target:
                    results.append({
                        "class": class_name,
                        "subject": subject,
                        "chapter": chapter,
                    })

    return results


def get_curriculum():
    return CURRICULUM


# Backward-compatible alias.
curriculum = CURRICULUM
