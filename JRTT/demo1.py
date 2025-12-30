import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en-IE;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.toutiao.com/",
    "sec-ch-ua": "\\Google",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\\Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}
cookies = {
    "tt_webid": "7584726441728689705",
    "ttcid": "fb0887581a56433fbce05688850f99c682",
    "local_city_cache": "%E5%8E%A6%E9%97%A8",
    "csrftoken": "0750a288c2887b0840d889232ba1dc26",
    "x-web-secsdk-uid": "76faf570-6d24-45b1-b9c8-37fd1fa3d1c3",
    "s_v_web_id": "verify_mj9p669s_UM4DOlhd_kWo4_4ai9_9Lwq_KdWWHJutsBeU",
    "passport_csrf_token": "ba79642040c4d549d8038f9e2c8e5894",
    "passport_csrf_token_default": "ba79642040c4d549d8038f9e2c8e5894",
    "n_mh": "KqMGNgEFjJdMbP8U41qILlazIXtpnQF0sACDcby8Ak4",
    "sso_uid_tt": "3de176ee342a3bb568fc242a7834245e",
    "sso_uid_tt_ss": "3de176ee342a3bb568fc242a7834245e",
    "toutiao_sso_user": "61dd5a902bd79d71f0c3508fab97cd0f",
    "toutiao_sso_user_ss": "61dd5a902bd79d71f0c3508fab97cd0f",
    "sid_ucp_sso_v1": "1.0.0-KDgzNzc4NmY0NzZjNGMyM2VkZjAzMDQwNmIwNDZiN2QzN2YwMjJjNDIKHgi9hcDM0c2MBRDduonKBhgYIAwwiLTGpgY4BkD0BxoCaGwiIDYxZGQ1YTkwMmJkNzlkNzFmMGMzNTA4ZmFiOTdjZDBm",
    "ssid_ucp_sso_v1": "1.0.0-KDgzNzc4NmY0NzZjNGMyM2VkZjAzMDQwNmIwNDZiN2QzN2YwMjJjNDIKHgi9hcDM0c2MBRDduonKBhgYIAwwiLTGpgY4BkD0BxoCaGwiIDYxZGQ1YTkwMmJkNzlkNzFmMGMzNTA4ZmFiOTdjZDBm",
    "passport_auth_status": "63b3d63229a1295d35c1e4fd0bc60550%2C",
    "passport_auth_status_ss": "63b3d63229a1295d35c1e4fd0bc60550%2C",
    "sid_guard": "63cd0add324e75fe572365f8bb9078e8%7C1765956958%7C5184001%7CSun%2C+15-Feb-2026+07%3A35%3A59+GMT",
    "uid_tt": "1c088f67e1c68e4ca50a0fad0e3b6f12",
    "uid_tt_ss": "1c088f67e1c68e4ca50a0fad0e3b6f12",
    "sid_tt": "63cd0add324e75fe572365f8bb9078e8",
    "sessionid": "63cd0add324e75fe572365f8bb9078e8",
    "sessionid_ss": "63cd0add324e75fe572365f8bb9078e8",
    "session_tlb_tag": "sttt%7C9%7CY80K3TJOdf5XI2X4u5B46P________-xbZeqsr3MTSrd749vZ37u4t8bBSZi1wpOixtd4b0unLA%3D",
    "is_staff_user": "false",
    "sid_ucp_v1": "1.0.0-KDNiZmQ2NmJjZGYyODczYzhiMTdlNTYyMDgzZGI2OWIwNWE0MmViMGQKGAi9hcDM0c2MBRDeuonKBhgYIAw4BkD0BxoCbHEiIDYzY2QwYWRkMzI0ZTc1ZmU1NzIzNjVmOGJiOTA3OGU4",
    "ssid_ucp_v1": "1.0.0-KDNiZmQ2NmJjZGYyODczYzhiMTdlNTYyMDgzZGI2OWIwNWE0MmViMGQKGAi9hcDM0c2MBRDeuonKBhgYIAw4BkD0BxoCbHEiIDYzY2QwYWRkMzI0ZTc1ZmU1NzIzNjVmOGJiOTA3OGU4",
    "odin_tt": "748c8a09156935377ac805b75487a5c11544e938f5d4ed4d526f6ce410f894396a9e8e1cd5d88e3141b92a99d46e522c",
    "gfkadpd": "24,6457",
    "__feed_out_channel_key": "military",
    "_S_DPR": "1",
    "_S_IPAD": "0",
    "_S_WIN_WH": "923_911",
    "tt_scid": "EyeN4yabn3Iy4mTBftUhCjJ3W8Am3D6O6UBzFE7ZCmcPSViYBESq5LFUuh0lwko74cf7",
    "ttwid": "1%7CmLv1ZoaGdU70YsVKkriwzGAcuxUC0fPIbqDrIJ1xaQU%7C1766469200%7C037638601285dccd7e0fbb0620418b643fa5d603a9304947bf1a3a54eea4daf2",
    "tt_anti_token": "o4PhnAcs-b89112a3c465758f0f57bbd1969786a641179d1286ec6c3b6db1c38896723f70"
}
def get_hot():
    url = "https://www.toutiao.com/hot-event/hot-board/"
    params = {
        "origin": "toutiao_pc",
        }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    results = response.json()['data']
    for result in results:
        Url = result['Url']
        ClusterIdStr = result['ClusterId']
        url = get_detail_url(Url)
        detail_dict = get_hot_detail(url)
        comment_list = get_comment(ClusterIdStr)
        title = result['Title']
        return {
            '帖子ID': ClusterIdStr,
            '帖子标题': title,
            '帖子作者': detail_dict['media_name'],
            '帖子创建时间':detail_dict['create_at'],
            '帖子内容': detail_dict['content'],
            '帖子链接': url,
            '阅读数': detail_dict['read_count'],
            '评论数': detail_dict['comment_count'],
            '点赞数': detail_dict['like_count'],
            '评论时间': comment_list['comment_create_time'],
            '评论IP': comment_list['comment_publish_loc_info'],
            '评论内容': comment_list['comment_text'],
            '评论者': comment_list['comment_user_name']
        }

