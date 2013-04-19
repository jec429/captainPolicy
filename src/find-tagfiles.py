#!/usr/bin/python
#
#  Used internally by the doxygen fragment.  This must be run in the cmt
# directory. 

import optparse
import commands
import re

def System(command, forcerun=False):
    """Run a command if this isn't a dry run.  The dryrun argument """
    if options.trace: print "Trace: " + command
    if not options.DryRun or forcerun: os.system(command)
    
def CommandOutput(command, forcerun=False):
    """Run a command if this isn't a dry run."""
    if options.trace: print "Trace: " + command
    if not options.DryRun or forcerun:
        return commands.getoutput(command)

def CMTPackage():
    """Return the current package name."""
    output = CommandOutput("cmt show macro_value package")
    return output
    
def CMTPackageRoot():
    """Return the current package name."""
    output = CommandOutput("cmt show macro_value PACKAGE_ROOT")
    return output
    
parser = optparse.OptionParser()
parser.add_option("-d","--dry-run", dest="DryRun",
                  action = "store_true", default=False,
                  help="do a dry run without running the actual commands")
parser.add_option("-t", "--trace",action="store_true",
                  dest="trace", default=False,
                  help="print commands before executing them")
parser.add_option("--no-trace",action="store_false",
                  dest="trace",
                  help="don't print commands before executing them")

(options, args) = parser.parse_args()

# Get the package root.
packageRoot = CMTPackageRoot()

# Generate and run the CMT command to find all of the doxygen tag
# files.  The output with the files is tagged with "%%%%%".

cmd = "cmt broadcast '("
cmd += "if [ -x ../dox -a -d ../../<version> ];"
cmd += "then "
cmd += "echo %%%%% <package> <version> with version directory;"
cmd += "echo %%%%% "
cmd += "`cmt show macro_value PACKAGE_ROOT`/dox/<package>_<version>.tag"
cmd += "="
cmd += "`cmt show macro_value PACKAGE_ROOT`/dox;"
cmd += "elif [ -x ../dox ];"
cmd += "then "
cmd += "echo %%%%% "
cmd += "`cmt show macro_value PACKAGE_ROOT`/dox/<package>_<version>.tag"
cmd += "="
cmd += "`cmt show macro_value PACKAGE_ROOT`/dox;"
cmd += "fi"
cmd += ")'"

output = CommandOutput(cmd)

# Find the tag files in the output of the CMT command.
matchs = re.findall(r"(?m)^%%%%% (.*)$",output)

# Find the name of the current package.
package = "/" + CMTPackage() + "/"

# Remove the current package from the tag file list and dump the rest
# to standard output.
for i in matchs:
    match = re.search(package,i)
    if match == None: print i
