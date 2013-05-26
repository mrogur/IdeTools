import sublime, sublime_plugin, sys, os, re, imp, pprint, shutil, ftplib

#Some imports reload not be available in retail 
import IdeTools.projects.Project
imp.reload(IdeTools.projects.Project)
import IdeTools.helpers.JsonSettings
imp.reload(IdeTools.helpers.JsonSettings)

from pprint import pprint
from .projects.Project import Project
from .projects.PhpProject import PhpProject
from .helpers.JsonSettings import JsonSettings
from .helpers.AskChain import AskChain
#from .helpers.TemplateTools import *

class CreateProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        tools = Project(self.window) 
        tools.create()

class IdeToolsCommand(sublime_plugin.WindowCommand):
    def run(self, **args):
        class TemplateFile(object):
            def __init__(self, root, relativePath, filename):
                self.root = root
                self.relativePath = relativePath
                self.filename = filename
                self.targetPath = None
                self.fileObj = None

            def __repr__(self):
                return os.path.join(self.root, self.relativePath, self.filename)

            def read(self):
                if not self.targetPath:
                    raise IOError("Target path is not set")
                try:    
                    self.fileObj = open(os.path.join(self.targetPath, self.filename), encoding='utf-8')
                    return self.fileObj.read()
                except IOError as e:
                    print(e)
                    return False   

        class Template(object):
            def __init__(self, context, name, projectPath):
                self.context = context
                self.name = name
                self.projectPath = projectPath

                templatesFolder = os.path.join('IdeTools','templates',context,name)


                self.sublimePackagesTemplatesPath = os.path.join(sublime.packages_path()
                                                    ,templatesFolder)

                self.sublimeUserTemplatesPath = os.path.join(sublime.packages_path()
                                                    ,'User'
                                                    ,templatesFolder)
                
                self.userDirTemplatesPath = os.path.join(os.getenv('USERPROFILE') or os.getenv('HOME')
                                                    ,'.'+templatesFolder)


                self.projectPath = projectPath
                
                self.files = []
                #print(self.sublimePackagesTemplatesPath, self.sublimeUserTemplatesPath, self.userDirTemplatesPath)

            def scanTemplateFiles(self):
                for (root, dirs, files) in os.walk(self.sublimePackagesTemplatesPath):
                    for file in files:
                        self.files.append(self.getTemplateFile(root, file))

                pprint(self.files)            

            def getTemplateFile(self, root, file):
                dirs = [ self.sublimeUserTemplatesPath
                        ,self.userDirTemplatesPath]

                relativePath = root.replace(
                    self.sublimePackagesTemplatesPath, '').strip(os.sep)

                for d in dirs:
                    path = os.path.join(d, relativePath, file)
                    if os.path.exists(path):
                        root = d 

                return TemplateFile(root, relativePath, file)        
            
            def copyTemplateFiles(self):
                for file in self.files:
                    targetDir = os.path.join(self.projectPath, file.relativePath)
                    if not os.path.exists(targetDir):
                        os.makedirs(targetDir)                
                    shutil.copy(str(file), targetDir) 
                    file.targetPath = targetDir           

            def process(self):
                for f in self.files:
                    print(f)
                    buffer = f.read()
                    if buffer:
                        print(buffer)

                        

        
                
        template = Template('php','composer', '/Users/mrogur/Code/test/vc')
        template.scanTemplateFiles()
        template.copyTemplateFiles()
        template.process()
        #template.copyFiles()
        # def mu(result):
        #     print(result)

        # def vc(value):
        #     return re.match(r'^[a-zA-Z]\w+$',value) 

        # chain = AskChain(self.window, mu)
        # chain.add("Select focus", "key5", [['lick','select lick'],'second', 'third'])
        # chain.add("First", "key", "ciułała")
        # chain.add("Second", "key3", "kardaśmon", vc, errorType='error', errorMessage="Ni ni ni")
        # chain.add("Third", "ming", ['first','second', 'third'])
        # chain.add("Select focus", "key5", ['lick','second', 'third'])
        # chain.run()


class CreatePhpProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        tools = PhpProject(self.window)
        tools.create()  
        print("foo me")