#!/usr/bin/env python3
"""Render selected scenes using the project's isolated Python environment."""

import argparse
import os
from pathlib import Path
import shlex
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCENES = {
    "fourier": ("FourierBloom", "Rotating epicycles trace a luminous Fourier flower"),
    "golden": ("GoldenSpiral", "650 seeds settle into golden-angle phyllotaxis"),
    "lissajous": ("LissajousGarden", "Six harmonic curves evolve as their phase changes"),
    "torus": ("TorusKnot", "A trefoil is traced on a rotating 3D torus"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenes", nargs="*", help="Scene aliases, class names, or all (default)")
    parser.add_argument("--list", action="store_true", help="List available scenes")
    parser.add_argument("-q", "--quality", choices=["l", "m", "h", "p", "k"], default="h",
                        help="l: 480p15, m: 720p30, h: 1080p60, p: 1440p60, k: 2160p60")
    parser.add_argument("--preview", action="store_true", help="Open each result in your video player")
    parser.add_argument("--still", action="store_true", help="Save each scene's last frame as PNG")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without rendering")
    args = parser.parse_args()
    if args.list:
        for alias, (name, description) in SCENES.items():
            print(f"{alias:12} {name:18} {description}")
        return 0

    requested = args.scenes or ["all"]
    if "all" in requested and len(requested) != 1:
        parser.error("Use 'all' alone, or name individual scenes.")
    aliases = {name: alias for alias, (name, _) in SCENES.items()}
    selected = list(SCENES) if requested == ["all"] else [aliases.get(s, s) for s in requested]
    unknown = [s for s in selected if s not in SCENES]
    if unknown:
        parser.error(f"Unknown scene(s): {', '.join(unknown)}. Use --list to see choices.")
    selected = list(dict.fromkeys(selected))
    python = ROOT / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not args.dry_run:
        if not python.exists():
            parser.exit(1, "Project environment missing. Run ./scripts/setup.sh first.\n")
        check = subprocess.run([str(python), "-c", "import manim"], capture_output=True, text=True)
        if check.returncode:
            parser.exit(1, f"Manim could not be imported. Run ./scripts/setup.sh.\n{check.stderr}")

    for alias in selected:
        name = SCENES[alias][0]
        command = [str(python), "-m", "manim", "render", f"-q{args.quality}",
                   "--config_file", str(ROOT / "manim.cfg")]
        if args.preview:
            command.append("--preview")
        if args.still:
            command.append("--save_last_frame")
        command.extend([str(ROOT / "animations/gallery.py"), name])
        print(f"\n{'Would render' if args.dry_run else 'Rendering'} {name}:\n{shlex.join(command)}", flush=True)
        if not args.dry_run:
            result = subprocess.run(command, cwd=ROOT)
            if result.returncode:
                return result.returncode
    if not args.dry_run:
        print(f"\nFinished. Output directory: {ROOT / 'media'}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
