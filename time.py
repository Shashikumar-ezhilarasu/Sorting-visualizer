import tkinter as tk
import random
import time
import threading


class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Visualizer")
        
        # Configuration for canvas size and speed
        self.canvas_width = 600
        self.canvas_height = 400
        self.bar_data = []
        self.speed = tk.DoubleVar(value=0.01)  # Default speed of sorting

        # Setting up the UI components
        self.setup_ui()

    def setup_ui(self):
        # Canvas for visualization
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # Controls for sorting algorithm and array
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack()

        self.generate_button = tk.Button(self.controls_frame, text="Generate Array", command=self.generate_data)
        self.generate_button.grid(row=0, column=0)

        self.sort_button = tk.Button(self.controls_frame, text="Start Sorting", command=self.start_sorting)
        self.sort_button.grid(row=0, column=1)

        self.speed_slider = tk.Scale(self.controls_frame, from_=0.001, to=0.1, orient="horizontal", variable=self.speed)
        self.speed_slider.grid(row=0, column=2)

        # Dropdown for selecting the sorting algorithm
        self.sort_algorithm = tk.StringVar(value="Bubble Sort")
        self.algorithm_dropdown = tk.OptionMenu(self.controls_frame, self.sort_algorithm, "Bubble Sort", "Merge Sort", "Quick Sort")
        self.algorithm_dropdown.grid(row=0, column=3)

        # Label for displaying time and space complexity
        self.complexity_label = tk.Label(self.root, text="Complexity: ", font=("Helvetica", 12))
        self.complexity_label.pack()

        # Label for step-by-step explanation
        self.step_label = tk.Label(self.root, text="Step-by-step explanation will appear here.", font=("Helvetica", 10))
        self.step_label.pack()

        # Label to display sorting process status
        self.info_label = tk.Label(self.root, text="Select algorithm and press 'Start Sorting'.", font=("Helvetica", 12))
        self.info_label.pack()

    def generate_data(self):
        self.bar_data = [random.randint(10, 100) for _ in range(50)]
        self.display_array()
        self.info_label.config(text="Array generated!")

    def display_array(self, highlight=None):
        self.canvas.delete("all")
        bar_width = self.canvas_width / len(self.bar_data)

        for i, value in enumerate(self.bar_data):
            x0 = i * bar_width
            y0 = self.canvas_height - value
            x1 = (i + 1) * bar_width
            y1 = self.canvas_height
            color = "blue" if highlight is None or i not in highlight else "red"
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def bubble_sort(self):
        n = len(self.bar_data)
        for i in range(n):
            for j in range(0, n - i - 1):
                self.display_array(highlight=[j, j + 1])
                time.sleep(self.speed.get())
                if self.bar_data[j] > self.bar_data[j + 1]:
                    self.bar_data[j], self.bar_data[j + 1] = self.bar_data[j + 1], self.bar_data[j]
                    self.display_array(highlight=[j, j + 1])
                    time.sleep(self.speed.get())
        self.display_array(highlight=list(range(len(self.bar_data))))
        self.info_label.config(text="Bubble Sort completed!")
        self.update_complexity("O(n²)", "O(1)")

    def merge_sort(self):
        def merge(left, right):
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            result.extend(left[i:])
            result.extend(right[j:])
            return result

        def merge_sort_recursive(arr):
            if len(arr) <= 1:
                return arr
            mid = len(arr) // 2
            left = merge_sort_recursive(arr[:mid])
            right = merge_sort_recursive(arr[mid:])
            return merge(left, right)

        self.bar_data = merge_sort_recursive(self.bar_data)
        self.display_array(highlight=list(range(len(self.bar_data))))
        self.info_label.config(text="Merge Sort completed!")
        self.update_complexity("O(n log n)", "O(n)")

    def quick_sort(self):
        def partition(low, high):
            pivot = self.bar_data[high]
            i = low - 1
            for j in range(low, high):
                if self.bar_data[j] <= pivot:
                    i += 1
                    self.bar_data[i], self.bar_data[j] = self.bar_data[j], self.bar_data[i]
                    self.display_array(highlight=[i, j])
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
        self.update_complexity("O(n log n)", "O(log n)")

    def start_sorting(self):
        selected_algorithm = self.sort_algorithm.get()
        if selected_algorithm == "Bubble Sort":
            threading.Thread(target=self.bubble_sort).start()
        elif selected_algorithm == "Merge Sort":
            threading.Thread(target=self.merge_sort).start()
        elif selected_algorithm == "Quick Sort":
            threading.Thread(target=self.quick_sort).start()

    def update_complexity(self, time_complexity, space_complexity):
        self.complexity_label.config(text=f"Time Complexity: {time_complexity}, Space Complexity: {space_complexity}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
