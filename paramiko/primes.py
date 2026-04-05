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
Utility functions for dealing with primes.
"""

import os

from paramiko import util
from paramiko.common import byte_mask
from paramiko.ssh_exception import SSHException


def _roll_random(n):
    """returns a random # from 0 to N-1"""
    pass


class ModulusPack:
    """
    convenience object for holding the contents of the /etc/ssh/moduli file,
    on systems that have such a file.
    """

    def __init__(self):
        # pack is a hash of: bits -> [ (generator, modulus) ... ]
        self.pack = {}
        self.discarded = []

    def _parse_modulus(self, line):
        pass

    def read_file(self, filename):
        """
        :raises IOError: passed from any file operations that fail.
        """
        pass

    def get_modulus(self, min, prefer, max):
        pass
