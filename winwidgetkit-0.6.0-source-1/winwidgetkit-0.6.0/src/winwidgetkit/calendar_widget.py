import calendar, tkinter as tk
from datetime import date
from tkinter import colorchooser, simpledialog, messagebox
from .base import DesktopWidget
class CalendarWidget(DesktopWidget):
 def __init__(self,app,*,holidays=None,**kw):
  t=date.today();s=app.settings_for(kw["widget_id"]);self.year=s.get("year",t.year);self.month=s.get("month",t.month);self.holidays=s.get("holidays",holidays or {});kw.setdefault("title","Calendar");kw.setdefault("width",340);kw.setdefault("height",310);super().__init__(app,**kw);self.nav=tk.Frame(self.body,bg=self.color);self.nav.pack(fill="x");tk.Button(self.nav,text="<",command=lambda:self.change(-1)).pack(side="left");self.label=tk.Label(self.nav,bg=self.color,fg="white",font=("Segoe UI",10,"bold"));self.label.pack(side="left",expand=True);tk.Button(self.nav,text=">",command=lambda:self.change(1)).pack(side="right");self.grid=tk.Frame(self.body,bg=self.color);self.grid.pack(fill="both",expand=True,padx=5,pady=4);self.menu.insert_command(0,label="Add holiday",command=self.add_holiday);self.menu.insert_command(1,label="Remove holiday",command=self.remove_holiday);self.draw()
 def change(self,n):m=self.month+n;self.year+=(m-1)//12;self.month=(m-1)%12+1;self.draw();self.app.save_widget(self)
 def add_holiday(self):
  ds=simpledialog.askstring("Holiday date","Date in YYYY-MM-DD format:",parent=self.window)
  if not ds:return
  try:d=date.fromisoformat(ds)
  except ValueError:messagebox.showerror("Invalid date","Use YYYY-MM-DD.",parent=self.window);return
  name=simpledialog.askstring("Holiday name","Holiday name:",parent=self.window) or "Holiday";color=colorchooser.askcolor("#ef4444",parent=self.window)[1] or "#ef4444";self.holidays[ds]={"name":name,"color":color};self.year,self.month=d.year,d.month;self.draw();self.app.save_widget(self);self.app.log("holiday_added",date=ds,name=name,color=color)
 def remove_holiday(self):
  ds=simpledialog.askstring("Remove holiday","Exact date YYYY-MM-DD:",parent=self.window)
  if ds in self.holidays:del self.holidays[ds];self.draw();self.app.save_widget(self)
 def draw(self):
  for w in self.grid.winfo_children():w.destroy()
  self.label.config(text=f"{calendar.month_name[self.month]} {self.year}")
  for c,n in enumerate(("Mon","Tue","Wed","Thu","Fri","Sat","Sun")):tk.Label(self.grid,text=n,bg=self.color,fg="#7dd3fc").grid(row=0,column=c,sticky="nsew")
  today=date.today()
  for r,wk in enumerate(calendar.Calendar().monthdayscalendar(self.year,self.month),1):
   for c,d in enumerate(wk):
    key=f"{self.year:04d}-{self.month:02d}-{d:02d}" if d else "";holiday=self.holidays.get(key);bg=holiday["color"] if holiday else ("#fb7185" if d and date(self.year,self.month,d)==today else self.color);text=(str(d)+(" ★" if holiday else "")) if d else "";lab=tk.Label(self.grid,text=text,bg=bg,fg="white",font=("Segoe UI",8,"bold" if holiday else "normal"));lab.grid(row=r,column=c,sticky="nsew",padx=1,pady=1);lab.bind("<Enter>",lambda e,h=holiday:self.label.config(text=h["name"] if h else f"{calendar.month_name[self.month]} {self.year}"));lab.bind("<Leave>",lambda e:self.label.config(text=f"{calendar.month_name[self.month]} {self.year}"))
  for c in range(7):self.grid.columnconfigure(c,weight=1)
  for r in range(7):self.grid.rowconfigure(r,weight=1)
 def on_color_changed(self,c):self.nav.config(bg=c);self.label.config(bg=c);self.grid.config(bg=c);self.draw()
 def get_settings(self):d=super().get_settings();d.update(year=self.year,month=self.month,holidays=self.holidays);return d
