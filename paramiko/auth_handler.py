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
`.AuthHandler`
"""

import weakref
import threading
import time
import re

from paramiko.common import (
    cMSG_SERVICE_REQUEST,
    cMSG_DISCONNECT,
    DISCONNECT_SERVICE_NOT_AVAILABLE,
    DISCONNECT_NO_MORE_AUTH_METHODS_AVAILABLE,
    cMSG_USERAUTH_REQUEST,
    cMSG_SERVICE_ACCEPT,
    DEBUG,
    AUTH_SUCCESSFUL,
    INFO,
    cMSG_USERAUTH_SUCCESS,
    cMSG_USERAUTH_FAILURE,
    AUTH_PARTIALLY_SUCCESSFUL,
    cMSG_USERAUTH_INFO_REQUEST,
    WARNING,
    AUTH_FAILED,
    cMSG_USERAUTH_PK_OK,
    cMSG_USERAUTH_INFO_RESPONSE,
    MSG_SERVICE_REQUEST,
    MSG_SERVICE_ACCEPT,
    MSG_USERAUTH_REQUEST,
    MSG_USERAUTH_SUCCESS,
    MSG_USERAUTH_FAILURE,
    MSG_USERAUTH_BANNER,
    MSG_USERAUTH_INFO_REQUEST,
    MSG_USERAUTH_INFO_RESPONSE,
    cMSG_USERAUTH_GSSAPI_RESPONSE,
    cMSG_USERAUTH_GSSAPI_TOKEN,
    cMSG_USERAUTH_GSSAPI_MIC,
    MSG_USERAUTH_GSSAPI_RESPONSE,
    MSG_USERAUTH_GSSAPI_TOKEN,
    MSG_USERAUTH_GSSAPI_ERROR,
    MSG_USERAUTH_GSSAPI_ERRTOK,
    MSG_USERAUTH_GSSAPI_MIC,
    MSG_NAMES,
    cMSG_USERAUTH_BANNER,
)
from paramiko.message import Message
from paramiko.util import b, u
from paramiko.ssh_exception import (
    SSHException,
    AuthenticationException,
    BadAuthenticationType,
    PartialAuthentication,
)
from paramiko.server import InteractiveQuery
from paramiko.ssh_gss import GSSAuth, GSS_EXCEPTIONS


class AuthHandler:
    """
    Internal class to handle the mechanics of authentication.
    """

    def __init__(self, transport):
        self.transport = weakref.proxy(transport)
        self.username = None
        self.authenticated = False
        self.auth_event = None
        self.auth_method = ""
        self.banner = None
        self.password = None
        self.private_key = None
        self.interactive_handler = None
        self.submethods = None
        # for server mode:
        self.auth_username = None
        self.auth_fail_count = 0
        # for GSSAPI
        self.gss_host = None
        self.gss_deleg_creds = True

    def _log(self, *args):
        pass

    def is_authenticated(self):
        pass

    def get_username(self):
        pass

    def auth_none(self, username, event):
        pass

    def auth_publickey(self, username, key, event):
        pass

    def auth_password(self, username, password, event):
        pass

    def auth_interactive(self, username, handler, event, submethods=""):
        """
        response_list = handler(title, instructions, prompt_list)
        """
        pass

    def auth_gssapi_with_mic(self, username, gss_host, gss_deleg_creds, event):
        pass

    def auth_gssapi_keyex(self, username, event):
        pass

    def abort(self):
        pass

    # ...internals...

    def _request_auth(self):
        pass

    def _disconnect_service_not_available(self):
        pass

    def _disconnect_no_more_auth(self):
        pass

    def _get_key_type_and_bits(self, key):
        """
        Given any key, return its type/algorithm & bits-to-sign.

        Intended for input to or verification of, key signatures.
        """
        pass

    def _get_session_blob(self, key, service, username, algorithm):
        pass

    def wait_for_response(self, event):
        pass

    def _parse_service_request(self, m):
        pass

    def _generate_key_from_request(self, algorithm, keyblob):
        # For use in server mode.
        pass

    def _choose_fallback_pubkey_algorithm(self, key_type, my_algos):
        # Fallback: first one in our (possibly tweaked by caller) list
        pass

    def _finalize_pubkey_algorithm(self, key_type):
        # Short-circuit for non-RSA keys
        pass

    def _parse_service_accept(self, m):
        pass

    def _send_auth_result(self, username, method, result):
        # okay, send result
        pass

    def _interactive_query(self, q):
        # make interactive query instead of response
        pass

    def _parse_userauth_request(self, m):
        pass

    def _parse_userauth_success(self, m):
        pass

    def _parse_userauth_failure(self, m):
        pass

    def _parse_userauth_banner(self, m):
        pass
        # who cares.

    def _parse_userauth_info_request(self, m):
        pass

    def _parse_userauth_info_response(self, m):
        pass

    def _handle_local_gss_failure(self, e):
        pass

    # TODO 4.0: MAY make sense to make these tables into actual
    # classes/instances that can be fed a mode bool or whatever. Or,
    # alternately (both?) make the message types small classes or enums that
    # embed this info within themselves (which could also then tidy up the
    # current 'integer -> human readable short string' stuff in common.py).
    # TODO: if we do that, also expose 'em publicly.

    # Messages which should be handled _by_ servers (sent by clients)
    @property
    def _server_handler_table(self):
        pass

    # Messages which should be handled _by_ clients (sent by servers)
    @property
    def _client_handler_table(self):
        pass

    # NOTE: prior to the fix for #1283, this was a static dict instead of a
    # property. Should be backwards compatible in most/all cases.
    @property
    def _handler_table(self):
        pass


class GssapiWithMicAuthHandler:
    """A specialized Auth handler for gssapi-with-mic

    During the GSSAPI token exchange we need a modified dispatch table,
    because the packet type numbers are not unique.
    """

    method = "gssapi-with-mic"

    def __init__(self, delegate, sshgss):
        self._delegate = delegate
        self.sshgss = sshgss

    def abort(self):
        pass

    @property
    def transport(self):
        pass

    @property
    def _send_auth_result(self):
        pass

    @property
    def auth_username(self):
        pass

    @property
    def gss_host(self):
        pass

    def _restore_delegate_auth_handler(self):
        pass

    def _parse_userauth_gssapi_token(self, m):
        pass

    def _parse_userauth_gssapi_mic(self, m):
        pass

    def _parse_service_request(self, m):
        pass

    def _parse_userauth_request(self, m):
        pass

    __handler_table = {
        MSG_SERVICE_REQUEST: _parse_service_request,
        MSG_USERAUTH_REQUEST: _parse_userauth_request,
        MSG_USERAUTH_GSSAPI_TOKEN: _parse_userauth_gssapi_token,
        MSG_USERAUTH_GSSAPI_MIC: _parse_userauth_gssapi_mic,
    }

    @property
    def _handler_table(self):
        # TODO: determine if we can cut this up like we did for the primary
        # AuthHandler class.
        pass


class AuthOnlyHandler(AuthHandler):
    """
    AuthHandler, and just auth, no service requests!

    .. versionadded:: 3.2
    """

    # NOTE: this purposefully duplicates some of the parent class in order to
    # modernize, refactor, etc. The intent is that eventually we will collapse
    # this one onto the parent in a backwards incompatible release.

    @property
    def _client_handler_table(self):
        pass

    def send_auth_request(self, username, method, finish_message=None):
        """
        Submit a userauth request message & wait for response.

        Performs the transport message send call, sets self.auth_event, and
        will lock-n-block as necessary to both send, and wait for response to,
        the USERAUTH_REQUEST.

        Most callers will want to supply a callback to ``finish_message``,
        which accepts a Message ``m`` and may call mutator methods on it to add
        more fields.
        """
        pass

    def auth_none(self, username):
        pass

    def auth_publickey(self, username, key):
        pass

    def auth_password(self, username, password):
        pass

    def auth_interactive(self, username, handler, submethods=""):
        """
        response_list = handler(title, instructions, prompt_list)
        """
        pass

    # NOTE: not strictly 'auth only' related, but allows users to opt-in.
    def _choose_fallback_pubkey_algorithm(self, key_type, my_algos):
        pass
