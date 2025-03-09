from libqtile import bar
from libqtile.config import Screen
from .widgets import primary_widgets, secondary_widgets


# For adding transparency to your bar, add (background="#00000000")
# to the "Screen" line(s)
# For ex: Screen(top=bar.Bar(widgets=init_widgets_screen2(),
# background="#00000000", size=24)),
screens = [
    Screen(
        top=bar.Bar(
            widgets=primary_widgets,
            size=26,
            margin=(8, 12, 4, 12),
            background="#00000000")),
    Screen(
        top=bar.Bar(
            widgets=secondary_widgets,
            size=26,
            margin=(8, 12, 4, 12),
            background="#00000000")),
    ]
