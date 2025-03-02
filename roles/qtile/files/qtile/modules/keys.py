from pathlib import Path

from libqtile import qtile
from libqtile.config import Key, KeyChord
from libqtile.layout import TreeTab
from libqtile.lazy import lazy
from libqtile.log_utils import logger


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


keys = [
    # The essentials
    Key([mod], "Return", lazy.spawn(my_term), desc="Terminal"),
    Key([mod, "shift"], "Return", lazy.spawn("rofi -show drun -show-icons"), desc='Run Launcher'),
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
    Key([mod, "shift"], "space", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),

    # Treetab prompt
    Key([mod, "shift"], "a", add_treetab_section,
        desc='Prompt to add new section in treetab'),

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
    Key([mod], "Print", lazy.spawn("xfce4-screenshooter"), desc='Launch xfce4-screenshooter'),

    # Volume
    Key([], "XF86AudioMute", lazy.spawn("amixer -D pulse set Master toggle"), desc='Mute audio'),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -D pulse set Master 5%+"), desc='Raise audio volume'),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -D pulse set Master 5%-"), desc='Lower audio volume'),

    # Brightness
    Key([], 'XF86MonBrightnessUp', lazy.spawn('brightnessctl -q s +20%'), desc='Up brightness'),
    Key([], 'XF86MonBrightnessDown', lazy.spawn('brightnessctl -q s 20%-'), desc='Down brightness'),

    # ScratchPad
    KeyChord([mod], "s", [
        Key([], "k", lazy.group["scratchpad"].dropdown_toggle("keepass"), desc='Launch Keepass'),
        Key([], "g", lazy.group["scratchpad"].dropdown_toggle("gstm"), desc='Launch gSTM'),
    ], desc='Scratchpad group'),

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
    ], desc='Emacs group'),
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
    ], desc='Scritps group')
]


def modifier_name(key: str) -> str:
    if key == 'mod4':
        return 'Super'
    else:
        return key


def define_help_key(keys: list[Key]) -> Key:
    help_key = 'w'
    help_desc = 'Show qtile keys in rofi'
    keys_str = ''
    for key in keys:
        keypress = list(map(modifier_name, key.modifiers)) + [key.key]
        keypress_str = '-'.join(keypress)
        keys_str += keypress_str + ': ' + key.desc + '\n'
        if isinstance(key, KeyChord):
            for sub_key in key.submappings:
                keys_str += keypress_str + ', ' + sub_key.key + ': ' + sub_key.desc + '\n'
    keys_str += f'{modifier_name(mod)}-{help_key}: {help_desc}'

    launcher = 'rofi -show run -matching fuzzy'
    return Key([mod], help_key,
        lazy.spawn(f"echo -en '{keys_str}' | {launcher} -dmenu -p 'Qtile keys'", shell=True),
        desc=help_desc)
