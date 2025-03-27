"""
FireEye Main Entry Point

This script initializes the system, sets up components, and starts data collection.
"""

from imports import *
from component_manager import ComponentManager
from database_manager import DatabaseManager
from data_reader import DataReader
from diagnostics_checker import DiagnosticsCheck
from light_controller import LightController
from mode_controller import ModeController


def main():
    """Initializing classes"""
    components = ComponentManager()
    light = LightController(components)
    data_reader = DataReader(components)
    diagnostics = DiagnosticsCheck(components, data_reader)
    database = DatabaseManager()
    mode_controller = ModeController(components, data_reader, database)


if __name__ == "__main__":
    main()