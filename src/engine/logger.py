import os
from datetime import datetime
from engine.paths import get_base_dir

LOG_PATH = os.path.join(get_base_dir(), "data", "gridlaunch.log")


def log(*args,**kwargs):
    pass
    
