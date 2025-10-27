import json
import datetime
import matplotlib.pyplot as plt
import os

def save_simulation_results(simulator, filename=None):
    """Save simulation results to JSON file"""
    if filename is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"simulation_results_{timestamp}.json"
    
    results = {
        'timestamp': datetime.datetime.now().isoformat(),
        'configuration': {
            'num_frames': simulator.num_frames,
            'page_size': simulator.page_size,
            'algorithm': simulator.algorithm,
            'reference_string': simulator.reference_string
        },
        'statistics': simulator.get_statistics(),
        'history': simulator.history,
        'final_memory_state': simulator.get_memory_state(),
        'page_table': simulator.get_page_table()
    }
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
        
    return filename

def load_simulation_results(filename):
    """Load simulation results from JSON file"""
    with open(filename, 'r') as f:
        return json.load(f)

def generate_performance_report(simulator, algorithms=None):
    """Generate comparative performance report for multiple algorithms"""
    if algorithms is None:
        algorithms = ["FIFO", "LRU", "OPTIMAL", "CLOCK"]
    
    report = {
        'timestamp': datetime.datetime.now().isoformat(),
        'configuration': {
            'num_frames': simulator.num_frames,
            'page_size': simulator.page_size,
            'reference_string': simulator.reference_string
        },
        'comparison': {}
    }
    
    from memory_simulator import MemorySimulator
    
    for algo in algorithms:
        temp_simulator = MemorySimulator()
        temp_simulator.initialize(simulator.num_frames, simulator.page_size, algo)
        temp_simulator.set_reference_string(simulator.reference_string)
        
        # Run simulation
        for page in temp_simulator.reference_string:
            temp_simulator.simulate_step(page)
            
        report['comparison'][algo] = temp_simulator.get_statistics()
    
    return report

def plot_algorithm_comparison(report, save_path=None):
    """Create visualization comparing algorithm performance"""
    algorithms = list(report['comparison'].keys())
    fault_rates = [report['comparison'][algo]['fault_ratio'] for algo in algorithms]
    hit_rates = [report['comparison'][algo]['hit_ratio'] for algo in algorithms]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Page faults comparison
    bars1 = ax1.bar(algorithms, fault_rates, color='lightcoral', edgecolor='darkred')
    ax1.set_title('Page Fault Rates by Algorithm', fontweight='bold')
    ax1.set_ylabel('Fault Ratio')
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.1%}', ha='center', va='bottom')
    
    # Hit rates comparison
    bars2 = ax2.bar(algorithms, hit_rates, color='lightgreen', edgecolor='darkgreen')
    ax2.set_title('Hit Rates by Algorithm', fontweight='bold')
    ax2.set_ylabel('Hit Ratio')
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.1%}', ha='center', va='bottom')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def create_results_directory():
    """Create directory for saving simulation results"""
    results_dir = "simulation_results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    return results_dir
