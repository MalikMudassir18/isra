from os import path

__all__ = ['DATA_DIR', 'TENNANT']

CURR_DIR = path.dirname(path.abspath(__file__))
TENNANT = path.join(CURR_DIR, "config.json")


