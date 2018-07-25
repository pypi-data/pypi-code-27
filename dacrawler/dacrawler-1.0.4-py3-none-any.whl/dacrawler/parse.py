
class Parse ():
    
    def __init__ (self, html, region, key_name, access_key, secret_key, image_id, instance_type, max_cnt):
        self.html = html
        self.region = region
        self.key_name = key_name
        self.access_key = access_key
        self.secret_key = secret_key
        self.image_id = image_id
        self.instance_type = instance_type
        self.max_cnt = max_cnt
        
    def test (self) :
        return 'hello Parse'
    
if  __name__=="__main__" :
    prs = Parse(
        html          = "",
        region        = "ap-northeast-2",
        key_name      = "udpap2.pem",
        access_key    = "AKIAIPTSPE7MOZ3FXFFA",
        secret_key    = "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",
        image_id      = "ami-afd86dc1", 
        instance_type = "t2.micro",
        max_cnt       = 2
    )
    ret = prs.test()
    print(ret)