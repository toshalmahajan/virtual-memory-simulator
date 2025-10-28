# Virtual Memory Management Simulator

## 🎓 Academic Project - LPU CSE 234 Operating Systems

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Algorithms Implemented](#algorithms-implemented)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [GitHub Repository](#github-repository)
- [Contributors](#contributors)
- [Course Information](#course-information)
- [License](#license)

## 🎯 Project Overview

The **Virtual Memory Management Simulator** is an educational tool developed for **Lovely Professional University's CSE 234 - Operating Systems** course. This interactive application demonstrates core virtual memory concepts including paging, segmentation, page replacement algorithms, and memory fragmentation analysis.

### Key Objectives:
- Visualize virtual memory management concepts in real-time
- Provide hands-on experience with page replacement algorithms
- Demonstrate segmentation and fragmentation analysis
- Offer comparative analysis of algorithm performance

## ✨ Features

### 🖥️ Paging System
- **Multiple Page Replacement Algorithms**: FIFO, LRU, Optimal, Clock, Random
- **Real-time Visualization**: Color-coded memory frames and page tables
- **Page Fault Tracking**: Detailed monitoring of page faults and hits
- **Demand Paging**: Simulate on-demand page loading
- **Customizable Parameters**: Configurable memory frames and page sizes

### 📊 Segmentation System
- **Segment-based Memory Allocation**: Visual segment management
- **Fragmentation Analysis**: Internal and external fragmentation tracking
- **Segment Tables**: Real-time segment table visualization
- **Process Allocation**: Simulate process memory requirements

### 🎮 User Interface
- **Interactive GUI**: Built with Tkinter and Matplotlib
- **Step-by-Step Execution**: Controlled simulation progression
- **Auto-play Mode**: Automated simulation demonstration
- **Performance Metrics**: Real-time statistics and analytics
- **Algorithm Comparison**: Side-by-side performance analysis

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step Installation

```bash
# 1. Clone the repository
git clone https://github.com/toshalmahajan/virtual-memory-simulator.git
cd virtual-memory-simulator

# 2. Install required dependencies
pip install -r requirements.txt

# 3. Run the application
python run.py
Dependencies
All dependencies are listed in requirements.txt:

matplotlib>=3.5.0 - Data visualization and plotting

numpy>=1.21.0 - Numerical operations

💻 Usage
Starting the Application
bash
python run.py
Basic Operation
Configure Parameters:

Set number of memory frames

Select page replacement algorithm

Define reference string or generate randomly

Run Simulation:

Use Step Forward for controlled execution

Use Run All for complete simulation

Use Auto Play for automated demonstration

Analyze Results:

View real-time memory state

Monitor performance statistics

Compare algorithm efficiency

Example Reference Strings
1,2,3,4,1,2,5,1,2,3,4,5 - Classic Belady's Anomaly example

7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1 - Standard test pattern

🧠 Algorithms Implemented
Page Replacement Algorithms
Algorithm	Complexity	Description
FIFO	O(1)	First-In-First-Out replacement
LRU	O(n)	Least Recently Used replacement
Optimal	O(n²)	Future knowledge-based replacement
Clock	O(1) amortized	Second chance algorithm
Random	O(1)	Random page selection
Segmentation Features
Segment table management

Internal fragmentation calculation

External fragmentation analysis

Process allocation simulation

📁 Project Structure
text
virtual-memory-simulator/
├── src/
│   ├── main.py                 # Main GUI application
│   ├── memory_simulator.py     # Core memory management
│   ├── algorithms.py           # Page replacement algorithms
│   ├── visualization.py        # Matplotlib visualizations
│   ├── segmentation.py         # Segmentation system
│   └── utils.py               # Utility functions
├── tests/
│   ├── test_algorithms.py      # Algorithm unit tests
│   └── test_simulator.py       # Simulator functionality tests
├── docs/
│   └── README.md              # Detailed documentation
├── requirements.txt           # Python dependencies
├── .gitignore                # Git configuration
└── run.py                    # Application launcher

Paging System Interface

Memory frames visualization

Page table display

Algorithm performance metrics

Segmentation System Interface

Segment memory layout

Fragmentation analysis

Process allocation view

🔗 GitHub Repository
Repository: virtual-memory-simulator

Commit History
The project maintains a comprehensive commit history with 7+ meaningful commits:

Initial commit: Complete virtual memory simulator with paging and segmentation systems

feat: Implement FIFO, LRU, Optimal page replacement algorithms

feat: Add memory frame management and page fault tracking

feat: Implement real-time memory visualization with Matplotlib

feat: Add segmentation system with fragmentation analysis

feat: Implement interactive GUI with tabs and controls

test: Add unit tests and comprehensive documentation

👥 Contributors
Toshal Mahajan - Developer - GitHub Profile

🎓 Course Information
Course: CSE 234 - Operating Systems

University: Lovely Professional University

Learning Outcomes
This project demonstrates understanding of:

Virtual memory management concepts

Page replacement algorithms

Segmentation and paging systems

Memory fragmentation analysis

GUI application development

📄 License
This project is developed for educational purposes as part of the LPU CSE 234 course requirements.

🤝 Contributing
While this is an academic project, suggestions and improvements are welcome. Please feel free to fork the repository and submit pull requests.


Email: toshalmahajan11@gmail.com

GitHub Issues: Create an issue

Developed with ❤️ for LPU CSE 234 - Operating Systems
