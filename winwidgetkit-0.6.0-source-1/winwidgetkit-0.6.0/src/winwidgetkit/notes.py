import tkinter as tk
from tkinter import simpledialog
from .base import DesktopWidget
class NoteWidget(DesktopWidget):
 def __init__(self,app,*,max_notes=5,**kw):
  kw.setdefault("title","Notes");kw.setdefault("width",340);kw.setdefault("height",260);kw.setdefault("color","#f4d35e");s=app.settings_for(kw["widget_id"]);self.max_notes=int(s.get("max_notes",max_notes));self.notes=s.get("notes",[{"title":"Note 1","text":""}]);self.index=min(s.get("index",0),len(self.notes)-1);super().__init__(app,**kw);self.bar=tk.Frame(self.body,bg=self.color);self.bar.pack(fill="x");tk.Button(self.bar,text="<",command=lambda:self.switch(-1)).pack(side="left");self.counter=tk.Label(self.bar,bg=self.color,fg="#222");self.counter.pack(side="left",expand=True);tk.Button(self.bar,text=">",command=lambda:self.switch(1)).pack(side="right");tk.Button(self.bar,text="+",command=self.add).pack(side="right");self.editors=tk.Frame(self.body,bg=self.color);self.editors.pack(fill="both",expand=True,padx=5,pady=5);self.texts=[];self.menu.insert_command(0,label="Set max notes",command=self.set_max);self.menu.insert_command(1,label="Delete current note",command=self.delete);self.render();self.window.bind("<Configure>",lambda e:self.render_if_layout_changed())
 def visible_count(self):return 2 if self.window.winfo_width()>=560 and len(self.notes)>1 else 1
 def save_current(self):
  for offset,t in enumerate(self.texts):
   i=(self.index+offset)%len(self.notes);self.notes[i]["text"]=t.get("1.0","end-1c")
 def render_if_layout_changed(self):
  count=self.visible_count()
  if count!=len(self.texts):self.save_current();self.render()
 def render(self):
  for w in self.editors.winfo_children():w.destroy()
  self.texts=[];count=self.visible_count()
  for offset in range(count):
   i=(self.index+offset)%len(self.notes);frame=tk.LabelFrame(self.editors,text=self.notes[i]["title"],bg=self.color,fg="#222");frame.pack(side="left",fill="both",expand=True,padx=3);text=tk.Text(frame,wrap="word",undo=True,bg="#fff6b7",fg="#222",font=("Segoe UI",11));text.pack(fill="both",expand=True);text.insert("1.0",self.notes[i]["text"]);text.bind("<KeyRelease>",lambda e:self.autosave());self.texts.append(text)
  self.counter.config(text=f"{self.index+1}/{len(self.notes)}  Max {self.max_notes}")
 def autosave(self):self.save_current();self.app.save_widget(self)
 def switch(self,n):self.save_current();self.index=(self.index+n)%len(self.notes);self.render();self.app.save_widget(self)
 def add(self):
  if len(self.notes)>=self.max_notes:return
  self.save_current();self.notes.append({"title":f"Note {len(self.notes)+1}","text":""});self.index=len(self.notes)-1;self.render();self.app.save_widget(self);self.app.log("note_added",id=self.widget_id)
 def delete(self):
  if len(self.notes)==1:self.notes[0]["text"]=""
  else:self.notes.pop(self.index);self.index=min(self.index,len(self.notes)-1)
  self.render();self.app.save_widget(self)
 def set_max(self):
  n=simpledialog.askinteger("Max notes","Maximum number of notes:",initialvalue=self.max_notes,minvalue=1,maxvalue=100,parent=self.window)
  if n:self.max_notes=n;self.notes=self.notes[:n];self.index=min(self.index,len(self.notes)-1);self.render();self.app.save_widget(self)
 def on_color_changed(self,c):self.bar.config(bg=c);self.counter.config(bg=c);self.editors.config(bg=c);self.render()
 def get_settings(self):
  if hasattr(self,"texts"):self.save_current()
  d=super().get_settings();d.update(max_notes=self.max_notes,notes=self.notes,index=self.index);return d
