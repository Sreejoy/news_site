
# Linux Server Setup
# ---

import os
import sys
import commands


install_str = "sudo pip install -U pip"
install_str_easy_install = "sudo easy_install"
apt_get_str = "sudo apt-get install"


# Installation function
def install(type = "", module_name = "", module_version = None, cmd = ""):
    command = ""
    
    if type == "pip":
        command = "%s %s" % (install_str, module_name)
        if module_version:
            command = "%s==%s" % (command, module_version)
    elif type == "apt-get":
        command = "%s %s --yes" % (apt_get_str, module_name)
    elif type == "easy_install":
        command = "%s %s" % (install_str_easy_install, module_name)
    else:
        command = cmd
    print "Installing: %s " %command
    status, output = commands.getstatusoutput(command)
    print output

    print (78 * '-')
    if status == 0:
        print "Successfully Installed: %s " %module_name
    else:
        print "Failed to Install: %s " %module_name
    print (78 * '-')


def Installer_With_Pip():
    
    # Check and install simplejson
    try:
        import simplejson
    except ImportError as e:
        install(type="pip", module_name="simplejson")


    # Check and install django 1.8.2
    try:
        install(type="pip", module_name="django", module_version="1.8.2" )
    except:
        print "unable to install/update django"


    # Check and install requests
    try:
        import requests
    except ImportError as e:
        install(type="pip", module_name="requests")

    install(type="pip", module_name="requests[security]")

    try:
        import easy_install
    except Exception as e:
        install(type="pip", module_name="easy_install")

class Logger(object):
    def __init__(self,name):
        self.name = name
        self.terminal = sys.stdout
        self.log = open(self.name,"w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def close(self):
        self.log.close()


def main():

## Install PIP
    print (78 * '-')
    print ('Python PIP Installation')
    print (78 * '-')
    os.system("sudo add-apt-repository universe")
    os.system("sudo apt-get update --yes")
    install(type = "apt-get", module_name = "python-pip")

#Install Dependecy for Requests
    print (78 * '-')
    print ('Dependency for Requests')
    print (78 * '-')
    os.system("sudo apt-get install libffi-dev libssl-dev --yes")


## Install all PIP modules
    print (78 * '-')
    print ('Python Module PIP Installation')
    print (78 * '-')
    Installer_With_Pip()


## Install Waitress
    print (78 * '-')
    print ('Install waitress')
    print (78 * '-')
    install(type = "apt-get", module_name = "python-waitress")	



    sys.stdout.close()


if __name__=="__main__":
    main()
