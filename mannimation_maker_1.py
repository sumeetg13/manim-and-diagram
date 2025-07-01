from manim import *

class UserOrdersSchema(Scene):
    def construct(self):
        title = Text("Database Schema", font_size=48).to_edge(UP)
        self.play(Write(title))

        user_fields = [
            ["user_id", "INT", "PK"],
            ["name", "VARCHAR", ""],
            ["email", "VARCHAR", "UNIQUE"],
            ["username", "VARCHAR", ""],
            ["password", "VARCHAR", ""]
        ]

        orders_fields = [
            ["order_id", "INT", "PK"],
            ["user_id", "INT", "FK"],
            ["product_id", "INT", "FK"],
            ["quantity", "INT", ""]
        ]

        product_fields = [
            ["product_id", "INT", "PK"],
            ["name", "VARCHAR", ""],
            ["quantity", "INT", ""]
        ]

        user_table = Table(
            [["Column", "Type", "Key"]] + user_fields,
            include_outer_lines=True,
            line_config={"stroke_width": 1},
            element_to_mobject=lambda x: Text(str(x), font_size=30)
        ).scale(0.45)

        orders_table = Table(
            [["Column", "Type", "Key"]] + orders_fields,
            include_outer_lines=True,
            line_config={"stroke_width": 1},
            element_to_mobject=lambda x: Text(str(x), font_size=30)
        ).scale(0.45)

        product_table = Table(
            [["Column", "Type", "Key"]] + product_fields,
            include_outer_lines=True,
            line_config={"stroke_width": 1},
            element_to_mobject=lambda x: Text(str(x), font_size=30)
        ).scale(0.45)

         # Arrange tables with spacing
        tables = VGroup(user_table, orders_table, product_table)
        tables.arrange(RIGHT, buff=0.5)

        # Shift inward for margin (left/right padding)
        tables.shift(DOWN * 0.5 + LEFT * 0.5)  # Adjust LEFT value to tune spacing

        # Animate tables
        self.play(Create(user_table), Create(orders_table), Create(product_table))
        self.wait()

        # Highlight FK rows
        fk1 = orders_table.get_rows()[2].copy().set_fill(ORANGE, opacity=0.4)
        fk2 = orders_table.get_rows()[3].copy().set_fill(ORANGE, opacity=0.4)
        self.play(FadeIn(fk1), FadeIn(fk2))
        self.wait(0.5)

        # Arrows
        arrow1 = Arrow(
            start=orders_table.get_cell((3, 1)).get_left(),
            end=user_table.get_cell((2, 1)).get_right(),
            color=BLUE,
            buff=0.1
        )
        arrow2 = Arrow(
            start=orders_table.get_cell((4, 1)).get_right(),
            end=product_table.get_cell((2, 1)).get_left(),
            color=BLUE,
            buff=0.1
        )

        self.play(GrowArrow(arrow1), GrowArrow(arrow2))
        self.wait(2)
