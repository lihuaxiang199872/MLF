import time
import requests
import execjs
from datetime import datetime

headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en-IE;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "origin": "https://search.bilibili.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://search.bilibili.com/all?keyword=AI&from_source=webtop_search&spm_id_from=333.1007&search_source=5&page=2&o=24",
    "sec-ch-ua": "\\Google",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\\Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}
cookies = {
    "buvid3": "6BB9C378-14FD-7CDF-A108-51AF288F929303281infoc",
    "b_nut": "1764834803",
    "_uuid": "AFA85643-2DFE-7CE7-3F2F-10783E5F87F6104142infoc",
    "CURRENT_QUALITY": "0",
    "buvid_fp": "e3376fa998e60cc87e3f5babb528a77c",
    "buvid4": "A9DCEDDA-E589-07EF-3B43-7BFC3294000904656-025120415-XDvCUQzBHeE0HE8/h43Ztg%3D%3D",
    "rpdid": "|(J|)YYJ~lJ~0J'u~YR)JR)|l",
    "bsource": "search_baidu",
    "b_lsid": "F75E12D5_19B4F163B53",
    "SESSDATA": "2a5b718a%2C1782110441%2C33f23%2Ac2CjBHpERBhsWzklI38F4yJt5Xvs5j_ABIelkkQ75YJq-vc9ktaFN6yR8njUx2yleOwfwSVmRYZmRDdlZyVlBZMkJMaXg2cFVsNFFaUUFMWUc1cm9HQXIxMlJ2S2ZpR1hIZG5JTUFLSS1QcnJTbkNzNm9zM3BLQUlyemdVVkpaV1VhODIxMWpxMzlnIIEC",
    "bili_jct": "54aa238902bc15cfd977ba5784e884e0",
    "DedeUserID": "3537118345300308",
    "DedeUserID__ckMd5": "9e0a26645d39c622",
    "CURRENT_FNVAL": "2000",
    "home_feed_column": "4",
    "browser_resolution": "853-911",
    "theme-tip-show": "SHOWED",
    "bili_ticket": "eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjY4MTc2NTksImlhdCI6MTc2NjU1ODM5OSwicGx0IjotMX0.DcigKfkbIiITSKfV1pf6mEqJJYSbD9-iWC1mbQWjCiI",
    "bili_ticket_expires": "1766817599",
    "sid": "ew8hvg4m"
}
def get_search(keyword):
    url = "https://api.bilibili.com/x/web-interface/wbi/search/type"
    for i in range(1,2):
        params = {
            "category_id": "",
            "search_type": "video",
            "ad_resource": "5654",
            "__refresh__": "true",
            "_extra": "",
            "context": "",
            "page": i,
            "page_size": "42",
            "pubtime_begin_s": "0",
            "pubtime_end_s": "0",
            "from_source": "",
            "from_spmid": "333.337",
            "platform": "pc",
            "highlight": "1",
            "single_column": "0",
            "keyword": keyword,
            "qv_id": "PvsGcO2h6nNmCHsbqum0XWx52drQ71LZ",
            "source_tag": "3",
            "gaia_vtoken": "",
            "dynamic_offset": "24",
            "web_roll_page": "1",
            "web_location": "1430654",
            "w_rid": "d933408047329da0165e068f333c7cc1",
            "wts": "1766558489"
        }
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        results = response.json()['data']['result']
        print(results)
        for result in results:
            title = result['title']
            url = result['arcurl']
            author =result['author']
            mid = result['id']
            like = result['like']
            review =result['review']
            pubdate = result['pubdate']
            description = result['description']
            comment = get_comment(mid)
            return {
                "title": title,
                "url": url,
                "author": author,
                "mid": mid,
                "like": like,
                "review": review,
                "description": description,
                "pubdate": datetime.fromtimestamp(pubdate).strftime('%Y-%m-%d %H:%M:%S'),
                'comment_name':comment['comment_name'],
                'comment_content':comment['comment_content'],
                'comment_time':comment['comment_time'],
            }


def get_w_rid_js(mid,wts):
    # 读取 JS 文件
    with open('w_rid.js', 'r', encoding='utf-8') as f:
        js_code = f.read()

    # 创建 JS 环境
    ctx = execjs.compile(js_code)

    # 调用函数
    a = "ea1db124af3c7062474693fa704f4ff8"
    v = f"mode=3&oid={mid}&pagination_str=%7B%22offset%22%3A%22%22%7D&plat=1&seek_rpid=&type=1&web_location=1315875&wts={wts}"

    w_rid = ctx.call('Qe.exports', v + a)
    return w_rid
def get_comment(mid):
    wts = str(int(time.time()))  # 当前时间戳
    w_rid = get_w_rid_js(mid,wts)
    url =f"https://api.bilibili.com/x/v2/reply/wbi/main?oid={mid}&type=1&mode=3&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&web_location=1315875&w_rid={w_rid}&wts={wts}"
    response = requests.get(url, headers=headers, cookies=cookies)
    results = response.json()['data']['replies']
    for result in results:
        comment_name = result['member']['uname']
        comment_content = result['content']['message']
        comment_time = result['ctime']
        return {
            'comment_name': comment_name,
            'comment_content': comment_content,
            'comment_time': datetime.fromtimestamp(comment_time).strftime('%Y-%m-%d %H:%M:%S'),
        }
def main():
    print(get_search('美国'))
    # print(get_comment('115749653912205'))
if __name__ == '__main__':
    main()

