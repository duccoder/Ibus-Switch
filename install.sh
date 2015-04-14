#!/bin/sh

sudo apt-get install ibus-unikey -y
sudo apt-get install python-appindicator -y
CURRENTDIR=$(pwd)

touch ibus-switch.desktop
printf "[Desktop Entry]\nName[en]=Ibus Switch\nExec=$CURRENTDIR/switch.sh\nIcon=application-default-icon\nX-GNOME-Autostart-enabled=true\nType=Application" >> ibus-switch.desktop

sudo mv ibus-switch.desktop ~/.config/autostart/ibus-switch.desktop
printf "\n"
echo "Install Completed! Please logout or reboot system to see effect!!!"
