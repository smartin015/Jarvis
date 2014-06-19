# Copyright 2011, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import json

_GOODBYE_MESSAGE = 'Goodbye'

d = {
			"tab1":{
				"tab1item1":{
					"id":"tab1item1",
					"text":"Tab1Item1",
					"picpath":""
				},
				"tab1item2":{
					"id":"tab1item2",
					"text":"Tab1Item2",
					"picpath":""
				},
				"tab1item3":{
					"id":"tab1item3",
					"text":"Tab1Item3",
					"picpath":""
				}
			}, 
			"tab2":{
				"tab2item1":{
					"id":"tab2item1",
					"text":"Tab2Item1",
					"picpath":""
				},
				"tab2item2":{
					"id":"tab2item2",
					"text":"Tab2ItemB",
					"picpath":""
				},
				"tab2item3":{
					"id":"tab2item3",
					"text":"Tab2Item3",
					"picpath":""
				}
			}
		}
n = {"type": "say", "data":d};
		

def web_socket_do_extra_handshake(request):
    # This example handler accepts any request. See origin_check_wsh.py for how
    # to reject access from untrusted scripts based on origin value.

    pass  # Always accept.


def web_socket_transfer_data(request):
    j = json.dumps(n)
    request.ws_stream.send_message(j, binary=False)
    while True:
        line = request.ws_stream.receive_message()
        if line is None:
            request.ws_stream.send_message("a", binary=False)
            print "a"
            return
        if isinstance(line, unicode):
            request.ws_stream.send_message("b", binary=False)
            print "b"
            if line == _GOODBYE_MESSAGE:
                return
        else:
            request.ws_stream.send_message("c", binary=False)
            print "c"
            request.ws_stream.send_message(line, binary=True)


# vi:sts=4 sw=4 et
