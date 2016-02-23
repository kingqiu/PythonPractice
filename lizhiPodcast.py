#! /usr/bin/python3.4
# coding=utf-8
import requests
import re
import io
import os
import shutil

import sys
import dropbox

# Add OAuth2 access token here.
# You can generate one for yourself in the App Console.
# See <https://blogs.dropbox.com/developers/2014/05/generate-an-access-token-for-your-own-account/>
TOKEN = '<type Your own TOKEN key here>'

LOCALFILE = ''
BACKUPPATH = ''

# 晓松奇谈2016 and others
# can support multiple sources from lizhi.fm
fm_list = [
           'http://www.lizhi.fm/679472/',
           'http://www.lizhi.fm/193491/'
           ]


def requests_file(file_url, filename):
    r = requests.get(file_url)
    if r.status_code == requests.codes.ok:
        with io.open(filename, 'wb') as file:
            file.write(r.content)
            file.flush()
            file.close()


def move_episodes():
    source = os.listdir('.')
    for file in source:
        if file.endswith('.mp3'):
            #index = file.find('_')
            #folder_name = file[:index]
            folder_name = 'media'
            if folder_name not in source:
                os.mkdir(folder_name)
            destination = './' + folder_name + '/'
            shutil.move(file, destination)

# Uploads contents of LOCALFILE to Dropbox
def backup(dFilename):
    client = dropbox.client.DropboxClient(TOKEN)
    print 'linked account: ', client.account_info()
    LOCALFILE = './' + dFilename
    BACKUPPATH = '/Apps/justcast/ChinesePodcasts/' + dFilename

    ff = open(LOCALFILE, 'rb')
    response = client.put_file(BACKUPPATH, ff)
    print 'uploaded: ', response


def main():
    for fm in fm_list:
        r = requests.get(fm)

        r1 = r'data-url="(.*?\.mp3)"'
        r1_comp = re.compile(r1)
        r2 = r'data-radio-name="(.*?)"'
        r2_comp = re.compile(r2)
        r3 = r'data-title="(.*?)"'
        r3_comp = re.compile(r3)

        first_mp3_url = re.findall(r1_comp, r.text)[0]
        radio_name = re.findall(r2_comp, r.text)[0]
        title = re.findall(r3_comp, r.text)[0]
        final_filename = radio_name + '_' + title + '.mp3'
        encode_finalfilename = final_filename + '\n'

        f = open('./latest.txt', 'r+')
        if (encode_finalfilename.encode("utf-8")) not in f.readlines():
            print("downloading " + final_filename.encode("utf-8"))
            requests_file(first_mp3_url, final_filename)
            backup(final_filename)
            f.write(encode_finalfilename.encode("utf-8"))
        f.flush()
        f.close()
        #LOCALFILE = './' + final_filename
        #print("LOCALFILE:" + LOCALFILE)

        move_episodes()
        print("done")


if __name__ == '__main__':
    main()
