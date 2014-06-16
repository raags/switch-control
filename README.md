switch-control
===
A simple tool to run cisco switch commands via an ssh connection

Uses [paramiko](http://www.paramiko.org/) to manage and send commands via ssh

## Usage:

$ ./switch-control.py --help
usage: switch-control.py [-h] [-s [SWITCHNAME [SWITCHNAME ...]]] [-u USERNAME]
                         [-p PASSWORD] [-v] [-d] (-c COMMAND | -f FILE)

Runs CISCO IOS commands on a remote cisco switch non-interactively using a ssh
connection. The commands can be either read from the commandline or a file

optional arguments:
  -h, --help            show this help message and exit
  -s [SWITCHNAME [SWITCHNAME ...]], --switchname [SWITCHNAME [SWITCHNAME ...]]
                        switch name
  -u USERNAME, --username USERNAME
                        username
  -p PASSWORD, --password PASSWORD
                        password
  -v, --verbose         Verbose output
  -d, --debug           Verbose output
  -c COMMAND, --command COMMAND
                        specify the command to run
  -f FILE, --file FILE  read commands from a file

## Todo

- Handle mulitple switches via threads
