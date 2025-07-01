from manim import *

class UserTableScene(Scene):
    def construct(self):
        title = Text("User Table Schema", font_size=48).to_edge(UP)
        self.play(Write(title))

        headers = ["Column", "Type", "Key"]
        fields = [
            ["user_id", "INT", "PK"],
            ["name", "VARCHAR", ""],
            ["email", "VARCHAR", "UNIQUE"],
            ["username", "VARCHAR", ""],
            ["password", "VARCHAR", ""]
        ]

        table_data = [headers] + fields

        table = Table(
            table_data,
            include_outer_lines=True,
            line_config={"stroke_width": 1},
            element_to_mobject=lambda x: Text(str(x), font_size=30)
        ).scale(0.75)

        table.move_to(DOWN * 0.5)

        self.play(Create(table))
        self.wait()

        for i in range(1, len(table_data)):
            highlight = table.get_rows()[i].copy().set_fill(YELLOW, opacity=0.4)
            self.play(FadeIn(highlight), run_time=0.3)
            self.wait(0.2)
            self.play(FadeOut(highlight), run_time=0.3)

        self.wait(2)
