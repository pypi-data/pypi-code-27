import collections
import operator
import urllib.parse

import lxml.cssselect
import lxml.etree

from sacad.cover import CoverImageFormat, CoverImageMetadata, CoverSourceQuality, CoverSourceResult
from sacad.sources.base import CoverSource


AmazonDigitalImageFormat = collections.namedtuple("AmazonDigital",
                                                  ("id",
                                                   "slice_count",
                                                   "total_res"))
AMAZON_DIGITAL_IMAGE_FORMATS = [AmazonDigitalImageFormat(0, 1, 600),  # http://z2-ec2.images-amazon.com/R/1/a=B00BJ93R7O+c=A17SFUTIVB227Z+d=_SCR(0,0,0)_=.jpg
                                AmazonDigitalImageFormat(1, 2, 700),  # http://z2-ec2.images-amazon.com/R/1/a=B00BJ93R7O+c=A17SFUTIVB227Z+d=_SCR(1,1,1)_=.jpg
                                AmazonDigitalImageFormat(1, 4, 1280),  # http://z2-ec2.images-amazon.com/R/1/a=B01NBTSVDN+c=A17SFUTIVB227Z+d=_SCR(1,3,3)_=.jpg
                                AmazonDigitalImageFormat(2, 3, 1025),  # http://z2-ec2.images-amazon.com/R/1/a=B00BJ93R7O+c=A17SFUTIVB227Z+d=_SCR(2,2,2)_=.jpg
                                AmazonDigitalImageFormat(2, 5, 1920),  # http://z2-ec2.images-amazon.com/R/1/a=B01NBTSVDN+c=A17SFUTIVB227Z+d=_SCR(2,4,4)_=.jpg
                                AmazonDigitalImageFormat(3, 4, 1500),  # http://z2-ec2.images-amazon.com/R/1/a=B00BJ93R7O+c=A17SFUTIVB227Z+d=_SCR(3,3,3)_=.jpg
                                AmazonDigitalImageFormat(3, 7, 2560)]  # http://z2-ec2.images-amazon.com/R/1/a=B01NBTSVDN+c=A17SFUTIVB227Z+d=_SCR(3,6,6)_=.jpg
AMAZON_DIGITAL_IMAGE_FORMATS.sort(key=operator.attrgetter("total_res"), reverse=True)


class AmazonDigitalCoverSourceResult(CoverSourceResult):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, source_quality=CoverSourceQuality.NORMAL, **kwargs)


class AmazonDigitalCoverSource(CoverSource):

  """ Cover source returning Amazon.com digital music images. """

  BASE_URL = "https://www.amazon.com/gp"
  DYNAPI_KEY = "A17SFUTIVB227Z"
  RESULTS_SELECTORS = (lxml.cssselect.CSSSelector("div#dm_mp3Player div.mp3Cell"),
                       lxml.cssselect.CSSSelector("div#dm_mp3Player li.s-mp3-federated-bar-item"))
  IMG_SELECTORS = (lxml.cssselect.CSSSelector("img.productImage"),
                   lxml.cssselect.CSSSelector("img.s-access-image"))
  LINK_SELECTOR = lxml.cssselect.CSSSelector("a")

  def __init__(self, *args, **kwargs):
    super().__init__(*args, allow_cookies=True, **kwargs)

  def getSearchUrl(self, album, artist):
    """ See CoverSource.getSearchUrl. """
    url = "%s/search" % (__class__.BASE_URL)
    params = collections.OrderedDict()
    params["search-alias"] = "digital-music"
    params["field-keywords"] = " ".join(map(__class__.unaccentuate,
                                            map(str.lower,
                                                (artist, album))))
    params["sort"] = "relevancerank"
    return __class__.assembleUrl(url, params)

  def updateHttpHeaders(self, headers):
    """ See CoverSource.updateHttpHeaders. """
    headers["User-Agent"] = "Mozilla/5.0 Firefox/47.0"

  async def parseResults(self, api_data):
    """ See CoverSource.parseResults. """
    results = []

    # parse page
    parser = lxml.etree.HTMLParser()
    html = lxml.etree.XML(api_data.decode("utf-8"), parser)

    for page_struct_version in range(len(__class__.RESULTS_SELECTORS)):
      result_divs = __class__.RESULTS_SELECTORS[page_struct_version](html)
      if result_divs:
        break

    for rank, result_div in enumerate(result_divs, 1):
      # get thumbnail & full image url
      img_node = __class__.IMG_SELECTORS[page_struct_version](result_div)[0]
      thumbnail_url = img_node.get("src")
      thumbnail_url = thumbnail_url.replace("Stripe-Prime-Only", "")
      url_parts = thumbnail_url.rsplit(".", 2)
      img_url = ".".join((url_parts[0], url_parts[2]))

      # assume size is fixed
      size = (500, 500)

      # try to get higher res image...
      if self.target_size > size[0]:  # ...but only if needed
        self.logger.debug("Looking for optimal subimages configuration...")
        product_url = __class__.LINK_SELECTOR(result_div)[0].get("href")
        product_url = urllib.parse.urlsplit(product_url)
        product_id = product_url.path.split("/")[3]

        # TODO don't pick up highest res image if used asked less?
        for amazon_img_format in AMAZON_DIGITAL_IMAGE_FORMATS:
          self.logger.debug("Trying %u subimages..." % (amazon_img_format.slice_count ** 2))
          urls = tuple(self.generateImgUrls(product_id,
                                            __class__.DYNAPI_KEY,
                                            amazon_img_format.id,
                                            amazon_img_format.slice_count))
          url_ok = await self.probeUrl(urls[-1])
          if not url_ok:
            # images at this size are not available
            continue

          # images at this size are available
          img_url = urls
          size = (amazon_img_format.total_res,) * 2
          break

      # assume format is always jpg
      format = CoverImageFormat.JPEG

      # add result
      results.append(AmazonDigitalCoverSourceResult(img_url,
                                                    size,
                                                    format,
                                                    thumbnail_url=thumbnail_url,
                                                    source=self,
                                                    rank=rank,
                                                    check_metadata=CoverImageMetadata.SIZE))

    return results

  def generateImgUrls(self, product_id, dynapi_key, format_id, slice_count):
    """ Generate URLs for slice_count^2 subimages of a product. """
    for x in range(slice_count):
      for y in range(slice_count):
        yield ("http://z2-ec2.images-amazon.com/R/1/a=" + product_id +
               "+c=" + dynapi_key +
               "+d=_SCR%28" + str(format_id) + "," + str(x) + "," + str(y) + "%29_=.jpg")
