from pathlib import Path
import os,tkinter as tk
from tkinter import filedialog,messagebox
from .base import DesktopWidget
class ShortcutWidget(DesktopWidget):
 def __init__(self,app,*,target=None,label=None,**kw):
  kw.setdefault("title","Shortcut");kw.setdefault("height",145);super().__init__(app,**kw);self.target=app.settings_for(self.widget_id).get("target",target or "");self.custom_label=label;self.icon=tk.Label(self.body,text="↗",font=("Segoe UI",30,"bold"),bg=self.color,fg="#fbbf24");self.icon.pack();self.name=tk.Label(self.body,bg=self.color,fg="white");self.name.pack();self.refresh();self.menu.insert_command(0,label="Select target",command=self.select);self.icon.bind("<Double-1>",lambda e:self.open());self.name.bind("<Double-1>",lambda e:self.open())
 def refresh(self):self.name.config(text=self.custom_label or (Path(self.target).name if self.target else "Choose a file"))
 def select(self):
  v=filedialog.askopenfilename(parent=self.window)
  if v:self.target=v;self.custom_label=None;self.refresh();self.app.save_widget(self)
 def open(self):
  if not self.target:return self.select()
  try:os.startfile(self.target);self.app.log("shortcut_opened",target=self.target)
  except OSError as e:messagebox.showerror("Cannot open",str(e),parent=self.window)
 def on_color_changed(self,c):self.icon.config(bg=c);self.name.config(bg=c)
 def get_settings(self):d=super().get_settings();d["target"]=self.target;return d
