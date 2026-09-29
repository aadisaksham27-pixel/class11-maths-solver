import tkinter as tk
from tkinter import ttk, messagebox
from solver import solve, detect_chapter


class MathsApp:

    def __init__(self, root):

        self.root = root

        # =====================================================
        # WINDOW
        # =====================================================

        root.title("Class 11 Maths Solver")
        root.geometry("1100x750")
        root.minsize(850, 600)

        # =====================================================
        # STYLE
        # =====================================================

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 26, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 11)
        )

        style.configure(
            "Section.TLabel",
            font=("Segoe UI", 11, "bold")
        )

        # =====================================================
        # MAIN FRAME
        # =====================================================

        main = ttk.Frame(
            root,
            padding=25
        )

        main.pack(
            fill="both",
            expand=True
        )

        # =====================================================
        # HEADER
        # =====================================================

        ttk.Label(
            main,
            text="CLASS 11 MATHS SOLVER",
            style="Title.TLabel"
        ).pack(
            anchor="w"
        )

        ttk.Label(
            main,
            text="CBSE / NCERT • Class XI Mathematics",
            style="Subtitle.TLabel"
        ).pack(
            anchor="w",
            pady=(0, 20)
        )

        # =====================================================
        # CHAPTER
        # =====================================================

        chapter_frame = ttk.Frame(main)

        chapter_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        ttk.Label(
            chapter_frame,
            text="Chapter:",
            style="Section.TLabel"
        ).pack(
            side="left"
        )

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

        self.chapter = ttk.Combobox(
            chapter_frame,
            values=chapters,
            state="readonly",
            width=42
        )

        self.chapter.current(0)

        self.chapter.pack(
            side="left",
            padx=12
        )

        # =====================================================
        # QUESTION
        # =====================================================

        ttk.Label(
            main,
            text="Enter your question:",
            style="Section.TLabel"
        ).pack(
            anchor="w"
        )

        self.question = tk.Text(
            main,
            height=7,
            font=("Consolas", 14),
            wrap="word"
        )

        self.question.pack(
            fill="x",
            pady=(6, 12)
        )

        # =====================================================
        # BUTTONS
        # =====================================================

        button_frame = ttk.Frame(main)

        button_frame.pack(
            fill="x",
            pady=(0, 12)
        )

        ttk.Button(
            button_frame,
            text="SOLVE",
            command=self.solve_question
        ).pack(
            side="left",
            padx=(0, 8)
        )

        ttk.Button(
            button_frame,
            text="CLEAR",
            command=self.clear
        ).pack(
            side="left",
            padx=(0, 8)
        )

        ttk.Button(
            button_frame,
            text="COPY ANSWER",
            command=self.copy_answer
        ).pack(
            side="left"
        )

        # =====================================================
        # DETECTED CHAPTER
        # =====================================================

        self.detected = ttk.Label(
            main,
            text="Chapter detected: —",
            font=("Segoe UI", 10, "bold")
        )

        self.detected.pack(
            anchor="w",
            pady=(0, 8)
        )

        # =====================================================
        # SOLUTION
        # =====================================================

        ttk.Label(
            main,
            text="Solution:",
            style="Section.TLabel"
        ).pack(
            anchor="w"
        )

        result_frame = ttk.Frame(main)

        result_frame.pack(
            fill="both",
            expand=True,
            pady=(6, 0)
        )

        self.result = tk.Text(
            result_frame,
            font=("Consolas", 13),
            wrap="word",
            state="disabled"
        )

        scrollbar = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=self.result.yview
        )

        self.result.configure(
            yscrollcommand=scrollbar.set
        )

        self.result.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # =====================================================
        # EXAMPLES
        # =====================================================

        ttk.Label(
            main,
            text=(
                "Examples:  x^2 - 5*x + 6 = 0   |   "
                "AP 3,7,11,15... 10th term   |   "
                "10P3   |   differentiate x^3 + 2*x^2"
            ),
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            pady=(8, 0)
        )

        # =====================================================
        # KEYBOARD SHORTCUT
        # =====================================================

        root.bind(
            "<Control-Return>",
            lambda event: self.solve_question()
        )

        self.question.focus()

    # =========================================================
    # SOLVE
    # =========================================================

    def solve_question(self):

        question = self.question.get(
            "1.0",
            tk.END
        ).strip()

        if not question:

            messagebox.showinfo(
                "Class 11 Maths Solver",
                "Please enter a Maths question."
            )

            return

        selected_chapter = self.chapter.get()

        try:

            if selected_chapter == "Auto Detect":

                detected_chapter = detect_chapter(
                    question
                )

                self.detected.config(
                    text=f"Chapter detected: {detected_chapter}"
                )

            else:

                detected_chapter = selected_chapter

                self.detected.config(
                    text=f"Chapter selected: {detected_chapter}"
                )

            answer = solve(
                question,
                detected_chapter
            )

            self.result.config(
                state="normal"
            )

            self.result.delete(
                "1.0",
                tk.END
            )

            self.result.insert(
                tk.END,
                answer
            )

            self.result.config(
                state="disabled"
            )

        except Exception as error:

            self.result.config(
                state="normal"
            )

            self.result.delete(
                "1.0",
                tk.END
            )

            self.result.insert(
                tk.END,
                "Something went wrong.\n\n"
                f"Error:\n{error}"
            )

            self.result.config(
                state="disabled"
            )

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self):

        self.question.delete(
            "1.0",
            tk.END
        )

        self.result.config(
            state="normal"
        )

        self.result.delete(
            "1.0",
            tk.END
        )

        self.result.config(
            state="disabled"
        )

        self.detected.config(
            text="Chapter detected: —"
        )

        self.question.focus()

    # =========================================================
    # COPY ANSWER
    # =========================================================

    def copy_answer(self):

        answer = self.result.get(
            "1.0",
            tk.END
        ).strip()

        if not answer:

            return

        self.root.clipboard_clear()

        self.root.clipboard_append(
            answer
        )

        self.root.update()

        messagebox.showinfo(
            "Copied",
            "Solution copied to clipboard."
        )


# =============================================================
# START
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = MathsApp(root)

    root.mainloop()