# WinWidgetKit 0.6.0

## Install on Windows

Extract the ZIP, then double-click `install_windows.bat`. After installation, use `run_demo.bat`.

## New features

- Calendar holidays: right-click the calendar, select **Add holiday**, enter `YYYY-MM-DD`, a name, and a custom date color. Holiday dates show a star and reveal their name when hovered.
- Notes: yellow by default, autosaves while typing, supports a configurable maximum of 1 to 100 notes, previous/next switching, adding and deleting notes, and responsive text space. At 560 pixels wide or larger, two notes appear side by side.
- Magic Orb: click the orb or **Ask the Orb** to receive a random YES or NO answer.

## Retained features

Clock numbers and alarms, stopwatch and laps, resizable widgets, shortcut widget, Focus Orb, CombinedWidget, CustomWidget, ScriptWidget, colors, two-second right-click color picker, always-on-top, persistence, and closing activity logs.

## Example

```python
from winwidgetkit import WidgetApp, CalendarWidget, NoteWidget, MagicOrbWidget

app = WidgetApp(app_name="My Dashboard")
CalendarWidget(app, widget_id="calendar", holidays={
    "2026-12-25": {"name": "Holiday", "color": "#dc2626"}
})
NoteWidget(app, widget_id="notes", x=380, max_notes=10)
MagicOrbWidget(app, widget_id="magic", x=750)
app.run()
```

Only run trusted Python scripts. The activity log is not an antivirus scan.
