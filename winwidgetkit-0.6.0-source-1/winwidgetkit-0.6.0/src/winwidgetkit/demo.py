from . import WidgetApp,AnalogClockWidget,StopwatchWidget,CalendarWidget,ShortcutWidget,FocusOrbWidget,MagicOrbWidget,NoteWidget
def main():
 app=WidgetApp(app_name="WinWidgetKit 0.6 Demo",default_color="#263653")
 AnalogClockWidget(app,widget_id="clock",x=20,y=20,show_numbers=True)
 StopwatchWidget(app,widget_id="stopwatch",x=270,y=20)
 CalendarWidget(app,widget_id="calendar",x=570,y=20,holidays={"2026-12-25":{"name":"Holiday","color":"#dc2626"}})
 ShortcutWidget(app,widget_id="shortcut",x=20,y=350,label="Choose a file")
 FocusOrbWidget(app,widget_id="focus",x=270,y=350,minutes=25)
 MagicOrbWidget(app,widget_id="magic",x=580,y=350)
 NoteWidget(app,widget_id="notes",x=880,y=20,max_notes=8)
 app.run()
if __name__=="__main__":main()
