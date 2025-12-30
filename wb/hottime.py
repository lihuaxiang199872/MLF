import requests
from datetime import datetime
from bs4 import BeautifulSoup
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en-IE;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "client-version": "v2.47.141",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://weibo.com/hot/weibo/102803",
    "sec-ch-ua": "\\Google",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\\Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "server-version": "v2025.12.17.2",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
    "x-xsrf-token": "N--rze5l-RYIzujnClbRLw4S"
}
cookies = {
    "XSRF-TOKEN": "N--rze5l-RYIzujnClbRLw4S",
    "SCF": "AhDjvdhJNMnwuRQd5XpuiSCKo8jKBoBLUAbp6hJiEKhJqFeCUqcvjBk9d74n7i7G5DmWoSKTBSOcukIN-KrST-0.",
    "SUB": "_2A25ERic5DeRhGe5N61AX8S_Pwj-IHXVnOibxrDV8PUNbmtANLWSskW9NdR2Q6iwFOlqMSYfqVNKzeqZcFU6IMQV0",
    "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9W5y7XsAToXrEOiKeqsJY2wa5JpX5KzhUgL.Fon0ehzceK201Ke2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMRe05ESo2pe0.0",
    "ALF": "02_1768547433",
    "_s_tentry": "weibo.com",
    "Apache": "875309026841.9373.1765955882398",
    "SINAGLOBAL": "875309026841.9373.1765955882398",
    "ULV": "1765955882403:1:1:1:875309026841.9373.1765955882398:",
    "webim_unReadCount": "%7B%22time%22%3A1765960435641%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A4%2C%22msgbox%22%3A0%7D",
    "WBPSESS": "3OL9DxHbwY5BHzlwXKMvoJji72lSHTELNL6-Uj8fnGLt-vpKJoFEXiGaS97WJ6pAbZ3811yfkizU5BCM0LDuLVnMDMs5b6djw_5uJv-fsWtK8MLmBtwFPyqDdY7XMrnpOwD8iL5QMVch_xJAHozjbA=="
}
def convert_weekday_timezone(date_str):
    """
    将 'Wed Dec 17 10:00:26 +0800 2025'
    转换为 '2025-12-17 10:00:26'
    """
    try:
        dt = datetime.strptime(
            date_str.strip(),
            "%a %b %d %H:%M:%S %z %Y"
        )
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError(f"日期格式错误：{date_str}")
def get_detail_url():
    url = "https://weibo.com/ajax/feed/hottimeline"
    params = {
        "since_id": "0",
        "refresh": "0",
        "group_id": "102803600343",
        "containerid": "102803_ctg1_600343_-_ctg1_600343",
        "extparam": "discover|new_feed",
        "max_id": "0",
        "count": "10"
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    results = response.json()['statuses']
    for item in results:
        x_id = item['id']
        created_at = convert_weekday_timezone(item['created_at'])
        attitudes_count = item['attitudes_count'] # 点赞数
        comments_count = item['comments_count'] # 评论数
        reposts_count = item['reposts_count'] # 转发数
        text_raw = item['text_raw']
        user_id = item['user']['id']
        main_url = url
        # print(x_id, created_at, attitudes_count, comments_count, reposts_count, text_raw, user_id)
        get_user_info(user_id)
        get_comment(x_id,user_id)
def get_comment(x_id,user_id):
    url = "https://weibo.com/ajax/statuses/buildComments"
    params = {
        "flow": "0",
        "is_reload": "1",
        "id": x_id,
        "is_show_bulletin": "2",
        "is_mix": "0",
        "count": "10",
        "uid": user_id,
        "fetch_level": "0",
        "locale": "zh-CN"
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    results = response.json()['data']
    for item in results:
        comment_text_raw = item['text']
        comment_created_at = convert_weekday_timezone(item['created_at'])
        comment_like_counts = item['like_counts']
        comment_screen_name = item['user']['screen_name']
        comment_location = item['user']['location']
        # print(comment_text_raw, comment_created_at, comment_like_counts, comment_screen_name, comment_location)
        return {
            'comment_text': comment_text_raw,
            'comment_created_at': comment_created_at,
            'comment_like_counts': comment_like_counts,
            'comment_screen_name': comment_screen_name,
            'comment_location': comment_location
        }
def get_user_info(user_id):
    url = "https://weibo.com/ajax/profile/info"
    params = {
        "uid": user_id
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    results = response.json()['data']['user']
    user_description = results['description']
    user_followers_count = results['followers_count'] # 粉丝数
    user_friends_count = results['friends_count'] # 关注人数
    user_screen_name = results['screen_name']
    user_comment_cnt = results['status_total_counter']['comment_cnt'] #总评论数
    user_like_cnt = results['status_total_counter']['like_cnt'] #总点赞数
    user_repost_cnt = results['status_total_counter']['repost_cnt'] #总转发数
    user_total_cnt_format = results['status_total_counter']['total_cnt_format'] # 总转赞数
    verified_reason = results['verified_reason']
    return {
        'user_description': user_description,
        'user_followers_count': user_followers_count,
        'user_friends_count': user_friends_count,
        'user_screen_name': user_screen_name,
        'user_comment_cnt': user_comment_cnt,
        'user_like_cnt': user_like_cnt,
        'user_repost_cnt': user_repost_cnt,
        'user_total_cnt_format': user_total_cnt_format,
        'verified_reason': verified_reason
    }
def get_search(key):
    url = "https://s.weibo.com/weibo"
    params = {
        "q": key
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params).text
    soup = BeautifulSoup(response, 'html.parser')
    x_ids = [div.get('mid') for div in soup.find_all('div', class_='card-wrap') if div and div.get('mid')]
    created_ats = [div.find('a').text for div in soup.find_all('div',class_='from') if div.find('a') and div.find('a').text]
    links = [div.find('a').get('href') for div in soup.find_all('div',class_='from') if div.find('a') and div.find('a').get('href')]
    attitudes_counts = [span.text for span in soup.find_all('span', class_='woo-like-count') if span and span.text]
    comments_counts = [a.text for a in soup.find_all('a',{'action-type':'feed_list_comment'}) if a and a.text]
    reposts_counts = [a.text for a in soup.find_all('a',{'action-type':'feed_list_forward'}) if a and a.text]
    text_raws = [p.text for p in soup.find_all('p',{'node-type':'feed_list_content'}) if p and p.text]
    # print(len(x_id),len(created_at),len(attitudes_count),len(comments_count),len(reposts_count),len(text_raw),len(link))
    for index,x_ids in enumerate(x_ids):
        x_id = x_ids.split()
        created_at = created_ats[index].split()
        user_id = links[index].split('/')[3].split()
        attitudes_count = attitudes_counts[index].split()
        comments_count = comments_counts[index].split()
        reposts_count = reposts_counts[index].split()
        text_raw = text_raws[index].split()

def main():
    # get_detail_url()
    # print(get_user_info(1752917463))
    # get_comment('5244781438961139',9141079573)
    get_search('五哈')
if __name__ == '__main__':
    main()