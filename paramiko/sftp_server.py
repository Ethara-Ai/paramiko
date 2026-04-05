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
Server-mode SFTP support.
"""

import os
import errno
import sys
from hashlib import md5, sha1

from paramiko import util
from paramiko.sftp import (
    BaseSFTP,
    Message,
    SFTP_FAILURE,
    SFTP_PERMISSION_DENIED,
    SFTP_NO_SUCH_FILE,
    int64,
)
from paramiko.sftp_si import SFTPServerInterface
from paramiko.sftp_attr import SFTPAttributes
from paramiko.common import DEBUG
from paramiko.server import SubsystemHandler
from paramiko.util import b


# known hash algorithms for the "check-file" extension
from paramiko.sftp import (
    CMD_HANDLE,
    SFTP_DESC,
    CMD_STATUS,
    SFTP_EOF,
    CMD_NAME,
    SFTP_BAD_MESSAGE,
    CMD_EXTENDED_REPLY,
    SFTP_FLAG_READ,
    SFTP_FLAG_WRITE,
    SFTP_FLAG_APPEND,
    SFTP_FLAG_CREATE,
    SFTP_FLAG_TRUNC,
    SFTP_FLAG_EXCL,
    CMD_NAMES,
    CMD_OPEN,
    CMD_CLOSE,
    SFTP_OK,
    CMD_READ,
    CMD_DATA,
    CMD_WRITE,
    CMD_REMOVE,
    CMD_RENAME,
    CMD_MKDIR,
    CMD_RMDIR,
    CMD_OPENDIR,
    CMD_READDIR,
    CMD_STAT,
    CMD_ATTRS,
    CMD_LSTAT,
    CMD_FSTAT,
    CMD_SETSTAT,
    CMD_FSETSTAT,
    CMD_READLINK,
    CMD_SYMLINK,
    CMD_REALPATH,
    CMD_EXTENDED,
    SFTP_OP_UNSUPPORTED,
)

_hash_class = {"sha1": sha1, "md5": md5}


class SFTPServer(BaseSFTP, SubsystemHandler):
    """
    Server-side SFTP subsystem support.  Since this is a `.SubsystemHandler`,
    it can be (and is meant to be) set as the handler for ``"sftp"`` requests.
    Use `.Transport.set_subsystem_handler` to activate this class.
    """

    def __init__(
        self,
        channel,
        name,
        server,
        sftp_si=SFTPServerInterface,
        *args,
        **kwargs
    ):
        """
        The constructor for SFTPServer is meant to be called from within the
        `.Transport` as a subsystem handler.  ``server`` and any additional
        parameters or keyword parameters are passed from the original call to
        `.Transport.set_subsystem_handler`.

        :param .Channel channel: channel passed from the `.Transport`.
        :param str name: name of the requested subsystem.
        :param .ServerInterface server:
            the server object associated with this channel and subsystem
        :param sftp_si:
            a subclass of `.SFTPServerInterface` to use for handling individual
            requests.
        """
        BaseSFTP.__init__(self)
        SubsystemHandler.__init__(self, channel, name, server)
        transport = channel.get_transport()
        self.logger = util.get_logger(transport.get_log_channel() + ".sftp")
        self.ultra_debug = transport.get_hexdump()
        self.next_handle = 1
        # map of handle-string to SFTPHandle for files & folders:
        self.file_table = {}
        self.folder_table = {}
        self.server = sftp_si(server, *args, **kwargs)

    def _log(self, level, msg):
        pass

    def start_subsystem(self, name, transport, channel):
        pass

    def finish_subsystem(self):
        pass

    @staticmethod
    def convert_errno(e):
        """
        Convert an errno value (as from an ``OSError`` or ``IOError``) into a
        standard SFTP result code.  This is a convenience function for trapping
        exceptions in server code and returning an appropriate result.

        :param int e: an errno code, as from ``OSError.errno``.
        :return: an `int` SFTP error code like ``SFTP_NO_SUCH_FILE``.
        """
        pass

    @staticmethod
    def set_file_attr(filename, attr):
        """
        Change a file's attributes on the local filesystem.  The contents of
        ``attr`` are used to change the permissions, owner, group ownership,
        and/or modification & access time of the file, depending on which
        attributes are present in ``attr``.

        This is meant to be a handy helper function for translating SFTP file
        requests into local file operations.

        :param str filename:
            name of the file to alter (should usually be an absolute path).
        :param .SFTPAttributes attr: attributes to change.
        """
        pass

    # ...internals...

    def _response(self, request_number, t, *args):
        pass

    def _send_handle_response(self, request_number, handle, folder=False):
        pass

    def _send_status(self, request_number, code, desc=None):
        pass

    def _open_folder(self, request_number, path):
        pass

    def _read_folder(self, request_number, folder):
        pass

    def _check_file(self, request_number, msg):
        # this extension actually comes from v6 protocol, but since it's an
        # extension, i feel like we can reasonably support it backported.
        # it's very useful for verifying uploaded files or checking for
        # rsync-like differences between local and remote files.
        pass

    def _convert_pflags(self, pflags):
        """convert SFTP-style open() flags to Python's os.open() flags"""
        pass

    def _process(self, t, request_number, msg):
        pass


from paramiko.sftp_handle import SFTPHandle
