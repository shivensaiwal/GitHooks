#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import datetime


# Limit Checkstyle test to new classes only. You can use the following
# template:
#
#export CHECKSTYLE_START_DATE='2014-01-01 00:00:00 +0200'
#

# Config
checkstyle_jar = os.getenv('CHECKSTYLE_JAR', "/Users/shivensaiwal/Desktop/MyWork/checkstyle-8.19-all.jar")
checkstyle_cfg = os.getenv('CHECKSTYLE_CFG', "/Users/shivensaiwal/Desktop/MyWork/checkstyle.xml")

failing_test_should_prevent_commit = True

min_date_of_first_commit = os.getenv('CHECKSTYLE_START_DATE','2014-01-01 00:00:00 +0200')

java_cmd = "java"
git_cmd = "git"

# Init
import re
import subprocess
import sys

def parse_date(val):
    # We're not using python-dateutil, since it's not available out of the box on some machines
    m = re.match('[0-9]{4}-[0-9]{2}-[0-9]{2}', val)
    if m:
        return datetime.datetime.strptime(m.group(0), '%Y-%m-%d')
    else:
        raise Exception("Invalid date format: %s" % val)

try:
    import colorama

    colorama.init()

    style_ok = colorama.Fore.GREEN
    style_err = colorama.Fore.RED
    style_warn = colorama.Fore.YELLOW
    style_details = colorama.Style.DIM
    style_reset = colorama.Style.RESET_ALL
except ImportError as err:
    # Colorama dependency is optional, since some people may not be able to install it locally
    style_ok = ""
    style_err = ""
    style_warn = ""
    style_details = ""
    style_reset = ""

if not os.path.isfile(checkstyle_jar):
    sys.stderr.write("checkstyle JAR not found (%s)\n" % checkstyle_jar)
    sys.exit(1)

if not os.path.isfile(checkstyle_cfg):
    sys.stderr.write("checkstyle config not found (%s)\n" % checkstyle_cfg)
    sys.exit(1)

if "check_output" not in dir( subprocess ):
    sys.stderr.write("python >= 2.7 is required\n")
    sys.exit(1)

if min_date_of_first_commit is not None:
     min_date_of_first_commit = parse_date(min_date_of_first_commit)

# Fetch files to commit
file_list = subprocess.check_output([git_cmd, "diff", "--cached", "--name-only", "--diff-filter=ACM"])
file_list = [f for f in file_list.splitlines() if f.decode("utf-8").endswith('.java')]

# Run Checkstyle
def first_commit_before_date(source_file, dt):
    commits = subprocess.check_output([git_cmd, "log", "--format=%ai", source_file])
    if len(commits) == 0:
        return False
    first_commit = commits.splitlines()[-1]
    first_commit = parse_date(first_commit)
    return first_commit < dt

failed_checks = 0
for source_file in file_list:
    if min_date_of_first_commit is not None and first_commit_before_date(source_file, min_date_of_first_commit):
        print ('Checkstyle: ' + source_file + style_warn + ' SKIPPED (too old)' + style_reset)
        continue

    try:
        subprocess.check_output([java_cmd, "-jar", checkstyle_jar, "-c", checkstyle_cfg, source_file.decode("utf-8")])
        print ('Checkstyle: ' + source_file.decode("utf-8") + style_ok + ' OK' + style_reset)
    except subprocess.CalledProcessError as err:
        failed_checks = failed_checks + 1
        print ('Checkstyle: ' + source_file.decode("utf-8") + style_err + ' FAILED' + style_reset)
        # Print Checkstyle details
        checkRegexp = re.compile(r'\.java:')
        for m in err.output.splitlines():
            print(m.decode("utf-8"))


# Decisions
if failed_checks == 0:
    print ("%d Checkstyle tests passed" % len(file_list))
elif failing_test_should_prevent_commit:
    print (style_err + "%d Checkstyle tests failed" % failed_checks + style_reset)
    sys.exit(2)
else:
    print (style_warn + "%d Checkstyle tests failed (won't block the commit)" % failed_checks + style_reset)
    sys.exit(0)
