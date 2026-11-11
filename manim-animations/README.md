# Mathematical motion studies

Four Python/Manim animations with a midnight palette, luminous curves, deliberate
timing, and mathematical labels. No LaTeX, external images, or paid assets required.

| Command name | Scene | What happens | Approx. duration |
| --- | --- | --- | --- |
| `fourier` | `FourierBloom` | Four rotating vectors draw a complex Fourier flower | 18 s |
| `golden` | `GoldenSpiral` | 650 seeds change from repeating spokes to golden-angle packing | 20 s |
| `lissajous` | `LissajousGarden` | Six frequency ratios draw curves, then sweep through a phase cycle | 20 s |
| `torus` | `TorusKnot` | A trefoil appears on a wireframe torus as the camera orbits | 22 s |

## Setup on macOS

Run from this project folder. Homebrew must already be installed.

```bash
brew install python@3.13 cairo pango pkg-config
./scripts/setup.sh
./scripts/run.sh fourier
```

Setup creates `.venv/` and installs the pinned Manim version from `requirements.txt`.
It can be rerun safely and does not require activating the environment. Python 3.11+
is required; macOS's system Python 3.9 is too old. To choose an interpreter:

```bash
PYTHON=/opt/homebrew/bin/python3.13 ./scripts/setup.sh
```

On Debian/Ubuntu, install the native prerequisites below, ensure `python3` is 3.11+
(`python3 --version`), and then run `./scripts/setup.sh`:

```bash
sudo apt-get install python3-dev python3-venv build-essential pkg-config libcairo2-dev libpango1.0-dev
```

For Windows setup, follow the [official Manim installation guide](https://docs.manim.community/en/stable/installation/uv.html),
create a `.venv` with Python 3.11+, install `requirements.txt`, and use
`python scripts/render.py` instead of the shell wrappers.

## Render and play

```bash
# List the scenes (also works before setup).
./scripts/build.sh --list

# Quickly render and play one or several samples at 480p / 15 fps.
./scripts/run.sh golden
./scripts/run.sh fourier lissajous

# Render all four at 1080p / 60 fps.
./scripts/build.sh all

# Render and play at 1080p / 60 fps.
./scripts/run.sh torus -q h

# Render selected scenes at 720p / 30 fps or 4K / 60 fps.
./scripts/build.sh fourier golden -q m
./scripts/build.sh torus -q k

# Export the last frame of every scene as a PNG.
./scripts/build.sh all --still

# Inspect the commands without installing dependencies or rendering.
./scripts/build.sh all --dry-run
```

`build.sh` saves files; `run.sh` also opens them in the default player. Both work
from any directory. With no scene argument, they render all four. Quality flags:
`l` = 480p15, `m` = 720p30, `h` = 1080p60, `p` = 1440p60, `k` = 2160p60.
Start with low quality while editing; the 650-seed scene and the 3D scene take
longer at high resolution. These samples are silent.

Manim writes videos under `media/videos/` (usually
`media/videos/gallery/1080p60/FourierBloom.mp4`) and stills under `media/images/`.
Its render log reports the output location. Intermediate files and caches stay
inside `media/`, which is ignored by Git.

## Customize the animation

Edit `animations/gallery.py`:

- **Fourier:** change `terms`, a list of `(frequency, radius)` pairs. Negative
  frequencies rotate clockwise. Keep the radii's sum below about 2.7 to fit the layout.
- **Phyllotaxis:** change `count`, `spacing`, or `initial_angle`. Each seed uses
  radius `c sqrt(n)` and angle `n × angle`; the final angle is `pi × (3 - sqrt(5))`.
- **Lissajous:** edit the six `ratios`. Integer ratios close after `t = 2 pi`.
  The shared phase tracker continuously changes their silhouettes.
- **Torus:** change `major` and `minor`, or replace `(2t, 3t)` with another pair
  of coprime integer windings. Update the displayed equations when changing the math.

Palette and label styling are defined at the top of the file. `run_time` controls
individual sequences. `manim.cfg` sets the renderer, output folder, and background.
To render directly with Manim, from the project root:

```bash
.venv/bin/python -m manim -pql animations/gallery.py FourierBloom
```

The project pins [Manim Community 0.22.1](https://pypi.org/project/manim/0.22.1/).
See the [Manim quickstart](https://docs.manim.community/en/stable/tutorials/quickstart.html)
for an introduction to scenes, mobjects, and animations.

## Verification status

The source syntax and script command handling were checked during creation.
Actual rendering and visual inspection remain unverified: the authoring environment
has no Manim/Cairo/Pango installation and could not resolve PyPI to install Manim.
After setup, `./scripts/build.sh all -q l` renders every scene for an initial check.
