# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from pathlib import Path
import subprocess
from typing import Callable, List  # noqa: F401

from libqtile import bar, hook, extension, layout, qtile, widget
from libqtile.config import Click, Drag, DropDown, Group, Key, KeyChord, Match, ScratchPad, Screen
from libqtile.layout import TreeTab
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from libqtile.utils import guess_terminal, send_notification
import qtile_extras.hook
import qtile_extras.widget
from qtile_extras.widget.decorations import BorderDecoration
from qtile_extras.widget.decorations import PowerLineDecoration

import colors

mod = "mod4"  # Sets mod key to SUPER/WINDOW
my_term = "alacritty"  # My terminal of choice
my_browser = "firefox"  # My browser of choice
my_emacs = "emacsclient -c -a 'emacs' "  # The space at the end is IMPORTANT!

# Get home path
home = str(Path.home())

# Allows you to input a name when adding treetab section.
@lazy.layout.function
def add_treetab_section(layout: TreeTab) -> None:
    prompt = qtile.widgets_map["prompt"]
    prompt.start_input("Section name: ", layout.add_section)


# A function for hide/show all the windows in a group
@lazy.function
def minimize_all(qtile) -> None:
    for win in qtile.current_group.windows:
        if hasattr(win, 'toggle_minimize'):
            win.toggle_minimize()


# A function for toggling between MAX and MONADTALL layouts
@lazy.function
def maximize_by_switching_layout(qtile) -> None:
    current_layout_name = qtile.current_group.layout.name
    if current_layout_name == 'monadtall':
        qtile.current_group.layout = 'max'
    elif current_layout_name == 'max':
        qtile.current_group.layout = 'monadtall'

if qtile.core.name == 'x11':
    pass
elif qtile.core.name == 'wayland':
    pass

