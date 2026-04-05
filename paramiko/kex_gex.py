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
Variant on `KexGroup1 <paramiko.kex_group1.KexGroup1>` where the prime "p" and
generator "g" are provided by the server.  A bit more work is required on the
client side, and a **lot** more on the server side.
"""

import os
from hashlib import sha1, sha256

from paramiko import util
from paramiko.common import DEBUG, byte_chr, byte_ord, byte_mask
from paramiko.message import Message
from paramiko.ssh_exception import SSHException


(
    _MSG_KEXDH_GEX_REQUEST_OLD,
    _MSG_KEXDH_GEX_GROUP,
    _MSG_KEXDH_GEX_INIT,
    _MSG_KEXDH_GEX_REPLY,
    _MSG_KEXDH_GEX_REQUEST,
) = range(30, 35)

(
    c_MSG_KEXDH_GEX_REQUEST_OLD,
    c_MSG_KEXDH_GEX_GROUP,
    c_MSG_KEXDH_GEX_INIT,
    c_MSG_KEXDH_GEX_REPLY,
    c_MSG_KEXDH_GEX_REQUEST,
) = [byte_chr(c) for c in range(30, 35)]


class KexGex:

    name = "diffie-hellman-group-exchange-sha1"
    min_bits = 1024
    max_bits = 8192
    preferred_bits = 2048
    hash_algo = sha1

    def __init__(self, transport):
        self.transport = transport
        self.p = None
        self.q = None
        self.g = None
        self.x = None
        self.e = None
        self.f = None
        self.old_style = False

    def start_kex(self, _test_old_style=False):
        pass

    def parse_next(self, ptype, m):
        pass

    # ...internals...

    def _generate_x(self):
        # generate an "x" (1 < x < (p-1)/2).
        pass

    def _parse_kexdh_gex_request(self, m):
        pass

    def _parse_kexdh_gex_request_old(self, m):
        # same as above, but without min_bits or max_bits (used by older
        # clients like putty)
        pass

    def _parse_kexdh_gex_group(self, m):
        pass

    def _parse_kexdh_gex_init(self, m):
        pass

    def _parse_kexdh_gex_reply(self, m):
        pass


class KexGexSHA256(KexGex):
    name = "diffie-hellman-group-exchange-sha256"
    hash_algo = sha256
