#!usr/bin/python3

import subprocess
import sys
import os
import argparse


#                                     VARIABLES                                #
ZIP_DIR = './zips/'
BROWSER_DIR = './browsers/'
MIN_VERSION = 57


#                                     FUNCTIONS                                #

def get_url(version):
    ''' Creates the url of a specific version on Mozzila ftp for linux 64 bits.

    Parameters:
    version(int): The selected version

    Returns:
    String: the url of the version.
    '''
    version_string = str(version) + ".0"
    url = "https://ftp.mozilla.org/pub/firefox/releases/" + version_string + "/linux-x86_64/en-US/firefox-" + version_string + ".tar.bz2"
    return url


def get_latest_version():
    ''' Retrieve the latest release version number of Firefox.
    It will download the zip for the latest.

    Returns:
    int: the latest version available.
    '''
    subprocess.run("wget --content-disposition -P " + ZIP_DIR +
                   " 'https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US'",
                   shell=True, check=True)
    ffLatestVersion = ""
    for file in os.listdir(ZIP_DIR):
        if file.endswith(".tar.bz2"):
            ffLatestVersion = file

    if ffLatestVersion == "":
        print("Error downloading Firefox")
        sys.exit(1)
    latest = int(ffLatestVersion.replace("firefox-", "")[:2])
    return latest

def download_version(version):
    ''' Download a specific version of Firefox for linux 64 bits.

    Parameters:
    version(int) The selected version.
    '''
    url = get_url(version)
    if not os.path.exists("./zips/firefox-" + str(version) + ".0.tar.bz2"):
        try:
            subprocess.run("wget --content-disposition -P " + ZIP_DIR + " " + url, shell=True, check=True)
        except Exception as e:
            print("Failed downloading version " + str(version))
            if DEBUG:
                print(e)
                print("url : " + str(url))
    else:
        print("Firefox " + str(version) + " is already downloaded, skipping...")

def extract(version):
    ''' Exctract the tarball of a specific firefox version. The tarball must be situated in the ZIP_DIR folder.

    Parameters:
    version(int): The selected version.
    '''
    filename = ZIP_DIR + "firefox-" + str(version) + ".0.tar.bz2"
    if not os.path.exists(BROWSER_DIR +"firefox-" + str(version)):
        print("Unpacking firefox-"+str(version))
        try:
            subprocess.run("tar -jxf " + filename + " -C " + BROWSER_DIR, shell=True, check=True)
            subprocess.run("rm "+ BROWSER_DIR + "firefox/updater", shell=True, check=True)
            subprocess.run("mv " + BROWSER_DIR + "firefox "+ BROWSER_DIR + "firefox-" + str(version),shell=True, check=True)
        except Exception as e:
            print("Failed extracting " + filename)
            if DEBUG:
                print(e)
    else:
        print("Firefox " + str(version) + " is already unpacked, skipping...")



def firefox_downloader(versions = 'all', clean = True):
    ''' Download and extract selected versions of Firefox.

    Parameters:
    versions(list(int) or String): A list containing that the user wish to download, or the string 'all' for versions from 33 to latest - optional, default is 'all' string
    clean(bool): Flag indicating to remove tarballs after extraction.
    '''
    if not os.path.exists(ZIP_DIR):
        os.mkdir(ZIP_DIR)
    if not os.path.exists(BROWSER_DIR):
        os.mkdir(BROWSER_DIR)

    if versions == 'all':
        latest = get_latest_version()
        versions = [k for k in range(MIN_VERSION, latest+1)]

    for version in versions:
        download_version(version)
        extract(version)
        if clean:
            try:
                subprocess.run("rm "+ ZIP_DIR + "firefox-" + str(version) + ".0.tar.bz2", shell=True, check=True)
            except Exception as e:
                if DEBUG:
                    print(e)


def delete(version):
    ''' Delete tarballs and binaries for a specific version

    Parameters:
    version(int): Selected version.
    '''
    subprocess.run("rm ./zips/firefox-" + str(version) + ".0.tar.bz2", shell=True, check=True)
    subprocess.run("rm -rf ./browsers/firefox-" + str(version), shell=True, check=True)



#                                   MAIN                                       #


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--debug', help='Activate debug prints', action='store_true',default='False')
    parser.add_argument('-v', '--version', help="Set this if you need a single version. Default is all version from 57 to latest.", type=int)
    parser.add_argument('-z', '--zips', help="Keep compressed browser files. Default is delete.", action='store_true', default='False')
    args = parser.parse_args()
    return args

def main(args):
    if args.debug:
        DEBUG = True
    if args.version:
        firefox_downloader(versions = [args.version], clean = not (args.zips))
    else:
        firefox_downloader(clean = not (args.zips))



if __name__ == "__main__":
    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x, not Python 2.x\n")
        sys.exit(1)
    args = parse_arguments()
    main(args)
