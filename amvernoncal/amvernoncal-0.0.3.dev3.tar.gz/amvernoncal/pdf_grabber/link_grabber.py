import requests
import urllib.parse
from bs4 import BeautifulSoup


# Default URL for the page that has the link to the calendar
CALENDAR_PAGE = "http://www.ctarthurmurray.com/dance-studios/vernon-ct"


def get_pdf_link(calendar_page=CALENDAR_PAGE):
    """ Returns the absolute URL for a calendar, given the link to the page
        that contains the link to the calendar.
    """
    r = requests.get(calendar_page)
    soup = BeautifulSoup(r.content, "lxml")

    cal_btn = soup.find("a", class_="cta-btn", text="View Class Calendar")
    pdf_sub_link = cal_btn.get("href")
    pdf_link = urllib.parse.urljoin(calendar_page, pdf_sub_link)

    return pdf_link


def download(link):
    """ Downloads a static file given its absolute URL """
    filename = urllib.parse.unquote(link.split("/")[-1])
    r = requests.get(link, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return filename


def download_pdf(calendar_page=CALENDAR_PAGE):
    """ Download the PDF given a link to a page that contains a link to the
        calendar
    """
    link = get_pdf_link(calendar_page)
    filename = urllib.parse.unquote(link.split("/")[-1])
    print("Downloading '{}'...".format(filename))
    download(link)
    print("Download complete.")
