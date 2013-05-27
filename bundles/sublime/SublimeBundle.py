from IdeTools.tools.Bundle import Bundle

class SublimeBundle(Bundle):
    def __init__(self,path, options):
        print("Sublime bundle")
        super().__init__(path, options)