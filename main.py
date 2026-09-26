import tkinter as tk
from tkinter import ttk, messagebox
from solver import solve, detect_chapter
from solver import is_chapter_supported
from solver import get_supported_chapters


# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("Class 11 Maths Solver")
root.geometry("1100x700")
root.minsize(900, 600)
root.configure(bg="#10141c")


# ---------------- COLORS ----------------
BG = "#10141c"
PANEL = "#181e29"
PANEL2 = "#202735"
TEXT = "#f1f5f9"
MUTED = "#94a3b8"
ACCENT = "#4f8cff"
SUCCESS = "#22c55e"


# ---------------- HEADER ----------------
header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=30, pady=(25, 10))

title = tk.Label(
    header,
    text="CLASS 11 MATHS SOLVER",
    font=("Segoe UI", 26, "bold"),
    bg=BG,
    fg=TEXT
)
title.pack(anchor="w")

subtitle = tk.Label(
    header,
    text="CBSE / NCERT  •  Class XI Mathematics",
    font=("Segoe UI", 11),
    bg=BG,
    fg=MUTED
)
subtitle.pack(anchor="w", pady=(3, 0))


# ---------------- MAIN AREA ----------------
main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True, padx=30, pady=10)

main.columnconfigure(0, weight=1)
main.columnconfigure(1, weight=1)
main.rowconfigure(1, weight=1)


# ---------------- LEFT PANEL ----------------
left = tk.Frame(main, bg=PANEL)
left.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))

left.columnconfigure(0, weight=1)
left.rowconfigure(3, weight=1)

tk.Label(
    left,
    text="PROBLEM",
    font=("Segoe UI", 12, "bold"),
    bg=PANEL,
    fg=TEXT
).grid(row=0, column=0, sticky="w", padx=20, pady=(20, 8))


# Chapter
chapter_var = tk.StringVar(value="Auto Detect")

chapters = [
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

chapter_box = ttk.Combobox(
    left,
    textvariable=chapter_var,
    values=chapters,
    state="readonly",
    font=("Segoe UI", 10)
)
chapter_box.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 15))


# Question box
question_box = tk.Text(
    left,
    height=15,
    wrap="word",
    font=("Consolas", 12),
    bg="#0d1117",
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    padx=15,
    pady=15
)
question_box.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 15))


# Buttons
buttons = tk.Frame(left, bg=PANEL)
buttons.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 20))

buttons.columnconfigure(0, weight=1)
buttons.columnconfigure(1, weight=1)
buttons.columnconfigure(2, weight=1)


def clear_question():
    question_box.delete("1.0", "end")
    answer_box.config(state="normal")
    answer_box.delete("1.0", "end")
    answer_box.config(state="disabled")
    detected_label.config(text="Detected chapter: —")


def copy_answer():
    answer = answer_box.get("1.0", "end").strip()

    if not answer:
        messagebox.showinfo("Copy Answer", "There is no answer to copy.")
        return

    root.clipboard_clear()
    root.clipboard_append(answer)
    root.update()

    messagebox.showinfo("Copied", "Solution copied to clipboard!")


def solve_problem():
    question = question_box.get("1.0", "end").strip()

    if not question:
        messagebox.showwarning(
            "No Question",
            "Please enter a Class 11 Maths question."
        )
        return

    try:
        selected = chapter_var.get()

        if selected == "Auto Detect":
            selected = detect_chapter(question)

        result = solve(question, selected)

        detected_label.config(
            text=f"Detected chapter: {selected}"
        )

        answer_box.config(state="normal")
        answer_box.delete("1.0", "end")
        answer_box.insert("1.0", result)
        answer_box.config(state="disabled")

    except Exception as error:
        answer_box.config(state="normal")
        answer_box.delete("1.0", "end")
        answer_box.insert(
            "1.0",
            "Unable to solve this question.\n\n"
            "Try writing the question in a simpler mathematical form.\n\n"
            f"Details: {error}"
        )
        answer_box.config(state="disabled")


