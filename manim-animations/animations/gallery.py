"""Four standalone scenes. Render using scripts/build.sh or Manim directly.

All labels use Pango Text: no LaTeX installation is needed.
Change the constants inside each construct() to explore the mathematics.
"""

import numpy as np
from manim import (
    DEGREES, PI, TAU, WHITE,
    Circle, Create, DashedLine, Dot, FadeIn, FadeOut, LaggedStart,
    Line, ParametricFunction, Rotate, RoundedRectangle, Scene,
    ShowIncreasingSubsets, Text, ThreeDScene, Transform,
    ValueTracker, VGroup, always_redraw, color_gradient, linear,
)

INK = "#080D1A"
MUTED = "#8B9CB8"
CYAN = "#57E5E0"
VIOLET = "#A78BFA"
PINK = "#FF6FAE"
GOLD = "#FFD580"
PALETTE = [CYAN, VIOLET, PINK, GOLD]


def typography(title, subtitle, footer):
    """A consistent 16:9 title area and quiet footer, outside the artwork."""
    heading = Text(title, font_size=34, weight="BOLD", color=WHITE)
    heading.move_to([0, 3.28, 0])
    sub = Text(subtitle, font_size=17, color=MUTED).move_to([0, 2.78, 0])
    note = Text(footer, font_size=17, color=MUTED).move_to([0, -3.55, 0])
    return VGroup(heading, sub, note)


def glow_path(function, color=CYAN, t_range=(0, TAU, 0.02)):
    """A restrained halo underneath a sharp mathematical curve."""
    line = ParametricFunction(function, t_range=t_range, color=color, stroke_width=2.4)
    halo = line.copy().set_stroke(width=9, opacity=0.12)
    return VGroup(halo, line)


class FourierBloom(Scene):
    """A finite complex Fourier series, decomposed into rotating vectors."""

    def construct(self):
        self.camera.background_color = INK
        labels = typography(
            "FOURIER BLOOM", "A handful of circles. An unexpected silhouette.",
            "z(t) = 1.55 exp(it) + 0.62 exp(-3it) + 0.30 exp(5it) + 0.16 exp(9it)",
        )
        labels[2].scale(0.86)
        origin = np.array([-3.35, -0.30, 0.0])
        shift = np.array([6.7, 0, 0])
        terms = [(1, 1.55), (-3, 0.62), (5, 0.30), (9, 0.16)]
        clock = ValueTracker(0)

        def vertices(t):
            points = [origin.copy()]
            for frequency, radius in terms:
                points.append(points[-1] + radius * np.array([
                    np.cos(frequency * t), np.sin(frequency * t), 0,
                ]))
            return points

        def mechanism():
            points = vertices(clock.get_value())
            parts = VGroup()
            for i, (_, radius) in enumerate(terms):
                parts.add(Circle(radius, color=PALETTE[i], stroke_width=1.2,
                                 stroke_opacity=0.38).move_to(points[i]))
                parts.add(Line(points[i], points[i + 1], color=PALETTE[i], stroke_width=2))
                parts.add(Dot(points[i], radius=0.035, color=PALETTE[i]))
            return parts

        circles = always_redraw(mechanism)
        bridge = always_redraw(lambda: DashedLine(
            vertices(clock.get_value())[-1], vertices(clock.get_value())[-1] + shift,
            color=MUTED, stroke_width=1, stroke_opacity=0.35, dash_length=0.08,
        ))
        tip = always_redraw(lambda: Dot(vertices(clock.get_value())[-1] + shift,
                                       radius=0.055, color=GOLD))
        curve = glow_path(lambda t: vertices(t)[-1] + shift, CYAN, (0, TAU, 0.008))
        self.play(FadeIn(labels), FadeIn(circles), run_time=1.4)
        self.add(bridge, tip)
        self.play(Create(curve[0]), Create(curve[1]), clock.animate.set_value(TAU),
                  run_time=14, rate_func=linear)
        for item in (circles, bridge, tip):
            item.clear_updaters()
        self.play(FadeOut(bridge), FadeOut(tip), curve[1].animate.set_color(GOLD), run_time=1)
        self.wait(2)


class GoldenSpiral(Scene):
    """Vogel's phyllotaxis model, changing from a rational angle to the golden angle."""

    def construct(self):
        self.camera.background_color = INK
        labels = typography(
            "NATURE'S IRRATIONAL DESIGN", "One rule places every seed.",
            "r = c sqrt(n)     |     angle = n × 137.507764...°",
        )
        count = 650
        golden_angle = PI * (3 - np.sqrt(5))
        initial_angle = 140 * DEGREES
        center = np.array([0, -0.22, 0])
        spacing = 0.101
        colors = color_gradient([GOLD, PINK, VIOLET, CYAN], count)

        def location(n, angle):
            return center + spacing * np.sqrt(n) * np.array([
                np.cos(n * angle), np.sin(n * angle), 0,
            ])

        seeds = VGroup(*[
            Dot(location(n, initial_angle), radius=0.026 + 0.014 * n / count, color=colors[n])
            for n in range(count)
        ])
        angle_label = Text("140°  /  repeating spokes", font_size=19, color=GOLD)
        angle_label.move_to([4.65, 0.2, 0]).scale(0.8)
        self.play(FadeIn(labels), FadeIn(angle_label), run_time=1)
        self.play(ShowIncreasingSubsets(seeds), run_time=5, rate_func=linear)
        self.wait(1)
        angle = ValueTracker(initial_angle)

        # Rotate each seed around the center; interpolation of Cartesian positions
        # would cut through the disk and obscure the actual angular change.
        def update_seeds(group):
            for n, seed in enumerate(group):
                seed.move_to(location(n, angle.get_value()))

        seeds.add_updater(update_seeds)
        final_label = Text("137.507764...°\n\ngolden angle", font_size=19, color=CYAN)
        final_label.move_to(angle_label).scale(0.9)
        self.play(angle.animate.set_value(golden_angle), Transform(angle_label, final_label),
                  run_time=7)
        seeds.clear_updaters()
        self.play(Rotate(seeds, angle=PI / 5, about_point=center), run_time=4, rate_func=linear)
        self.wait(2)


