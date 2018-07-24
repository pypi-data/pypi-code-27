"""  
    filesdownloader

    Function to download files from web to target directory.
    Enable async download of multiple files.

    Required: requests, grequests

"""

import os, sys, re
import string
import random
import requests, grequests
from functools import partial



USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36' 
headers = { 'User-Agent': USER_AGENT }

def dl_files_to_dir(urllist, tgt_folder, job_size = 100):
    """
        Download all files from list of url link to tgt dir
        Args:
            urllist: list of the url retrieved from the google image search
            tgt_folder: dir at which the files to be stored
        Kwargs:
            job_size: (int) number of downloads to spawn.

    """
    if len(urllist) == 0:
        print "No links in urllist"
        return


    def dl_file(r, folder_dir, filename, *args, **kwargs):
        fname = os.path.join(folder_dir, filename)
        with open(fname, 'wb') as my_file:
            # Read by 4KB chunks
            for byte_chunk in r.iter_content(chunk_size=1024*10):#4096?
                if byte_chunk:
                    my_file.write(byte_chunk)
                    my_file.flush()
                    os.fsync(my_file)

        r.close()

       
    do_stuff = []
    
    for run_num, tgt_url in enumerate(urllist):
        print tgt_url
        # handle the tgt url to be use as basename
        basename = os.path.basename(tgt_url)
        file_name = re.sub('[^A-Za-z0-9.]+', '_', basename ) #prevent special characters in filename

        #handling grequest
        action_item =  grequests.get(tgt_url, hooks={'response': partial(dl_file, folder_dir = tgt_folder, filename=file_name)}, headers= headers,  stream=True)  
        do_stuff.append(action_item)

    grequests.map(do_stuff, size=job_size)

    print "All downloads completed"



if __name__ == "__main__":
    urllist = []
    tgt_folder = r'C:\data\temp\strip_site\webdev4' 
    dl_files_to_dir(urllist, tgt_folder, job_size = 100)


