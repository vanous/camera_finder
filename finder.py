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


def main():
    print("Hello from camera finder!")

    RECEIVE_PORT = 7711
    SEND_PORT = 7701
    _socket = socket(AF_INET, SOCK_DGRAM)
    _socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    _socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    try:
        _socket.bind(("", RECEIVE_PORT))
    except OSError as e:
        print(e)
        raise ValueError("Socket opening error")
    _socket.sendto(build_packet(), ("<broadcast>", SEND_PORT))

    while True:
        data = b""
        try:
            data = _socket.recv(1024)
        except Exception as e:
            print(e)

        print(struct.unpack("B", data[0:1]))
        print(struct.unpack("18B", data[1:19]))
        print(struct.unpack("18B", data[19:37]))
        print(struct.unpack("16B", data[37:53]))


def build_packet():
    content = []
    content.append(struct.pack("B", 1))
    content.append(
        struct.pack("18B", *[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    )

    # stitch together
    print(content, b"".join(content))
    return b"".join(content)


if __name__ == "__main__":
    main()
