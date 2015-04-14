#!/usr/bin/env python
import os
import sys
import gtk
import appindicator
import subprocess
import json
from pprint import pprint

currentDir = os.path.dirname(os.path.realpath(__file__));
with open(currentDir + '/config.json') as data_file:
    config = json.load(data_file)

class IbusEngineIndicator:
    def __init__(self):
        self.ind = appindicator.Indicator ("ibus-engine-indicator", "indicator-keyboard-En", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status (appindicator.STATUS_ACTIVE)

        # create a menu
        self.menu = gtk.Menu()

        # create items for the menu - labels, checkboxes, radio buttons and images are supported:
        process = subprocess.Popen(["ibus", "engine"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        currentEngine, err = process.communicate()
        if len(currentEngine) == 0:
            currentEngine = "xkb:us::eng"
        group = gtk.RadioMenuItem(None)
        for key in config['engine']:
            radio = gtk.RadioMenuItem(group, config['engine'][key]["name"])
            radio.connect("activate", self.on_menu_select, key)
            if key == currentEngine.rstrip():
                radio.set_active(True)
            radio.show()
            self.menu.append(radio)

        image = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        image.connect("activate", self.quit)
        image.show()
        self.menu.append(image)
                    
        self.menu.show()

        self.ind.set_menu(self.menu)

    def on_menu_select(self, widget, key):
        if widget.get_active():
            process = subprocess.Popen(["ibus", "engine", key], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, err = process.communicate()
            if len(err) == 0:
                self.ind.set_icon (config['engine'][key]["icon"])
                subprocess.call(["notify-send", "Ibus", "Ibus engine had been switch to " + config['engine'][key]["name"]])

    def quit(self, widget, data=None):
        gtk.main_quit()


def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    indicator = IbusEngineIndicator()
    main()