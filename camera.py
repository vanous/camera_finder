import struct
from socket import (
    AF_INET,
    SHUT_RDWR,
    SO_BROADCAST,
    SO_REUSEADDR,
    SOCK_DGRAM,
    SOL_SOCKET,
    socket,
    inet_pton,
)


def main():
    print("Hello from python-camera!")

    RECEIVE_PORT = 7701
    SEND_PORT = 7711
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

    while True:
        data = b""
        try:
            data = receive_socket.recv(1024)
        except Exception as e:
            print(e)
        print("got data", data)
        print("packet", struct.unpack("B", data[0:1]))
        print("client", struct.unpack("18s", data[1:19]))
        print("mac", struct.unpack("18B", data[19:37]))
        print("ip", struct.unpack("16B", data[37:53]))

        if struct.unpack("B", data[0:1])[0] == 1:
            send_socket.sendto(build_response(), ("<broadcast>", SEND_PORT))


def build_response():
    content = []
    content.append(struct.pack("B", 11))

    model_id = "PyCam"
    content.append(
        struct.pack("18s", model_id.encode("utf-8")[:18].ljust(18, b"\x00"))
    )  # model name
    content.append(struct.pack("18B", *[0] * 18))  #  MAC

    ipv4_address = "192.168.20.144"
    content.append(
        struct.pack("16s", ipv4_address.encode("utf-8")[:16].ljust(16, b"\x00"))
    )  # ip address
    content.append(struct.pack("16B", *[0] * 16))  #  subnet mask
    content.append(struct.pack("16B", *[0] * 16))  #  gateway
    content.append(struct.pack("20B", *[0] * 20))  #  pasword
    content.append(struct.pack("B", 0))  #  reserved
    content.append(struct.pack("H", 80))  #  port
    content.append(struct.pack("B", 0))  #  status
    model_name = "My name"
    content.append(
        struct.pack("10s", model_name.encode("utf-8")[:10].ljust(10, b"\x00"))
    )  # model name
    content.append(struct.pack("B", 0))  #  reserved
    content.append(struct.pack("H", 80))  #  http port
    content.append(struct.pack("H", 0))  #  device port
    content.append(struct.pack("H", 0))  #  tcp port
    content.append(struct.pack("H", 0))  #  udp port
    content.append(struct.pack("H", 0))  #  upload port
    content.append(struct.pack("H", 0))  #  multicast port
    content.append(struct.pack("B", 0))  #  network mode
    content.append(struct.pack("128s", "".encode("utf-8")))  #  DDNS url
    content.append(struct.pack("B", 0))  #  ip type
    print("len", len(content))
    print("len2", len(b"".join(content)))
    print(b"".join(content))

    # stitch together
    return b"".join(content)


if __name__ == "__main__":
    main()
