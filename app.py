"""
Root launcher for SalesPulse AI Streamlit Application.
Invokes Frontend/app.py seamlessly.
"""

import sys
import os

# Add root directory to sys.path to ensure relative package imports resolve
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Frontend.app import *
