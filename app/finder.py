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
from app.common import build_packet, read_packet


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
    send_socket.sendto(
        build_packet(
            mode=1, model_id="PyCamFinder", ip_address="10.1.1.1", model_name="Finder"
        ),
        ("<broadcast>", SEND_PORT),
    )

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
        # print(response)


if __name__ == "__main__":
    main()
