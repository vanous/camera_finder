# Copyright (C) none 
#
# This file is part of Camera Finder.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import struct
from types import SimpleNamespace


class ByteWriter:
    def __init__(self):
        self.data = bytearray()  # Use bytearray for mutable byte storage

    def write(self, fmt, *values):
        # Pack the values according to the format and append to the data
        packed_data = struct.pack(fmt, *values)
        self.data.extend(packed_data)

    def get_bytes(self):
        return bytes(self.data)  # Return an immutable bytes object


class ByteReader:
    def __init__(self, data):
        self.data = data
        self.offset = 0

    def read(self, fmt):
        size = struct.calcsize(fmt)
        value = struct.unpack(fmt, self.data[self.offset : self.offset + size])
        self.offset += size
        return value


def build_packet(mode=1, model_id="", ip_address="10.0.0.1", model_name=""):
    writer = ByteWriter()
    writer.write("B", mode)  # mode

    writer.write("18s", model_id.encode("utf-8")[:18].ljust(18, b"\x00"))  # model name
    writer.write("18B", *[0] * 18)  #  MAC

    writer.write(
        "16s", ip_address.encode("utf-8")[:16].ljust(16, b"\x00")
    )  # ip address
    writer.write("16B", *[0] * 16)  #  subnet mask
    writer.write("16B", *[0] * 16)  #  gateway
    writer.write("20B", *[0] * 20)  #  pasword
    writer.write("B", 0)  #  reserved
    writer.write("H", 80)  #  port
    writer.write("B", 0)  #  status
    writer.write(
        "10s", model_name.encode("utf-8")[:10].ljust(10, b"\x00")
    )  # model name
    writer.write("B", 0)  #  reserved
    writer.write("H", 80)  #  http port
    writer.write("H", 0)  #  device port
    writer.write("H", 0)  #  tcp port
    writer.write("H", 0)  #  udp port
    writer.write("H", 0)  #  upload port
    writer.write("H", 0)  #  multicast port
    writer.write("B", 0)  #  network mode
    writer.write("128s", "".encode("utf-8"))  #  DDNS url
    writer.write("B", 0)  #  ip type
    return writer.get_bytes()


def read_packet(data):
    response = SimpleNamespace()
    reader = ByteReader(data)
    response.mode = reader.read("B")[0]
    response.client = reader.read("18s")[0].rstrip(b"x\00")
    response.mac = reader.read("18B")[0]
    response.ip = reader.read("16s")[0].rstrip(b"\x00")
    response.mask = reader.read("16B")
    response.gateway = reader.read("16B")
    response.password = reader.read("20B")
    response.reserved = reader.read("B")
    response.port = reader.read("H")[0]
    response.status = reader.read("B")
    response.name = reader.read("10s")[0].rstrip(b"\x00")
    return response
