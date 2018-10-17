from copyheaders import headers_raw_to_dict

post_headers_raw = b'''
Accept:*/*
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.9
Cache-Control:no-cache
Connection:keep-alive
DNT:1
Host:emweb.securities.eastmoney.com
Pragma:no-cache
Referer:http://emweb.securities.eastmoney.com/FinanceAnalysis/Index?type=web&code=sh603180
User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36
X-Requested-With:XMLHttpRequest
'''
# 把header转化为字典类型
header_dict = headers_raw_to_dict(post_headers_raw)

class SpiderHeaderUtil:

    @staticmethod
    def  get_df_header():
        return header_dict;