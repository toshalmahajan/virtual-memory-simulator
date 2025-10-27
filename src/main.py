import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
from collections import deque
import time
from memory_simulator import MemorySimulator
from algorithms import PageReplacementAlgorithms
from visualization import MemoryVisualizer
from segmentation import SegmentationSimulator, SegmentationVisualizer

class VirtualMemoryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Virtual Memory Management Simulator - LPU CSE 234")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize simulators
        self.simulator = MemorySimulator()
        self.visualizer = MemoryVisualizer()
        self.seg_simulator = SegmentationSimulator()
        self.seg_visualizer = SegmentationVisualizer()
        
        # Current step tracking
        self.current_step = 0
        self.auto_play = False
        
        self.setup_gui()
        self.apply_initial_config()
        
    def setup_gui(self):
        # Create main paned window for resizable sections
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_paned)
        main_paned.add(self.notebook, weight=2)
        
        # Right frame for statistics and history
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=1)
        
        # Create tabs
        self.setup_paging_tab()
        self.setup_segmentation_tab()
        self.setup_statistics_panel(right_frame)
        self.setup_history_panel(right_frame)
        
    def setup_paging_tab(self):
        # Paging Tab
        paging_frame = ttk.Frame(self.notebook)
        self.notebook.add(paging_frame, text="📄 Paging System")
        
        # Control panel for paging
        control_frame = ttk.LabelFrame(paging_frame, text="Paging Controls", padding="15")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Top control row
        top_frame = ttk.Frame(control_frame)
        top_frame.pack(fill=tk.X, pady=5)
        
        # Memory configuration
        ttk.Label(top_frame, text="Memory Frames:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.frames_var = tk.StringVar(value="4")
        ttk.Entry(top_frame, textvariable=self.frames_var, width=8).grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(top_frame, text="Page Size:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.page_size_var = tk.StringVar(value="1024")
        ttk.Entry(top_frame, textvariable=self.page_size_var, width=10).grid(row=0, column=3, padx=(0, 20))
        
        # Algorithm selection
        ttk.Label(top_frame, text="Algorithm:").grid(row=0, column=4, sticky=tk.W, padx=(0, 10))
        self.algorithm_var = tk.StringVar(value="FIFO")
        algorithms = ["FIFO", "LRU", "OPTIMAL", "CLOCK", "RANDOM"]
        algo_combo = ttk.Combobox(top_frame, textvariable=self.algorithm_var, 
                                 values=algorithms, state="readonly", width=12)
        algo_combo.grid(row=0, column=5, padx=(0, 20))
        
        # Middle control row
        mid_frame = ttk.Frame(control_frame)
        mid_frame.pack(fill=tk.X, pady=5)
        
        # Reference string configuration
        ttk.Label(mid_frame, text="Reference String:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.ref_string_var = tk.StringVar(value="1,2,3,4,1,2,5,1,2,3,4,5")
        ref_entry = ttk.Entry(mid_frame, textvariable=self.ref_string_var, width=40)
        ref_entry.grid(row=0, column=1, columnspan=3, sticky=tk.W+tk.E, padx=(0, 20))
        
        # Reference string generation
        ttk.Label(mid_frame, text="Max Page:").grid(row=0, column=4, sticky=tk.W, padx=(0, 10))
        self.max_page_var = tk.StringVar(value="7")
        ttk.Entry(mid_frame, textvariable=self.max_page_var, width=8).grid(row=0, column=5, padx=(0, 10))
        
        ttk.Label(mid_frame, text="Length:").grid(row=0, column=6, sticky=tk.W, padx=(0, 10))
        self.length_var = tk.StringVar(value="15")
        ttk.Entry(mid_frame, textvariable=self.length_var, width=8).grid(row=0, column=7, padx=(0, 20))
        
        # Bottom control row - buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        buttons = [
            ("Generate Random", self.generate_random),
            ("Apply Config", self.apply_config),
            ("Reset", self.reset_simulation),
            ("Step Forward", self.step_forward),
            ("Run All", self.run_all),
            ("Auto Play", self.toggle_auto_play),
            ("Compare Algorithms", self.compare_algorithms)
        ]
        
        for i, (text, command) in enumerate(buttons):
            ttk.Button(button_frame, text=text, command=command).grid(
                row=0, column=i, padx=5, sticky=tk.W+tk.E)
        
        button_frame.columnconfigure(tuple(range(len(buttons))), weight=1)
        
        # Paging visualization
        viz_frame = ttk.LabelFrame(paging_frame, text="Paging Visualization", padding="10")
        viz_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create matplotlib figure for paging
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def setup_segmentation_tab(self):
        # Segmentation Tab
        segmentation_frame = ttk.Frame(self.notebook)
        self.notebook.add(segmentation_frame, text="📊 Segmentation System")
        
        # Segmentation controls
        seg_control_frame = ttk.LabelFrame(segmentation_frame, text="Segmentation Controls", padding="10")
        seg_control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Segment configuration
        ttk.Label(seg_control_frame, text="Segment Sizes (KB, comma-separated):").grid(row=0, column=0, sticky=tk.W)
        self.seg_sizes_var = tk.StringVar(value="64,128,256,128,64")
        ttk.Entry(seg_control_frame, textvariable=self.seg_sizes_var, width=30).grid(row=0, column=1, padx=5)
        
        ttk.Button(seg_control_frame, text="Initialize Segments", 
                  command=self.initialize_segments).grid(row=0, column=2, padx=5)
        
        # Process allocation
        ttk.Label(seg_control_frame, text="Process Requirements (name:size):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.process_req_var = tk.StringVar(value="Code:32,Data:64,Stack:16")
        ttk.Entry(seg_control_frame, textvariable=self.process_req_var, width=30).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(seg_control_frame, text="Allocate Process", 
                  command=self.allocate_process).grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Button(seg_control_frame, text="Deallocate All", 
                  command=self.deallocate_all).grid(row=1, column=3, padx=5, pady=5)
        
        # Segmentation visualization
        seg_viz_frame = ttk.LabelFrame(segmentation_frame, text="Segmentation Visualization", padding="10")
        seg_viz_frame.pack(fill=tk.BOTH, expand=True)
        
        self.seg_fig = Figure(figsize=(10, 6), dpi=100)
        self.seg_canvas = FigureCanvasTkAgg(self.seg_fig, seg_viz_frame)
        self.seg_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def setup_statistics_panel(self, parent):
        stats_frame = ttk.LabelFrame(parent, text="Real-time Statistics", padding="10")
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create text widget for statistics
        self.stats_text = scrolledtext.ScrolledText(stats_frame, width=35, height=15, font=('Consolas', 10))
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
    def setup_history_panel(self, parent):
        history_frame = ttk.LabelFrame(parent, text="Simulation History", padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create text widget for history
        self.history_text = scrolledtext.ScrolledText(history_frame, width=35, height=15, font=('Consolas', 9))
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
    def apply_initial_config(self):
        self.apply_config()
        
    def generate_random(self):
        try:
            max_page = int(self.max_page_var.get())
            length = int(self.length_var.get())
            ref_string = [random.randint(1, max_page) for _ in range(length)]
            self.ref_string_var.set(','.join(map(str, ref_string)))
        except ValueError:
            messagebox.showerror("Error", "Invalid max page or length value!")
            
    def apply_config(self):
        try:
            num_frames = int(self.frames_var.get())
            page_size = int(self.page_size_var.get())
            algorithm = self.algorithm_var.get()
            ref_string = [int(x.strip()) for x in self.ref_string_var.get().split(',')]
            
            self.simulator.initialize(num_frames, page_size, algorithm)
            self.simulator.set_reference_string(ref_string)
            
            self.current_step = 0
            self.update_display()
            messagebox.showinfo("Success", "Paging configuration applied successfully!")
            
        except ValueError as e:
            messagebox.showerror("Error", "Invalid input values! Please check your inputs.")
            
    def initialize_segments(self):
        try:
            sizes = [int(x.strip()) for x in self.seg_sizes_var.get().split(',')]
            total_memory = sum(sizes) * 2  # Double for visualization space
            self.seg_simulator = SegmentationSimulator(total_memory)
            self.seg_simulator.initialize_segments(sizes)
            self.update_segmentation_display()
            messagebox.showinfo("Success", f"Segments initialized: {sizes}")
        except ValueError:
            messagebox.showerror("Error", "Invalid segment sizes!")
            
    def allocate_process(self):
        try:
            requirements = {}
            for req in self.process_req_var.get().split(','):
                name, size = req.split(':')
                requirements[name.strip()] = int(size.strip())
            
            process_id = len(self.seg_simulator.segment_table) // 3 + 1
            allocations = self.seg_simulator.allocate_process(process_id, requirements)
            
            if allocations:
                messagebox.showinfo("Success", f"Process {process_id} allocated segments: {allocations}")
            else:
                messagebox.showwarning("Warning", "Could not allocate all required segments!")
                
            self.update_segmentation_display()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid process requirements: {e}")
            
    def deallocate_all(self):
        self.seg_simulator = SegmentationSimulator(self.seg_simulator.total_memory)
        sizes = [int(x.strip()) for x in self.seg_sizes_var.get().split(',')]
        self.seg_simulator.initialize_segments(sizes)
        self.update_segmentation_display()
        messagebox.showinfo("Success", "All processes deallocated!")
            
    def reset_simulation(self):
        self.simulator.reset()
        self.current_step = 0
        self.auto_play = False
        self.update_display()
        self.history_text.delete(1.0, tk.END)
        
    def step_forward(self):
        if self.current_step < len(self.simulator.reference_string):
            page = self.simulator.reference_string[self.current_step]
            step_info = self.simulator.simulate_step(page)
            self.log_step(step_info)
            self.current_step += 1
            self.update_display()
        else:
            messagebox.showinfo("Simulation Complete", "All steps have been executed!")
            
    def run_all(self):
        self.reset_simulation()
        total_steps = len(self.simulator.reference_string)
        
        for i in range(total_steps):
            page = self.simulator.reference_string[i]
            step_info = self.simulator.simulate_step(page)
            self.log_step(step_info)
            
        self.current_step = total_steps
        self.update_display()
        messagebox.showinfo("Simulation Complete", f"Executed all {total_steps} steps!")
        
    def toggle_auto_play(self):
        self.auto_play = not self.auto_play
        if self.auto_play:
            self.auto_play_step()
            
    def auto_play_step(self):
        if self.auto_play and self.current_step < len(self.simulator.reference_string):
            self.step_forward()
            self.root.after(1000, self.auto_play_step)  # 1 second delay
            
    def compare_algorithms(self):
        if not self.simulator.reference_string:
            messagebox.showwarning("Warning", "Please set a reference string first!")
            return
            
        algorithms = ["FIFO", "LRU", "OPTIMAL", "CLOCK"]
        results = {}
        
        original_algorithm = self.simulator.algorithm
        
        for algo in algorithms:
            # Create temporary simulator for comparison
            temp_simulator = MemorySimulator()
            temp_simulator.initialize(
                int(self.frames_var.get()),
                int(self.page_size_var.get()),
                algo
            )
            temp_simulator.set_reference_string(self.simulator.reference_string)
            
            # Run complete simulation
            for page in temp_simulator.reference_string:
                temp_simulator.simulate_step(page)
                
            stats = temp_simulator.get_statistics()
            results[algo] = stats
            
        # Display comparison results
        comparison_window = tk.Toplevel(self.root)
        comparison_window.title("Algorithm Comparison")
        comparison_window.geometry("600x400")
        
        text_widget = scrolledtext.ScrolledText(comparison_window, width=70, height=20)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget.insert(tk.END, "ALGORITHM COMPARISON RESULTS\n")
        text_widget.insert(tk.END, "=" * 50 + "\n\n")
        
        for algo, stats in results.items():
            text_widget.insert(tk.END, f"{algo}:\n")
            text_widget.insert(tk.END, f"  Page Faults: {stats['page_faults']}\n")
            text_widget.insert(tk.END, f"  Hit Ratio: {stats['hit_ratio']:.2%}\n")
            text_widget.insert(tk.END, f"  Fault Ratio: {stats['fault_ratio']:.2%}\n\n")
            
    def log_step(self, step_info):
        timestamp = f"Step {step_info['step_number']:02d}"
        page = step_info['page']
        action = step_info['action']
        
        log_entry = f"{timestamp}: Page {page} - {action}"
        
        if step_info['page_fault']:
            if step_info.get('replaced_page') is not None:
                log_entry += f" (Replaced page {step_info['replaced_page']} in frame {step_info['frame_index']})"
            else:
                log_entry += f" (Loaded in frame {step_info['frame_index']})"
                
        log_entry += "\n"
        
        self.history_text.insert(tk.END, log_entry)
        self.history_text.see(tk.END)
        
    def update_display(self):
        # Clear previous figure
        self.fig.clear()
        
        # Update visualization
        self.visualizer.plot_memory_state(self.fig, self.simulator)
        
        # Update statistics
        stats = self.simulator.get_statistics()
        self.update_statistics_display(stats)
        
        # Refresh canvas
        self.canvas.draw()
        
    def update_segmentation_display(self):
        self.seg_fig.clear()
        self.seg_visualizer.plot_segmentation_memory(self.seg_fig, self.seg_simulator)
        self.seg_canvas.draw()
        
    def update_statistics_display(self, stats):
        self.stats_text.delete(1.0, tk.END)
        
        self.stats_text.insert(tk.END, "CURRENT SIMULATION STATUS\n")
        self.stats_text.insert(tk.END, "=" * 30 + "\n\n")
        
        self.stats_text.insert(tk.END, f"Algorithm: {self.simulator.algorithm}\n")
        self.stats_text.insert(tk.END, f"Memory Frames: {self.simulator.num_frames}\n")
        self.stats_text.insert(tk.END, f"Page Size: {self.simulator.page_size} bytes\n\n")
        
        self.stats_text.insert(tk.END, "PERFORMANCE METRICS\n")
        self.stats_text.insert(tk.END, "-" * 20 + "\n")
        self.stats_text.insert(tk.END, f"Total Accesses: {stats['total_accesses']}\n")
        self.stats_text.insert(tk.END, f"Page Hits: {stats['hits']}\n")
        self.stats_text.insert(tk.END, f"Page Faults: {stats['page_faults']}\n")
        self.stats_text.insert(tk.END, f"Hit Ratio: {stats['hit_ratio']:.2%}\n")
        self.stats_text.insert(tk.END, f"Fault Ratio: {stats['fault_ratio']:.2%}\n\n")
        
        # Current progress
        if len(self.simulator.reference_string) > 0:
            progress = self.current_step / len(self.simulator.reference_string) * 100
            self.stats_text.insert(tk.END, f"Progress: {progress:.1f}%\n")
            self.stats_text.insert(tk.END, f"Steps: {self.current_step}/{len(self.simulator.reference_string)}\n")

def start_application():
    root = tk.Tk()
    app = VirtualMemoryGUI(root)
    root.mainloop()

if __name__ == "__main__":
    start_application()
