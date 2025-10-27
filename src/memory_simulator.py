import time
from collections import deque, OrderedDict
from algorithms import PageReplacementAlgorithms

class MemoryFrame:
    def __init__(self, frame_id):
        self.frame_id = frame_id
        self.page = None
        self.allocated = False
        self.last_accessed = 0
        self.reference_bit = 0
        self.load_time = 0
        self.access_count = 0
        
    def allocate(self, page, timestamp):
        self.page = page
        self.allocated = True
        self.last_accessed = timestamp
        self.reference_bit = 1
        self.load_time = timestamp
        self.access_count = 1
        
    def deallocate(self):
        old_page = self.page
        self.page = None
        self.allocated = False
        self.reference_bit = 0
        self.access_count = 0
        return old_page
        
    def access(self, timestamp):
        self.last_accessed = timestamp
        self.reference_bit = 1
        self.access_count += 1
        
    def clear_reference_bit(self):
        self.reference_bit = 0

class MemorySimulator:
    def __init__(self):
        self.num_frames = 4
        self.page_size = 1024
        self.memory_frames = []
        self.page_table = {}
        self.algorithm_handler = PageReplacementAlgorithms()
        self.reference_string = []
        self.history = []
        self.time_counter = 0
        self.reset()
        
    def initialize(self, num_frames, page_size, algorithm):
        self.num_frames = num_frames
        self.page_size = page_size
        self.algorithm = algorithm
        self.reset()
        
    def reset(self):
        self.memory_frames = [MemoryFrame(i) for i in range(self.num_frames)]
        self.page_table = {}
        self.history = []
        self.time_counter = 0
        self.page_faults = 0
        self.hits = 0
        
    def set_reference_string(self, ref_string):
        self.reference_string = ref_string
        
    def simulate_step(self, page):
        self.time_counter += 1
        step_info = {
            'step_number': self.time_counter,
            'page': page,
            'memory_state': [frame.page if frame.allocated else None for frame in self.memory_frames],
            'page_fault': False,
            'replaced_page': None,
            'frame_index': None,
            'action': 'Hit'
        }
        
        # Check if page is already in memory
        if page in self.page_table and self.page_table[page] is not None:
            frame_index = self.page_table[page]
            self.memory_frames[frame_index].access(self.time_counter)
            self.hits += 1
            step_info['action'] = 'Hit'
            step_info['frame_index'] = frame_index
        else:
            # Page fault occurred
            self.page_faults += 1
            step_info['page_fault'] = True
            step_info['action'] = 'Page Fault'
            
            # Find free frame
            free_frame_index = self.find_free_frame()
            
            if free_frame_index is not None:
                # Allocate to free frame
                frame_index = free_frame_index
                self.memory_frames[frame_index].allocate(page, self.time_counter)
                self.page_table[page] = frame_index
                step_info['frame_index'] = frame_index
            else:
                # Need to replace a page
                victim_frame_index = self.select_victim_frame()
                victim_frame = self.memory_frames[victim_frame_index]
                
                step_info['replaced_page'] = victim_frame.page
                step_info['frame_index'] = victim_frame_index
                
                # Remove old page from page table
                if victim_frame.page in self.page_table:
                    del self.page_table[victim_frame.page]
                
                # Deallocate victim frame and allocate new page
                victim_frame.deallocate()
                victim_frame.allocate(page, self.time_counter)
                self.page_table[page] = victim_frame_index
                
        # Record memory state for history
        current_state = {
            'time': self.time_counter,
            'page': page,
            'memory': [frame.page if frame.allocated else -1 for frame in self.memory_frames],
            'page_fault': step_info['page_fault'],
            'replaced_page': step_info['replaced_page']
        }
        self.history.append(current_state)
        
        return step_info
    
    def find_free_frame(self):
        for i, frame in enumerate(self.memory_frames):
            if not frame.allocated:
                return i
        return None
    
    def select_victim_frame(self):
        if self.algorithm == "FIFO":
            return self.algorithm_handler.fifo(self.memory_frames)
        elif self.algorithm == "LRU":
            return self.algorithm_handler.lru(self.memory_frames)
        elif self.algorithm == "OPTIMAL":
            return self.algorithm_handler.optimal(self.memory_frames, self.reference_string, self.time_counter)
        elif self.algorithm == "CLOCK":
            return self.algorithm_handler.clock(self.memory_frames, self.time_counter)
        elif self.algorithm == "RANDOM":
            return self.algorithm_handler.random_replacement(self.memory_frames)
        else:
            return self.algorithm_handler.fifo(self.memory_frames)
    
    def get_statistics(self):
        total_accesses = self.hits + self.page_faults
        hit_ratio = self.hits / total_accesses if total_accesses > 0 else 0
        fault_ratio = self.page_faults / total_accesses if total_accesses > 0 else 0
        
        # Calculate memory utilization
        allocated_frames = sum(1 for frame in self.memory_frames if frame.allocated)
        memory_utilization = allocated_frames / self.num_frames
        
        return {
            'total_accesses': total_accesses,
            'hits': self.hits,
            'page_faults': self.page_faults,
            'hit_ratio': hit_ratio,
            'fault_ratio': fault_ratio,
            'memory_utilization': memory_utilization,
            'algorithm': self.algorithm
        }
    
    def get_memory_state(self):
        return [{
            'frame_id': frame.frame_id,
            'page': frame.page,
            'allocated': frame.allocated,
            'last_accessed': frame.last_accessed,
            'reference_bit': frame.reference_bit,
            'access_count': frame.access_count
        } for frame in self.memory_frames]
    
    def get_page_table(self):
        return self.page_table.copy()
