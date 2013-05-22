import sublime, sublime_plugin, sys, os, re, imp

#Some imports reload not be available in retail 
import IdeTools.projects.Project
imp.reload(IdeTools.projects.Project)
import IdeTools.helpers.JsonSettings
imp.reload(IdeTools.helpers.JsonSettings)

from .projects.Project import Project
from .projects.PhpProject import PhpProject
from .helpers.JsonSettings import JsonSettings
from .helpers.AskChain import AskChain

class CreateProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        tools = Project(self.window) 
        tools.create()

class IdeToolsCommand(sublime_plugin.WindowCommand):
    def run(self, **args):

        def mu(result):
            print(result)

        def vc(value):
            return re.match(r'^[a-zA-Z]\w+$',value) 

        chain = AskChain(self.window, mu)
        chain.add("Select focus", "key5", [['lick','select lick'],'second', 'third'])
        chain.add("First", "key", "ciułała")
        chain.add("Second", "key3", "kardaśmon", vc, errorType='error', errorMessage="Ni ni ni")
        chain.add("Third", "ming", ['first','second', 'third'])
        chain.add("Select focus", "key5", ['lick','second', 'third'])
        chain.run()


class CreatePhpProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        tools = PhpProject(self.window)
        tools.create()  
        print("foo me")