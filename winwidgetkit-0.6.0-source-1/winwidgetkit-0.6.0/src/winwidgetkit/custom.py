import importlib.util
from pathlib import Path
from .base import DesktopWidget
class CustomWidget(DesktopWidget):
 def __init__(self,app,*,build,color_handler=None,**kw):self.handler=color_handler;super().__init__(app,**kw);build(self)
 def on_color_changed(self,c):
  if self.handler:self.handler(self,c)
class ScriptWidget(CustomWidget):
 def __init__(self,app,*,script_path,**kw):
  p=Path(script_path).resolve();spec=importlib.util.spec_from_file_location(f"widget_{p.stem}",p)
  if not spec or not spec.loader:raise ImportError(p)
  m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);kw.setdefault("color",getattr(m,"DEFAULT_COLOR",None));super().__init__(app,build=m.build,color_handler=getattr(m,"on_color",None),**kw)
