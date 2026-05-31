# HardSurface Pro - Procedural Hard-Surface Generation Addon for Blender
# Copyright (C) 2024 HardSurface Pro Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

"""
Logging utilities for debugging and development.
Provides simple logging functionality for the addon.
"""

import sys


class Logger:
    """Simple logger for addon debugging."""
    
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    
    level = INFO
    
    @staticmethod
    def set_level(level: int):
        """Set the logging level."""
        Logger.level = level
    
    @staticmethod
    def debug(message: str):
        """Log a debug message."""
        if Logger.level <= Logger.DEBUG:
            print(f"[HS DEBUG] {message}")
    
    @staticmethod
    def info(message: str):
        """Log an info message."""
        if Logger.level <= Logger.INFO:
            print(f"[HS INFO] {message}")
    
    @staticmethod
    def warning(message: str):
        """Log a warning message."""
        if Logger.level <= Logger.WARNING:
            print(f"[HS WARNING] {message}", file=sys.stderr)
    
    @staticmethod
    def error(message: str):
        """Log an error message."""
        if Logger.level <= Logger.ERROR:
            print(f"[HS ERROR] {message}", file=sys.stderr)
