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
import subprocess
from typing import Callable, List  # noqa: F401

from groups import groups
import hooks
from keys import mod, my_term, keys, home
from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Match, Screen
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from qtile_extras.widget.decorations import BorderDecoration
from qtile_extras.widget.decorations import PowerLineDecoration

import colors


# https://github.com/m-col/qtile-config/blob/master/config.py
IS_WAYLAND: bool = qtile.core.name == "wayland"
IS_XEPHYR: bool = int(os.environ.get("QTILE_XEPHYR", 0)) > 0



if qtile.core.name == 'x11':
    pass
elif qtile.core.name == 'wayland':
    pass


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

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
