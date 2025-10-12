import struct

class BinaryDataReader:
    def __init__(self, data):
        self.data = data
        self.offset = 0

    def read_bytes(self, length):
        if self.offset + length > len(self.data):
            raise ValueError("Attempt to read beyond the end of the buffer.")
        chunk = self.data[self.offset:self.offset + length]
        self.offset += length
        return chunk

    def read_byte(self):
        return self.read_bytes(1)[0]

    def read_byte_as_hex(self):
        return f"{self.read_bytes(1)[0]:02X}"

    def read_int32(self):
        return struct.unpack(">I", self.read_bytes(4))[0]

    def read_int32_as_hex(self):
        return struct.unpack(">I", self.read_bytes(4))[0]

    def read_hex3(self):
        return int.from_bytes(self.read_bytes(3), byteorder='big')

    def skip(self, length):
        if self.offset + length > len(self.data):
            raise ValueError("Attempt to skip beyond the end of the buffer.")
        self.offset += length

    def to_seek(self, position):
        if position < 0 or position > len(self.data):
            raise ValueError("Invalid seek position.")
        self.offset = position

    def get_position(self):
        return self.offset
