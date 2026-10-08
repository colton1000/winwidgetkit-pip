from .core import WidgetApp,DesktopWidget,set_default_color,get_default_color
from .clock import AnalogClockWidget
from .stopwatch import StopwatchWidget
from .calendar_widget import CalendarWidget
from .shortcut import ShortcutWidget
from .orbs import FocusOrbWidget,MagicOrbWidget
from .notes import NoteWidget
from .group import CombinedWidget
from .custom import CustomWidget,ScriptWidget
__version__="0.6.0"
__all__=["WidgetApp","DesktopWidget","AnalogClockWidget","StopwatchWidget","CalendarWidget","ShortcutWidget","FocusOrbWidget","MagicOrbWidget","NoteWidget","CombinedWidget","CustomWidget","ScriptWidget","set_default_color","get_default_color"]
