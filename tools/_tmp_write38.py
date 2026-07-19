from pathlib import Path
import json

extra38 = [
"鵝口瘡白斑不易刮除，需與奶垢分辨後再決定是否用藥",
" thrush",
]
Path("tools/_b77_extra38.json").write_text(json.dumps(extra38, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote", len(extra38))
