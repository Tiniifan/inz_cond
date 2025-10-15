import struct

class BinaryDataReader:
    def __init__(self, data, order='big'):
        self.data = data
        self._offset = 0
        self._order = order
    
    @property
    def length(self):
        return len(self.data)
    
    @property
    def offset(self):
        return self._offset
    
    @property
    def order(self):
        return self._order
    
    @order.setter
    def order(self, value):
        if value not in ('big', 'little'):
            raise ValueError("Order must be 'big' or 'little'")
        self._order = value
    
    def read_bytes(self, length):
        if self._offset + length > len(self.data):
            raise ValueError("Attempt to read beyond the end of the buffer.")
        chunk = self.data[self._offset:self._offset + length]
        self._offset += length
        return chunk
    
    def read_byte(self):
        return self.read_bytes(1)[0]
    
    def read_byte_as_hex(self):
        return f"{self.read_bytes(1)[0]:02X}"
    
    def read_int32(self, order=None):
        byte_order = order if order else self._order
        format_char = ">I" if byte_order == 'big' else "<I"
        return struct.unpack(format_char, self.read_bytes(4))[0]
    
    def read_int24(self, order=None):
        byte_order = order if order else self._order
        return int.from_bytes(self.read_bytes(3), byteorder=byte_order)
    
    def skip(self, length):
        if self._offset + length > len(self.data):
            raise ValueError("Attempt to skip beyond the end of the buffer.")
        self._offset += length
    
    def to_seek(self, position):
        if position < 0 or position > len(self.data):
            raise ValueError("Invalid seek position.")
        self._offset = position