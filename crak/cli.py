""" main app for brute force password cracker """
#########
#  cli.py
#
#  Description:
#  dictionary based password cracker
#
#  Author:
#  Stephen Eaton <seaton@strobotics.com.au>


import argparse
import pandas as pd
from passlib.hosts import linux_context

VERSION = "0.0.2"

# get and parse command line arguments
PARSER = argparse.ArgumentParser(
    description="Perform a dictionary \
                    crack on a list of encrypted passwords using a wordlist"
)

PARSER.add_argument(
    "shadowfile",
    type=argparse.FileType("r"),
    help="Shadow password file containing crypted passwords",
)

PARSER.add_argument(
    "--version",
    action="version",
    version="%(prog)s v" + VERSION,
    help="prints version information",
)

PARSER.add_argument(
    "-d",
    "--worddict",
    type=argparse.FileType("r"),
    help="Word dictionary files to use in attack",
    required=False,
)
PARSER.add_argument(
    "-u",
    "--username",
    type=str,
    help="specific username - if not defined then all users in shadow \
                           file will be attempted",
    required=False,
)
ARGS = PARSER.parse_args()

# global Data frame holding username and password information read in from file
DF = pd.DataFrame()


def load_shadowfile():
    """loads and cleans up the shadow file into a Data Frame for processing"""
    global DF
    # Read the shadow file first two columns
    df = pd.read_csv(
        ARGS.shadowfile,
        sep=":",
        header=None,
        usecols=[0, 1],
        names=["username", "password"],
    )
    df = df.set_index("username")
    # remove unwanted rows
    df = df[(df.password != "!") & (df.password != "*") & (df.password != "x")]
    DF = DF.append(df)


def list_users():
    """Lists all users in the shadow file with a password"""
    print("list of usernames in shadow file")
    # display the current data frame
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print(DF)


def validate_args():
    "Validates cli arguments"
    if ARGS.worddict is not None:
        if ARGS.shadowfile == ARGS.worddict:
            print("ERROR: password and dictionary filenames are the same")
            exit(1)
        if ARGS.username is not None and ARGS.username not in DF.index:
            print("ERROR: username does not exist")
            exit(1)


def crak(username):
    """
    assumes there is a global pandas data frame - DF containing
    the usernames and password.

    Will verify the crypted password with a dictionary list
    until a match is found or it reaches the end of the list
    """
    dictfile = ARGS.worddict
    # reset position in file to start
    dictfile.seek(0)
    password = DF.password[username]
    passwd_found = False
    for word in dictfile.readlines():
        word = word.strip("\n")
        verified = linux_context.verify(word, password)
        if verified:
            passwd_found = True
            print("*** FOUND PASSWORD ***")
            print("Username:", username)
            print("Password:", word)
            print("**********************")
            break
    if not passwd_found:
        print("No password found:", username)


def main():
    "App Mainline"

    print("")
    print("-=(", PARSER.prog, "v", VERSION, ")=-")
    print("")

    load_shadowfile()
    if ARGS.worddict is None:
        list_users()
    else:
        validate_args()
        if ARGS.username is not None:
            # specific username
            print("starting to crack password for user:", ARGS.username)
            crak(ARGS.username)
        else:
            # loop though all users in dataframe
            print("starting to crack passwords for all users")
            for username, _ in DF.iterrows():
                crak(username)


if __name__ == "__main__":
    main()
