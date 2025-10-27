import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.figure import Figure
import numpy as np

class MemoryVisualizer:
    def __init__(self):
        self.colors = plt.cm.Set3(np.linspace(0, 1, 12))
        
    def plot_memory_state(self, fig, simulator):
        memory_frames = simulator.memory_frames
        current_step = simulator.time_counter
        total_steps = len(simulator.reference_string) if simulator.reference_string else 0
        
        # Create subplots
        gs = fig.add_gridspec(2, 2, width_ratios=[3, 1], height_ratios=[2, 1])
        
        # Main memory visualization
        ax1 = fig.add_subplot(gs[0, 0])
        self.plot_memory_frames(ax1, memory_frames, current_step)
        
        # Page table visualization
        ax2 = fig.add_subplot(gs[0, 1])
        self.plot_page_table(ax2, simulator.page_table)
        
        # Reference string progress
        ax3 = fig.add_subplot(gs[1, 0])
        self.plot_reference_progress(ax3, simulator.reference_string, current_step)
        
        # Statistics
        ax4 = fig.add_subplot(gs[1, 1])
        self.plot_statistics(ax4, simulator.get_statistics())
        
        fig.tight_layout()
        
    def plot_memory_frames(self, ax, memory_frames, current_step):
        ax.clear()
        ax.set_title(f'Memory Frames (Step: {current_step})', fontsize=14, fontweight='bold')
        
        num_frames = len(memory_frames)
        
        for i, frame in enumerate(memory_frames):
            x = i % 4
            y = i // 4
            
            # Draw frame rectangle
            color = self.colors[frame.page % len(self.colors)] if frame.allocated and frame.page is not None else 'lightgray'
            rect = patches.Rectangle((x, y), 0.8, 0.8, linewidth=2, 
                                   edgecolor='black', facecolor=color, alpha=0.8)
            ax.add_patch(rect)
            
            # Frame info
            if frame.allocated and frame.page is not None:
                ax.text(x + 0.4, y + 0.6, f'Page {frame.page}', 
                       ha='center', va='center', fontweight='bold', fontsize=12)
                ax.text(x + 0.4, y + 0.3, f'Frame {frame.frame_id}', 
                       ha='center', va='center', fontsize=10)
                ax.text(x + 0.4, y + 0.1, f'Ref: {frame.reference_bit}', 
                       ha='center', va='center', fontsize=9)
            else:
                ax.text(x + 0.4, y + 0.4, 'Free', 
                       ha='center', va='center', fontsize=11, style='italic')
        
        ax.set_xlim(0, 4)
        ax.set_ylim(0, (num_frames + 3) // 4)
        ax.set_aspect('equal')
        ax.axis('off')
        
    def plot_page_table(self, ax, page_table):
        ax.clear()
        ax.set_title('Page Table', fontsize=14, fontweight='bold')
        
        if not page_table:
            ax.text(0.5, 0.5, 'No pages loaded', 
                   ha='center', va='center', fontsize=12, style='italic')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            return
            
        pages = list(page_table.keys())
        frames = list(page_table.values())
        
        y_pos = np.arange(len(pages))
        
        ax.barh(y_pos, frames, color='skyblue', edgecolor='black')
        ax.set_yticks(y_pos)
        ax.set_yticklabels([f'Page {p}' for p in pages])
        ax.set_xlabel('Frame Number')
        ax.grid(axis='x', alpha=0.3)
        
        # Add frame numbers on bars
        for i, v in enumerate(frames):
            ax.text(v + 0.1, i, str(v), va='center', fontweight='bold')
            
    def plot_reference_progress(self, ax, reference_string, current_step):
        ax.clear()
        ax.set_title('Reference String Progress', fontsize=14, fontweight='bold')
        
        if not reference_string:
            ax.text(0.5, 0.5, 'No reference string set', 
                   ha='center', va='center', fontsize=12, style='italic')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            return
            
        x = np.arange(len(reference_string))
        colors = ['red' if i < current_step else 'gray' for i in range(len(reference_string))]
        
        bars = ax.bar(x, [1] * len(reference_string), color=colors, alpha=0.7)
        
        # Add page numbers on bars
        for i, (bar, page) in enumerate(zip(bars, reference_string)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height/2,
                   str(page), ha='center', va='center', fontweight='bold',
                   color='white' if i < current_step else 'black')
        
        ax.set_xlabel('Step')
        ax.set_ylabel('Page')
        ax.set_xticks(x)
        ax.set_yticks([])
        ax.set_ylim(0, 1.2)
        
    def plot_statistics(self, ax, statistics):
        ax.clear()
        ax.set_title('Performance Metrics', fontsize=14, fontweight='bold')
        
        if not statistics or statistics['total_accesses'] == 0:
            ax.text(0.5, 0.5, 'No data available', 
                   ha='center', va='center', fontsize=12, style='italic')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            return
            
        metrics = ['Hit Ratio', 'Fault Ratio']
        values = [statistics['hit_ratio'], statistics['fault_ratio']]
        colors = ['green', 'red']
        
        bars = ax.bar(metrics, values, color=colors, alpha=0.7, edgecolor='black')
        
        # Add percentage labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                   f'{value:.1%}', ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylabel('Ratio')
        ax.set_ylim(0, 1)
        ax.grid(axis='y', alpha=0.3)
        
        # Add additional info
        info_text = f"Total: {statistics['total_accesses']}\n"
        info_text += f"Hits: {statistics['hits']}\n"
        info_text += f"Faults: {statistics['page_faults']}\n"
        info_text += f"Algorithm: {statistics['algorithm']}"
        
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes, 
               va='top', ha='left', fontsize=10,
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
