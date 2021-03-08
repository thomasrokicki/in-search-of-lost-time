''' This file downloads all the needed chromedrivers to run available versions.
As chromedrivers often support 1 or 2 chrome versions, we need to download a lot.
'''


import subprocess
import sys
import os
import json
import zipfile
import stat



ALL_VERSIONS = [int(folder[-2:]) for folder in os.listdir("./browsers")]


def download_drivers():
    if not os.path.exists('./chromedrivers'):
        os.mkdir('./chromedrivers')
    with open('./bindings.json','r') as json_file:
        bindings = json.load(json_file)
    for version in ALL_VERSIONS:
        driver_version = bindings[str(version)]
        url = 'https://chromedriver.storage.googleapis.com/' + driver_version + '/chromedriver_linux64.zip'
        filename = './chromedrivers/chromedriver_' + driver_version + '.zip'
        subprocess.run("wget --content-disposition -O " + filename + " " + url , shell=True, check=True)
        try:
            os.mkdir('./chromedrivers/chromedriver_' + driver_version)
            with zipfile.ZipFile(filename,"r") as zip_ref:
                zip_ref.extractall("./chromedrivers/chromedriver_" + driver_version)
                os.chmod("./chromedrivers/chromedriver_" + driver_version + "/chromedriver",0o744)

        except Exception as e:
            print(e)
        os.remove(filename)


if __name__ == "__main__":
    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x, not Python 2.x\n")
        sys.exit(1)
    download_drivers()
