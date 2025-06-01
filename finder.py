import struct
from socket import (
    AF_INET,
    SHUT_RDWR,
    SO_BROADCAST,
    SO_REUSEADDR,
    SOCK_DGRAM,
    SOL_SOCKET,
    socket,
)
import time


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


def main():
    print("Hello from camera finder!")

    RECEIVE_PORT = 7711
    SEND_PORT = 7701
    receive_socket = socket(AF_INET, SOCK_DGRAM)
    receive_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    receive_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    send_socket = socket(AF_INET, SOCK_DGRAM)
    send_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    send_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    try:
        receive_socket.bind(("", RECEIVE_PORT))
    except OSError as e:
        print(e)
        raise ValueError("Socket opening error")
    send_socket.sendto(build_packet(), ("<broadcast>", SEND_PORT))

    while True:
        data = b""
        try:
            data = receive_socket.recv(1024)
        except Exception as e:
            print(e)
        reader = ByteReader(data)
        print("packet", reader.read("B")[0])
        print("client", reader.read("18s")[0].rstrip(b"x\00"))
        print("mac", reader.read("18B")[0])
        print("ip", reader.read("16s")[0].rstrip(b"\x00"))
        reader.read("16B")  # mask
        reader.read("16B")  # gateway
        reader.read("20B")  # passwd
        reader.read("B")  # reserved
        reader.read("H")  # port
        reader.read("B")  # status
        print("name", reader.read("10s")[0].rstrip(b"\x00"))


def build_packet():
    writer = ByteWriter()
    writer.write("B", 1)

    model_id = "PyCamFinder"
    writer.write("18s", model_id.encode("utf-8")[:18].ljust(18, b"\x00"))  # model name
    writer.write("18B", *[0] * 18)  #  MAC

    ipv4_address = "192.168.20.144"
    writer.write(
        "16s", ipv4_address.encode("utf-8")[:16].ljust(16, b"\x00")
    )  # ip address
    writer.write("16B", *[0] * 16)  #  subnet mask
    writer.write("16B", *[0] * 16)  #  gateway
    writer.write("20B", *[0] * 20)  #  pasword
    writer.write("B", 0)  #  reserved
    writer.write("H", 80)  #  port
    writer.write("B", 0)  #  status
    model_name = "Finder"
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


if __name__ == "__main__":
    main()
