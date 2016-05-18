# -*- coding: utf-8 -*-
# supervisor-alert - Receive notifications for supervisor process events
# Copyright 2016 Rahiel Kasim
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import argparse
from functools import partial
from os.path import expanduser
import shlex
from subprocess import check_call, CalledProcessError

from supervisor.childutils import listener, get_headers

__version__ = "0.2"


def main():
    parser = argparse.ArgumentParser(description="Supervisor event listener to notify on process events.",
                                     epilog="Homepage: https://github.com/rahiel/supervisor-alert")
    parser.add_argument("-c", "--command", help="Specify the command to process the event messages.")
    parser.add_argument("--telegram", help="Use telegram-send to send event messages.", action="store_true")
    parser.add_argument("--version", action="version", version="%(prog)s {}".format(__version__))
    args = parser.parse_args()

    s = "PROCESS_STATE_"

    if args.telegram:
        alert = telegram
    elif args.command:
        alert = partial(send, command=shlex.split(args.command))
    else:
        raise Exception("No command specified.")

    while True:
        headers, payload = listener.wait()
        event_name = headers["eventname"]

        if event_name.startswith(s):
            event_name = event_name[len(s):].lower()
            data = get_headers(payload)  # keys: from_state, pid, processname
            process_name = data["processname"]
            message = process_name + " has entered state " + event_name
            alert(message)
        else:
            listener.ok()


def telegram(message):
    """Send message with telegram-send."""
    try:
        check_call(["telegram-send", message])
        listener.ok()
    except OSError:     # command not found
        cmd = expanduser("~/.local/bin/telegram-send")
        check_call([cmd, message])
        listener.ok()
    except CalledProcessError:
        listener.fail()


def send(command, message):
    "Send message with an arbitrary command."
    try:
        check_call(command + [message])
        listener.ok()
    except CalledProcessError:
        listener.fail()


def configure():
    """Guide user to set up supervisor-alert."""
    pass


if __name__ == "__main__":
    main()
