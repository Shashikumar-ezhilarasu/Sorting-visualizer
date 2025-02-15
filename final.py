import tkinter as tk
from tkinter import ttk
import random
import time
import threading

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Visualizer")
        self.root.geometry("900x900")
        self.root.config(bg="#f5f5f5")

        self.algorithms = {
            "Bubble Sort": self.bubble_sort,
            "Selection Sort": self.selection_sort,
            "Insertion Sort": self.insertion_sort,
            "Quick Sort": self.quick_sort,
        }

        self.algorithm_descriptions = {
            "Bubble Sort": "Bubble Sort repeatedly compares adjacent elements and swaps them if they are in the wrong order. "
                           "This process is repeated until the array is sorted. It is simple but inefficient for large datasets.",
            "Selection Sort": "Selection Sort divides the array into a sorted and unsorted part. It repeatedly finds the minimum "
                              "element in the unsorted part and places it at the beginning of the sorted part.",
            "Insertion Sort": "Insertion Sort builds the sorted array one element at a time by taking an element from the unsorted "
                              "part and placing it in its correct position in the sorted part.",
            "Quick Sort": "Quick Sort is a divide-and-conquer algorithm. It picks a pivot element, partitions the array around the pivot, "
                          "and recursively sorts the left and right partitions.",
        }

        self.selected_algorithm = tk.StringVar()
        self.selected_algorithm.set("Bubble Sort")
        self.speed = tk.DoubleVar()
        self.speed.set(0.01)
        self.bar_color = "#3498db"
        self.sorted_color = "#2ecc71"
        self.bar_data = []
        self.sorting_thread = None

        self.create_widgets()

    def create_widgets(self):
        # Algorithm selection
        tk.Label(self.root, text="Sorting Algorithm", bg="black", font=("Arial", 14)).pack(pady=10)
        algorithm_menu = ttk.Combobox(
            self.root, textvariable=self.selected_algorithm, values=list(self.algorithms.keys()), state="readonly"
        )
        algorithm_menu.pack(pady=5)

        # Speed control
        tk.Label(self.root, text="Visualization Speed (Lower = Faster)", bg="black", font=("Arial", 14)).pack(pady=10)
        speed_slider = ttk.Scale(self.root, from_=0.01, to=1.0, variable=self.speed, orient="horizontal")
        speed_slider.pack(pady=5)

        # Array input options
        input_frame = tk.Frame(self.root, bg="#f5f5f5")
        input_frame.pack(pady=20)
        tk.Label(input_frame, text="Input Array (comma-separated)", bg="black", font=("Arial", 12)).pack(side="left")
        self.input_array_entry = ttk.Entry(input_frame, width=40)
        self.input_array_entry.pack(side="left", padx=10)
        tk.Button(input_frame, text="Set Array", command=self.set_array, bg="#3498db", fg="black").pack(side="left")

        # Randomize button
        tk.Button(self.root, text="Randomize Array", command=self.generate_array, bg="#ff5733", fg="black").pack(pady=10)

        # Canvas for visualizing sorting
        self.canvas = tk.Canvas(self.root, width=800, height=400, bg="white")
        self.canvas.pack(pady=20)

        # Buttons for sorting
        button_frame = tk.Frame(self.root, bg="#f5f5f5")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Start Sort", command=self.start_sort, bg="white", fg="black").pack(side="left", padx=10)
        tk.Button(button_frame, text="Reset", command=self.reset, bg="#c0392b", fg="black").pack(side="left", padx=10)

        # Information display
        self.info_label = tk.Label(self.root, text="", bg="white", font=("Arial", 12), fg="black")
        self.info_label.pack(pady=10)

        # Sorting algorithm description
        self.description_label = tk.Label(self.root, text="", wraplength=800, bg="white", font=("Arial", 12), fg="black", justify="left")
        self.description_label.pack(pady=20)

        # Detailed explanation of each step
        self.step_label = tk.Label(self.root, text="", wraplength=800, bg="white", font=("Arial", 12), fg="black", justify="left")
        self.step_label.pack(pady=20)

    def set_array(self):
        try:
            array_input = self.input_array_entry.get()
            self.bar_data = list(map(int, array_input.split(",")))
            self.display_array()
            self.info_label.config(text="Custom array set. Choose an algorithm and click 'Start Sort'.")
        except ValueError:
            self.info_label.config(text="Invalid input! Please enter integers separated by commas.")

    def generate_array(self):
        self.bar_data = [random.randint(10, 100) for _ in range(30)]  # 30 random elements
        self.display_array()
        self.info_label.config(text="Random array generated. Choose an algorithm and click 'Start Sort'.")

    def display_array(self, highlight=[]):
        self.canvas.delete("all")
        canvas_width = 800
        canvas_height = 400
        bar_width = canvas_width / len(self.bar_data)
        max_value = max(self.bar_data) if self.bar_data else 1

        for i, value in enumerate(self.bar_data):
            x0 = i * bar_width
            y0 = canvas_height - (value / max_value) * canvas_height
            x1 = (i + 1) * bar_width
            y1 = canvas_height

            color = self.sorted_color if i in highlight else self.bar_color
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
            self.canvas.create_text(x0 + bar_width / 2, y0 - 10, text=str(value), font=("Arial", 8), fill="black")

        self.root.update_idletasks()

    def start_sort(self):
        if not self.bar_data:
            self.info_label.config(text="No array to sort! Generate or input an array first.")
            return

        if self.sorting_thread is None or not self.sorting_thread.is_alive():
            selected_algo = self.selected_algorithm.get()
            self.info_label.config(text=f"Sorting using {selected_algo}...")
            self.description_label.config(text=self.algorithm_descriptions[selected_algo])
            self.step_label.config(text="")
            self.sorting_thread = threading.Thread(target=self.algorithms[selected_algo])
            self.sorting_thread.start()

    def reset(self):
        self.bar_data = []
        self.canvas.delete("all")
        self.info_label.config(text="Array reset. Generate or input a new array to start.")
        self.description_label.config(text="")
        self.step_label.config(text="")

    def bubble_sort(self):
        n = len(self.bar_data)
        for i in range(n - 1):
            for j in range(n - i - 1):
                if self.bar_data[j] > self.bar_data[j + 1]:
                    self.bar_data[j], self.bar_data[j + 1] = self.bar_data[j + 1], self.bar_data[j]
                    self.display_array(highlight=[j, j + 1])
                    self.step_label.config(text=f"Swapped elements at indices {j} and {j+1}.")
                    time.sleep(self.speed.get())
        self.display_array(highlight=list(range(len(self.bar_data))))
        self.info_label.config(text="Bubble Sort completed!")

    def selection_sort(self):
        n = len(self.bar_data)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if self.bar_data[j] < self.bar_data[min_idx]:
                    min_idx = j
            self.bar_data[i], self.bar_data[min_idx] = self.bar_data[min_idx], self.bar_data[i]
            self.display_array(highlight=[i, min_idx])
            self.step_label.config(text=f"Moved minimum element to index {i}.")
            time.sleep(self.speed.get())
        self.display_array(highlight=list(range(len(self.bar_data))))
        self.info_label.config(text="Selection Sort completed!")

    def insertion_sort(self):
        n = len(self.bar_data)
        for i in range(1, n):
            key = self.bar_data[i]
            j = i - 1
            while j >= 0 and self.bar_data[j] > key:
                self.bar_data[j + 1] = self.bar_data[j]
                j -= 1
                self.display_array(highlight=[j + 1, i])
                self.step_label.config(text=f"Inserted {key} into the sorted part of the array.")
                time.sleep(self.speed.get())
            self.bar_data[j + 1] = key
        self.display_array(highlight=list(range(len(self.bar_data))))
        self.info_label.config(text="Insertion Sort completed!")

    def quick_sort(self):
        def partition(low, high):
            pivot = self.bar_data[high]
            i = low - 1
            for j in range(low, high):
                if self.bar_data[j] < pivot:
                    i += 1
                    self.bar_data[i], self.bar_data[j] = self.bar_data[j], self.bar_data[i]
                    self.display_array(highlight=[i, j])
                    self.step_label.config(text=f"Swapped {self.bar_data[i]} and {self.bar_data[j]}.")
                    time.sleep(self.speed.get())
            self.bar_data[i + 1], self.bar_data[high] = self.bar_data[high], self.bar_data[i + 1]
            return i + 1

        def quick_sort_recursive(low, high):
            if low < high:
                pi = partition(low, high)
                quick_sort_recursive(low, pi - 1)
                quick_sort_recursive(pi + 1, high)

        quick_sort_recursive(0, len(self.bar_data) - 1)
        self.display_array(highlight=list(range(len(self.bar_data))))
        self.info_label.config(text="Quick Sort completed!")

#main
if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
