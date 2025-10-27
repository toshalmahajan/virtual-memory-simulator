import random
from collections import deque

class PageReplacementAlgorithms:
    def __init__(self):
        self.clock_pointer = 0
        
    def fifo(self, memory_frames):
        """First-In-First-Out page replacement"""
        oldest_time = float('inf')
        victim_frame = 0
        
        for i, frame in enumerate(memory_frames):
            if frame.load_time < oldest_time:
                oldest_time = frame.load_time
                victim_frame = i
                
        return victim_frame
    
    def lru(self, memory_frames):
        """Least Recently Used page replacement"""
        oldest_time = float('inf')
        victim_frame = 0
        
        for i, frame in enumerate(memory_frames):
            if frame.last_accessed < oldest_time:
                oldest_time = frame.last_accessed
                victim_frame = i
                
        return victim_frame
    
    def optimal(self, memory_frames, reference_string, current_time):
        """Optimal page replacement (requires future knowledge)"""
        future_uses = {}
        
        for i, frame in enumerate(memory_frames):
            page = frame.page
            # Find next use of this page in reference string
            next_use = float('inf')
            
            for j in range(current_time, len(reference_string)):
                if reference_string[j] == page:
                    next_use = j
                    break
                    
            future_uses[i] = next_use
        
        # Select frame with largest next use time (or never used again)
        victim_frame = max(future_uses, key=future_uses.get)
        return victim_frame
    
    def clock(self, memory_frames, current_time):
        """Clock (Second Chance) page replacement"""
        while True:
            frame = memory_frames[self.clock_pointer]
            
            if frame.reference_bit == 0:
                victim = self.clock_pointer
                self.clock_pointer = (self.clock_pointer + 1) % len(memory_frames)
                return victim
            else:
                frame.clear_reference_bit()
                self.clock_pointer = (self.clock_pointer + 1) % len(memory_frames)
    
    def random_replacement(self, memory_frames):
        """Random page replacement"""
        return random.randint(0, len(memory_frames) - 1)
    
    def lfu(self, memory_frames):
        """Least Frequently Used page replacement"""
        min_access_count = float('inf')
        victim_frame = 0
        
        for i, frame in enumerate(memory_frames):
            if frame.access_count < min_access_count:
                min_access_count = frame.access_count
                victim_frame = i
                
        return victim_frame
    
    def mfu(self, memory_frames):
        """Most Frequently Used page replacement"""
        max_access_count = -1
        victim_frame = 0
        
        for i, frame in enumerate(memory_frames):
            if frame.access_count > max_access_count:
                max_access_count = frame.access_count
                victim_frame = i
                
        return victim_frame
