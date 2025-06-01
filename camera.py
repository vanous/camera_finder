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
        print("data", data[0])
        if struct.unpack("B", data[0:1])[0] == 1:
            send_socket.sendto(build_response(), ("<broadcast>", SEND_PORT))


def build_response():
    content = []
    content.append(struct.pack("B", 11))

    model_id = "PyCam"
    content.append(
        struct.pack("18s", model_id.encode("utf-8")[:10].ljust(10, b"\x00"))
    )  # model name
    content.append(struct.pack("18B", *[0] * 18))  #  MAC

    ipv4_address = "192.168.1.1"
    packed_ipv4 = list(inet_pton(AF_INET, ipv4_address))
    print(packed_ipv4)
    content.append(
        struct.pack("16B", *packed_ipv4 + [0] * (16 - len(packed_ipv4)))
    )  # IP address
    content.append(struct.pack("16B", *[0] * 16))  #  subnet mask
    content.append(struct.pack("16B", *[0] * 16))  #  gateway
    content.append(struct.pack("20B", *[0] * 20))  #  unused
    content.append(struct.pack("H", 80))  #  port
    content.append(struct.pack("B", 0))  #  upnp mapping status
    model_name = "My name"
    content.append(
        struct.pack("10s", model_name.encode("utf-8")[:10].ljust(10, b"\x00"))
    )  # model name
    content.append(struct.pack("H", 80))  #  port
    content.append(struct.pack("H", 80))  #  port
    content.append(struct.pack("4H", 0, 0, 0, 0))  #  unused
    content.append(struct.pack("B", 0))  #  ip type
    content.append(struct.pack("128s", "".encode("utf-8")))  #  DDNS url

    # stitch together
    return b"".join(content)


if __name__ == "__main__":
    main()
