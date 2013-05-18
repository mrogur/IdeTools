import sublime, sublime_plugin, sys, os, re, imp

#import IdeTools
#from  .projects.project import Project
from .projects import *

from .projects.project import Project



imp.reload(project)

# from IdeTools.projects.project import Project
# from IdeTools.pathutil.pathutil import PathUtil
class CreateProjectCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        tools = Project(self.view.window())
        tools.create()  