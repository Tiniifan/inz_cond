class Level5Function:
    def __init__(self, name, args):
        self._name = name
        self._args = args
    
    @property
    def name(self):
        return self._name
    
    @property
    def args(self):
        return self._args
    
    def __repr__(self):
        return (f"<Level5Function name={self.name} "
                f"args={self.args}>")