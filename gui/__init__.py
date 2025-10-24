"""
GUI Package
-----------
Contains all Tkinter window and page classes for the CPU Scheduling Simulator.
"""

from .welcome_page import WelcomePage
from .menu_page import MenuPage
from .lrjf_page import LRJFPage
from .rr_page import RRPage
from .srjf_page import SRJFPage
from .battle_royal_page import BattleRoyalPage

__all__ = ["WelcomePage", "MenuPage", "LRJFPage", "RRPage", "SRJFPage", "BattleRoyalPage"]