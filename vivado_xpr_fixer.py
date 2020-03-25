#!/usr/bin/python
import sys
import os.path
import xml.etree.ElementTree as ET

"""
To install this file as a Git hook:

1. Copy this file to the directory ".git/hooks"
2. 

"""

__PRODUCT__ = "Vivado XPR Path Fixer"
__AUTHOR__ = "JP Sheehan <jps111@uclive.ac.nz>"


HOOKS_FILE = "./.git/hooks/post-merge"


def change_paths_in_xpr(filename):
    """ Corrects the path of the project inside the XPR file. """
    # Vivado expects the backslashes to be forward slashes
    new_project_path = os.path.realpath(filename).replace("\\", "/")
    print_info("expected project path: \t{}".format(new_project_path))

    # Get the path from the XPR file
    tree = ET.parse(filename)
    root = tree.getroot()
    old_project_path = root.get("Path")
    print_info("actual project path: \t{}".format(old_project_path))

    success = True
    if old_project_path == new_project_path:
        print_info(
            "project path appears correct, no changes made")
    else:
        # Update the XPR file with the new path
        root.set("Path", new_project_path)
        ET.ElementTree(root).write(
            filename, xml_declaration=True, encoding="utf-8")
        try:
            print_info("project path updated, changes saved")
        except Exception as ex:
            print_error(
                "an error occurred while writing file\n" + str(ex))
            success = False

    return success


def first(iterable):
    """ Returns the first element in the iterable or None if it doesn't exist. """
    for element in iterable:
        return element
    return None


def find_xpr_filename(directory="."):
    """ Returns the filename of the first xpr file found in the directory. """
    return first(filter(lambda fname: fname.endswith(".xpr"), os.listdir(directory)))


def print_usage_and_exit(code=2):
    """ Prints the program usage and exits. """
    print(
        """USAGE: {} install | remove | status | update
\tinstall - Installs this script as a git hook. This automatically runs the "update" command after running "git pull".
\tremove - Removes the git hook.
\tupdate - Updates the XPR file with the new path information.""".format(os.path.basename(sys.argv[0])))
    sys.exit(code)


def print_error(message):
    """ Prints an error message. """
    print("ERROR: {}".format(message))


def print_info(message):
    """ Prints an informative message. """
    print("INFO: {}".format(message))


def print_status():
    """ Prints status. """
    if os.path.exists(HOOKS_FILE) and os.path.isfile(HOOKS_FILE):
        print_info("this script appears to be is installed as a git hook")
    else:
        print_info("this script is not installed as a git hook")


def install_hook():
    """ Installs the git hook for this file. """
    with open(HOOKS_FILE, "w") as f:
        f.writelines(["#!/bin/sh\r\n", "# Git hook for {} by {}\r\n".format(
            __PRODUCT__, __AUTHOR__), "exec python {} update\r\n".format(os.path.basename(sys.argv[0]))])
    print_info("Installed git hook successfully")
    print_info("\"python\" (version 3) must be in the PATH variable")


def remove_hook():
    """ Removes the git hook for this file. """
    if os.path.exists(HOOKS_FILE):
        os.unlink(HOOKS_FILE)
    print_info("Removed git hook successfully")


def main():
    """ The main function. """

    # Print the program info
    print("{} by {}".format(__PRODUCT__, __AUTHOR__))

    # Get the filename from the program arguments or current directory
    filename = None
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "install":
            install_hook()
            sys.exit(0)
        elif command == "remove":
            remove_hook()
            sys.exit(0)
        elif command == "status":
            print_status()
            sys.exit(0)
        elif command == "update":
            filename = find_xpr_filename(".")
            if filename is not None:
                filename = os.path.join(".", filename)
        else:
            print_error("undefined command \"{}\"".format(command))
            print_usage_and_exit()
    else:
        print_usage_and_exit()

    # Take action based on the filename
    if filename is None:
        print_usage_and_exit()
    elif not os.path.exists(filename):
        print_error(
            "file or directory name \"{}\" does not exist".format(filename))
        sys.exit(-1)
    else:
        if change_paths_in_xpr(filename):
            sys.exit(0)
        else:
            sys.exit(-1)


if __name__ == "__main__":
    main()
