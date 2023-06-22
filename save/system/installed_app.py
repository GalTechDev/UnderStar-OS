from system.lib import import_module

import sys
sys.path.append('/Users/maxence/Documents/GitHub')
import classbot

all_app=import_module("app", True)
all_app.update({"classbot":classbot})