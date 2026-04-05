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

import bcrypt

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher

import nacl.signing

from paramiko.message import Message
from paramiko.pkey import PKey, OPENSSH_AUTH_MAGIC, _unpad_openssh
from paramiko.util import b
from paramiko.ssh_exception import SSHException, PasswordRequiredException


class Ed25519Key(PKey):
    """
    Representation of an `Ed25519 <https://ed25519.cr.yp.to/>`_ key.

    .. note::
        Ed25519 key support was added to OpenSSH in version 6.5.

    .. versionadded:: 2.2
    .. versionchanged:: 2.3
        Added a ``file_obj`` parameter to match other key classes.
    """

    name = "ssh-ed25519"

    def __init__(
        self, msg=None, data=None, filename=None, password=None, file_obj=None
    ):
        self.public_blob = None
        verifying_key = signing_key = None
        if msg is None and data is not None:
            msg = Message(data)
        if msg is not None:
            self._check_type_and_load_cert(
                msg=msg,
                key_type=self.name,
                cert_type="ssh-ed25519-cert-v01@openssh.com",
            )
            verifying_key = nacl.signing.VerifyKey(msg.get_binary())
        elif filename is not None:
            with open(filename, "r") as f:
                pkformat, data = self._read_private_key("OPENSSH", f)
        elif file_obj is not None:
            pkformat, data = self._read_private_key("OPENSSH", file_obj)

        if filename or file_obj:
            signing_key = self._parse_signing_key_data(data, password)

        if signing_key is None and verifying_key is None:
            raise ValueError("need a key")

        self._signing_key = signing_key
        self._verifying_key = verifying_key

    def _parse_signing_key_data(self, data, password):
        pass

    def asbytes(self):
        pass

    @property
    def _fields(self):
        pass

    # TODO 4.0: remove
    def get_name(self):
        pass

    def get_bits(self):
        pass

    def can_sign(self):
        pass

    def sign_ssh_data(self, data, algorithm=None):
        pass

    def verify_ssh_sig(self, data, msg):
        pass
