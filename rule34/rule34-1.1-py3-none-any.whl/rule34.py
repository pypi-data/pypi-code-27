from __future__ import print_function
from collections import defaultdict
from xml.etree import cElementTree as ET
import asyncio
import async_timeout
import aiohttp

class Rule34_Error(Exception):
    """Rule34 rejected you"""
    def __init__(self, message, *args):
        self.message = message
        super(Rule34_Error, self).__init__(message, *args)


class Request_Rejected(Exception):
    """The Rule34 API wrapper rejected your request"""
    def __init__(self, message, *args):
        self.message = message
        super(Request_Rejected, self).__init__(message, *args)

class SelfTest_Failed(Exception):
    """The self test failed"""
    def __init__(self, message, *args):
        self.message = message
        super(SelfTest_Failed, self).__init__(message, *args)

class Rule34:
    def __init__(self, loop, timeout=10):
        """
        :param loop: the event loop
        :param timeout: how long requests are allowed to run until timing out
        """
        self.session = aiohttp.ClientSession(loop=loop)
        self.timeout = timeout

    def ParseXML(self, rawXML):
        """Parses entities as well as attributes following this XML-to-JSON "specification"
            Using https://stackoverflow.com/a/10077069"""
        if "Search error: API limited due to abuse" in str(rawXML.items()):
            raise Rule34_Error('Rule34 rejected your request due to "API abuse"')

        d = {rawXML.tag: {} if rawXML.attrib else None}
        children = list(rawXML)
        if children:
            dd = defaultdict(list)
            for dc in map(self.ParseXML, children):
                for k, v in dc.items():
                    dd[k].append(v)
            d = {rawXML.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
        if rawXML.attrib:
            d[rawXML.tag].update(('@' + k, v) for k, v in rawXML.attrib.items())
        if rawXML.text:
            text = rawXML.text.strip()
            if children or rawXML.attrib:
                if text:
                    d[rawXML.tag]['#text'] = text
            else:
                d[rawXML.tag] = text
        return d

    @staticmethod
    def urlGen(tags=None, limit=None, id=None, PID=None, deleted=None, **kwargs):
        """Generates a URL to access the api using your input:
        :param tags: str ||The tags to search for. Any tag combination that works on the web site will work here. This includes all the meta-tags
        :param limit: str ||How many posts you want to retrieve
        :param id: int ||The post id.
        :param PID: int ||The page number.
        :param deleted: bool||If True, deleted posts will be included in the data
        :param kwargs:
        :return: url string, or None
        All arguments that accept strings *can* accept int, but strings are recommended
        If none of these arguments are passed, None will be returned
        """
        # I have no intentions of adding "&last_id=" simply because its response can easily be massive, and all it returns is ``<post deleted="[ID]" md5="[String]"/>`` which has no use as far as im aware
        URL = "https://rule34.xxx/index.php?page=dapi&s=post&q=index"
        if PID != None:
            URL += "&pid={}".format(PID)
        if limit != None:
            URL += "&limit={}".format(limit)
        if id != None:
            URL += "&id={}".format(id)
        if tags != None:
            tags = str(tags).replace(" ", "+")
            URL += "&tags={}".format(tags)
        if deleted == True:
            URL += "&deleted=show"
        if PID != None or limit != None or id != None or tags != None:
            return URL + "&rating:explicit"
        else:
            return None

    async def totalImages(self, tags):
        """Returns the total amount of images for the tag
        :param tags:
        :return: int
        """
        with async_timeout.timeout(10):
            url = self.urlGen(tags=tags, PID=0)
            async with self.session.get(url=url) as XMLData:
                XMLData = await XMLData.read()
                XMLData = ET.XML(XMLData)
                XML = self.ParseXML(XMLData)
            return int(XML['posts']['@count'])
        return None

    
    async def getImageURLS(self, tags, fuzzy=False, singlePage=False):
        """gatherrs a list of image URLS
        :param tags: the tags youre searching
        :param fuzzy: enable or disable fuzzy search, default disabled
        :param singlePage: when enabled, limits the search to one page (100 images), default disabled
        :return: list
        """
        if fuzzy:
            tags = tags.split(" ")
            for tag in tags:
                tag = tag + "~"
            temp = " "
            tags = temp.join(tags)
            print(tags)
        num = await self.totalImages(tags)
        if num != 0:
            PID = 0
            imgList = []
            XML = None
            t = True
            tempURL = self.urlGen(tags=tags, PID=PID)
            while t:
                with async_timeout.timeout(10):
                    async with self.session.get(url=tempURL) as XML:
                        XML = await XML.read()
                        XML = ET.XML(XML)
                        XML = self.ParseXML(XML)
                if XML is None:
                    return None
                if len(imgList) >= int(XML['posts']['@count']):  # "if we're out of images to process"
                    t = False  # "end the loop"
                else:
                    for data in XML['posts']['post']:
                        imgList.append(str(data['@file_url']))
                if singlePage:
                    return imgList
                PID += 1
            return imgList
        else:
            return None
    
    async def getPostData(self, PostID):
        """Returns a dict with all the information available about the post
        :param PostID: The ID of the post
        :return: dict
        """
        url = self.urlGen(id=str(PostID))
        XML =None
        with async_timeout.timeout(10):
            async with self.session.get(url=url) as XML:
                XML = await XML.read()
            XML = self.ParseXML(ET.XML(XML))
            data = XML['posts']['post']
            return data
        return None

def selfTest():
    """
    Self tests the script for travis-ci, i know it causes a "Unclosed client session" but it doesnt matter
    """
    try:
        loop = asyncio.get_event_loop()
        r34 = Rule34(loop)
        data = loop.run_until_complete(r34.getImageURLS("gay", singlePage=True))
        if data is not None and len(data) != 0:
            print("self test passed")
            exit(0)
        else:
            raise SelfTest_Failed("Automated self test failed to gather images")
    except Exception as e:
        raise SelfTest_Failed("Automated self test failed with this error:\n{}".format(e))

if __name__ == "__main__":
    try:
        selfTest()
    except Exception as e:
        print(e)
        exit(1)
