import tkinter as tk
from process import run_algorithm


# Main application window
class SearchApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure window properties
        self.title("Search Algorithms")
        self.geometry("900x700")
        self.configure(bg="#1e1e2f")
        self.resizable(False, False)

        # Store the currently selected algorithm
        self.current_algorithm = None

        # Start by showing the main menu
        self.create_main_menu()

    # Add a simple hover color effect to buttons
    def add_hover(self, button):
        def on_enter(e):
            button.config(bg="#4e73df")

        def on_leave(e):
            button.config(bg="#2e59d9")

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    # Remove all widgets from the window
    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    # Create the main menu screen
    def create_main_menu(self):
        self.clear_screen()

        # Center frame for layout
        frame = tk.Frame(self, bg="#1e1e2f")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title text
        title = tk.Label(
            frame,
            text="SEARCH ALGORITHMS",
            font=("Arial", 26, "bold"),
            bg="#1e1e2f",
            fg="white"
        )
        title.pack(pady=20)

        # Available algorithms
        algorithms = ["DFS", "BFS", "GBFS", "A*", "CUS1", "CUS2"]

        # Create a button for each algorithm
        for algo in algorithms:
            btn = tk.Button(
                frame,
                text=algo,
                font=("Arial", 14),
                bg="#2e59d9",
                fg="white",
                width=15,
                relief="flat",
                command=lambda a=algo: self.open_testcase_screen(a)
            )
            btn.pack(pady=8)
            self.add_hover(btn)

        # Button to compare all algorithms at once
        compare_btn = tk.Button(
            frame,
            text="COMPARE ALL",
            font=("Arial", 14, "bold"),
            bg="#1cc88a",
            fg="white",
            width=15,
            relief="flat",
            command=self.open_compare_screen
        )
        compare_btn.pack(pady=15)
        self.add_hover(compare_btn)

    # Screen for selecting a testcase
    def open_testcase_screen(self, algorithm):
        self.current_algorithm = algorithm
        self.clear_screen()

        title = tk.Label(
            self,
            text=f"{algorithm} - Select Testcase",
            font=("Arial", 20, "bold"),
            bg="#1e1e2f",
            fg="white"
        )
        title.pack(pady=20)

        grid_frame = tk.Frame(self, bg="#1e1e2f")
        grid_frame.pack()

        # Create 30 testcase buttons arranged in a grid
        for i in range(30):
            testcase = f"testcase{str(i+1).zfill(2)}"

            btn = tk.Button(
                grid_frame,
                text=str(i+1),
                width=5,
                height=2,
                bg="#2e59d9",
                fg="white",
                relief="flat",
                command=lambda t=testcase: self.run_testcase(t)
            )

            btn.grid(row=i // 6, column=i % 6, padx=10, pady=10)
            self.add_hover(btn)

        # Back button
        back_btn = tk.Button(
            self,
            text="Back",
            bg="#e74a3b",
            fg="white",
            width=10,
            relief="flat",
            command=self.create_main_menu
        )
        back_btn.pack(pady=20)
        self.add_hover(back_btn)

        # Text box to display results
        self.result_box = tk.Text(
            self,
            height=30,
            width=90,
            bg="#111122",
            fg="white",
            font=("Consolas", 10)
        )
        self.result_box.pack(pady=10)

    # Run the selected algorithm and show result
    def run_testcase(self, testcase):
        data = run_algorithm(self.current_algorithm, testcase)

        # Clear previous output
        self.result_box.delete("1.0", tk.END)

        if data is None:
            self.result_box.insert(tk.END, "Error: Algorithm returned no data.")
            return

        if data["cost"] is None:
            self.result_box.insert(tk.END, data["result"])
            return

        output = f"""
Algorithm: {self.current_algorithm}
Testcase: {testcase}

{data['result']}

Cost: {data['cost']}
Time used: {data['time']:.6f} seconds
Memory used: {data['memory']:.2f} KB
Optimal: {'YES' if data['optimal'] else 'NO'}
"""

        self.result_box.insert(tk.END, output)

    # Screen to select testcase for comparison
    def open_compare_screen(self):
        self.current_algorithm = "COMPARE"
        self.clear_screen()

        title = tk.Label(
            self,
            text="COMPARE ALL - Select Testcase",
            font=("Arial", 20, "bold"),
            bg="#1e1e2f",
            fg="white"
        )
        title.pack(pady=20)

        grid_frame = tk.Frame(self, bg="#1e1e2f")
        grid_frame.pack()

        for i in range(30):
            testcase = f"testcase{str(i+1).zfill(2)}"

            btn = tk.Button(
                grid_frame,
                text=str(i+1),
                width=5,
                height=2,
                bg="#2e59d9",
                fg="white",
                relief="flat",
                command=lambda t=testcase: self.run_comparison(t)
            )

            btn.grid(row=i // 6, column=i % 6, padx=10, pady=10)
            self.add_hover(btn)

        back_btn = tk.Button(
            self,
            text="Back",
            bg="#e74a3b",
            fg="white",
            width=10,
            relief="flat",
            command=self.create_main_menu
        )
        back_btn.pack(pady=20)
        self.add_hover(back_btn)

    # Run all algorithms and display comparison results
    def run_comparison(self, testcase):
        self.clear_screen()

        title = tk.Label(
            self,
            text=f"Comparison - {testcase}",
            font=("Arial", 20, "bold"),
            bg="#1e1e2f",
            fg="white"
        )
        title.pack(pady=15)

        algorithms = ["DFS", "BFS", "GBFS", "A*", "CUS1", "CUS2"]

        container = tk.Frame(self, bg="#1e1e2f")
        container.pack()

        boxes = {}

        # Create result panels (2 rows x 3 columns)
        for i, algo in enumerate(algorithms):
            frame = tk.Frame(container, bg="#2a2a40", bd=2, relief="ridge")
            frame.grid(row=i // 3, column=i % 3, padx=10, pady=10)

            label = tk.Label(
                frame,
                text=algo,
                font=("Arial", 12, "bold"),
                bg="#2a2a40",
                fg="white"
            )
            label.pack()

            text_box = tk.Text(
                frame,
                height=12,
                width=35,
                bg="#111122",
                fg="white",
                font=("Consolas", 9)
            )
            text_box.pack(padx=5, pady=5)

            boxes[algo] = text_box

        # Execute each algorithm and show its result
        for algo in algorithms:
            data = run_algorithm(algo, testcase)

            if data is None:
                boxes[algo].insert(tk.END, "Error")
                continue

            if data["cost"] is None:
                boxes[algo].insert(tk.END, data["result"] + "\nCost: N/A")
                continue

            output = f"""{data['result']}

Cost: {data['cost']}
Time: {data['time']:.6f}s
Memory: {data['memory']:.2f}KB
Optimal: {'YES' if data['optimal'] else 'NO'}"""

            boxes[algo].insert(tk.END, output)

        back_btn = tk.Button(
            self,
            text="Back",
            bg="#e74a3b",
            fg="white",
            width=10,
            relief="flat",
            command=self.create_main_menu
        )
        back_btn.pack(pady=20)
        self.add_hover(back_btn)


if __name__ == "__main__":
    app = SearchApp()
    app.mainloop()