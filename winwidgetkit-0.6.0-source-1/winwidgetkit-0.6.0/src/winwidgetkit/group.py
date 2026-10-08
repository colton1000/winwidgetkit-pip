import tkinter as tk
from .base import DesktopWidget
class CombinedWidget(DesktopWidget):
 def __init__(self,app,*,panels=None,columns=2,**kw):
  kw.setdefault("title","Combined Widget");kw.setdefault("width",480);kw.setdefault("height",330);self.frames=[];super().__init__(app,**kw);self.content=tk.Frame(self.body,bg=self.color);self.content.pack(fill="both",expand=True)
  for i,(title,builder) in enumerate(panels or []):f=tk.LabelFrame(self.content,text=title,bg=self.color,fg="white");f.grid(row=i//columns,column=i%columns,sticky="nsew",padx=4,pady=4);self.frames.append(f);builder(f,self)
  for c in range(columns):self.content.columnconfigure(c,weight=1)
 def on_color_changed(self,c):self.content.config(bg=c);[f.config(bg=c) for f in self.frames]
