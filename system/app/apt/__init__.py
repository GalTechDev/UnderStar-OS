import system.app.apt.install as install
import system.app.apt.uninstall as uninstall
from system.lib import *

Lib = App()
Lib.app.fusion([install, uninstall])