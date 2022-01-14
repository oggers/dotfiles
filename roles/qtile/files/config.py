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



from typing import List  # noqa: F401

from libqtile import bar, hook, extension, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

import os
import subprocess


mod = "mod4"
terminal = guess_terminal()


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([home])


colors = [["#282c34", "#282c34"],
          ["#1c1f24", "#1c1f24"],
          ["#dfdfdf", "#dfdfdf"],
          ["#ff6c6b", "#ff6c6b"],
          ["#98be65", "#98be65"],
          ["#da8548", "#da8548"],
          ["#51afef", "#51afef"],
          ["#c678dd", "#c678dd"],
          ["#46d9ff", "#46d9ff"],
          ["#a9a1e1", "#a9a1e1"]]


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html

    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
    Key([mod], "m", lazy.spawn("rofi -show drun"),
        desc="rofi"),

    #
    Key([mod, "shift"], "w", lazy.to_screen(1)),
    Key([mod, "shift"], "e", lazy.to_screen(0)),

    # screenshots
    Key([], "Print", lazy.spawn('xfce4-screenshooter')),
]


# https://www.nerdfonts.com
#  nf-linux-archlinux
#  nf-mdi-email
#  nf-fa-firefox
#  nf-oct-terminal
#  nf-dev-windows
groups = [Group(i) for i in ["1  ", "2  ", "3  ", "4  ", "5  ", "6", "7", "8", "9"]]

for i, group in enumerate(groups, 1):
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], str(i), lazy.group[group.name].toscreen(),
            desc="Switch to group {}".format(group.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], str(i), lazy.window.togroup(group.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(group.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])
layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": "e1acff",
                "border_normal": "1D2330"
                }

layouts = [
    layout.Columns(**layout_theme,
        border_focus_stack=['#d75f5f', '#8f3d3d']),
    layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(**layout_theme),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Noto Sans Regular',
    #font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets = [
        widget.Sep(
            linewidth = 0,
            padding = 6,
            foreground = colors[2],
            background = colors[0]
        ),
        widget.GroupBox(
            disable_drag=True,
            #other_current_screen_border="#44475a",
            #other_screen_border="#44475a",
            margin_y = 3,
            margin_x = 0,
            padding_y = 5,
            padding_x = 3,
            borderwidth = 3,
            active = colors[2],
            inactive = colors[7],
            rounded = False,
            highlight_color = colors[1],
            highlight_method = "line",
            this_current_screen_border = colors[6],
            this_screen_border = colors [4],
            other_current_screen_border = colors[6],
            other_screen_border = colors[4],
            foreground = colors[2],
            background = colors[0]
        ),
        widget.TextBox(
            text = '|',
            font = "Ubuntu Mono",
            background = colors[0],
            foreground = '474747',
            padding = 2,
            fontsize = 14
        ),
        widget.CurrentLayoutIcon(
            custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
            foreground = colors[2],
            background = colors[0],
            padding = 0,
            scale = 0.7
        ),
        widget.CurrentLayout(
            foreground = colors[2],
            background = colors[0],
            padding = 5
        ),
        widget.TextBox(
            text = '|',
            font = "Ubuntu Mono",
            background = colors[0],
            foreground = '474747',
            padding = 2,
            fontsize = 14
        ),
        widget.WindowTabs(
            background = colors[0],
        ),
        # widget.WindowName(
        #     foreground = colors[6],
        #     background = colors[0],
        #     padding = 0
        # ),
        widget.Chord(
            chords_colors={
                'launch': ("#ff0000", "#ffffff"),
            },
            name_transform=lambda name: name.upper(),
        ),
        widget.TextBox(
            text='',
            font = "Ubuntu Mono",
            background = colors[0],
            foreground = colors[5],
            padding = 0,
            fontsize = 37
        ),
        widget.CheckUpdates(
            update_interval = 1800,
            distro = "Arch_checkupdates",
            display_format = "Updates: {updates} ",
            no_update_string = '',
            foreground = colors[1],
            colour_have_updates = colors[1],
            colour_no_updates = colors[1],
            mouse_callbacks = {
                'Button1': lambda: qtile.cmd_spawn(terminal + ' -e sudo pacman -Syu')},
            padding = 5,
            background = colors[5]
        ),
        widget.TextBox(
            text = '',
            font = "Ubuntu Mono",
            background = colors[5],
            foreground = colors[0],
            padding = 0,
            fontsize = 37
        ),
        widget.Systray(
            background = colors[0],
            padding = 5
        ),
        widget.TextBox(
            text = '',
            font = "Ubuntu Mono",
            background = colors[0],
            foreground = colors[7],
            padding = 0,
            fontsize = 37
        ),
        widget.Volume(
            foreground = colors[1],
            background = colors[7],
            #emoji = True,
            fontsize = 12,
            fmt = 'Vol: {}',
            #theme_path='/usr/share/icons/Papirus/24x24/status/',
            mouse_callbacks={
                'Button2': lambda : qtile.cmd_spawn('pavucontrol')},
            padding = 5
        ),
        widget.TextBox(
            text = '',
            font = "Ubuntu Mono",
            background = colors[7],
            foreground = colors[9],
            padding = 0,
            fontsize = 37
        ),
        widget.Clock(
            foreground = colors[1],
            background = colors[9],
            format='%Y-%m-%d %a %H:%M %p'),
        widget.QuickExit(
            default_text='  ',
            background = colors[0],
        ),
        widget.Sep(
            linewidth = 0,
            padding = 6,
            foreground = colors[2],
            background = colors[0]
        ),
    ]
    # if os.path.isdir("/sys/module/battery"):
    #     widgets.insert(-1, widget.Battery(format=" {char} {percent:2.0%} ",
    #                                charge_char="⚡", discharge_char="🔋",
    #                                full_char="⚡", unknown_char="⚡",
    #                                empty_char="⁉️ ", update_interval=2,
    #                                show_short_text=False,
    #                                default_text=""))
    #     widgets.insert(-1, widget.Battery(fmt="<span color='#666'>{}</span> ",
    #                                format="{hour:d}:{min:02d}",
    #                                update_interval=2, show_short_text=True,
    #                                default_text=""))
    return widgets

screens = [
    Screen(
        top=bar.Bar(
            widgets=init_widgets_list(),
            size=20,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
    Screen(
        top=bar.Bar(
            widgets=init_widgets_list(),
            size=20,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

# from https://github.com/ramnes/qtile-config/blob/98e097cfd8d5dd1ab1858c70babce141746d42a7/config.py#L108
@hook.subscribe.screen_change
def set_screens(qtile, event):
    """
    Called when the output configuration is changed (e.g. via randr in X11).
    """
    subprocess.run(["autorandr", "--change"])
    qtile.cmd_restart()


dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='polkit-gnome-authentication-agent-1'),  # Gnome
    Match(wm_class='forticlient'),  # forticlient
    Match(wm_class='megasync'),  # MegaSync
    Match(wm_class='pavucontrol'),  # MegaSync
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