def get_recomment():
    url = "https://www.toutiao.com/api/pc/list/feed?channel_id=0&max_behot_time=1766472371&offset=0&category=pc_profile_recommend&aid=24&app_name=toutiao_web&a_bogus=Yj8wQmz6di6NkVWd5W9LfY3qVUa3YZQ80t9bMDhq1dV99g39HMYF9exLHOvvgQbjiG/BIeDjy4hSYpPMx5AJA3vRHuDKUIcgmESDeM32so0j5HJyCjuQJ0UqmktISlc25k3WE/i8wwIaSYukW9Fe5h2RbfqbapEk96EtO939lNE6HB3v"
    response = requests.get(url, headers=headers, cookies=cookies)
    results = response.json()['data']
    for result in results:
        group_id = result['group_id']
        title = result['title']
        media_name = result['media_name']
        publish_time = datetime.fromtimestamp(result['publish_time']).strftime('%Y-%m-%d %H:%M:%S')
        read_count = result['read_count']
        comment_count = result['comment_count']
        like_count = result['like_count']
        url = result['url']
        comment_list = get_comment(group_id)
        content = get_detail(url)
        return {
            '帖子ID': group_id,
            '帖子标题':title,
            '帖子作者':media_name,
            '帖子创建时间':publish_time,
            '帖子内容':content,
            '帖子链接':url,
            '阅读数':read_count,
            '评论数':comment_count,
            '点赞数':like_count,
            '评论时间':comment_list['comment_create_time'],
            '评论IP':comment_list['comment_publish_loc_info'],
            '评论内容':comment_list['comment_text'],
            '评论者':comment_list['comment_user_name']
        }

def get_search(keyword):
    url = "https://so.toutiao.com/search"
    params = {
        "source": "pagination",
        "keyword": keyword,
        "pd": "information",
        "action_type": "pagination",
        "page_num": "1",
        "from": "news",
        "cur_tab_title": "news",
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params).text
    pattern = r'window\.T\s*&&\s*T\.flow\(\{\s*data\s*:\s*(.*?)(?=,\s*src_id\s*:)'
    data_list = re.findall(pattern, response, re.S)
    for data in data_list:
        json_data = json.loads(data)
        group_id = json_data['id']
        title = json_data['title']
        media_name = json_data['media_name']
        publish_time = json_data['datetime']
        read_count = json_data['read_count']
        comment_count = json_data['comment_count']
        like_count = json_data['digg_count']
        url = f'https://www.toutiao.com/article/{group_id}/'
        comment_list = get_comment(group_id)
        content = get_detail(url)
        print(url)
        return {
            '帖子ID': group_id,
            '帖子标题': title,
            '帖子作者': media_name,
            '帖子创建时间': publish_time,
            '帖子内容': content,
            '帖子链接': url,
            '阅读数': read_count,
            '评论数': comment_count,
            '点赞数': like_count,
            '评论时间': comment_list['comment_create_time'],
            '评论IP': comment_list['comment_publish_loc_info'],
            '评论内容': comment_list['comment_text'],
            '评论者': comment_list['comment_user_name']
        }

