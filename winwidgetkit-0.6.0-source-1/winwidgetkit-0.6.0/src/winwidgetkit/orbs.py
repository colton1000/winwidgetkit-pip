import math,random,time,tkinter as tk
from .base import DesktopWidget
class FocusOrbWidget(DesktopWidget):
 def __init__(self,app,*,minutes=25,**kw):
  kw.setdefault("title","Focus Orb");kw.setdefault("width",290);kw.setdefault("height",300);s=app.settings_for(kw["widget_id"]);self.duration=s.get("duration",minutes*60);self.remaining=s.get("remaining",self.duration);self.running=False;self.started=0;self.angle=0;self.sparks=[];super().__init__(app,**kw);self.canvas=tk.Canvas(self.body,bg=self.color,highlightthickness=0);self.canvas.pack(fill="both",expand=True);self.canvas.bind("<Button-1>",self.spark);self.button=tk.Button(self.body,text="Start Focus",command=self.toggle);self.button.place(relx=.5,rely=.91,anchor="center");self.animate()
 def current(self):return max(0,self.remaining-(time.perf_counter()-self.started if self.running else 0))
 def toggle(self):
  if self.running:self.remaining=self.current();self.running=False;self.button.config(text="Start Focus")
  else:self.remaining=self.remaining or self.duration;self.started=time.perf_counter();self.running=True;self.button.config(text="Pause Focus")
  self.app.save_widget(self)
 def spark(self,e):
  for _ in range(12):self.sparks.append([e.x,e.y,random.uniform(-2,2),random.uniform(-3,-1),20])
 def animate(self):
  try:
   rem=self.current();self.angle+=2
   if self.running and rem<=0:self.running=False;self.remaining=0;self.window.bell();self.button.config(text="Restart Focus")
   c=self.canvas;c.delete("all");w,h=max(20,c.winfo_width()),max(20,c.winfo_height());x,y=w/2,h*.43;r=min(w,h)*.24*(1+.04*math.sin(math.radians(self.angle)));cols=("#7dd3fc","#a78bfa","#fb7185","#fbbf24")
   for i,col in enumerate(cols):rr=r+i*9;c.create_oval(x-rr,y-rr,x+rr,y+rr,outline=col,width=3)
   c.create_arc(x-r-15,y-r-15,x+r+15,y+r+15,start=90,extent=-360*(rem/self.duration),style="arc",outline="white",width=6);c.create_text(x,y,text=f"{int(rem//60):02d}:{int(rem%60):02d}",fill="white",font=("Segoe UI",24,"bold"));alive=[]
   for s in self.sparks:s[0]+=s[2];s[1]+=s[3];s[3]+=.15;s[4]-=1;c.create_oval(s[0]-2,s[1]-2,s[0]+2,s[1]+2,fill=random.choice(cols),outline="");alive.append(s) if s[4]>0 else None
   self.sparks=alive;self.job=self.window.after(33,self.animate)
  except tk.TclError:pass
 def on_color_changed(self,c):self.canvas.config(bg=c)
 def get_settings(self):d=super().get_settings();d.update(duration=self.duration,remaining=self.current());return d
class MagicOrbWidget(DesktopWidget):
 def __init__(self,app,**kw):
  kw.setdefault("title","Magic Orb");kw.setdefault("width",280);kw.setdefault("height",270);kw.setdefault("color","#241044");self.answer="Ask a question";self.angle=0;super().__init__(app,**kw);self.canvas=tk.Canvas(self.body,bg=self.color,highlightthickness=0);self.canvas.pack(fill="both",expand=True);self.canvas.bind("<Button-1>",lambda e:self.ask());self.ask_button=tk.Button(self.body,text="Ask the Orb",command=self.ask);self.ask_button.place(relx=.5,rely=.9,anchor="center");self.animate()
 def ask(self):self.answer=random.choice(("YES","NO"));self.app.log("magic_orb_answer",answer=self.answer);self.pulse=18
 def animate(self):
  try:
   self.angle+=3;c=self.canvas;c.delete("all");w,h=max(20,c.winfo_width()),max(20,c.winfo_height());x,y=w/2,h*.43;r=min(w,h)*.27;glow=8+5*math.sin(math.radians(self.angle));c.create_oval(x-r-glow,y-r-glow,x+r+glow,y+r+glow,outline="#a78bfa",width=5);c.create_oval(x-r,y-r,x+r,y+r,fill="#3b1773",outline="#e9d5ff",width=3);c.create_oval(x-r*.62,y-r*.62,x+r*.62,y+r*.62,fill="#140624",outline="#c4b5fd",width=2);c.create_text(x,y,text=self.answer,fill="white",font=("Segoe UI",18,"bold"),width=int(r*1.1));self.job=self.window.after(40,self.animate)
  except tk.TclError:pass
 def on_color_changed(self,c):self.canvas.config(bg=c)
