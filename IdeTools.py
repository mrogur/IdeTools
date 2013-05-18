import sublime, sublime_plugin, sys, os, re, imp

#import IdeTools
#from  .projects.project import Project
from .projects import *

from .projects.project import Project
from .projects.PhpProject import PhpProject



imp.reload(project)
#imp.reload(PhpProject) 

# from IdeTools.projects.project import Project
# from IdeTools.pathutil.pathutil import PathUtil
class CreateProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        tools = Project(self.window)
        tools.create()  

class CreatePhpProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        tools = PhpProject(self.window)
        tools.create()  
        print("fuck me now kurwa")