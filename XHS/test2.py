import json

import requests
import re

from bs4 import BeautifulSoup

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en-IE;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "origin": "https://www.xiaohongshu.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.xiaohongshu.com/",
    "sec-ch-ua": "\\Google",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\\Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "x-b3-traceid": "640fe8aef042b95c",
    "x-s": "XYS_2UQhPsHCH0c1Pjh9HjIj2erjwjQhyoPTqBPT49pjHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQTJdPIPAZlg98yGLTlGAzdyDrUpp8bzgz1JUR9p98V2nTypB8awepnc04x2bSkJLDUy0mD+7iF8orlJf8tyMZhpFzNLgSI+b8MyD+3GS8pc0mnJAYHcSkV+BkHPbmCLoYd2pkSNAzd+nzC8SmPqoQVLgbeGfpTcfWEGFzmPrkHaMY/Lb4Pwb+1Pn8+c9EIqMQCLDkcpnbLP9ltJFT/Jfznnfl0yLLIaSQQyAmOarGROaHVHdWFH0ijJ9Qx8n+FHdF=",
    "x-s-common": "2UQAPsHC+aIjqArjwjHjNsQhPsHCH0rjNsQhPaHCH0c1Pjh9HjIj2eHjwjQgynEDJ74AHjIj2ePjwjQhyoPTqBPT49pjHjIj2ecjwjHMN0Z1+UHVHdWMH0ijP/SjP0GU8eLA+AmYP/zCP0+MJBrEP/z38BH9Gfbxyg+DwBRk2f4340ZMPeZIPeLUPADIPjHVHdW9H0ijHjIj2eqjwjHjNsQhwsHCHDDAwoQH8B4AyfRI8FS98g+Dpd4daLP3JFSb/BMsn0pSPM87nrldzSzQ2bPAGdb7zgQB8nph8emSy9E0cgk+zSS1qgzianYt8p+s/LzN4gzaa/+NqMS6qS4HLozoqfQnPbZEp98QyaRSp9P98pSl4oSzcgmca/P78nTTL08z/sVManD9q9z18np/8db8aob7JeQl4epsPrzsagW3Lr4ryaRApdz3agYDq7YM47HFqgzkanYMGLSbP9LA/bGIa/+nprSe+9LI4gzVPDbrJg+P4fprLFTALMm7+LSb4d+kpdzt/7b7wrQM498cqBzSpr8g/FSh+bzQygL9nSm7qSmM4epQ4flY/BQdqA+l4oYQ2BpAPp87arS34nMQyFSE8nkdqMD6pMzd8/4SL7bF8aRr+7+rG7mkqBpD8pSUzozQcA8Szb87PDSb/d+/qgzVJfl/4LExpdzQ4fRSy7bFP9+y+7+nJAzdaLp/2LSiz/W3wLzpag8C2/zQwrRQynP7nSm7cLS9ygGFJURAzrlDqA8c4M8QcA4SL9c7q9cIL0zQzg8APFSo/gzn4MpQynzAP7P6q7Yy/fpkpdzjGMpS8pSn49YQ4fVhG9L78n8M4FbP8DEA8db7qDShJozQ2bk/J7p7/94n47mAq0zi8pL68/8P4fprLo4Bag8dqAbUJ7PlzbkkanD7q9kjJ7PA87QBaLLI8/+c4o8QynQa/7b7/FRl4BYQ2BpA2bm7+FSicnpnLozianW6qMSl4b+oqg4EJpm7zrS9anTQPFSF+BboLAz8N9pk4gzxanSTqDSb/7+/pdzCcfR+womAcg+8pp+LanSyqAQl4rYyqg4Mag8DqM4l4oplaLbApDG9qAbByrEQzLkApf8O8/+l4omPpd4lag898n8n478QyLTSpemM2LS9/9p/Jd8SzobFwLSh+d+3qg4kz9hh/FSbqdSQ4f4A2rMd8nTYN9pxz0mAnpmFLLSkzSQQPFMbJMmF/rSeJLpQye8Ay7mUPUTmN9pg4gzjaLpIPfpM4erU2DbAngkd8/ml49Q6Lo4oag8yqrSbz/YULoc3tM878DSh+g+DGA8S2op7pokl4o+QzaVhnSmF+DSkpDP3GFSDa/+OqM8s/7+kzd8S8S87PBQl4BzQ2rSManT6q9zn4rEQ4fpSPA4bqLSiLLEHGfTSagYi2LS9+fpnqgq7qgp7/74l4FbQP7mDanYm8/bYn0FjNsQhwaHCPAGlPAGA+/P7NsQhP/Zjw0ZVHdWlPaHCHfE6qfMYJsQR",
    "x-t": "1765934487389",
    "x-xray-traceid": "cd94f2eba6bd2963073549fed2499e93"
}
cookies = {
    "abRequestId": "6b7017a3-16c5-53e2-87fa-4fa56980442e",
    "xsecappid": "xhs-pc-web",
    "a1": "19b262d5370a14z23ula914kdb6bajisd8oizgkv050000523902",
    "webId": "340e907e3bff6105d7cddb92cacb6756",
    "gid": "yjDJKJfK2if4yjDJKJf2qYkTW80y4uJq710jlh8y4TfDK328D0V3Mu8882Jqj8J8WWid4D8i",
    "web_session": "040069b443fd5e4a2c40b059743b4b9515608e",
    "unread": "{%22ub%22:%22693d01c5000000001e0338f0%22%2C%22ue%22:%2269411bed000000001e0332d7%22%2C%22uc%22:23}",
    "webBuild": "5.0.7",
    "loadts": "1765933805954",
    "acw_tc": "0ad58ce117659344167406202e9854154df065d518be53c65dbad0046493d5",
    "websectiga": "2845367ec3848418062e761c09db7caf0e8b79d132ccdd1a4f8e64a11d0cac0d",
    "sec_poison_id": "ca1b4ac1-9f82-41c3-836b-efd1a5a1dde9"
}


