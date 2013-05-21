import sublime, sublime_plugin, sys, os, re, imp

#Some imports reload not be available in retail 
import IdeTools.projects.Project
imp.reload(IdeTools.projects.Project)
import IdeTools.helpers.JsonSettings
imp.reload(IdeTools.helpers.JsonSettings)

from .projects.Project import Project
from .projects.PhpProject import PhpProject
from .helpers.JsonSettings import JsonSettings

class CreateProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        tools = Project(self.window) 
        tools.create()

class IdeToolsCommand(sublime_plugin.WindowCommand):
    def run(self, **args):
        config = JsonSettings()  
        config.data = '{"dom": "otwarty", "fuck":"me", "help":[{"value": "ąąąą"}]}'
        print(config.data)  
        print(type(config.data))

class CreatePhpProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        tools = PhpProject(self.window)
        tools.create()  
        print("foo me")