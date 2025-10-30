"""
GUI Package
-----------
Contains all Tkinter window and page classes for the CPU Scheduling Simulator.
"""

"""
GUI Package
-----------
Contains all Tkinter window and page classes for the CPU Scheduling Simulator.

This package re-exports page classes for `from gui import <Page>` usage. The
shared `ScrollableFrame` widget lives in `gui.scrollable_frame` and is also
exported here for backwards-compatibility.
"""

# Export the scrollable frame from its own submodule first (safe — it does not
# import `gui`, so this avoids circular imports when pages import the widget).
from .scrollable_frame import ScrollableFrame

from .welcome_page import WelcomePage
from .menu_page import MenuPage
from .fcfs_page import FCFSPage
from .lrjf_page import LRJFPage
from .rr_page import RRPage
from .srjf_page import SRJFPage
from .battle_royal_page import BattleRoyalPage
from .sjf_page import SJFPage

__all__ = [
    "WelcomePage",
    "MenuPage",
    "FCFSPage",
    "LRJFPage",
    "RRPage",
    "SRJFPage",
    "BattleRoyalPage",
    "SJFPage",
    "ScrollableFrame",
]
