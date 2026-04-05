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
from paramiko.common import max_byte, zero_byte, byte_ord, byte_chr

import paramiko.util as util
from paramiko.util import b
from paramiko.sftp import int64


class BERException(Exception):
    pass


class BER:
    """
    Robey's tiny little attempt at a BER decoder.
    """

    def __init__(self, content=bytes()):
        self.content = b(content)
        self.idx = 0

    def asbytes(self):
        pass

    def __str__(self):
        return self.asbytes()

    def __repr__(self):
        return "BER('" + repr(self.content) + "')"

    def decode(self):
        pass

    def decode_next(self):
        pass

    @staticmethod
    def decode_sequence(data):
        pass

    def encode_tlv(self, ident, val):
        # no need to support ident > 31 here
        pass

    def encode(self, x):
        pass

    @staticmethod
    def encode_sequence(data):
        pass