keys = [
    # The essentials
    Key([mod], "Return", lazy.spawn(my_term), desc="Terminal"),
    Key([mod, "shift"], "Return", lazy.spawn("rofi -show drun"), desc='Run Launcher'),
    Key([mod], "b", lazy.spawn(my_browser), desc='Web browser'),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.spawn("dm-logout -r"), desc="Logout menu"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Switch between windows
    # Some layouts like 'monadtall' only need to use j/k to move
    # through the stack, but other layouts like 'columns' will
    # require all four directions h/j/k/l to move around.
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h",
        lazy.layout.shuffle_left(),
        lazy.layout.move_left().when(layout=["treetab"]),
        desc="Move window to the left/move tab left in treetab"),

    Key([mod, "shift"], "l",
        lazy.layout.shuffle_right(),
        lazy.layout.move_right().when(layout=["treetab"]),
        desc="Move window to the right/move tab right in treetab"),

    Key([mod, "shift"], "j",
        lazy.layout.shuffle_down(),
        lazy.layout.section_down().when(layout=["treetab"]),
        desc="Move window down/move down a section in treetab"),

    Key([mod, "shift"], "k",
        lazy.layout.shuffle_up(),
        lazy.layout.section_up().when(layout=["treetab"]),
        desc="Move window downup/move up a section in treetab"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "space", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),

    # Treetab prompt
    Key([mod, "shift"], "a", add_treetab_section, desc='Prompt to add new section in treetab'),

    # Grow/shrink windows left/right.
    # This is mainly for the 'monadtall' and 'monadwide' layouts
    # although it does also work in the 'bsp' and 'columns' layouts.
    Key([mod], "equal",
        lazy.layout.grow_left().when(layout=["bsp", "columns"]),
        lazy.layout.grow().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"),

    Key([mod], "minus",
        lazy.layout.grow_right().when(layout=["bsp", "columns"]),
        lazy.layout.shrink().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"),

    # Grow windows up, down, left, right.  Only works in certain layouts.
    # Works in 'bsp' and 'columns' layout.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "m", lazy.layout.maximize(), desc='Toggle between min and max sizes'),
    Key([mod], "t", lazy.window.toggle_floating(), desc='toggle floating'),
    Key([mod], "f", maximize_by_switching_layout(), lazy.window.toggle_fullscreen(), desc='toggle fullscreen'),
    Key([mod, "shift"], "m", minimize_all(), desc="Toggle hide/show all windows on current group"),

    # Switch focus of monitors
    Key([mod], "period", lazy.next_screen(), desc='Move focus to next monitor'),
    Key([mod], "comma", lazy.prev_screen(), desc='Move focus to prev monitor'),

    # screenshot
    # Key([mod], "Print", lazy.spawn(home + "/.config/qtile/scripts/screenshot.sh")),
    Key([mod], "Print", lazy.spawn("xfce4-screenshooter")),

    # Volume
    Key([], "XF86AudioMute", lazy.spawn("amixer -D pulse set Master toggle")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -D pulse set Master 5%+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -D pulse set Master 5%-")),

    # ScratchPad
    KeyChord([mod], "s", [
        Key([], "k", lazy.group["scratchpad"].dropdown_toggle("keepass")),
        Key([], "g", lazy.group["scratchpad"].dropdown_toggle("gstm")),
    ]),

    # Emacs programs launched using the key chord CTRL+e followed by 'key'
    KeyChord([mod], "e", [
        Key([], "e", lazy.spawn(my_emacs), desc='Emacs Dashboard'),
        Key([], "a", lazy.spawn(my_emacs + "--eval '(emms-play-directory-tree \"~/Music/\")'"), desc='Emacs EMMS'),
        Key([], "b", lazy.spawn(my_emacs + "--eval '(ibuffer)'"), desc='Emacs Ibuffer'),
        Key([], "d", lazy.spawn(my_emacs + "--eval '(dired nil)'"), desc='Emacs Dired'),
        Key([], "i", lazy.spawn(my_emacs + "--eval '(erc)'"), desc='Emacs ERC'),
        Key([], "s", lazy.spawn(my_emacs + "--eval '(eshell)'"), desc='Emacs Eshell'),
        Key([], "v", lazy.spawn(my_emacs + "--eval '(vterm)'"), desc='Emacs Vterm'),
        Key([], "w", lazy.spawn(my_emacs + "--eval '(eww \"distro.tube\")'"), desc='Emacs EWW'),
        Key([], "F4", lazy.spawn("killall emacs"),
            lazy.spawn("/usr/bin/emacs --daemon"),
            desc='Kill/restart the Emacs daemon')
    ]),
    # Dmenu/rofi scripts launched using the key chord SUPER+p followed by 'key'
    KeyChord([mod], "p", [
        Key([], "h", lazy.spawn("dm-hub -r"), desc='List all dmscripts'),
        # Key([], "a", lazy.spawn("dm-sounds -r"), desc='Choose ambient sound'),
        # Key([], "b", lazy.spawn("dm-setbg -r"), desc='Set background'),
        Key([], "c", lazy.spawn("dm-colpick -r"), desc='Choose color'),
        # Key([], "e", lazy.spawn("dm-confedit -r"), desc='Choose a config file to edit'),
        Key([], "f", lazy.spawn("dm-fonts -r"), desc='View fonts'),
        # Key([], "i", lazy.spawn("dm-maim -r"), desc='Take a screenshot'),
        Key([], "j", lazy.spawn("rofimoji"), desc='Choose an emoji'),
        Key([], "k", lazy.spawn("dm-kill -r"), desc='Kill processes '),
        Key([], "m", lazy.spawn("dm-man -r"), desc='View manpages'),
        # Key([], "n", lazy.spawn("dm-note -r"), desc='Store and copy notes'),
        # Key([], "o", lazy.spawn("dm-bookman -r"), desc='Browser bookmarks'),
        # Key([], "p", lazy.spawn("rofi-pass"), desc='Logout menu'),
        Key([], "q", lazy.spawn("dm-logout -r"), desc='Logout menu'),
        # Key([], "r", lazy.spawn("dm-radio -r"), desc='Listen to online radio'),
        Key([], "s", lazy.spawn("dm-websearch -r"), desc='Search various engines'),
        # Key([], "t", lazy.spawn("dm-translate -r"), desc='Translate text')
    ])
]

groups = []
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]

group_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]
# group_labels = ["DEV", "WWW", "SYS", "DOC", "VBOX", "CHAT", "MUS", "VID", "GFX",]
# group_labels = ["", "", "", "", "", "", "", "", "",]

