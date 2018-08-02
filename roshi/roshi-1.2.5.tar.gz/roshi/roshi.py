import bs4
import os
import requests
import multiprocessing
import zipfile
import io
from tqdm import tqdm

SOURCES = {
    'reader': {
        'base_url': 'https://www.mangareader.net'
    },
    'jaminis': {
        'base_url': 'https://jaiminisbox.com/reader/series/'
    },
}

# Helpers
def sluggify(string):
    tokens = ":', "
    temp = string.lower()
    for token in tokens:
        temp = temp.replace(token, "-")

    return temp
    


class Manga:
    def __init__(self, name):
        # TODO: Add option to specifiy save location
        self._name = name
        self._slug_name = sluggify(name)

    def get_series(self, source = 'reader'):
        # TODO: Multiprocessing for series
        # TODO: Add option to give file path
        source_url = SOURCES[source]['base_url']
        url = source_url + '/' + self._slug_name
        req = requests.get(url)
        soup = bs4.BeautifulSoup(req.text, 'lxml')
        chapters = soup.select('#listing tr a')

        for chapter in tqdm(chapters):
            chapter_url = source_url + chapter.get('href')
            chapter_name, content = self._get_chapter_m_reader(chapter_url)
            with open("{}.cbz".format(chapter_name), "wb") as f:
                f.write(content)


    def get_latest(self, save_file = True):
        chapter_name, content = self._get_latest_jamini(SOURCES['jaminis']['base_url'] + self._slug_name)

        if save_file:
            with open("{}.cbz".format(chapter_name), "wb") as f:
                f.write(content)
        else:
            # Use this for telegram
            return chapter_name, content


    def __str__(self):
        return "<Manga - Series:{}>".format(self._name)

    # Scraping Helper functions

    # Recieves the url to get the latest chapter from Jamini's Box
    # Returns the file object
    def _get_latest_jamini(self, url):
        req = requests.get(url)
        soup = bs4.BeautifulSoup(req.text, 'lxml')
        latest_tag = soup.select('.group')[0].select('.element')[0]
        chapter_name = latest_tag.select('.title')[0].select('a')[0].get("title")
        chapter_name = chapter_name.replace(":", " -")
        latest_url = latest_tag.select('.icon_wrapper')[0].select('a')[0].get('href')
        latest_req = requests.get(latest_url)

        return (chapter_name, latest_req.content)

    # Recieves the url to get the latest chapter from
    # Returns the file object
    def _get_latest_m_reader(self):
        pass


    def _get_chapter_m_reader(self, chapter_url):
        # TODO: Multiprocessing for image downloading
        def get_image(url):
            image_req = requests.get(url)
            soup = bs4.BeautifulSoup(image_req.text, 'lxml')
            img = soup.select('#img')
            image_url = img[0].get('src')
            image_req = requests.get(image_url)
            
            return image_req.content

        chapter_req = requests.get(chapter_url)
        soup = bs4.BeautifulSoup(chapter_req.text, 'lxml')
        pages = soup.select('#pageMenu option')
        chapter_name = soup.select('#mangainfo div h1')[0].get_text()

        in_mem_zip = io.BytesIO()
        with zipfile.ZipFile(in_mem_zip, "w") as chapter_zip:
            for i, page in enumerate(pages):
                page_url = SOURCES['reader']['base_url'] + page.get('value')
                page_name = 'Page-' + str(i + 1) + '.jpg'
                chapter_zip.writestr(page_name, get_image(page_url))

        chapter_content = in_mem_zip.getvalue()
        in_mem_zip.close()

        return (chapter_name, chapter_content)


