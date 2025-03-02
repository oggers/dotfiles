import subprocess

from .keys import my_term
from libqtile import qtile, widget
from libqtile.lazy import lazy
from .colors import colors
from qtile_extras.widget.decorations import BorderDecoration, RectDecoration


widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize=12,
    padding=3,
    background=colors[0]
)


decoration_group = {
    "decorations": [
        RectDecoration(
            colour='#00000000', use_widget_background=True, radius=15,
            filled=True, group=True, clip=True, ignore_extrawidth=True)
    ],
}


decoration_border = {
    'decorations': [
        RectDecoration(
            colour='#00000000', line_colour='#ffffff', line_width=3,
            use_widget_background=True, radius=15, filled=True,
            group=True, clip=True, ignore_extrawidth=True)
    ]
}


primary_widgets = [
    widget.Image(
        filename="~/.config/qtile/icons/logo.png",
        scale="False",
        mouse_callbacks={'Button1': lambda: qtile.spawn('rofi -show drun')},
        **decoration_border,
        ),
    widget.TextBox(
        text='',
        fontsize=18,
        padding=9,
        mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(my_term)},
        ),
    widget.TextBox(
        text='󰈹',
        fontsize=20,
        padding=9,
        mouse_callbacks={'Button1': lambda: qtile.cmd_spawn('firefox')},
        ),
    widget.TextBox(
        text='',
        fontsize=19,
        padding=10,
        mouse_callbacks={'Button1': lambda: qtile.cmd_spawn('thunar')},
        ),
    widget.Sep(
        padding=12,
        foreground='#00000000',
        ),
    widget.CurrentLayoutIcon(
        # custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
        foreground=colors[1],
        padding=4,
        scale=0.6
        ),
    # widget.CurrentLayout(
    #     font='Ubuntu Mono',
    #     fontsize=16,
    #     foreground=colors[1],
    #     padding=14,
    #     **decoration_group,
    #     background=colors[6],
    #     ),
    widget.TaskList(
        font='Ubuntu Mono',
        fontsize=12,
        icon_size=20,
        padding=6,
        highlight_method='text',
        border=colors[8],
        title_width_method='uniform',
        theme_mode='preferred',
        spacing=-2,
        borderwidth=1,
        max_title_width=100,
        ),
    widget.Spacer(
        ),
    widget.GroupBox(
        font='Ubuntu Mono',
        fontsize=16,
        padding=10,
        center_aligned=True,
        highlight_method='line',
        # block_highlight_text_color=colors['dark'],
        highlight_color=colors[2],  # ['orange'],
        inactive=colors[7],  # ['white'],
        hide_unused=True,
        active=colors[8],  # ['orange'],
        this_current_screen_border=colors[7],  # ['orange'],
        this_screen_border=colors[4],  # ['orange'],
        other_current_screen_border=colors[7],  # ['orange'],
        other_screen_border=colors[4],  # ['orange'],
        urgent_border=colors[4],  # ['orange'],
        rounded=True,
        disable_drag=True,
        **decoration_group,
        background=colors[0],
        ),
    widget.Spacer(
        ),
    widget.PulseVolume(
        mode='icon',
        emoji=True,
        #theme_path='/usr/share/icons/BeautyLine/',
        bar_width=50,
        bar_height=75,
        channel='Master',
        icon_size=28,
        padding=14,
        volume_down_command='XF86AudioLowerVolume',
        volume_up_command='XF86AudioRaiseVolume',
        mouse_callbacks={'Button3': lambda: qtile.cmd_spawn("pavucontrol")},
        **decoration_group,
        background=colors[0],
        ),
    widget.Sep(
        padding=14,
        background=colors[0],
        foreground='#00000000',  # transparency
        **decoration_group
        ),

    widget.Spacer(length=8),
    widget.CheckUpdates(
        distro='Arch_yay',
        foreground=colors[4],
        execute=my_term + " -e yay -Syu --confirm",
        # mouse_callbacks={'Button1': lazy.spawn(my_term + " -e sudo pacman -Syu --confirm")},
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
        mouse_callbacks={
            "Button1": lazy.group['scratchpad'].dropdown_toggle('khal')},
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
    widget.Spacer(length=8),
    widget.Systray(padding=3),
    widget.Spacer(length=8),
    widget.TextBox(
        padding=5,
        text=" ",
        fontsize=20,
        # mouse_callbacks={"Button1": lambda: qtile.spawn(home + "/.config/qtile/scripts/powermenu.sh")},
        mouse_callbacks={"Button1": lambda: qtile.spawn("dm-logout -r")},
    ),

]


secondary_widgets = primary_widgets[:-4] + primary_widgets[-2:]