group_layouts = ["monadtall", "monadtall", "tile", "tile", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall"]

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
        DropDown('gstm', ['gstm'], on_focus_lost_hide=True, warp_pointer=True, opacity=0.9, height=0.8, width=0.4),
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

colors = colors.DoomOne

layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": colors[8],
                "border_normal": colors[0]
                }

layouts = [
    # layout.Bsp(**layout_theme),
    # layout.Floating(**layout_theme)
    # layout.RatioTile(**layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Matrix(**layout_theme),
    layout.MonadTall(**layout_theme),
    # layout.MonadWide(**layout_theme),
    layout.Tile(
         shift_windows=True,
         border_width=0,
         margin=0,
         ratio=0.335,
         ),
    layout.Max(
         border_width=0,
         margin=0,
         ),
    # layout.Stack(**layout_theme, num_stacks=2),
    # layout.Columns(**layout_theme),
    # layout.TreeTab(
    #      font = "Ubuntu Bold",
    #      fontsize = 11,
    #      border_width = 0,
    #      bg_color = colors[0],
    #      active_bg = colors[8],
    #      active_fg = colors[2],
    #      inactive_bg = colors[1],
    #      inactive_fg = colors[0],
    #      padding_left = 8,
    #      padding_x = 8,
    #      padding_y = 6,
    #      sections = ["ONE", "TWO", "THREE"],
    #      section_fontsize = 10,
    #      section_fg = colors[7],
    #      section_top = 15,
    #      section_bottom = 15,
    #      level_shift = 8,
    #      vspace = 3,
    #      panel_width = 240
    #      ),
    # layout.Zoomy(**layout_theme),
]

widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize=12,
    padding=0,
    background=colors[0]
)

extension_defaults = widget_defaults.copy()

decor_right = {
    "decorations": [
        PowerLineDecoration(
            path="arrow_right"
            # path="rounded_right"
            # path="forward_slash"
            # path="back_slash"
        )
    ],
}

