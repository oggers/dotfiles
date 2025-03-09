from libqtile import layout
from libqtile.config import Match
from .colors import colors


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
    layout.MonadWide(**layout_theme),
    layout.Tile(
        **layout_theme
        #  shift_windows=True,
        #  border_width=0,
        #  margin=0,
        #  ratio=0.335,
         ),
    layout.Max(
        **layout_theme
         # border_width=0,
         # margin=0,
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
        Match(wm_class="megasync"),       # megasync
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
