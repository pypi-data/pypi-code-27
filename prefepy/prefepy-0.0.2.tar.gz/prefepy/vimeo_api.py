import vimeo

class VimeoApi:
    def __init__(self):
        CLIENT_IDENTIFIER = unicode("ecc42707d88b1ff5659a831eaae849cca76c7c43", ("utf-8"))
        CLIENT_SECRET = unicode(
            "G5fT0yPeH69GyvQUsrKPklA+3Quqg16oplLy1k8edL5tssv97GPbbNoeqgr36l1MCUor4sws8pK71n+Ie/6wCPgeB+FvfbiDO6lktRxD3xOj3aMi5w6OPKIASog+I1X6",
            ("utf-8"))
        TOKEN = unicode("e770e2ac7592ee362e177aa337d41f80", ("utf-8"))
        VIMEO_OAUTH_HEADERS = {
            'Accept': 'application/vnd.vimeo.*+json;version=3.0',
            'Authorization': TOKEN
        }
        self.v = vimeo.VimeoClient(
            token=TOKEN,
            key=CLIENT_IDENTIFIER,
            secret=CLIENT_SECRET
        )

    def get_category_vids(self, category, num_videos):
        url = 'https://api.vimeo.com/categories/sports/videos?sort=date&direction=desc&privacy.embed=public&content_rating=safe&featured=true'

        sport_vids = self.v.get(url)
        sport_vids_dict = sport_vids.json()
        return sport_vids_dict