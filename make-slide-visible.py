import shutil
from pathlib import Path
import manim_slides

base = Path(manim_slides.__path__[0]) / "assets"
export_dir = Path("exported-slides")
export_dir.mkdir(exist_ok=True)

# Copy assets
for asset in ["index.html", "app.js", "style.css"]:
    shutil.copy(base / asset, export_dir)

# Copy your JSON slide
shutil.copy("slides/manslide/CanvasExample.json", export_dir / "CanvasExample.json")
