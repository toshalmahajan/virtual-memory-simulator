#!/usr/bin/env python3
"""
Virtual Memory Management Simulator
Main executable file
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import start_application

if __name__ == "__main__":
    start_application()
