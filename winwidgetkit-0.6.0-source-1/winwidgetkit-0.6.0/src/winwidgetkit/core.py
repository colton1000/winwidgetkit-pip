import json, os, tkinter as tk
from pathlib import Path
from datetime import datetime
from tkinter import colorchooser
DEFAULT_COLOR="#24283b"
def set_default_color(c):
 global DEFAULT_COLOR;DEFAULT_COLOR=c
def get_default_color():return DEFAULT_COLOR
class Logger:
 def __init__(self,name,folder=None):self.name=name;self.lines=[];self.folder=Path(folder) if folder else Path.home()/"Downloads";self.log("application_started",library="tkinter")
 def log(self,event,**data):
  line=f"[{datetime.now().astimezone().isoformat(timespec='seconds')}] {event}"+(" | "+"; ".join(f"{k}={v}" for k,v in data.items()) if data else "");self.lines.append(line);print("[WinWidgetKit]",line,flush=True)
 def write(self):
  try:self.folder.mkdir(parents=True,exist_ok=True)
  except OSError:self.folder=Path.cwd()
  safe="".join(c if c.isalnum() or c in "-_" else "_" for c in self.name);p=self.folder/f"{safe}_{datetime.now():%Y-%m-%d_%H-%M-%S}.log.txt";p.write_text("WinWidgetKit Activity Report\n\n"+"\n".join(self.lines),encoding="utf-8");print("Log saved:",p)
class WidgetApp:
 def __init__(self,config_path=None,default_color=None,app_name="WinWidgetKit App",logging=True,log_directory=None):
  self.root=tk.Tk();self.root.withdraw();self.default_color=default_color;self.widgets=[];self.quitting=False;path=Path(config_path) if config_path else Path(os.getenv("APPDATA",Path.home()))/"WinWidgetKit"/"widgets.json";self.config_path=path;path.parent.mkdir(parents=True,exist_ok=True)
  try:self.config=json.loads(path.read_text(encoding="utf-8"))
  except (OSError,json.JSONDecodeError):self.config={}
  self.logger=Logger(app_name,log_directory) if logging else None
 def log(self,event,**data):
  if self.logger:self.logger.log(event,**data)
 def settings_for(self,i):return self.config.get(i,{})
 def save_widget(self,w):
  try:self.config[w.widget_id]=w.get_settings();t=self.config_path.with_suffix(".tmp");t.write_text(json.dumps(self.config,indent=2),encoding="utf-8");t.replace(self.config_path)
  except (OSError,tk.TclError) as e:self.log("save_failed",error=repr(e))
 def register(self,w):self.widgets.append(w);self.log("widget_created",id=w.widget_id,type=type(w).__name__)
 def unregister(self,w):
  if w in self.widgets:self.widgets.remove(w)
  if not self.widgets and not self.quitting:self.quitting=True;self.root.after_idle(self.root.quit)
 def run(self):
  try:self.root.mainloop()
  finally:
   if self.logger:self.logger.log("application_closed");self.logger.write()
   try:self.root.destroy()
   except tk.TclError:pass
