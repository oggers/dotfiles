import asyncio
import os
import subprocess
import time

from groups import groups
from libqtile import hook, qtile
from libqtile.log_utils import logger
from libqtile.utils import send_notification
import qtile_extras.hook


@qtile_extras.hook.subscribe.up_battery_low
def battery_low():
    send_notification("Power HQ", "Battery is running low")


@qtile_extras.hook.subscribe.up_battery_critical
def battery_critical():
    send_notification(
        "Power HQ", "Battery is critically low. Plug in power cable.")


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
async def resume():
    subprocess.run(["xrandr", "--auto"])  # to activate all connected devices
    await asyncio.sleep(1)
    subprocess.run(["autorandr", "--change"])
    qtile.reload_config()


# from https://github.com/ramnes/qtile-config/blob/98e097cfd8d5dd1ab1858c70babce141746d42a7/config.py#L108
# https://docs.qtile.org/en/latest/manual/ref/hooks.html#libqtile.hook.subscribe.screen_change
#@hook.subscribe.screen_change
def set_screens(event):
    """
    Called when the output configuration is changed (e.g. via randr in X11).
    """
    logger.info('set_screens %s', qtile)
    # subprocess.run(["autorandr", "--change"])
    # qtile.restart()
    qtile.reload_config()
    # qtile.reconfigure_screens()
    # qtile.reconfigure_screens()


#@hook.subscribe.screens_reconfigured
async def outputs_changed():
    logger.warning('Screens reconfigured')
    await asyncio.sleep(1)
    logger.warning('Reloading config...')
    qtile.reload_config()
    send_notification("qtile", "Screens have been reconfigured.")


# https://docs.qtile.org/en/latest/manual/faq.html#how-can-i-get-my-groups-to-stick-to-screens
# @hook.subscribe.screens_reconfigured
# async def _():
#     logger.error('screens_reconfigured %s', qtile.screens)
#     for w in widgets_screen1:
#         if isinstance(widget.GroupBox, w):
#             if len(qtile.screens) > 1:
#                 w.visible_groups = '12345'
#             else:
#                 w.visible_groups = None  # show all
#             if hasattr(w, 'bar'):
#                 w.bar.draw()
#     qtile.restart()


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.Popen([home + '/.config/qtile/autostart.sh'])


@hook.subscribe.client_new
def libreoffice(window):
    wm_class = window.get_wm_class()
    if wm_class is None:
        wm_class = []
    if [x for x in wm_class if x.startswith("libreoffice")]:
        window.disable_floating()


@hook.subscribe.client_new
def slight_delay(window):
    time.sleep(0.04)


# When application launched automatically focus it's group
@hook.subscribe.client_new
def modify_window(client):
    for group in groups:  # follow on auto-move
        match = next((m for m in group.matches if m.compare(client)), None)
        if match:
            targetgroup = client.qtile.groups_map[group.name]  # there can be multiple instances of a group
            targetgroup.toscreen(toggle=False)
            break
