import os, sublime

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
