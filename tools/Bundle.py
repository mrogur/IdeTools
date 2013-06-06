import os, sublime


from pprint import pprint
from .JsonSettings import JsonSettings
from ..IdeToolsError import IdeToolsError



class BundlesIterator(object):
    def __init__(self):
        self.bundles = Bundles()
        self.counter = 0

    def __iter__(self):
        return self 

    def __next__(self):
        if self.counter>=len(self.bundles.bundles):
            raise StopIteration
        item =  self.bundles.bundlesList[self.counter]    
        self.counter += 1
        return item


class BundlesPromptMapper(BundlesIterator):
    def __init__(self):
        super().__init__()
    def __next__(self):
        item = super().__next__()

        try:
            description = item['description']
        except IndexError:
            description = 'No description'    

        return [item['name'], description]



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

    """Class constructor"""
    def __init__(self):
        self.bundlesDir = os.path.join(sublime.packages_path(), 'IdeTools', 'bundles')
        self.config = JsonSettings()
        self.bundles = []
        self.bundlesList = []
        self.loadBundlesList()

    """Load installed bundles list and config files"""    
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
                    raise IdeToolsError("Loading bundle error"+e.message)
                else:
                    # bundlePath = os.path.join(self.bundlesDir, file)
                    if 'bundle' not in self.config.data:
                        self.config.data['bundle'] = file
                        self.config.save()

                    self.bundles.append(file)
                    self.bundlesList.append(self.config.data)
        print(self.bundles)
        pprint(self.bundlesList)

    """Dynamically loads Bundle class"""

    def loadBundle(self, bundleName):
        if not bundleName in self.bundles:
                raise IdeToolsError("No bundle with name: "+bundleName)
        bundlePackage = bundleName.capitalize() + 'Bundle'
        try:
            bundleModuleName = 'IdeTools.bundles.'+bundleName+'.'+bundlePackage
            bundleModule = __import__(bundleModuleName, fromlist=[bundlePackage])
        except ImportError:
            raise IdeToolsError("No bundle installed:"+bundleName)
        else:
            bundlePath = os.path.join(self.bundlesDir, bundleName)
            bundleClass = getattr(bundleModule, bundlePackage)
            return bundleClass(bundlePath, self.bundles[bundleName])
