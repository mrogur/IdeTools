import os, sublime, sys
from .JsonSettings import JsonSettings


class TemplateLoader(object):
    def __init__(self, templateName):
        self.path = templatePath
        self.name = templateName
        self.configFile = os.path.join(self.path, self.name, self.name+'.idetools-template') 
        self.config = None
    def loadConfig(self):
        try:
            settings = JsonSettings(path=self.configFile)
            settings.load()
        except (OSError, ValueError) as e:
            print(e)
            return False    
        else:
            self.config = settings
            return True

        
                    