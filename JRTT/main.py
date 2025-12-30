import json
import re
import requests
import pandas as pd
import os
import time
from datetime import datetime
from typing import Dict, List, Any
from bs4 import BeautifulSoup

# 使用你提供的headers和cookies
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


class ToutiaoScraper:
    def __init__(self):
        self.headers = headers
        self.cookies = cookies
        self.all_data = []

    def safe_get(self, data: Dict, keys: List[str], default: Any = "") -> Any:
        """安全获取嵌套字典的值"""
        try:
            for key in keys:
                if isinstance(data, dict):
                    data = data.get(key)
                elif isinstance(data, list) and isinstance(key, int) and 0 <= key < len(data):
                    data = data[key]
                else:
                    return default
                if data is None:
                    return default
            return data if data is not None else default
        except (KeyError, TypeError, IndexError, AttributeError):
            return default

    def safe_find(self, soup, selector: str, attribute: str = None, default: Any = ""):
        """安全查找BeautifulSoup元素"""
        try:
            element = soup.select_one(selector)
            if element:
                if attribute:
                    return element.get(attribute, default)
                else:
                    text = element.get_text(strip=True)
                    return text if text else default
            return default
        except Exception:
            return default

    def get_hot_board(self, max_items: int = 10) -> List[Dict]:
        """获取热榜数据"""
        print("正在获取今日头条热榜...")

        hot_items = []
        try:
            url = "https://www.toutiao.com/hot-event/hot-board/"
            params = {"origin": "toutiao_pc"}

            response = requests.get(url, headers=self.headers, cookies=self.cookies,
                                    params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            results = self.safe_get(data, ['data'], [])

            for i, result in enumerate(results[:max_items]):
                try:
                    hot_items.append({
                        'Url': self.safe_get(result, ['Url']),
                        'ClusterIdStr': self.safe_get(result, ['ClusterIdStr']),
                        'Title': self.safe_get(result, ['Title']),
                        'HotValue': self.safe_get(result, ['HotValue']),
                        'Label': self.safe_get(result, ['Label'])
                    })
                except Exception as e:
                    print(f"解析热榜条目失败 {i}: {e}")
                    continue

            print(f"获取到 {len(hot_items)} 条热榜数据")

        except Exception as e:
            print(f"获取热榜失败: {e}")

        return hot_items

    def get_recommend_feed(self, max_items: int = 10) -> List[Dict]:
        """获取推荐内容"""
        print("正在获取今日头条推荐内容...")

        recommend_items = []
        try:
            url = "https://www.toutiao.com/api/pc/list/feed?channel_id=0&min_behot_time=0&offset=0&refresh_count=1&category=pc_profile_recommend&aid=24&app_name=toutiao_web&msToken=rjjaF5EOrOZzW8vLMXIbcZtKKpG-92T_bBB_tThJ-wmv8sSs-br0xtDZ8LtEz4iVghPZ6Ksb5iyeRsp4URYcxiuG7IoHiaU4B8PcADzZkn0KA0lyDL8cEQ%3D%3D&a_bogus=dX80%2FQ86dDDpDfS25WOLfY3qV6-3Y82T0t9bMDhqvnVspL39HMTP9exE9RhvJKYjiG%2FBIeDjy4hbO3xprQI90Zwf7Wsx%2F2CZmyh0tMeg5xSSs1Xrejusr0DF-vUUSaBB5vlUrOXgqXlHFbYsAnAn4XoRbfeycNyk96EtO939lNE6HB35"
            response = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=15)
            response.raise_for_status()
            data = response.json()

            results = self.safe_get(data, ['data'], [])

            for i, result in enumerate(results[:max_items]):
                try:
                    publish_time = self.safe_get(result, ['publish_time'])
                    if publish_time:
                        publish_time_str = datetime.fromtimestamp(publish_time).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        publish_time_str = ''

                    recommend_items.append({
                        'group_id': str(self.safe_get(result, ['group_id'])),
                        'title': self.safe_get(result, ['title']),
                        'media_name': self.safe_get(result, ['media_name']),
                        'publish_time': publish_time_str,
                        'read_count': self.safe_get(result, ['read_count']),
                        'comment_count': self.safe_get(result, ['comment_count']),
                        'like_count': self.safe_get(result, ['like_count']),
                        'url': self.safe_get(result, ['url'])
                    })
                except Exception as e:
                    print(f"解析推荐条目失败 {i}: {e}")
                    continue

            print(f"获取到 {len(recommend_items)} 条推荐内容")

        except Exception as e:
            print(f"获取推荐内容失败: {e}")

        return recommend_items

    def search_content(self, keyword: str, max_items: int = 10) -> List[Dict]:
        """搜索内容"""
        print(f"正在搜索关键词: {keyword}")

        search_items = []
        try:
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

            response = requests.get(url, headers=self.headers, cookies=self.cookies,
                                    params=params, timeout=15)
            response.raise_for_status()

            # 使用正则表达式提取数据
            pattern = r'window\.T\s*&&\s*T\.flow\(\{\s*data\s*:\s*(.*?)(?=,\s*src_id\s*:)'
            data_list = re.findall(pattern, response.text, re.S)

            for i, data_str in enumerate(data_list[:max_items]):
                try:
                    json_data = json.loads(data_str)

                    search_items.append({
                        'group_id': str(self.safe_get(json_data, ['id'])),
                        'title': self.safe_get(json_data, ['title']),
                        'media_name': self.safe_get(json_data, ['media_name']),
                        'datetime': self.safe_get(json_data, ['datetime']),
                        'read_count': self.safe_get(json_data, ['read_count']),
                        'comment_count': self.safe_get(json_data, ['comment_count']),
                        'digg_count': self.safe_get(json_data, ['digg_count']),
                        'url': f'https://www.toutiao.com/article/{self.safe_get(json_data, ["id"])}/'
                    })
                except Exception as e:
                    print(f"解析搜索结果失败 {i}: {e}")
                    continue

            print(f"搜索到 {len(search_items)} 条结果")

        except Exception as e:
            print(f"搜索失败: {e}")

        return search_items

    def get_detail_url(self, url: str) -> str:
        """获取详情页链接"""
        try:
            response = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            link_element = soup.select_one('div.feed-card-article-l a')

            if link_element and link_element.get('href'):
                href = link_element.get('href')
                if href.startswith('http'):
                    return href
                else:
                    return 'https://www.toutiao.com' + href

        except Exception as e:
            print(f"获取详情页链接失败 {url}: {e}")

        return url

    def get_hot_detail(self, url: str) -> Dict:
        """获取热榜详情"""
        detail_info = {
            'title': '',
            'create_at': '',
            'media_name': '',
            'read_count': '',
            'comment_count': '',
            'like_count': '',
            'content': ''
        }

        try:
            response = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 提取标题
            title = self.safe_find(soup, 'div.article-content h1')
            if not title:
                title = self.safe_find(soup, 'h1[class*="title"]')

            # 提取发布时间
            create_at = self.safe_find(soup, 'div.article-meta span')

            # 提取媒体名称
            media_name = self.safe_find(soup, 'span.name a')
            if not media_name:
                media_name = self.safe_find(soup, 'a[class*="media"]')

            # 提取点赞数
            like_count = self.safe_find(soup, 'div.detail-like span')

            # 提取内容
            content_element = soup.find('article', class_='syl-article-base')
            if not content_element:
                content_element = soup.find('div', class_='article-content')

            content = ''
            if content_element:
                content = content_element.get_text(strip=True, separator='\n')

            detail_info.update({
                'title': title,
                'create_at': create_at,
                'media_name': media_name,
                'like_count': like_count,
                'content': content
            })

        except Exception as e:
            print(f"获取热榜详情失败 {url}: {e}")

        return detail_info

    def get_detail_content(self, url: str) -> str:
        """获取文章详情内容"""
        content = ''
        try:
            response = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            content_element = soup.find('article', class_='syl-article-base')

            if content_element:
                content = content_element.get_text(strip=True, separator='\n')
            else:
                # 尝试其他选择器
                content_element = soup.find('div', class_='article-content')
                if content_element:
                    content = content_element.get_text(strip=True, separator='\n')

        except Exception as e:
            print(f"获取详情内容失败 {url}: {e}")

        return content

    def get_comments(self, group_id: str, max_comments: int = 20) -> List[Dict]:
        """获取评论"""
        all_comments = []

        if not group_id:
            return all_comments

        try:
            url = "https://www.toutiao.com/article/v4/tab_comments/"
            params = {
                "aid": "24",
                "app_name": "toutiao_web",
                "offset": "0",
                "count": str(max_comments),
                "group_id": group_id,
                "item_id": group_id,
            }

            response = requests.get(url, headers=self.headers, cookies=self.cookies,
                                    params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            results = self.safe_get(data, ['data'], [])

            for comment_data in results:
                try:
                    comment = self.safe_get(comment_data, ['comment'], {})

                    create_time = self.safe_get(comment, ['create_time'])
                    if create_time:
                        comment_create_time = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        comment_create_time = ''

                    all_comments.append({
                        'comment_create_time': comment_create_time,
                        'comment_publish_loc_info': self.safe_get(comment, ['publish_loc_info']),
                        'comment_text': self.safe_get(comment, ['text']),
                        'comment_user_name': self.safe_get(comment, ['user_name'])
                    })

                except Exception as e:
                    print(f"解析评论失败: {e}")
                    continue

        except Exception as e:
            print(f"获取评论失败 {group_id}: {e}")

        return all_comments

    def combine_data(self, post_info: Dict, comments: List[Dict]) -> List[Dict]:
        """组合数据，每条评论作为一行"""
        combined_rows = []

        # 如果没有评论，至少创建一行包含帖子信息
        if not comments:
            row = post_info.copy()
            row.update({
                '评论时间': '',
                '评论IP': '',
                '评论内容': '',
                '评论者': ''
            })
            combined_rows.append(row)
        else:
            for comment in comments:
                row = post_info.copy()
                row.update({
                    '评论时间': comment.get('comment_create_time', ''),
                    '评论IP': comment.get('comment_publish_loc_info', ''),
                    '评论内容': comment.get('comment_text', ''),
                    '评论者': comment.get('comment_user_name', '')
                })
                combined_rows.append(row)

        return combined_rows

    def scrape_hot_board(self, max_items: int = 10, max_comments: int = 10) -> bool:
        """爬取热榜数据"""
        print(f"开始爬取今日头条热榜，最多 {max_items} 条...")

        hot_items = self.get_hot_board(max_items)
        if not hot_items:
            print("没有获取到热榜数据")
            return False

        total_processed = 0

        for i, item in enumerate(hot_items, 1):
            try:
                print(f"\n处理第 {i}/{len(hot_items)} 条热榜内容...")

                # 获取详情页链接
                detail_url = self.get_detail_url(item['Url'])
                if not detail_url:
                    print(f"无法获取详情页链接，跳过")
                    continue

                # 获取详情信息
                detail_info = self.get_hot_detail(detail_url)

                # 构建帖子信息
                post_info = {
                    '帖子ID': item['ClusterIdStr'],
                    '帖子标题': detail_info['title'] or item['Title'],
                    '帖子作者': detail_info['media_name'],
                    '帖子创建时间': detail_info['create_at'],
                    '帖子内容': detail_info['content'],
                    '帖子链接': detail_url,
                    '阅读数': detail_info['read_count'],
                    '评论数': detail_info['comment_count'],
                    '点赞数': detail_info['like_count'],
                    '热度值': item['HotValue'],
                    '标签': item['Label'],
                    '来源': '热榜'
                }

                # 获取评论
                comments = self.get_comments(item['ClusterIdStr'], max_comments)

                # 合并数据
                combined_rows = self.combine_data(post_info, comments)
                self.all_data.extend(combined_rows)

                print(f"  标题: {post_info['帖子标题'][:50]}...")
                print(f"  获取到 {len(comments)} 条评论")

                total_processed += 1

                # 避免请求过快
                if i < len(hot_items):
                    time.sleep(1)

            except Exception as e:
                print(f"处理热榜内容失败: {e}")
                continue

        print(f"\n总共处理了 {total_processed} 条热榜内容")
        return total_processed > 0

    def scrape_recommend(self, max_items: int = 10, max_comments: int = 10) -> bool:
        """爬取推荐内容"""
        print(f"开始爬取今日头条推荐内容，最多 {max_items} 条...")

        recommend_items = self.get_recommend_feed(max_items)
        if not recommend_items:
            print("没有获取到推荐内容")
            return False

        total_processed = 0

        for i, item in enumerate(recommend_items, 1):
            try:
                print(f"\n处理第 {i}/{len(recommend_items)} 条推荐内容...")

                # 获取内容详情
                content = self.get_detail_content(item['url'])

                # 构建帖子信息
                post_info = {
                    '帖子ID': item['group_id'],
                    '帖子标题': item['title'],
                    '帖子作者': item['media_name'],
                    '帖子创建时间': item['publish_time'],
                    '帖子内容': content,
                    '帖子链接': item['url'],
                    '阅读数': item['read_count'],
                    '评论数': item['comment_count'],
                    '点赞数': item['like_count'],
                    '热度值': '',
                    '标签': '',
                    '来源': '推荐'
                }

                # 获取评论
                comments = self.get_comments(item['group_id'], max_comments)

                # 合并数据
                combined_rows = self.combine_data(post_info, comments)
                self.all_data.extend(combined_rows)

                print(f"  标题: {post_info['帖子标题'][:50]}...")
                print(f"  获取到 {len(comments)} 条评论")

                total_processed += 1

                # 避免请求过快
                if i < len(recommend_items):
                    time.sleep(1)

            except Exception as e:
                print(f"处理推荐内容失败: {e}")
                continue

        print(f"\n总共处理了 {total_processed} 条推荐内容")
        return total_processed > 0

    def scrape_search(self, keyword: str, max_items: int = 10, max_comments: int = 10) -> bool:
        """搜索内容"""
        print(f"开始搜索今日头条内容，关键词: {keyword}，最多 {max_items} 条...")

        search_items = self.search_content(keyword, max_items)
        if not search_items:
            print("没有搜索结果")
            return False

        total_processed = 0

        for i, item in enumerate(search_items, 1):
            try:
                print(f"\n处理第 {i}/{len(search_items)} 条搜索结果...")

                # 获取内容详情
                content = self.get_detail_content(item['url'])

                # 构建帖子信息
                post_info = {
                    '帖子ID': item['group_id'],
                    '帖子标题': item['title'],
                    '帖子作者': item['media_name'],
                    '帖子创建时间': item['datetime'],
                    '帖子内容': content,
                    '帖子链接': item['url'],
                    '阅读数': item['read_count'],
                    '评论数': item['comment_count'],
                    '点赞数': item['digg_count'],
                    '热度值': '',
                    '标签': '',
                    '来源': '搜索'
                }

                # 获取评论
                comments = self.get_comments(item['group_id'], max_comments)

                # 合并数据
                combined_rows = self.combine_data(post_info, comments)
                self.all_data.extend(combined_rows)

                print(f"  标题: {post_info['帖子标题'][:50]}...")
                print(f"  获取到 {len(comments)} 条评论")

                total_processed += 1

                # 避免请求过快
                if i < len(search_items):
                    time.sleep(1)

            except Exception as e:
                print(f"处理搜索结果失败: {e}")
                continue

        print(f"\n总共处理了 {total_processed} 条搜索结果")
        return total_processed > 0

    def save_to_excel(self, filename: str = "今日头条数据.xlsx", mode: str = 'w'):
        """保存数据到Excel文件"""
        if not self.all_data:
            print("没有数据需要保存")
            return

        # 定义表头顺序
        headers_order = [
            '帖子ID', '帖子标题', '帖子作者', '帖子创建时间', '帖子内容', '帖子链接',
            '阅读数', '评论数', '点赞数', '热度值', '标签', '来源',
            '评论时间', '评论IP', '评论内容', '评论者'
        ]

        # 创建DataFrame
        df_data = []
        for row in self.all_data:
            ordered_row = {}
            for header in headers_order:
                ordered_row[header] = row.get(header, '')
            df_data.append(ordered_row)

        df = pd.DataFrame(df_data, columns=headers_order)

        try:
            if mode == 'a' and os.path.exists(filename):
                # 追加模式
                with pd.ExcelWriter(filename, engine='openpyxl', mode='a',
                                    if_sheet_exists='overlay') as writer:
                    try:
                        existing_df = pd.read_excel(filename, sheet_name='今日头条')
                        combined_df = pd.concat([existing_df, df], ignore_index=True)
                    except:
                        combined_df = df

                    combined_df.to_excel(writer, index=False, sheet_name='今日头条')

                    # 调整列宽
                    worksheet = writer.sheets['今日头条']
                    for idx, col in enumerate(combined_df.columns):
                        column_length = max(
                            combined_df[col].astype(str).map(len).max(),
                            len(col)
                        ) + 2
                        column_width = min(column_length, 50)
                        column_letter = chr(65 + idx) if idx < 26 else chr(64 + idx // 26) + chr(65 + idx % 26)
                        worksheet.column_dimensions[column_letter].width = column_width

                    print(f"已追加数据到: {filename}")

            else:
                # 写入模式（覆盖）
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='今日头条')

                    # 调整列宽
                    worksheet = writer.sheets['今日头条']
                    for idx, col in enumerate(df.columns):
                        column_length = max(
                            df[col].astype(str).map(len).max(),
                            len(col)
                        ) + 2
                        column_width = min(column_length, 50)
                        column_letter = chr(65 + idx) if idx < 26 else chr(64 + idx // 26) + chr(65 + idx % 26)
                        worksheet.column_dimensions[column_letter].width = column_width

                    print(f"已创建新文件: {filename}")

        except Exception as e:
            print(f"保存文件时出错: {e}")
            if mode == 'a':
                print("尝试创建新文件...")
                self.save_to_excel(filename, mode='w')

    def clear_data(self):
        """清空已爬取的数据"""
        self.all_data = []
        print("已清空爬取的数据")

    def run_scraper(self):
        """运行爬虫程序（交互式）"""
        print("=" * 50)
        print("今日头条数据采集程序")
        print("=" * 50)
        print("1. 采集推荐内容")
        print("2. 采集热榜内容")
        print("3. 搜索关键词采集")
        print("=" * 50)

        choice = input("请选择模式 (1/2/3): ").strip()

        if choice == '1':
            # 采集推荐内容
            max_items = int(input("请输入最大采集数量 (默认10): ") or "10")
            max_comments = int(input("请输入每条最大评论数 (默认10): ") or "10")

            print("\n开始采集推荐内容...")
            success = self.scrape_recommend(max_items=max_items, max_comments=max_comments)

        elif choice == '2':
            # 采集热榜内容
            max_items = int(input("请输入最大采集数量 (默认10): ") or "10")
            max_comments = int(input("请输入每条最大评论数 (默认10): ") or "10")

            print("\n开始采集热榜内容...")
            success = self.scrape_hot_board(max_items=max_items, max_comments=max_comments)

        elif choice == '3':
            # 搜索关键词采集
            keyword = input("请输入搜索关键词: ").strip()
            if not keyword:
                print("关键词不能为空")
                return

            max_items = int(input("请输入最大采集数量 (默认10): ") or "10")
            max_comments = int(input("请输入每条最大评论数 (默认10): ") or "10")

            print(f"\n开始搜索关键词: {keyword}")
            success = self.scrape_search(keyword=keyword, max_items=max_items, max_comments=max_comments)

        else:
            print("无效的选择")
            return

        # 保存数据
        if self.all_data:
            output_file = input("请输入输出文件名 (默认: 今日头条数据.xlsx): ").strip()
            if not output_file:
                output_file = "今日头条数据.xlsx"

            mode_choice = input("保存模式: 1.覆盖(w) 2.追加(a) (默认1): ").strip()
            mode = 'a' if mode_choice == '2' else 'w'

            self.save_to_excel(output_file, mode)
            print(f"\n数据已保存到: {output_file}")
            print(f"总数据行数: {len(self.all_data)}")
        else:
            print("没有成功抓取到数据")


def main():
    """主函数"""
    scraper = ToutiaoScraper()

    # 方法1：直接调用
    # 采集推荐内容
    # scraper.scrape_recommend(max_items=5, max_comments=5)

    # 采集热榜内容
    # scraper.scrape_hot_board(max_items=5, max_comments=5)

    # 搜索内容
    # scraper.scrape_search(keyword="科技", max_items=5, max_comments=5)

    # 保存数据
    # scraper.save_to_excel("今日头条.xlsx")

    # 方法2：交互式运行
    scraper.run_scraper()


if __name__ == '__main__':
    main()

#今日头条推荐数据.xlsx
#今日头条热榜数据.xlsx
#今日头条搜索军演数据.xlsx