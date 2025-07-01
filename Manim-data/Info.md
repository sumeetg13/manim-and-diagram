



## low quality :

manim -pql --resolution 1920,1080 mannimation_maker_1.py UserOrdersSchema

## high quality :

manim -pqh --resolution 1920,1080 mannimation_maker.py UserTableScene

## export Images : 

manim -pqh --format=svg mannimation_maker.py UserOrdersSchema

## export with transparent image :

manim -pqh --format=png --transparent mannimation_maker.py UserOrdersSchema


## SLIDES :

manim-slides render your_scene.py
manim-slides serve your_scene.py