solve_button = tk.Button(
    buttons,
    text="SOLVE",
    command=solve_problem,
    font=("Segoe UI", 11, "bold"),
    bg=ACCENT,
    fg="white",
    activebackground=ACCENT,
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    pady=10
)
solve_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))

clear_button = tk.Button(
    buttons,
    text="CLEAR",
    command=clear_question,
    font=("Segoe UI", 10, "bold"),
    bg=PANEL2,
    fg=TEXT,
    activebackground=PANEL2,
    relief="flat",
    cursor="hand2",
    pady=10
)
clear_button.grid(row=0, column=1, sticky="ew", padx=5)

copy_button = tk.Button(
    buttons,
    text="COPY",
    command=copy_answer,
    font=("Segoe UI", 10, "bold"),
    bg=PANEL2,
    fg=TEXT,
    activebackground=PANEL2,
    relief="flat",
    cursor="hand2",
    pady=10
)
copy_button.grid(row=0, column=2, sticky="ew", padx=(5, 0))


# ---------------- RIGHT TOP ----------------
info = tk.Frame(main, bg=PANEL)
info.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=(0, 10))

detected_label = tk.Label(
    info,
    text="Detected chapter: —",
    font=("Segoe UI", 11, "bold"),
    bg=PANEL,
    fg=SUCCESS
)
detected_label.pack(anchor="w", padx=20, pady=18)


# ---------------- RIGHT SOLUTION ----------------
right = tk.Frame(main, bg=PANEL)
right.grid(row=1, column=1, sticky="nsew", padx=(10, 0))

right.columnconfigure(0, weight=1)
right.rowconfigure(1, weight=1)

tk.Label(
    right,
    text="SOLUTION",
    font=("Segoe UI", 12, "bold"),
    bg=PANEL,
    fg=TEXT
).grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))


answer_frame = tk.Frame(right, bg="#0d1117")
answer_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

answer_frame.columnconfigure(0, weight=1)
answer_frame.rowconfigure(0, weight=1)

answer_box = tk.Text(
    answer_frame,
    wrap="word",
    font=("Consolas", 12),
    bg="#0d1117",
    fg=TEXT,
    relief="flat",
    padx=15,
    pady=15
)
answer_box.grid(row=0, column=0, sticky="nsew")

answer_scroll = ttk.Scrollbar(
    answer_frame,
    orient="vertical",
    command=answer_box.yview
)
answer_scroll.grid(row=0, column=1, sticky="ns")

answer_box.configure(yscrollcommand=answer_scroll.set)
answer_box.config(state="disabled")


# ---------------- EXAMPLES ----------------
examples = tk.Frame(root, bg=BG)
examples.pack(fill="x", padx=30, pady=(0, 20))

tk.Label(
    examples,
    text="QUICK EXAMPLES",
    font=("Segoe UI", 10, "bold"),
    bg=BG,
    fg=MUTED
).pack(anchor="w", pady=(0, 7))


example_questions = [
    "x^2 - 5*x + 6 = 0",
    "10P3",
    "Find the 10th term of AP 3, 7, 11, 15",
    "differentiate x^3 + 2*x^2",
    "Find slope between (1,2) and (4,8)"
]


def put_example(text):
    question_box.delete("1.0", "end")
    question_box.insert("1.0", text)


example_frame = tk.Frame(examples, bg=BG)
example_frame.pack(fill="x")

for i, example in enumerate(example_questions):
    btn = tk.Button(
        example_frame,
        text=example,
        command=lambda q=example: put_example(q),
        font=("Segoe UI", 9),
        bg=PANEL2,
        fg=TEXT,
        activebackground=PANEL2,
        relief="flat",
        cursor="hand2",
        padx=10,
        pady=7
    )
    btn.pack(side="left", padx=(0, 7))


# ---------------- SHORTCUT ----------------
def keyboard_solve(event=None):
    solve_problem()


root.bind("<Control-Return>", keyboard_solve)


# ---------------- START ----------------
root.mainloop()