class LissajousGarden(Scene):
    """Six frequency ratios with synchronized phase evolution."""

    def construct(self):
        self.camera.background_color = INK
        labels = typography(
            "THE LISSAJOUS GARDEN", "Two oscillations become a language of curves.",
            "x = sin(a t + phase)     |     y = sin(b t)",
        )
        ratios = [(1, 1), (1, 2), (2, 3), (3, 4), (3, 5), (5, 6)]
        centers = [np.array([x, y, 0]) for y in [1.18, -1.40] for x in [-4.3, 0, 4.3]]
        colors = color_gradient([CYAN, VIOLET, PINK, GOLD], len(ratios))
        cards, curves = VGroup(), VGroup()
        phase = ValueTracker(PI / 2)

        def curve_for(a, b, center, color):
            return glow_path(lambda t: center + np.array([
                1.40 * np.sin(a * t + phase.get_value()), 0.82 * np.sin(b * t), 0,
            ]), color, (0, TAU, 0.015))

        for (a, b), center, color in zip(ratios, centers, colors):
            card = RoundedRectangle(width=3.9, height=2.38, corner_radius=0.18,
                                    stroke_color="#26344D", stroke_width=1,
                                    fill_color="#10192A", fill_opacity=0.8).move_to(center)
            tag = Text(f"{a} : {b}", font_size=16, color=color)
            tag.move_to(center + np.array([0, -1.02, 0]))
            cards.add(VGroup(card, tag))
            curves.add(curve_for(a, b, center, color))

        self.play(FadeIn(labels), LaggedStart(*[FadeIn(card) for card in cards], lag_ratio=0.12))
        self.play(*[Create(curve) for curve in curves], run_time=5, rate_func=linear)
        self.wait(0.8)
        for curve, (a, b), center, color in zip(curves, ratios, centers, colors):
            curve.add_updater(lambda m, a=a, b=b, center=center, color=color:
                              m.become(curve_for(a, b, center, color)))
        self.play(phase.animate.set_value(PI / 2 + TAU), run_time=10, rate_func=linear)
        for curve in curves:
            curve.clear_updaters()
        self.wait(2)


class TorusKnot(ThreeDScene):
    """A (2, 3) torus knot: two trips around the axis, three around the tube."""

    def construct(self):
        self.camera.background_color = INK
        self.set_camera_orientation(phi=66 * DEGREES, theta=-42 * DEGREES, zoom=0.88)
        labels = typography(
            "A KNOT IN THREE DIMENSIONS", "A closed orbit on a torus becomes a trefoil.",
            "x = (R + r cos(3t)) cos(2t)    y = (R + r cos(3t)) sin(2t)    z = r sin(3t)",
        )
        labels[2].scale(0.79)
        self.add_fixed_in_frame_mobjects(labels)
        self.play(FadeIn(labels), run_time=1)
        major, minor = 2.0, 0.73

        def point(u, v):
            return np.array([(major + minor * np.cos(v)) * np.cos(u),
                             (major + minor * np.cos(v)) * np.sin(u), minor * np.sin(v)])

        # Wireframe avoids transparency/depth-sorting artifacts from filled surfaces.
        mesh = VGroup()
        for u in np.linspace(0, TAU, 24, endpoint=False):
            mesh.add(ParametricFunction(lambda v, u=u: point(u, v), t_range=(0, TAU, 0.08),
                                       color=CYAN, stroke_width=0.65, stroke_opacity=0.22))
        for v in np.linspace(0, TAU, 12, endpoint=False):
            mesh.add(ParametricFunction(lambda u, v=v: point(u, v), t_range=(0, TAU, 0.05),
                                       color=VIOLET, stroke_width=0.65, stroke_opacity=0.22))
        knot = ParametricFunction(lambda t: point(2 * t, 3 * t),
                                 t_range=(0, TAU, 0.008), color=GOLD, stroke_width=5)
        halo = knot.copy().set_stroke(color=PINK, width=13, opacity=0.16)
        self.play(Create(mesh), run_time=3)
        self.begin_ambient_camera_rotation(rate=0.13)
        self.play(Create(halo), Create(knot), run_time=9, rate_func=linear)
        self.wait(4)
        self.play(FadeOut(mesh), run_time=2)
        self.wait(3)
        self.stop_ambient_camera_rotation()
