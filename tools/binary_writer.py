import struct

class BinaryDataWriter:
    def __init__(self, order='big'):
        self._data = bytearray()
        self._offset = 0
        self._order = order
    
    @property
    def length(self):
        return len(self._data)
    
    @property
    def offset(self):
        return self._offset
    
    @property
    def data(self):
        return bytes(self._data)
    
    @property
    def order(self):
        return self._order
    
    @order.setter
    def order(self, value):
        if value not in ('big', 'little'):
            raise ValueError("Order must be 'big' or 'little'")
        self._order = value
    
    def write_bytes(self, b):
        end_offset = self._offset + len(b)
        if end_offset > len(self._data):
            self._data.extend(b'\x00' * (end_offset - len(self._data)))
        self._data[self._offset:end_offset] = b
        self._offset = end_offset
    
    def write_byte(self, value):
        if not 0 <= value <= 0xFF:
            raise ValueError("Byte value must be in range 0-255.")
        self.write_bytes(bytes([value]))
    
    def write_int32(self, value, order=None):
        if not 0 <= value <= 0xFFFFFFFF:
            raise ValueError("Int32 value must be in range 0-4294967295.")
        byte_order = order if order else self._order
        format_char = ">I" if byte_order == 'big' else "<I"
        self.write_bytes(struct.pack(format_char, value))
    
    def write_int24(self, value, order=None):
        if not 0 <= value <= 0xFFFFFF:
            raise ValueError("Hex3 value must be in range 0-16777215.")
        byte_order = order if order else self._order
        self.write_bytes(value.to_bytes(3, byteorder=byte_order))
    
    def skip(self, length):
        if self._offset + length > len(self._data):
            self._data.extend(b'\x00' * (self._offset + length - len(self._data)))
        self._offset += length
    
    def to_seek(self, position):
        if position < 0 or position > len(self._data):
            raise ValueError("Invalid seek position.")
        self._offset = position