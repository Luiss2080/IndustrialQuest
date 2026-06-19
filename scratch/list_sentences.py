import sys
import os

# Set CWD to root
sys.path.insert(0, os.path.abspath("."))
from src.datos_juego import TEMAS

for level_name, info in TEMAS.items():
    print(f"=== {level_name} ===")
    for item in info["frases"]:
        print(repr(item[0]))
