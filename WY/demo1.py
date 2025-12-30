import requests
from bs4 import BeautifulSoup

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en-IE;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://news.163.com/",
    "sec-ch-ua": "\\Google",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\\Windows",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}
cookies = {
    "nts_mail_user": "19859717157@163.com:-1:1",
    "NTES_P_UTID": "OVT1iVzAQFqRHYhO5erjsLlsTYN2H9Ug|1761040740",
    "_ntes_origin_from": "baidu",
    "_ntes_nuid": "ec6025b3d644b9983e4bfbfbb2d8276b",
    "_antanalysis_s_id": "1766382838786",
    "ne_analysis_trace_id": "1766382876011",
    "NTES_YD_SESS": "oLwY8mnAHkiVSYEaYu_1eDoS8ZTpqf6b0QnVsN5ksx2IceKDcQzbiWQltbZa4k0j0ceHpNtVfW5Z5vX9nuyrE5jsdKi_I6xiDmEd_2r1rcgoRkBAbUYw7luU2yOezXtrEBIoor55SMkzWoV8QvagLRpE97ocp4lHp4U7T0ScXfFlnnYE2tvoHdeTKMX52Y8eFsgZA_NSfqKJE.EQZ.MXftQXyIdl3gOYt2RHG02WRNJ6L",
    "NTES_YD_PASSPORT": "eowZZDNdkvpFnMvYpkZDk2KNeJyNuNgqrlCBthU9I5qfAZ_WA7Kw6g7kSwF9ILoEoAZGqPSaugyNYQW1N15gy9WR6tyEBK31kMbaMM0P5pi.HpMzyhUuhXG6NZHzcVNXMeOAEoy2d8CZ98jBDih94_HJFV1Thim43rvW_tdrxkiRZo7ivhTGf.dI6Hs2RHLxpM.2TtbC4SqI3e.IuFqOUqLG4",
    "S_INFO": "1766386623|0|0&60##|19559268045",
    "P_INFO": "19559268045|1766386623|0|163|00&99|null&null&null#fuj&350100#10#0#0|&0||19559268045",
    "cm_newmsg": "user%3D195*****045%26new%3D-1%26total%3D-1",
    "s_n_f_l_n3": "4a76d938577064c81766386629750",
    "UserProvince": "%u5168%u56FD",
    "NTES_CMT_USER_INFO": "1230420795%7C%E6%9C%89%E6%80%81%E5%BA%A6%E7%BD%91%E5%8F%8B19lHIX%7Chttp%3A%2F%2Fcms-bucket.nosdn.127.net%2F2018%2F08%2F13%2F078ea9f65d954410b62a52ac773875a1.jpeg%7Cfalse%7CeWQuNzVlNjlhNzg0YWExNDM0NWFAMTYzLmNvbQ%3D%3D",
    "pgr_n_f_l_n3": "4a76d938577064c817663866349257557",
    "vinfo_n_f_l_n3": "4a76d938577064c8.1.1.1766382838095.1766384321541.1766388166991"
}
start_url_list = ['https://news.163.com/domestic/','https://news.163.com/world/','https://war.163.com/','https://news.163.com/air/']
def get_detail_url():
    for url in start_url_list:
        response = requests.get(url, headers=headers, cookies=cookies).text
        soup = BeautifulSoup(response, 'html.parser')
        url_content = soup.find('div',class_='hidden')
        urls = [a.get('href') for a in url_content.find_all('a')]
        for index,url in enumerate(urls):
            if 'video' not in url:
                get_detail(url)

def get_detail(url):
    response = requests.get(url, headers=headers, cookies=cookies).text
    soup = BeautifulSoup(response, 'html.parser')
    title = soup.find('h1',class_='post_title').text.strip()
    create_at = soup.find('div',class_='post_info').text.split('来源')[0].strip()
    content = soup.find('div',class_='post_body')
    text = content.text.strip()
    img = [img.get('src') for img in content.find_all('img')]
    print(title,create_at,text,img)
    print()

def get_search(keyword):
    url = "https://www.163.com/search"
    params = {
        "keyword": keyword
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params).text
    soup = BeautifulSoup(response, 'html.parser')
    urls = [div.find('a').get('href') for div in soup.find_all('div',class_='keyword_img')]
    for url in urls:
        if 'video' not in url:
            get_detail(url)
def main():
    # get_detail_url()
    # get_detail('https://www.163.com/dy/article/KHET2NVJ051181GK.html')
    get_search('AI')
if __name__ == '__main__':
    main()