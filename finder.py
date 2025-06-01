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

        print(struct.unpack("B", data[0:1]))
        print(struct.unpack("18s", data[1:19]))
        print(struct.unpack("18B", data[19:37]))
        print(struct.unpack("16B", data[37:53]))


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
