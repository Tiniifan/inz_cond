import struct

class BinaryDataWriter:
    def __init__(self):
        self.data = bytearray()
        self.offset = 0

    def write_bytes(self, b):
        end_offset = self.offset + len(b)
        if end_offset > len(self.data):
            self.data.extend(b'\x00' * (end_offset - len(self.data)))
        self.data[self.offset:end_offset] = b
        self.offset = end_offset

    def write_byte(self, value):
        if not 0 <= value <= 0xFF:
            raise ValueError("Byte value must be in range 0-255.")
        self.write_bytes(bytes([value]))

    def write_int32(self, value):
        if not 0 <= value <= 0xFFFFFFFF:
            raise ValueError("Int32 value must be in range 0-4294967295.")
        self.write_bytes(struct.pack(">I", value))

    def write_hex3(self, value):
        if not 0 <= value <= 0xFFFFFF:
            raise ValueError("Hex3 value must be in range 0-16777215.")
        self.write_bytes(value.to_bytes(3, byteorder='big'))

    def skip(self, length):
        if self.offset + length > len(self.data):
            self.data.extend(b'\x00' * (self.offset + length - len(self.data)))
        self.offset += length

    def to_seek(self, position):
        if position < 0 or position > len(self.data):
            raise ValueError("Invalid seek position.")
        self.offset = position

    def get_position(self):
        return self.offset

    def get_data(self):
        return bytes(self.data)
