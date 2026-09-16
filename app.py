from flask import Flask, request, render_template_string
from solver import solve, detect_chapter

app = Flask(__name__)

CHAPTERS = [
    "Auto Detect",
    "Sets",
    "Relations & Functions",
    "Trigonometric Functions",
    "Complex Numbers & Quadratic Equations",
    "Linear Inequalities",
    "Permutations & Combinations",
    "Binomial Theorem",
    "Sequences & Series",
    "Straight Lines",
    "Conic Sections",
    "3D Geometry",
    "Limits & Derivatives",
    "Statistics",
    "Probability"
]

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Class 11 Maths Solver</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            background: #10141c;
            color: #f1f5f9;
            font-family: Arial, sans-serif;
        }

        .container {
            width: 100%;
            max-width: 900px;
            margin: auto;
            padding: 20px;
        }

        .header {
            padding: 10px 0 20px;
        }

        h1 {
            margin: 0;
            font-size: 28px;
        }

        .subtitle {
            color: #94a3b8;
            margin-top: 6px;
        }

        .card {
            background: #181e29;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 16px;
        }

        label {
            display: block;
            font-weight: bold;
            margin-bottom: 8px;
        }

        select,
        textarea {
            width: 100%;
            background: #0d1117;
            color: #f1f5f9;
            border: 1px solid #303846;
            border-radius: 9px;
            padding: 13px;
            font-size: 16px;
        }

        textarea {
            min-height: 150px;
            resize: vertical;
            font-family: monospace;
        }

        button {
            width: 100%;
            border: 0;
            border-radius: 9px;
            padding: 14px;
            margin-top: 12px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }

        .solve {
            background: #4f8cff;
            color: white;
        }

        .example {
            background: #202735;
            color: #f1f5f9;
        }

        .detected {
            color: #22c55e;
            font-weight: bold;
        }

        .answer {
            background: #0d1117;
            border-radius: 9px;
            padding: 16px;
            white-space: pre-wrap;
            overflow-x: auto;
            font-family: monospace;
            font-size: 15px;
            min-height: 100px;
        }

        .examples {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }

        .examples button {
            margin: 0;
            font-size: 13px;
        }

        @media (max-width: 600px) {
            .container {
                padding: 14px;
            }

            h1 {
                font-size: 23px;
            }

            .examples {
                grid-template-columns: 1fr;
            }
        }
    </style>

    <script>
        function putExample(text) {
            document.getElementById("question").value = text;
            document.getElementById("question").focus();
        }
    </script>
</head>

<body>

<div class="container">

    <div class="header">
        <h1>CLASS 11 MATHS SOLVER</h1>
        <div class="subtitle">
            CBSE / NCERT • Class XI Mathematics
        </div>
    </div>

    <div class="card">

        <form method="POST">

            <label>Chapter</label>

            <select name="chapter">
                {% for chapter in chapters %}
                    <option value="{{ chapter }}"
                    {% if chapter == selected_chapter %}selected{% endif %}>
                        {{ chapter }}
                    </option>
                {% endfor %}
            </select>

            <br><br>

            <label>Enter your question</label>

            <textarea
                id="question"
                name="question"
                placeholder="Example: x^2 - 5*x + 6 = 0"
            >{{ question }}</textarea>

            <button class="solve" type="submit">
                SOLVE
            </button>

        </form>

    </div>

    {% if result %}

    <div class="card">

        <div class="detected">
            Detected chapter: {{ detected }}
        </div>

        <br>

        <label>Solution</label>

        <div class="answer">{{ result }}</div>

    </div>

    {% endif %}

    <div class="card">

        <label>Quick Examples</label>

        <div class="examples">

            <button class="example"
                onclick="putExample('x^2 - 5*x + 6 = 0')">
                Quadratic Equation
            </button>

            <button class="example"
                onclick="putExample('10P3')">
                Permutation
            </button>

            <button class="example"
                onclick="putExample('Find the 10th term of AP 3, 7, 11, 15')">
                AP
            </button>

            <button class="example"
                onclick="putExample('differentiate x^3 + 2*x^2')">
                Differentiation
            </button>

            <button class="example"
                onclick="putExample('Find slope between (1,2) and (4,8)')">
                Straight Line
            </button>

        </div>

    </div>

</div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    question = ""
    result = ""
    detected = "—"
    selected_chapter = "Auto Detect"

    if request.method == "POST":

        question = request.form.get("question", "").strip()
        selected_chapter = request.form.get(
            "chapter",
            "Auto Detect"
        )

        if question:

            try:
                if selected_chapter == "Auto Detect":
                    selected_chapter = detect_chapter(question)

                detected = selected_chapter

                result = solve(
                    question,
                    selected_chapter
                )

            except Exception as error:

                result = (
                    "Unable to solve this question.\\n\\n"
                    "Try writing the mathematical expression "
                    "in a simpler form.\\n\\n"
                    f"Details: {error}"
                )

    return render_template_string(
        HTML,
        chapters=CHAPTERS,
        question=question,
        result=result,
        detected=detected,
        selected_chapter=selected_chapter
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )