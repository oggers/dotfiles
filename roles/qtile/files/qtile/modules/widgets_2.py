import subprocess

from .keys import my_term
from libqtile import qtile, widget
from libqtile.lazy import lazy
from .colors import colors
from qtile_extras.widget.decorations import BorderDecoration


widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize=12,
    padding=0,
    background=colors[0]
)


primary_widgets = [
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
        func=lambda: subprocess.check_output("printf $(uname -r)",
                                             shell=True, text=True),
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
