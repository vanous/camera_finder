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
    content = []
    content.append(struct.pack("B", 1))
    model_id = "PyCamFinder"
    content.append(
        struct.pack("18s", model_id.encode("utf-8")[:18].ljust(18, b"\x00"))
    )  # model name
    content.append(struct.pack("243B", *[0] * 243))  #  MAC

    # stitch together
    print(content, b"".join(content))
    return b"".join(content)


if __name__ == "__main__":
    main()
