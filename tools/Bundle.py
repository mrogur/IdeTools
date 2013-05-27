import os, sublime

from .JsonSettings import JsonSettings

class Bundle(object):
    def __init__(self, path, options):
        self.path = path
        self.name = options['name']
        self.description = options['description']
        self.options = options
        
    def __repr__(self):
        return self.path+' '+self.name+' '+self.description

        
class Bundles(object):
    """Class scanning bundles for templates"""
    def __init__(self):
        self.bundlesDir = os.path.join(sublime.packages_path(), 'IdeTools', 'bundles')
        self.config = JsonSettings()
        self.bundles = {}
        self.loadBundlesList()

    def loadBundlesList(self):
        os.chdir(self.bundlesDir)
        for file in os.listdir('.'):
            if os.path.isdir(file):
                try:
                    self.config.load(
                        os.path.join(
                            file
                           ,file.capitalize()+'.idetools-bundle' 
                        )
                    )
                except ValueError as e:
                    print(e)
                    raise e
                else:
                    bundlePath = os.path.join(self.bundlesDir, file)
                    if 'bundle' not in self.config.data:
                        self.config.data['bundle'] = file
                        self.config.save()

                    self.bundles[file] = self.config.data
        print(self.bundles)

    def loadBundle(self, bundleName):
        if not bundleName in self.bundles:
                raise ValueError("No bundle with name: "+bundleName)
        bundlePackage = bundleName.capitalize() + 'Bundle'
        try:
            bundleModuleName = 'IdeTools.bundles.'+bundleName+'.'+bundlePackage
            print( bundleModuleName)
            bundleModule = __import__(bundleModuleName, fromlist=[bundlePackage])
            print(bundleModule)                    
        except ImportError as e:
            print("No bundle")
        else:
            bundlePath = os.path.join(self.bundlesDir, bundleName)
            bundleClass = getattr(bundleModule, bundlePackage)
            return bundleClass(bundlePath, self.bundles[bundleName])
