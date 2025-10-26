class Level5Variable:
    def __init__(self, name, lifetime, value):
        self._name = name
        self._lifetime = lifetime
        self._value = value
    
    @property
    def name(self):
        return self._name
    
    @property
    def lifetime(self):
        return self._lifetime
    
    @property
    def value(self):
        return self._value
    
    def __repr__(self):
        return (f"<Level5Variable name={self.name} "
                f"lifetime={self.lifetime.name} "
                f"value={self.value}>")