import os, sublime, sys
from .JsonSettings import JsonSettings


class Template(object):
    def __init__(self, context, name):
        self.context = context
        self.name = name
        self.path = os.path.join(sublime.packages_path(),'IdeTools', context, name)
        self.userPath = os.path.join(sublime.packages_path(),'User','IdeTools', context, name)
        self.userHome = os.getenv('USERPROFILE') or os.getenv('HOME')

        print(self.path, self.userPath, self.userHome)


class TemplateLoader(object):
    def __init__(self, templatePath, templateName):
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

        
                    