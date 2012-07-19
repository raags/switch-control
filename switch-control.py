#!/usr/bin/python
"""

  Copyright (C) 2012 Raghu Udiyar <raghusiddarth@gmail.com>
  
  This copyrighted material is made available to anyone wishing to use,
  modify, copy, or redistribute it subject to the terms and conditions
  of the GNU General Public License, either version 2 of the License, or
  (at your option) any later version
 
  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software Foundation,
  Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

 
  Author       : Raghu Udiyar <raghusiddarth@gmail.com>
  Description  : Runs CISCO IOS commands on a remote cisco switch non-interactively using an ssh connection
  Usage        : switch-control.py --help

$Id: switch-control.py 507 2012-06-07 02:40:52Z rags $
"""

import re
import sys
import pexpect
import argparse
import getpass

VERSION="0.7"
DEBUG=0
LOGFILE="./switch.out"

class Switch:
    """Class used to initiate switch connection and run the commands"""
    
    def __init__(self, hostname, username="", password=""):
        """Instantiate object with hostname. username and password are optional"""

        self.hostname=hostname

#       To use configure commands the trailing host part may need to be truncated.
#       because the prompt changes
#
#       q=re.compile(".trail|.trailing")
#       host=q.split(hostname)[0]

        self.prompt="%s.*#$" % self.hostname

        if username:
            self.user = username
        else:
            self.user = getpass.getuser()

        print "Using username:%s" % self.user
        if password:
            self.passwd = password
        else:
            self.passwd = getpass.getpass("Switch password:")


    def connect(self):
        """Initiates the ssh connection to the Switch"""

        prompt = self.prompt
        sshcmd="ssh %s -l %s" % (self.hostname, self.user)
        
        self.child = pexpect.spawn(sshcmd)

        child = self.child
        child.setwinsize(400,400)

        if(DEBUG):
            child.logfile = open(LOGFILE, "w")
            sys.stderr.write("Writing to file %s\n" % LOGFILE)

        try:
            index = child.expect(['password:','(yes/no)? $'])
        except:
            sys.stderr.write("Connection aborted, is hostname correct?\n")
            exit(1)

        if (index==0):    
            child.sendline(self.passwd)
            try:
                child.expect(prompt)
            except:
                sys.stderr.write("Could not get prompt, is the password correct?\n")
                exit(1)

        elif (index==1):
            child.sendline("yes")
            child.expect('password:')
            child.sendline(self.passwd)
            try:
                child.expect(prompt)
            except:
                sys.stderr.write("Could not get prompt, is the password correct?\n")
                exit(1)
        else:    
            sys.stderr.write("Connection aborted, is hostname correct?\n")
            exit(1)

        print "Connection succeded"
            
#       Disables output scrolling
        child.sendline("terminal length 0")
        child.expect(prompt)
        

    def run(self, command):
        """Runs the provided command on the switch and returns the output if 'show' commands are issued"""
        child = self.child
        prompt = self.prompt

        child.sendline(command)
        child.expect(prompt)
        if "show" in command:
            print child.before


    def exit(self):
        """Exit from the switch"""
        print "exiting..."
        self.child.sendline("exit")



def getargs():
    parser = argparse.ArgumentParser(description="Runs CISCO IOS commands on a remote cisco switch non-interactively using a ssh connection. The commands can be either read from the commandline or a file. For debugging set DEBUG=1, debug output will be written to LOGFILE")
                                                  
    
    parser.add_argument('hostname', metavar='hostname', type=str, help='switch hostname')
    parser.add_argument('-u', '--username', type=str, help='switch username')
    parser.add_argument('-p', '--password', type=str, help='switch password')
    parser.add_argument('-v', '--version', action='version', version=VERSION)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--interactive', action='store_true', help='enter interactive mode (not implemented)')
    group.add_argument('-c', '--command', type=str, help='specify the command to run')
    group.add_argument('-f', '--file', type=str, help='read commands from a file')

    args = parser.parse_args()

    if args.interactive:
        print "interactive mode is in development"
        return
        
    if args.command:
        sw = Switch(args.hostname, args.username, args.password)
        sw.connect()
        sw.run(args.command)
        sw.exit()
        return
        
    if args.file:
        try:
            fd = open(args.file, "r")
        except IOError:
            sys.stderr.write("%s file does not exist\n" % args.file)
            exit(1)

        sw = Switch(args.hostname, args.username, args.password)
        sw.connect()

        for line in fd:
            sw.run(line)

        sw.exit()
        return


if __name__ == '__main__':
    
    getargs()
    exit(0)

# vim: autoindent tabstop=4 expandtab smarttab shiftwidth=4 softtabstop=4 tw=0
