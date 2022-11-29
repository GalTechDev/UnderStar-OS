import system.app.apt.install as install
import system.app.apt.uninstall as uninstall
from system.lib import *

app=App()
app.fusion([install,uninstall])