def init_widgets_list(screen: int) -> List:
    logger.warning('qtile.screens: %s', qtile.screens)
    widgets_list = [
        widget.Image(
            filename="~/.config/qtile/icons/logo.png",
            scale="False",
            mouse_callbacks={'Button1': lambda: qtile.spawn('rofi -show drun')},
        ),
        widget.Prompt(
            font="Ubuntu Mono",
            fontsize=14,
            foreground=colors[1],
        ),
        widget.GroupBox(
            fontsize=11,
            margin_y=5,
            margin_x=5,
            padding_y=0,
            padding_x=1,
            borderwidth=3,
            active=colors[8],
            inactive=colors[1],
            rounded=False,
            highlight_color=colors[2],
            highlight_method="line",
            this_current_screen_border=colors[7],
            this_screen_border=colors[4],
            other_current_screen_border=colors[7],
            other_screen_border=colors[4],
            # https://docs.qtile.org/en/latest/manual/faq.html#how-can-i-get-my-groups-to-stick-to-screens
            # visible_groups=None if len(qtile.screens) == 1 else '12345' if screen == 0 else '6789',
        ),
        widget.TextBox(
            text='|',
            font="Ubuntu Mono",
            foreground=colors[1],
            padding=2,
            fontsize=14
        ),
        widget.CurrentLayoutIcon(
            # custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
            foreground=colors[1],
            padding=4,
            scale=0.6
        ),
        widget.CurrentLayout(
            foreground=colors[1],
            padding=5
        ),
        widget.TextBox(
            text='|',
            font="Ubuntu Mono",
            foreground=colors[1],
            padding=2,
            fontsize=14
        ),
        widget.WindowName(
            foreground=colors[6],
            max_chars=40
        ),
        widget.GenPollText(
            update_interval=300,
            func=lambda: subprocess.check_output("printf $(uname -r)", shell=True, text=True),
            foreground=colors[3],
            fmt='❤  {}',
            decorations=[
                BorderDecoration(
                    colour=colors[3],
                    border_width=[0, 0, 2, 0],
                )
            ],
        ),
        widget.Spacer(length=8),
        widget.CPU(
            format=' Cpu: {load_percent}%',
            foreground=colors[4],
            mouse_callbacks={
               'Button1': lambda: qtile.spawn(my_term + ' -e htop'),  # Left click opens xterm
               #'Button3': lambda: qtile.spawn('htop'),   # Right click opens htop
            },
            decorations=[
                BorderDecoration(
                    colour=colors[4],
                    border_width=[0, 0, 2, 0],
               )
            ],
        ),
        widget.Spacer(length=8),
        widget.Memory(
            foreground=colors[8],
            mouse_callbacks={'Button1': lambda: qtile.spawn(my_term + ' -e htop')},
            font='Symbols Nerd Font',
            format='{MemUsed: .0f}{mm}',
            fmt=' Mem: {} used',
            decorations=[
                BorderDecoration(
                    colour=colors[8],
                    border_width=[0, 0, 2, 0],
                )
            ],
        ),
        widget.Spacer(length=8),
        widget.DF(
            update_interval=60,
            foreground=colors[5],
            mouse_callbacks={'Button1': lambda: qtile.spawn(my_term + ' -e df')},
            partition='/',
            # format='[{p}] {uf}{m} ({r:.0f}%)',
            format='{uf}{m} free',
            fmt='󱥎  Disk: {}',
            visible_on_warn=False,
            decorations=[
                BorderDecoration(
                    colour=colors[5],
                    border_width=[0, 0, 2, 0],
               )
            ],
        ),
        widget.Spacer(length=8),
        widget.Volume(
            foreground=colors[7],
            # emoji=True,
            # emoji_list=['', '󰕿', '󰖀', '󰕾'],
            fmt='󰕿  Vol: {}',
            mute_format='-',  # '' ,
            mouse_callbacks={'Button3': lambda: qtile.spawn('pavucontrol')},
            decorations=[
                BorderDecoration(
                    colour=colors[7],
                    border_width=[0, 0, 2, 0],
                )
            ],
        ),
        widget.Spacer(length=8),
        widget.CheckUpdates(
            distro='Arch_yay',
            foreground=colors[4],
            execute=my_term + " -e yay -Syu --confirm",
            #mouse_callbacks={'Button1': lazy.spawn(my_term + " -e sudo pacman -Syu --confirm")},
            decorations=[
                BorderDecoration(
                    colour=colors[4],
                    border_width=[0, 0, 2, 0],
                )
            ],
        ),
        # widget.KeyboardLayout(
        #     configured_keyboards=['es'],
        #     foreground=colors[4],
        #     fmt='⌨  Kbd: {}',
        #     decorations=[
        #         BorderDecoration(
        #             colour=colors[4],
        #             border_width=[0, 0, 2, 0],
        #         )
        #     ],
        # ),
        widget.Spacer(length=8),
        widget.Clock(
            foreground=colors[8],
            format="⏱  %a, %b %d - %H:%M",
            decorations=[
                BorderDecoration(
                    colour=colors[8],
                    border_width=[0, 0, 2, 0],
                )
            ],
        ),
        # widget.Spacer(length=8),
        # qtile_extras.widget.StatusNotifier(),
        # widget.Wlan(
        #     **decor_right,
        #     #background=Color2+".4",
        #     padding=10,
        #     format='{essid} {percent:2.0%}',
        #     mouse_callbacks={"Button1": lambda: qtile.spawn("alacritty -e nmtui")},
        # ),
        # qtile_extras.widget.Bluetooth(
        #     **decor_right,
        #     default_text=' {connected_devices}',
        #     foreground=colors[7],
        #     padding=10,
        #     mouse_callbacks={"Button1": lambda: qtile.spawn("blueman-manager")},
        # ),
        # only show systray on screen 0 becuase it cannot be displayed on mora than 1 screen
        *([widget.Spacer(length=8), widget.Systray(padding=3)] if screen == 0 else []),
        widget.Spacer(length=8),
        widget.TextBox(
            padding=5,
            text=" ",
            fontsize=20,
            # mouse_callbacks={"Button1": lambda: qtile.spawn(home + "/.config/qtile/scripts/powermenu.sh")},
            mouse_callbacks={"Button1": lambda: qtile.spawn("dm-logout -r")},
        ),

    ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list(0)
    return widgets_screen1

# All other monitors' bars will display everything but widgets 22 (systray) and 23 (spacer).
def init_widgets_screen2():
    widgets_screen2 = [w for w in init_widgets_list(1)
                       if not isinstance(w, widget.Systray)]
    return widgets_screen2

# For adding transparency to your bar, add (background="#00000000") to the "Screen" line(s)
# For ex: Screen(top=bar.Bar(widgets=init_widgets_screen2(), background="#00000000", size=24)),

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_list(0), size=26)),
            Screen(top=bar.Bar(widgets=init_widgets_list(1), size=26)),
            ]


