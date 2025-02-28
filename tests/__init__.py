"""
Tests package initialization.
"""
import os
import sys

# Add the project root to the Python path
# This ensures imports from the app package work correctly
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
