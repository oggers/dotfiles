#!/bin/sh

xrandr --output eDP --auto --output HDMI-A-0 --auto --left-of eDP
nm-applet &
volumeicon &
picom &
megasync &
cbatticon -u 20 -c "poweroff" -l 15 -r 3 &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
/usr/lib/xfce4/notifyd/xfce4-notifyd &
xfce4-clipman &
syncthing-gtk &
