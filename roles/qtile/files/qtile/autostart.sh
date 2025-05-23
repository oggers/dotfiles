#!/usr/bin/env bash

COLORSCHEME=DoomOne


### AUTOSTART PROGRAMAS ###
setxkbmap -layout es
picom --daemon &
xfce4-power-manager &
nm-applet &
volumeicon &
megasync &
flameshot &
blueman-applet &
cbatticon -u 20 -c "poweroff" -l 15 -r 3 &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
/usr/lib/xfce4/notifyd/xfce4-notifyd &
xfce4-clipman &
syncthing-gtk &
#xrandr --output eDP --auto --output HDMI-A-0 --auto --left-of eDP
#xrandr --output HDMI-A-0 --auto --primary --output eDP --auto --right-of HDMI-A-0
#xrandr --output HDMI-A-0 2560x1440 --primary --output eDP 1280x720+2560 --right-of HDMI-A-0
#"$HOME"/.screenlayout/dualmonitor.sh &
autorandr --change
sleep 1
conky -c "$HOME"/.config/conky/qtile/01/"$COLORSCHEME".conf || echo "Couldn't start conky."
python3 /usr/share/slimbookamdcontroller/src/slimbookamdcontrollerindicator.py
python3 /usr/share/slimbookbattery/src/slimbookbatteryindicator.py
