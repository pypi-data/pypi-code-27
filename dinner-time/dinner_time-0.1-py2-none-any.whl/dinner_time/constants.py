from os import path

ROOT_DIR = path.join(path.expanduser("~"), ".dinner_time")
RECIPES_FN = path.join(ROOT_DIR, "recipes.json")
CFG_FN = path.join(ROOT_DIR, "cfg.json")
GOOGLE_SHEETS_ENDPOINT = "https://docs.google.com/spreadsheets/d"
TAG_ALL = 'all'
