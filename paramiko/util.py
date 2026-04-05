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
Useful functions used by the rest of paramiko.
"""


import sys
import struct
import traceback
import threading
import logging

from paramiko.common import (
    DEBUG,
    zero_byte,
    xffffffff,
    max_byte,
    byte_ord,
    byte_chr,
)
from paramiko.config import SSHConfig


def inflate_long(s, always_positive=False):
    """turns a normalized byte string into a long-int
    (adapted from Crypto.Util.number)"""
    pass


def deflate_long(n, add_sign_padding=True):
    """turns a long-int into a normalized byte string
    (adapted from Crypto.Util.number)"""
    pass


def format_binary(data, prefix=""):
    pass


def format_binary_line(data):
    pass


def safe_string(s):
    pass


def bit_length(n):
    pass


def tb_strings():
    pass


def generate_key_bytes(hash_alg, salt, key, nbytes):
    """
    Given a password, passphrase, or other human-source key, scramble it
    through a secure hash into some keyworthy bytes.  This specific algorithm
    is used for encrypting/decrypting private key files.

    :param function hash_alg: A function which creates a new hash object, such
        as ``hashlib.sha256``.
    :param salt: data to salt the hash with.
    :type bytes salt: Hash salt bytes.
    :param str key: human-entered password or passphrase.
    :param int nbytes: number of bytes to generate.
    :return: Key data, as `bytes`.
    """
    pass


def load_host_keys(filename):
    """
    Read a file of known SSH host keys, in the format used by openssh, and
    return a compound dict of ``hostname -> keytype ->`` `PKey
    <paramiko.pkey.PKey>`. The hostname may be an IP address or DNS name.

    This type of file unfortunately doesn't exist on Windows, but on posix,
    it will usually be stored in ``os.path.expanduser("~/.ssh/known_hosts")``.

    Since 1.5.3, this is just a wrapper around `.HostKeys`.

    :param str filename: name of the file to read host keys from
    :return:
        nested dict of `.PKey` objects, indexed by hostname and then keytype
    """
    from paramiko.hostkeys import HostKeys

    return HostKeys(filename)


def parse_ssh_config(file_obj):
    """
    Provided only as a backward-compatible wrapper around `.SSHConfig`.

    .. deprecated:: 2.7
        Use `SSHConfig.from_file` instead.
    """
    pass


def lookup_ssh_host_config(hostname, config):
    """
    Provided only as a backward-compatible wrapper around `.SSHConfig`.
    """
    pass


def mod_inverse(x, m):
    # it's crazy how small Python can make this function.
    pass


_g_thread_data = threading.local()
_g_thread_counter = 0
_g_thread_lock = threading.Lock()


def get_thread_id():
    pass


def log_to_file(filename, level=DEBUG):
    """send paramiko logs to a logfile,
    if they're not already going somewhere"""
    logger = logging.getLogger("paramiko")
    if len(logger.handlers) > 0:
        return
    logger.setLevel(level)
    f = open(filename, "a")
    handler = logging.StreamHandler(f)
    frm = "%(levelname)-.3s [%(asctime)s.%(msecs)03d] thr=%(_threadid)-3d"
    frm += " %(name)s: %(message)s"
    handler.setFormatter(logging.Formatter(frm, "%Y%m%d-%H:%M:%S"))
    logger.addHandler(handler)


# make only one filter object, so it doesn't get applied more than once
class PFilter:
    def filter(self, record):
        pass


_pfilter = PFilter()


def get_logger(name):
    pass


def constant_time_bytes_eq(a, b):
    pass


class ClosingContextManager:
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()


def clamp_value(minimum, val, maximum):
    pass


def asbytes(s):
    """
    Coerce to bytes if possible or return unchanged.
    """
    pass


# TODO: clean this up / force callers to assume bytes OR unicode
def b(s, encoding="utf8"):
    """cast unicode or bytes to bytes"""
    pass


# TODO: clean this up / force callers to assume bytes OR unicode
def u(s, encoding="utf8"):
    """cast bytes or unicode to unicode"""
    if isinstance(s, bytes):
        return s.decode(encoding)
    elif isinstance(s, str):
        return s
    else:
        raise TypeError(f"Expected unicode or bytes, got {type(s)}")
