import tkinter as tk
from tkinter import ttk
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

class Segment:
    def __init__(self, segment_id, base, limit, name=""):
        self.segment_id = segment_id
        self.base = base
        self.limit = limit
        self.name = name
        self.allocated = False
        self.process_id = None
        
    def allocate(self, process_id, size):
        if size <= self.limit:
            self.allocated = True
            self.process_id = process_id
            return True
        return False
        
    def deallocate(self):
        self.allocated = False
        self.process_id = None

class SegmentationSimulator:
    def __init__(self, total_memory=1024):
        self.total_memory = total_memory
        self.segments = []
        self.segment_table = {}
        self.fragmentation_history = []
        
    def initialize_segments(self, segment_sizes, segment_names=None):
        self.segments = []
        base = 0
        
        for i, size in enumerate(segment_sizes):
            name = segment_names[i] if segment_names else f"Seg_{i}"
            segment = Segment(i, base, size, name)
            self.segments.append(segment)
            base += size
            
    def allocate_process(self, process_id, segment_requirements):
        """Allocate segments to a process"""
        allocations = {}
        
        for seg_name, size in segment_requirements.items():
            for segment in self.segments:
                if not segment.allocated and segment.limit >= size:
                    if segment.allocate(process_id, size):
                        allocations[seg_name] = segment.segment_id
                        self.segment_table[f"{process_id}_{seg_name}"] = {
                            'segment_id': segment.segment_id,
                            'base': segment.base,
                            'limit': segment.limit
                        }
                        break
        
        return allocations
    
    def calculate_fragmentation(self):
        """Calculate internal and external fragmentation"""
        total_allocated = 0
        internal_frag = 0
        external_frag = 0
        
        for segment in self.segments:
            if segment.allocated:
                total_allocated += segment.limit
                # Internal fragmentation: allocated but unused space within segment
                internal_frag += segment.limit * 0.1  # Estimate 10% internal fragmentation
            else:
                external_frag += segment.limit
                
        return {
            'internal_fragmentation': internal_frag,
            'external_fragmentation': external_frag,
            'total_fragmentation': internal_frag + external_frag
        }

class SegmentationVisualizer:
    def __init__(self):
        self.colors = plt.cm.tab10(np.linspace(0, 1, 10))
        
    def plot_segmentation_memory(self, fig, simulator):
        ax = fig.add_subplot(111)
        ax.clear()
        ax.set_title('Segmentation Memory Layout', fontsize=16, fontweight='bold')
        
        memory_usage = []
        current_base = 0
        
        for segment in simulator.segments:
            color = 'red' if segment.allocated else 'lightgreen'
            memory_usage.append({
                'base': segment.base,
                'limit': segment.limit,
                'allocated': segment.allocated,
                'name': segment.name,
                'process': segment.process_id
            })
            
            # Draw segment rectangle
            rect = patches.Rectangle(
                (0, segment.base), 1, segment.limit,
                linewidth=2, edgecolor='black', facecolor=color, alpha=0.7
            )
            ax.add_patch(rect)
            
            # Segment info text
            status = f"P{segment.process_id}" if segment.allocated else "Free"
            ax.text(0.5, segment.base + segment.limit/2, 
                   f"{segment.name}\n{status}\n{segment.limit}KB", 
                   ha='center', va='center', fontweight='bold', fontsize=10)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, simulator.total_memory)
        ax.set_xlabel('Segments')
        ax.set_ylabel('Memory Address Space (KB)')
        ax.set_xticks([])
        
        # Add fragmentation info
        frag_info = simulator.calculate_fragmentation()
        ax.text(0.02, 0.98, 
               f"Internal Frag: {frag_info['internal_fragmentation']:.1f}KB\n"
               f"External Frag: {frag_info['external_fragmentation']:.1f}KB\n"
               f"Total Frag: {frag_info['total_fragmentation']:.1f}KB",
               transform=ax.transAxes, va='top', fontsize=11,
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    def plot_segment_table(self, fig, segment_table):
        ax = fig.add_subplot(111)
        ax.clear()
        ax.set_title('Segment Table', fontsize=14, fontweight='bold')
        
        if not segment_table:
            ax.text(0.5, 0.5, 'No segments allocated', 
                   ha='center', va='center', fontsize=12, style='italic')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            return
            
        rows = []
        for key, value in segment_table.items():
            process_seg = key.split('_')
            rows.append([process_seg[0], process_seg[1], value['segment_id'], 
                        value['base'], value['limit']])
        
        # Create table
        table = ax.table(cellText=rows,
                        colLabels=['Process', 'Segment', 'ID', 'Base', 'Limit'],
                        cellLoc='center',
                        loc='center')
        
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)
        
        ax.axis('off')
