from datetime import datetime
import requests
from bs4 import BeautifulSoup

headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en-IE;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.zhihu.com/",
    "sec-ch-ua": "\\Google",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\\Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "x-api-version": "3.0.53",
    "x-requested-with": "fetch",
    "x-zse-93": "101_3_3.0",
    "x-zse-96": "2.0_bbet=0i/Vjt37dpIzYutOsIQUmgUWCISCqH7W1l7wm=CU9fqPk7gtMvf3yasnLqh",
    "x-zst-81": "3_2.0aR_sn77yn6O92wOB8hPZnQr0EMYxc4f18wNBUgpTQ6nxERFZB_Y0-4Lm-h3_tufIwJS8gcxTgJS_AuPZNcXCTwxI78YxEM20s4PGDwN8gGcYAupMWufIeQuK7AFpS6O1vukyQ_R0rRnsyukMGvxBEqeCiRnxEL2ZZrxmDucmqhPXnXFMTAoTF6RhRuLPFMx1Bq3ffcVLk_p8WJLqvu30ND3fLBC8Cg28pq20eg9LAwgO-upOzULfSJSTvASLjDXm0wwCJHpmzvLBc4cB_weBTbLBfcXmoXC_pwwYBcLKwGe81BcBdUwY39NLS4extg21JwXKbU3mZcLBCUXCAULC6JC9WBHxXCpGwgeCSD9_8GoxCqfzGqCK0bgG9Gc9brOYDCxqcLXCuDNsb8xC-w2qOqo99DesoDo_gvNOVDrGVDL9bTcVvBc_sCeCPqtp6bNf2C3CxUL0ThgOZCLm7JS_-BLfhBCpChHCK8LC"
}
cookies = {
    "_xsrf": "QLIWlrnwhUNK6y7zMw4z5AhmfwWGs8DO",
    "_zap": "ba83ebc2-0b02-49c3-b316-e493c3fef6ab",
    "d_c0": "HOZT1qO16RqPTp2HbVi8mk26q2ovTs6Xc3E=|1755140579",
    "Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49": "1755140581,1756880226",
    "__zse_ck": "004_8BrfvtDEEDWY3SqwN9kWV/Fbn3CSVXbtb=EJdSXP0rqDGVYLMNoSf5zqcxuQU1OCmxzvgXzxTV69G8pfUV6U8d8e2ZfNTKzhT8nMqcmJ6nuNwflrhZjbqdmw4hw5jWXq-j2Lokz42sVYe5ptvvod49Yj/QB5H/kFe5rocYme1Yf5x2vUbnX6L1bdcBzIuxbMWzI4ro58PwfBheRABhPETdbdkLy/DiQ5xYhEuIg5mLkEowhbWPC2AKJKqEBZNAtL4",
    "DATE": "1765432136091",
    "crystal": "U2FsdGVkX18xQsH7xtIfqBCMGxLkG765+XH0OnBt9QEDatgOLX5T63QKmvEioBHOcvCNZ0zfCzaDoq27cmhZsOIFg/2n92JqxEey4Z0THpU2H0aMuqnTVYMaXBFNHFRjhP1cRa2292nRJNfIE1Gz5CCS5oSuXrXdAiu2INWFWNu/0BUjgsEsKHk3pkWAmBN+w2DlA7f45oOYlfKQz0URc1YENCfA3pVTDPVMpxHWu9I+cGidegVAJsF7ZCoW+GqD",
    "vmce9xdq": "U2FsdGVkX19PGL1JO3OV06svokZGkIUVHkd6pjtLA0y5Okn6Z34iZj3/IOES0W8Zm1o+0eHKvzKwYyw9u+5LPWmDiHatYGthjRjOvWh7sq/tlEt7sAAIkCa0RiDoagwBZHqzzS0J5UYxh5oKLWnsCw==",
    "captcha_session_v2": "2|1:0|10:1766040148|18:captcha_session_v2|88:MHpsbXZCMC9vZU9TMXdnMkJoRTNtSkhvQ21SYlZBY3ZUTXNXanRGN0pOVC9xWld2WmxxKzZQZjBIeGtlZk0zTQ==|f76f53ecf9d97db95341bf3c754721b4e886738be3504b37c5f0a15e469e92e8",
    "SESSIONID": "N88ngyiCmcUgRHtpQXhTIIUgvQoHAI0lbp3BMAilna7",
    "JOID": "UVoUB0rUJIhqDkNiEahVHlLEVOIImx-1AWs7CFe7Rt4IWQkXYoKAywQNQWQR7lUSfdDiBTs75eGIliuSQ_9Kyyg=",
    "osd": "U1wXA0vWIotuD0FkEqxUHFTHUOMKnRyxAGk9C1O6RNgLXQgVZIGEygYLQmAQ7FMRedHgAzg_5OOOlS-TQflJzyk=",
    "__snaker__id": "73ZNeX3VWOwkhOJT",
    "gdxidpyhxdE": "tx1IT%2Fb%2BNCaxssqW602z7uif0AwMoOLp5X8Z32sRqi9L%2BjA%2FpEgiZDnyo2kPXpiTLR%2Fo%2BkhL0DIPpkex2P2%2BDbzCCWGvXMbPNqT5C7ysxnaXXRyTxU5bzSEZyaHXGOQK3o9y85bBEVj2LnUg146m3czprZZqVd7XW%5CtxRIXAZ%2FCDYBHz%3A1766041049328",
    "cmci9xde": "U2FsdGVkX19prtT/WWV+ybBPhwWwrdSSvkpIedEcpRZdLOcz1IA9XjKHLhEIOxRoe0ToC3eodMCdDI4mmLrhUQ==",
    "pmck9xge": "U2FsdGVkX187sygCOfANXGBs+47hCTIKCgcT3eR11FQ=",
    "assva6": "U2FsdGVkX1843PATqGEWuH0hU/21TQ1rezeWTfDsqek=",
    "assva5": "U2FsdGVkX18v++8UYNC00CJApqz7/z/OgmKiZhbRbw+BSBIQu28vKoIwRYyJKztP5wYaMnJrVcO733+fj2Gy0Q==",
    "o_act": "login",
    "ref_source": "other_https://www.zhihu.com/signin",
    "captcha_ticket_v2": "2|1:0|10:1766040213|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfRipzR1FBOU1HSngxcnhqVC5lOEd0UUJyb2VscnpPQ2dJZDY2dmRpNVVtbUdJeHF3SXZvRkpiVnlwa2ExYW9CbHczUkxvUlE0a3ppX0RnZjhWUXdvU2hyTms4anpEc0MuMEguTkZQRnZIYzJ6Q29WLkIyYXpvYk5WcFRQbWpNUFZHcENxY04qY3I1Qk1GbTZZTktfbHE4d3drbDRaWG40RDZHRXNxZTVMNFhvcnFvc1ZHNGhhNk1xazRPdkZGVlhldEJTSUUqYTEwQnlUTE15Tl9EUDBUeS5ac0licVdkWTEuUGZzVmpnWjYzX3RDMmViRWw0MnNBSmZ1QXZPdkVEenNiNnVoNkpaRl84b0ZMQTZfdXlQVVE0dnhCbGIzemlwb0kqWCpLYWZKQzFucnQuTlZjcHlWQVlqTGxudUYyeF9udnlyUlhtb1VpcU9nbmgqYXVlS2RfUWJyanhuU2RobmZCbnVJNDNPdUgxcjMwV2QzWi5UdDJ4SjBEWnQ4MEpSTml0ZUt0Y0w1Vi40U20uUUdZYjZ4aFdqSUN3Uy5RLnNNSmRneVBrbTlMbnlGY1Zsdk9LdmFCcCpBbzRfYmU0Qy5MS3RxdnY5RnBycWFkU1RaRzZ5ZEdBNHVmZlRyanZzZWI4MUd3NWUzcFFkNkZuV3A4NWU5UkJLQkJWaEpjOVphanY1dWc3N192X2lfMSJ9|3aa757f0e4053fdbf27b08ca8c1b7dab3df4b476723b221768eb7c6e63d42e4a",
    "z_c0": "2|1:0|10:1766040225|4:z_c0|92:Mi4xV2Z2ZVhBQUFBQUFjNWxQV283WHBHaVlBQUFCZ0FsVk5vZkF3YWdBQ0ZLTEwxS3RfVkx1dXJSZnl2eW9KeVlqTVdR|0c7451ed9f6ee409a2f9f848f23f616caf90b7da8dd20090c140319ceb6a8e24",
    "q_c1": "b491e9f440f64923874519549d7507ff|1766040225000|1766040225000",
    "BEC": "8b4a1b0a664dd5d88434ef53342ae417"
}
def get_detail_url(num):
    for i in range(0,num):
        url = "https://www.zhihu.com/api/v3/feed/topstory/recommend"
        params = {
            "action": "down",
            "ad_interval": "-10",
            "after_id": "11",
            "desktop": "true",
            "end_offset": "11",
            "page_number": num,
            "session_token": "db7b1af3511b06c17325a8e6116de1cc"
        }
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        results = response.json()['data']
        for result in results:
            title = result['target']['question']['title']
            content = result['target']['content']
            created_at = datetime.fromtimestamp(int(result['created_time'])).strftime('%Y-%m-%d %H:%M:%S')
            author_name = result['target']['author']['name']
            author_img = result['target']['author']['avatar_url']
            author_headline = result['target']['author']['headline']
            author_user_type = result['target']['author']['user_type']
            comment_count = result['target']['comment_count']
            comment_id = result['target']['id']
            voteup_count = result['target']['voteup_count']
            get_comment(comment_id)