def get_detail_url():
    url = "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes"
    data = {"keyword":"中国","page":1,"page_size":20,"search_id":"2fqatpwkvfwuny7gamfvz","sort":"general","note_type":0,"ext_flags":[],"geo":"","image_formats":["jpg","webp","avif"]}
    response = requests.post(url, headers=headers, cookies=cookies, json=data).json()['data']['items']
    for item in response:
        x_id = item['id']
        xsec_token = item['xsec_token']
        user_id = item['note_card']['user']['user_id']
        user_xsec_token = item['note_card']['user']['xsec_token']
        comment_info = get_comment(x_id, xsec_token)
        detail_info = get_detail(x_id, xsec_token)
        user_info = get_user_info(user_id, user_xsec_token)
        print(comment_info,detail_info,user_info)
        break

def get_detail(x_id, xsec_token):
    url = f"https://www.xiaohongshu.com/explore/{x_id}"
    params = {
        "xsec_token": f"{xsec_token}",
        "xsec_source": "pc_search",
        "source": "unknown"
    }
    response = requests.get(url, params=params, headers=headers, cookies=cookies).text
    pattern = r'"note"\s*:\s*(.*?)\s*"nioStore"\s*:'
    result = re.search(pattern, response, re.S)

    content = result.group(1)
    if content[-1] == ',':
        content = content[:-1]
    content = json.loads(content)
    firstNoteId = content['firstNoteId']
    data_json = content['noteDetailMap'][firstNoteId]['note']
    currentTime = data_json['time']
    title = data_json['title']
    desc = data_json['desc']
    type = data_json['type']
    if type == 'video':
        media_info = data_json['video']['media']['stream']['h265'][0]['masterUrl']
    else:
        media_info = [i['urlPre'] for i in data_json['imageList']]
    return {
        'firstNoteId': firstNoteId,
        'title': title,
        'desc': desc,
        'type': type,
        'media_info': media_info,
        'currentTime': currentTime,
    }


def get_comment(x_id, xsec_token):
    all_comment = []
    url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/page"
    params = {
        "note_id": f"{x_id}",
        "cursor": "",
        "top_comment_id": "",
        "image_formats": "jpg,webp,avif",
        "xsec_token": f"{xsec_token}"
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params).json()['data']['comments']
    for com in response:
        content = com['content']
        create_time = com['create_time']
        like_count = com['like_count']
        sub_comment_count = com['sub_comment_count']
        # sub_comment_cursor = com['sub_comment_cursor']
        all_comment.append({
            'create_time': create_time,
            'like_count': like_count,
            'sub_comment_count': sub_comment_count,
            'content': content
        })

    return all_comment


def get_user_info(x_id, xsec_token):
    url = f"https://www.xiaohongshu.com/user/profile/{x_id}"
    params = {
        "xsec_token": f"{xsec_token}",
        "xsec_source": "pc_note"
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params).text
    soup = BeautifulSoup(response, 'html.parser')
    user_name = soup.find('div', class_='user-name').text
    user_redId = soup.find('span', class_='user-redId').text
    user_ip = soup.find('span', class_='user-IP').text
    user_desc = soup.find('div', class_='user-desc').text
    user_interactions = [span.text for span in soup.find_all('span', class_='count')]
    show_count = user_interactions[0]
    fans_count = user_interactions[1]
    like_count = user_interactions[2]
    # print(user_name, user_redId, user_ip, user_desc,show_count, fans_count, like_count)
    return {
        'user_name': user_name,
        'user_redId': user_redId,
        'user_ip': user_ip,
        'user_desc': user_desc,
        'show_count': show_count,
        'fans_count': fans_count,
        'like_count': like_count
    }


def main():
    get_detail_url()
    # print(get_user_info('634ab300000000001802bcb8', 'ABO3M3yiI-rvZ1B5qTa1FtcR-UfnApFcwh7f1Cr1DpOaE='))


if __name__ == '__main__':
    main()
