"""
GUISCRCPY by srevinsaju
Get it on : https://github.com/srevinsaju/guiscrcpy
Licensed under GNU Public License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import shlex
import logging
import os
from guiscrcpy.platform.platform import System
environment = System()


def shellify(args):
    if environment.system() == 'Windows':
        return args
    else:
        return shlex.split(args)


_ = shellify


def decode(raw_output):
    pass


def decode_process(process):
    try:
        output = process.stdout.readlines()
        for i in range(len(output)):
            output[i] = output[i].decode('utf-8')
    except NameError:
        logging.error("No stdout in process.")
        output = ""
    return output


def check_existence(paths, file=(), directory=True, PATH=False):
    for i in paths:
        j = os.path.expanduser(i)
        if os.path.exists(j):  # direcory exists
            if directory and os.path.isdir(j):
                return [j]
            else:
                if environment.system() == 'Windows':
                    append = '.exe'
                else:
                    append = ''

                if (type(file) is list) or (type(file) is tuple):
                    for exe in file:
                        if os.path.exists(os.path.join(j, exe+append)):
                            return [os.path.join(j, exe+append)]
                else:

                    if os.path.exists(os.path.join(j, file+append)):
                        return [os.path.join(j, file+append)]
        else:
            logging.debug("{} doesn't exist".format(i))

    if PATH:
        new_paths = os.getenv('PATH').split(os.pathsep)
        found_path = check_existence(
            new_paths, file=file, directory=directory, PATH=False)
        if found_path:
            return found_path + ['path']
        else:
            return False
    else:
        return False