def get_comment(id):
    url = f"https://www.zhihu.com/api/v4/comment_v5/answers/{id}/root_comment"
    params = {
        "order_by": "score",
        "limit": "20",
        "offset": ""
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    results = response.json()['data']
    for result in results:
        comment_content = result['content']
        comment_created_at = datetime.fromtimestamp(int(result['created_time'])).strftime('%Y-%m-%d %H:%M:%S')
        comment_author_name = result['author']['name']
        print(comment_author_name)

def change_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取所有段落文本
    texts = []
    for p in soup.find_all('p'):
        text = p.get_text(strip=True)
        if text:  # 过滤空段落
            texts.append(text)

    # 组合成完整的文章
    full_text = '\n'.join(texts)
    return full_text
def get_search_content(keyword):
    url = "https://www.zhihu.com/api/v4/search_v3"
    params = {
        "gk_version": "gz-gaokao",
        "t": "general",
        "q": keyword,
        "correction": "1",
        "offset": "0",
        "limit": "20",
        "filter_fields": "",
        "lc_idx": "0",
        "show_all_topics": "0",
        "search_source": "Normal"
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    results = response.json()['data']
    for result in results:
        type = result['type']
        if type == 'search_result':
            title = result['object']['title']
            content = change_content(result['object']['content'])
            created_at = datetime.fromtimestamp(int(result['object']['created_time'])).strftime('%Y-%m-%d %H:%M:%S')
            author_name = result['object']['author']['name']
            author_img = result['object']['author']['avatar_url']
            author_headline = result['object']['author']['headline']
            author_user_type = result['object']['author']['user_type']
            comment_count = result['object']['comment_count']
            comment_id = result['object']['id']
            voteup_count = result['object']['voteup_count']
            print(content)
            # get_comment(comment_id)
def main():
    # get_detail_url(1)
    # get_comment('1985012426832377113')
    get_search_content('全球手机芯片')
if __name__ == '__main__':
    main()