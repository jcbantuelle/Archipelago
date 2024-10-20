import io
import os
import Utils
from kaitaistruct import KaitaiStream

class FileMod:

  def __init__(self, mod_class, filename, local_config):
    file_path = Utils.user_path(filename)
    self.file_size = os.path.getsize(file_path)

    file_io = KaitaiStream(open(file_path, 'rb'))

    self.file_contents = mod_class(file_io)
    self.file_contents._read()

    self.local_config = local_config

  def write_file(self):
    write_io = KaitaiStream(io.BytesIO(bytearray(self.file_size)))
    self.file_contents._write(write_io)

    return write_io.to_byte_array()
