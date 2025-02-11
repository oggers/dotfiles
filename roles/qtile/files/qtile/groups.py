from typing import Callable

from keys import keys, mod
from libqtile.config import DropDown, Group, Key, ScratchPad
from libqtile.lazy import lazy


groups = []
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]

group_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]
# group_labels = ["DEV", "WWW", "SYS", "DOC", "VBOX", "CHAT", "MUS", "VID", "GFX",]
# group_labels = ["", "", "", "", "", "", "", "", "",]

group_layouts = ["monadtall", "monadtall", "tile", "tile", "monadtall",
                 "monadtall", "monadtall", "monadtall", "monadtall"]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

# scratchpad
groups.append(
    ScratchPad('scratchpad', [
        DropDown('keepass', ['keepassxc'], opacity=0.9, height=0.8, width=0.7),
        DropDown('gstm', ['gstm'], on_focus_lost_hide=True, warp_pointer=True,
                 opacity=0.9, height=0.8, width=0.4),
    ])
)


def go_to_group(name: str) -> Callable:
    def _inner(qtile) -> None:
        if len(qtile.screens) == 1:
            qtile.groups_map[name].toscreen()
            return

        qtile.focus_screen(0 if name in '12345' else 1)
        qtile.groups_map[name].toscreen()

    return _inner


def go_to_group_and_move_window(name: str) -> Callable:
    def _inner(qtile):
        if len(qtile.screens) == 1:
            qtile.current_window.togroup(name, switch_group=True)
            return

        qtile.current_window.togroup(name, switch_group=False)
        qtile.focus_screen(0 if name in '12345' else 1)
        qtile.groups_map[name].toscreen()

    return _inner


for name in group_names:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                name,
                # lazy.function(go_to_group(i.name)),
                lazy.group[name].toscreen(),
                desc="Switch to group {}".format(name),
            ),
            # mod1 + shift + letter of group = move focused window to group
            Key(
                [mod, "shift"],
                name,
                # lazy.function(go_to_group_and_move_window(i.name)),
                lazy.window.togroup(name, switch_group=False),
                desc="Move focused window to group {}".format(name),
            ),
        ]
    )
