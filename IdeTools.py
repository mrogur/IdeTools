import sublime, sublime_plugin, sys, os, re, imp

from .projects.Project import Project
from .projects.PhpProject import PhpProject

class CreateProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        tools = Project(self.window)
        tools.create()  

class CreatePhpProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        tools = PhpProject(self.window)
        tools.create()  
        print("foo me")