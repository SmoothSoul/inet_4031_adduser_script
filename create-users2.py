#!/usr/bin/python3

# This updated script includes an interactive dry-run mode.
# When the user runs the script, they're prompted to enter Y or N.
# If 'Y' is selected, all system commands are skipped and replaced with print statements showing what *would* have run.
# The dry-run mode also reports skipped lines and malformed input lines.
# If 'N' is selected, the script performs the actual system changes, just like the original script.

# INET4031
# Dustin Tan
# 3/23/25
# 3/23/25


import os
import re
import sys

def main():
    # Ask user if they want to perform a dry run
    dry_run_input = input("Would you like to run in dry-run mode? (Y/N): ").strip().upper()
    dry_run = dry_run_input == "Y"

    for line in sys.stdin:
        # Skip comment lines
        match = re.match("^#", line)

        # Parse line
        fields = line.strip().split(':')

        # Handle invalid lines
        if match or len(fields) != 5:
            if dry_run:
                if match:
                    print("[DRY RUN] Skipped line (comment):", line.strip())
                elif len(fields) != 5:
                    print("[DRY RUN] Invalid line (not 5 fields):", line.strip())
            continue

        # Extract user details
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])
        groups = fields[4].split(',')

        # Create user
        print("==> Creating account for %s..." % (username))
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)
        if dry_run:
            print("[DRY RUN] Would run: %s" % cmd)
        else:
            os.system(cmd)

        # Set user password
        print("==> Setting the password for %s..." % (username))
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)
        if dry_run:
            print("[DRY RUN] Would run: %s" % cmd)
        else:
            os.system(cmd)

        # Add user to groups
        for group in groups:
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username, group))
                cmd = "/usr/sbin/adduser %s %s" % (username, group)
                if dry_run:
                    print("[DRY RUN] Would run: %s" % cmd)
                else:
                    os.system(cmd)

if __name__ == '__main__':
    main()