def get_detail_url(url):
    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        url = soup.find('div',class_='feed-card-article-l').find('a').get('href')
    except:
    # if 'article' not in url:
        url = soup.find('p',class_='content').find('a').get('href')
    return 'https://www.toutiao.com'+url

def get_hot_article_detail(url):
    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('div',class_='article-content').find('h1').text
    create_at = soup.find('div',class_='article-meta').find('span').text
    media_name = soup.find('span',class_='name').find('a').text
    read_count = ''
    comment_count = ''
    like_count = soup.find('div',class_='detail-like').find('span').text
    content = soup.find('article', class_='syl-article-base syl-page-article tt-article-content syl-device-pc').text
    return {
        'title': title,
        'media_name': media_name,
        'create_at': create_at,
        'read_count': read_count,
        'comment_count': comment_count,
        'like_count': like_count,
        'content': content
    }
def get_hot_detail(url):
    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    create_at = soup.find('span', class_='time').text
    media_name = soup.find('a', class_='name').text
    read_count = ''
    comment_count = ''
    like_count = soup.find('div', class_='detail-like').find('span').text
    content = soup.find('div', class_='weitoutiao-html').text
    return {
        'media_name': media_name,
        'create_at': create_at,
        'read_count': read_count,
        'comment_count': comment_count,
        'like_count': like_count,
        'content': content
    }

def get_detail(url):
    response = requests.get(url, headers=headers, cookies=cookies).text
    soup = BeautifulSoup(response, 'html.parser')
    content = soup.find('article', class_='syl-article-base syl-page-article tt-article-content syl-device-pc').text
    return content

def get_comment(group_id):
    url = "https://www.toutiao.com/article/v4/tab_comments/"
    params = {
        "aid": "24",
        "app_name": "toutiao_web",
        "offset": "0",
        "count": "20",
        "group_id": group_id,
        "item_id": group_id,
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    results = response.json()['data']
    for result in results:
        comment_create_time = result['comment']['create_time']
        comment_publish_loc_info = result['comment']['publish_loc_info']
        comment_text = result['comment']['text']
        comment_user_name = result['comment']['user_name']
        return {
            'comment_create_time': datetime.fromtimestamp(comment_create_time).strftime('%Y-%m-%d %H:%M:%S'),
            'comment_publish_loc_info': comment_publish_loc_info,
            'comment_text': comment_text,
            'comment_user_name': comment_user_name
        }

def main():
    # print(get_detail_url('https://www.toutiao.com/trending/7588072414128275497/?category_name=topic_innerflow&event_type=hot_board&log_pb=%7B%22category_name%22%3A%22topic_innerflow%22%2C%22cluster_type%22%3A%226%22%2C%22enter_from%22%3A%22click_category%22%2C%22entrance_hotspot%22%3A%22outside%22%2C%22event_type%22%3A%22hot_board%22%2C%22hot_board_cluster_id%22%3A%227588072414128275497%22%2C%22hot_board_impr_id%22%3A%2220251229092535ECC0FFFE38E4B07B1C44%22%2C%22jump_page%22%3A%22hot_board_page%22%2C%22location%22%3A%22news_hot_card%22%2C%22page_location%22%3A%22hot_board_page%22%2C%22source%22%3A%22trending_tab%22%2C%22style_id%22%3A%2240132%22%2C%22title%22%3A%22%E5%AA%92%E4%BD%93%EF%BC%9A%E5%9B%BD%E9%99%85%E7%A4%BE%E4%BC%9A%E4%B8%80%E8%87%B4%E8%AE%A4%E5%8F%AF%E4%B8%AD%E5%9B%BD%E6%96%A1%E6%97%8B%E6%9F%AC%E6%B3%B0%22%7D&rank=&style_id=40132&topic_id=7588072414128275497'))
    print(get_hot_detail('https://www.toutiao.com/w/1852769249821715/'))
    # num = input('请选择采集那一栏(1.推荐,2.热榜,3.关键字搜索)')
    # if num == '1':
    #     get_recomment()
    # elif num == '2':
    #     get_hot()
    # elif num == '3':
    #     get_search('AI')
    # else:
    #     print('没有这个选项')
if __name__ == '__main__':
    main()