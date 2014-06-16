#!/usr/bin/env python
"""
Runs CISCO IOS commands on a remote cisco switch non-interactively 
using an ssh connection
"""
from __future__ import print_function
import time, argparse, getpass, logging, paramiko

class Switch:
    """Build switch connection and run specified commands"""
    
    def __init__(self, switchname, username=None, password=None):
        """
        :param switchname: switchname
        :param username: switch username
        :param password: switch password
        """

        self.switchname = switchname
        if username:
            self.username = username
        else:
            self.username = getpass.getuser()
        
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("Using username: {0}".format(self.username))
        if password:
            self.password = password
        else:
            self.password = getpass.getpass("Switch password: ")

        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()      
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
              
    def connect(self):
        """Initiates the ssh connection to the Switch"""

        self.ssh.connect(self.switchname, username=self.username, password=self.password, allow_agent=False)              
        self.channel = self.ssh.invoke_shell()
        
        # disables output scrolling
        self.channel.send("terminal length 0\n")
        time.sleep(1)
        self.output = self.channel.recv(9999)
        self.channel.send("\n")

    def run(self, command):
        """Runs the provided command on the switch and returns the output if 'show' commands are issued"""
        
        self.logger.info("Running command: {0}".format(command))
        self.channel.send(command+"\n")
        time.sleep(2)
        if "show" in command:
            print(self.channel.recv(9999))

    def close(self):
        """Close connection"""
        self.logger.info("close connection")
        self.ssh.close()


def main():
    parser = argparse.ArgumentParser(description="Runs CISCO IOS commands on a remote     \
        cisco switch non-interactively using a ssh connection. The commands can be either \
        read from the commandline or a file")
                                                      
    parser.add_argument('-s', '--switchname', type=str, nargs='*', help='switch name')
    parser.add_argument('-u', '--username', type=str, help='username')
    parser.add_argument('-p', '--password', type=str, help='password')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-d', '--debug', action='store_true', help='Verbose output')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--command', type=str, help='specify the command to run')
    group.add_argument('-f', '--file', type=str, help='read commands from a file')

    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    elif args.debug:
        logging.basicConfig(level=logging.DEBUG)
    
    sw = Switch(args.switchname[0], args.username, args.password)
    sw.connect()
      
    if args.command:
        sw.run(args.command)
      
    elif args.file:
        try:
            with open(args.file) as f:
                for line in fd:
                    sw.run(line)
                  
        except IOError:
            print("Cannot read command file {0}".format(args.file))
            exit(1)
   
    sw.close()


if __name__ == '__main__':
    main()

# vim: autoindent tabstop=4 expandtab smarttab shiftwidth=4 softtabstop=4 tw=0
