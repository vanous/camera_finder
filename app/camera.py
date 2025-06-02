# Copyright (C) 2025 vanous
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

from app.common import build_packet, read_packet


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
        receive_socket.bind(("255.255.255.255", RECEIVE_PORT))
    except OSError as e:
        print(e)
        raise ValueError("Socket opening error")

    while True:
        data = b""
        try:
            data = receive_socket.recv(1024)
        except Exception as e:
            print(e)
        response = read_packet(data)
        print(f"""Client name: {response.client}
IP address: {response.ip}
Port: {response.port}
Model ID: {response.name}
""")
        print(len(data))
        print(response)

        if response.mode == 1 or response.mode == 6:
            print("respond")
            receive_socket.sendto(
                build_packet(
                    mode=11,
                    model_id="PyCam",
                    ip_address="10.0.0.1",
                    model_name="Camera",
                ),
                ("255.255.255.255", SEND_PORT),
            )


if __name__ == "__main__":
    main()
