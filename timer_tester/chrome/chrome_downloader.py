#!usr/bin/python3
import subprocess
import sys
import os
import argparse
from bs4 import BeautifulSoup
from urllib.request import urlopen
''' chrome_downloader.py - Download and extract available chrome releases.
Code by Pierre Laperdrix.
'''
#                                     VARIABLES                                #
ZIP_DIR = './zips/'
BROWSER_DIR = './browsers/'

#                                     FUNCTIONS                                #
def download_versions():
    print("Downloading the available Chrome browsers")

    # Get all URLS from SimpleJet
    with urlopen("https://www.slimjet.com/chrome/google-chrome-old-version.php") as conn:
        html = conn.read()
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all('a')

        for tag in links:
            link = tag.get('href', None)
            if link is not None and ".deb" in link and ("chrome64" in link or "amd64" in link):
                if "amd64" in link:
                    version = link[33:35]
                    subprocess.run("wget --content-disposition -O "+ ZIP_DIR + "chrome64_" + version + ".deb 'https://www.slimjet.com/chrome/" + link + "'", shell=True, check=True)
                else:
                    subprocess.run("wget --content-disposition -P "+ ZIP_DIR + " 'https://www.slimjet.com/chrome/" + link + "'", shell=True, check=True)

def extract():
    print("Extracting Chrome")
    for file in os.listdir(ZIP_DIR):
        subprocess.run("ar vx {} && mkdir {}chrome-{} && tar -C {}chrome-{} -xJf data.* && rm control.tar.?z "
                   "data.tar.xz debian-binary "
                   .format(ZIP_DIR + file, BROWSER_DIR, file[9:11], BROWSER_DIR, file[9:11]), shell=True, check=True)


def chrome_downloader():
    if not os.path.exists(ZIP_DIR):
        os.mkdir(ZIP_DIR)
    if not os.path.exists(BROWSER_DIR):
        os.mkdir(BROWSER_DIR)
    #download_versions()
    extract()


#                                   MAIN                                       #
if __name__ == "__main__":
    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x, not Python 2.x\n")
        sys.exit(1)
    chrome_downloader()