class DesktopWidget:
 def __init__(self,app,*,widget_id,x=40,y=40,width=230,height=170,min_width=150,min_height=100,color=None,title="Widget",always_on_top=False,resizable=True):
  self.app,self.widget_id=app,widget_id;self.min_width,self.min_height=min_width,min_height;s=app.settings_for(widget_id);self.color=s.get("color",color or app.default_color or DEFAULT_COLOR);self.always_on_top=s.get("always_on_top",always_on_top);x,y,w,h=s.get("x",x),s.get("y",y),s.get("width",width),s.get("height",height)
  self.window=tk.Toplevel(app.root);self.window.overrideredirect(True);self.window.geometry(f"{w}x{h}+{x}+{y}");self.window.config(bg=self.color);self.window.attributes("-topmost",self.always_on_top)
  shade=self.shade(self.color);self.header=tk.Frame(self.window,bg=shade,height=28,cursor="fleur");self.header.pack(fill="x");self.header.pack_propagate(False);self.title_label=tk.Label(self.header,text=title,bg=shade,fg="white",font=("Segoe UI",9,"bold"));self.title_label.pack(side="left",padx=8);self.close_button=tk.Label(self.header,text="x",bg=shade,fg="white");self.close_button.pack(side="right",padx=8);self.close_button.bind("<Button-1>",lambda e:self.close());self.body=tk.Frame(self.window,bg=self.color);self.body.pack(fill="both",expand=True)
  self.grip=tk.Label(self.window,text="◢",bg=self.color,fg="white",cursor="size_nw_se");
  if resizable:self.grip.place(relx=1,rely=1,anchor="se")
  self.grip.bind("<ButtonPress-1>",self.rs);self.grip.bind("<B1-Motion>",self.rm);self.grip.bind("<ButtonRelease-1>",self.re);self.menu=tk.Menu(self.window,tearoff=False);self.menu.add_command(label="Change color",command=self.choose_color);self.menu.add_command(label="Always on top",command=self.toggle_top);self.menu.add_separator();self.menu.add_command(label="Close",command=self.close);self.hold=None;self.held=False;self.bind_controls(self.window,self.header,self.title_label,self.body);app.register(self)
 @staticmethod
 def shade(c,f=.72):
  try:v=c.lstrip("#");r,g,b=(int(v[i:i+2],16) for i in (0,2,4));return f"#{int(r*f):02x}{int(g*f):02x}{int(b*f):02x}"
  except:return "#1a1a1a"
 def bind_controls(self,*cs):
  for c in cs:c.bind("<ButtonPress-1>",self.ds,add="+");c.bind("<B1-Motion>",self.dm,add="+");c.bind("<ButtonRelease-1>",self.de,add="+");c.bind("<ButtonPress-3>",self.rstart,add="+");c.bind("<ButtonRelease-3>",self.rend,add="+")
 def ds(self,e):self.do=(e.x_root-self.window.winfo_x(),e.y_root-self.window.winfo_y())
 def dm(self,e):self.window.geometry(f"+{max(0,e.x_root-self.do[0])}+{max(0,e.y_root-self.do[1])}")
 def de(self,e):self.app.save_widget(self);self.app.log("widget_moved",id=self.widget_id)
 def rs(self,e):self.ro=(e.x_root,e.y_root,self.window.winfo_width(),self.window.winfo_height())
 def rm(self,e):x,y,w,h=self.ro;self.window.geometry(f"{max(self.min_width,w+e.x_root-x)}x{max(self.min_height,h+e.y_root-y)}");self.grip.lift();self.on_resize()
 def re(self,e):self.app.save_widget(self);self.app.log("widget_resized",id=self.widget_id)
 def on_resize(self):pass
 def rstart(self,e):self.held=False;self.hold=self.window.after(2000,self.long_right)
 def long_right(self):self.hold=None;self.held=True;self.choose_color()
 def rend(self,e):
  if self.hold:self.window.after_cancel(self.hold);self.hold=None
  if not self.held:self.menu.tk_popup(e.x_root,e.y_root)
 def choose_color(self):
  c=colorchooser.askcolor(self.color,parent=self.window)[1]
  if c:self.set_color(c)
 def set_color(self,c):self.color=c;sh=self.shade(c);self.window.config(bg=c);self.body.config(bg=c);self.header.config(bg=sh);self.title_label.config(bg=sh);self.close_button.config(bg=sh);self.grip.config(bg=c);self.on_color_changed(c);self.app.save_widget(self)
 def on_color_changed(self,c):pass
 def toggle_top(self):self.always_on_top=not self.always_on_top;self.window.attributes("-topmost",self.always_on_top);self.app.save_widget(self)
 def get_settings(self):return {"x":self.window.winfo_x(),"y":self.window.winfo_y(),"width":self.window.winfo_width(),"height":self.window.winfo_height(),"color":self.color,"always_on_top":self.always_on_top}
 def close(self):self.app.save_widget(self);self.window.destroy();self.app.unregister(self)
