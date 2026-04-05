# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA.

"""
Standard SSH key exchange ("kex" if you wanna sound cool).  Diffie-Hellman of
1024 bit key halves, using a known "p" prime and "g" generator.
"""

import os
from hashlib import sha1

from paramiko import util
from paramiko.common import max_byte, zero_byte, byte_chr, byte_mask
from paramiko.message import Message
from paramiko.ssh_exception import SSHException


_MSG_KEXDH_INIT, _MSG_KEXDH_REPLY = range(30, 32)
c_MSG_KEXDH_INIT, c_MSG_KEXDH_REPLY = [byte_chr(c) for c in range(30, 32)]

b7fffffffffffffff = byte_chr(0x7F) + max_byte * 7
b0000000000000000 = zero_byte * 8


class KexGroup1:

    # draft-ietf-secsh-transport-09.txt, page 17
    P = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE65381FFFFFFFFFFFFFFFF  # noqa
    G = 2

    name = "diffie-hellman-group1-sha1"
    hash_algo = sha1

    def __init__(self, transport):
        self.transport = transport
        self.x = 0
        self.e = 0
        self.f = 0

    def start_kex(self):
        pass

    def parse_next(self, ptype, m):
        pass

    # ...internals...

    def _generate_x(self):
        # generate an "x" (1 < x < q), where q is (p-1)/2.
        # p is a 128-byte (1024-bit) number, where the first 64 bits are 1.
        # therefore q can be approximated as a 2^1023.  we drop the subset of
        # potential x where the first 63 bits are 1, because some of those
        # will be larger than q (but this is a tiny tiny subset of
        # potential x).
        pass

    def _parse_kexdh_reply(self, m):
        # client mode
        pass

    def _parse_kexdh_init(self, m):
        # server mode
        pass
