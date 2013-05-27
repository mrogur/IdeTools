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
                self.buffer = None

            def __repr__(self):
                return os.path.join(self.root, self.relativePath, self.filename)

            def read(self):
                if not self.targetPath:
                    raise IOError("Target path is not set")
                try:
                    self.fileObj = open(os.path.join(self.targetPath, self.filename), encoding='utf-8')
                    self.buffer = self.fileObj.read()
                    self.fileObj.close()

                    return True
                except IOError as e:
                    print(e)
                    return False   

            def save(self):
                open(os.path.join(self.targetPath, self.filename)
                        ,encoding='utf-8'
                        ,mode='w').write(self.buffer)                    
        
        
        class BundleTemplate(object):
            """Class scanning bundles for templates"""
            def __init__(self):
                self.bundlesDir = os.path.join(sublime.packages_path(), 'IdeTools', 'bundles')
                self.config = JsonSettings()
            def getBundles(self):
                    pass    
                
                
                

        class Template(object):
            def __init__(self, context, name, projectPath):
                self.context = context
                self.name = name
                self.projectPath = projectPath

                templatesFolder = os.path.join('IdeTools','bundles',context,'templates',name)


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
                    if f.read():
                        f.buffer= "#Alkomalko"+f.buffer
                        f.save()

                        

        
        self.window.create_output_panel("haha")
        self.window.run_command('show_panel', {"panel": "output.haha"})        
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