from os.path import dirname, basename, isfile, join
import glob
import importlib

modules = glob.glob(join(dirname(__file__), "*.py"))
days = [basename(f)[:-3] for f in modules if isfile(f) and basename(f)[0] != '_']

for d in days:
    dMod = importlib.import_module(f"days.{d}")
    globals()[d] = getattr(dMod, d)



