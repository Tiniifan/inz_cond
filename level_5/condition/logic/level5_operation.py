class Level5Operation:
    def __init__(self, operator_left, operator_right, operator_middle, operator_type="int"):     
        self._operator_left = operator_left
        self._operator_right = operator_right
        self._operator_middle = operator_middle
        self._operator_type = operator_type
    
    @property
    def operator_left(self):
        return self._operator_left
    
    @property
    def operator_right(self):
        return self._operator_right
    
    @property
    def operator_middle(self):
        return self._operator_middle
    
    @property
    def operator_type(self):
        return self._operator_type
    
    def __repr__(self):
        return (f"<Level5Operation "
                f"operator_left={self.operator_left} "
                f"operator_middle={self.operator_middle.name} "
                f"operator_right={self.operator_right} "
                f"operator_type={self.operator_type}>")
