from IdeTools.tools.Bundle import Bundle

class PhpBundle(Bundle):
    def __init__(self,path, options):
        print("Php bundle")
        super().__init__(path, options)