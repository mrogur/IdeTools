import os, sys, sublime

class IdeToolsConfig(object):
    def __init__(self, window=None):
        if window:
            self.window = window

            
    def load(self):
        pass

    def save(self):
        pass    

    
    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, window):
        print("Setting window")
        if not isinstance(window, sublime.Window):
            raise ValueError("window property must be a instance of sublime.Window class")            
        self._window = window    