if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list(0)
    widgets_screen1 = init_widgets_list(0)
    widgets_screen2 = init_widgets_list(1)

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)


def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)


def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)

@qtile_extras.hook.subscribe.up_battery_low
def battery_low():
    send_notification("Power HQ", "Battery is running low")


@qtile_extras.hook.subscribe.up_battery_critical
def battery_critical():
    send_notificacion("Power HQ", "Battery is critically low. Plug in power cable.")


@hook.subscribe.startup
def run_every_startup():
    send_notification("Qtile", "Config reloading is done.")


@qtile_extras.hook.subscribe.up_power_connected
def plugged_in():
    send_notification("Power HQ", "The power have been plugged in, charging up.")


@qtile_extras.hook.subscribe.up_power_disconnected
def unplugged():
    send_notification("Power HQ", "The power cable is disconnected, discharging.")


# Called when system wakes up from sleep, suspend or hibernate.
# https://docs.qtile.org/en/latest/manual/ref/hooks.html#libqtile.hook.subscribe.resume
@hook.subscribe.resume
def resume():
    subprocess.run(["xrandr", "--auto"])  # to activate all connected devices
    subprocess.run(["autorandr", "--change"])
    qtile.restart()


# from https://github.com/ramnes/qtile-config/blob/98e097cfd8d5dd1ab1858c70babce141746d42a7/config.py#L108
# https://docs.qtile.org/en/latest/manual/ref/hooks.html#libqtile.hook.subscribe.screen_change
@hook.subscribe.screen_change
def set_screens(qtile, event):
    """
    Called when the output configuration is changed (e.g. via randr in X11).
    """
    logger.info('set_screens %s', qtile)
    subprocess.run(["autorandr", "--change"])
    qtile.restart()
    # qtile.reload_config()


# https://docs.qtile.org/en/latest/manual/faq.html#how-can-i-get-my-groups-to-stick-to-screens
@hook.subscribe.screens_reconfigured
async def _():
    logger.error('screens_reconfigured %s', qtile.screens)
    for w in widgets_screen1:
        if isinstance(widget.GroupBox, w):
            if len(qtile.screens) > 1:
                w.visible_groups = '12345'
            else:
                w.visible_groups = None  # show all
            if hasattr(w, 'bar'):
                w.bar.draw()
    qtile.restart()

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_focus=colors[8],
    border_width=2,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="arandr"),         # arandr
        Match(wm_class="blueman-manager"),# Blueman-manager
        Match(wm_class="confirmreset"),   # gitk
        Match(wm_class="dialog"),         # dialog boxes
        Match(wm_class="download"),       # downloads
        Match(wm_class="error"),          # error msgs
        Match(wm_class="file_progress"),  # file progress boxes
        Match(wm_class='kdenlive'),       # kdenlive
        Match(wm_class="makebranch"),     # gitk
        Match(wm_class="maketag"),        # gitk
        Match(wm_class="notification"),   # notifications
        Match(wm_class="pavucontrol"),    # pavucontrol
        Match(wm_class='pinentry-gtk-2'), # GPG key password entry
        Match(wm_class="ssh-askpass"),    # ssh-askpass
        Match(wm_class="toolbar"),        # toolbars
        Match(wm_class="Yad"),            # yad boxes
        Match(title="branchdialog"),      # gitk
        Match(title='Confirmation'),      # tastyworks exit box
        Match(title='Qalculate!'),        # qalculate-gtk
        Match(title="pinentry"),          # GPG key password entry
        Match(title="tastycharts"),       # tastytrade pop-out charts
        Match(title="tastytrade"),        # tastytrade pop-out side gutter
        Match(title="tastytrade - Portfolio Report"), # tastytrade pop-out allocation
        Match(wm_class="tasty.javafx.launcher.LauncherFxApp"), # tastytrade settings
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
