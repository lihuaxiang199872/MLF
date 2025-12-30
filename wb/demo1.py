import requests
import pandas as pd
import os
from datetime import datetime
from typing import Dict, List, Any
import time
from bs4 import BeautifulSoup

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en-IE;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "client-version": "v2.47.141",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://weibo.com/",
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
    "_s_tentry": "weibo.com",
    "Apache": "875309026841.9373.1765955882398",
    "SINAGLOBAL": "875309026841.9373.1765955882398",
    "ULV": "1765955882403:1:1:1:875309026841.9373.1765955882398:",
    "ALF": "1769563044",
    "SUB": "_2A25EVab0DeRhGe5N61AX8S_Pwj-IHXVnKqY8rDV8PUJbkNANLUHykW1NdR2Q6mXCQEmHRC16tbJCCLwxaZHvxYll",
    "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9W5y7XsAToXrEOiKeqsJY2wa5JpX5KMhUgL.Fon0ehzceK201Ke2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMRe05ESo2pe0.0",
    "WBPSESS": "3OL9DxHbwY5BHzlwXKMvoJji72lSHTELNL6-Uj8fnGLt-vpKJoFEXiGaS97WJ6pAxWvQnNm0SrgAaZCfkKxKQKY-Eczr3_aWYGrykNU9wfrIXM5680jVIHts7tb0B__2Pit6sABtiUCVapUhLQbUKA=="
}


class WeiboScraper:
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

    def convert_weekday_timezone(self, date_str: str) -> str:
        """
        将 'Wed Dec 17 10:00:26 +0800 2025'
        转换为 '2025-12-17 10:00:26'
        """
        try:
            if not date_str or not isinstance(date_str, str):
                return ""
            dt = datetime.strptime(
                date_str.strip(),
                "%a %b %d %H:%M:%S %z %Y"
            )
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, AttributeError) as e:
            print(f"日期格式转换失败: {date_str}, 错误: {e}")
            return ""

    def get_hot_timeline(self, page: int = 1) -> List[Dict]:
        """获取热门时间线微博"""
        url = "https://weibo.com/ajax/feed/hottimeline"
        for i in range(1, page + 1):
            print(f"正在获取第 {i} 页热门微博...")

            params = {
                "since_id": "0",
                "refresh": "0",
                "group_id": "102803600343",
                "containerid": "102803_ctg1_600343_-_ctg1_600343",
                "extparam": "discover|new_feed",
                "max_id": str(i),  # 使用当前max_id
                "count": "10"
            }

            try:
                response = requests.get(url, headers=self.headers, cookies=self.cookies,
                                        params=params, timeout=15)
                response.raise_for_status()
                data = response.json()

                if 'statuses' not in data or not data['statuses']:
                    print(f"第 {i} 页没有更多微博数据")
                    break

                # 返回当前页的数据
                yield data['statuses']
                # 避免请求过快
                time.sleep(1)

            except requests.exceptions.RequestException as e:
                print(f"获取第 {i} 页热门微博失败: {e}")
                break
            except Exception as e:
                print(f"处理第 {i} 页数据时出错: {e}")
                break

    def search_weibo(self, keyword: str, page: int = 1) -> List[Dict]:
        """搜索微博"""
        url = "https://s.weibo.com/weibo"
        params = {
            "q": keyword,
            "page": page
        }

        try:
            # 搜索页面需要不同的headers
            search_headers = {
                "User-Agent": self.headers["user-agent"],
                "Referer": "https://s.weibo.com/",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9"
            }

            response = requests.get(url, headers=search_headers, cookies=self.cookies,
                                    params=params, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 解析搜索结果
            weibo_items = []
            card_wraps = soup.find_all('div', class_='card-wrap')

            for card in card_wraps:
                try:
                    # 获取微博ID
                    mid = card.get('mid', '').strip()
                    if not mid:
                        continue

                    # 获取发布时间和链接
                    from_div = card.find('div', class_='from')
                    if from_div:
                        time_link = from_div.find('a')
                        if time_link:
                            created_at = time_link.text.strip()
                            link = time_link.get('href', '').strip()
                            # 从链接中提取用户ID
                            if link:
                                parts = link.split('/')
                                if len(parts) > 3:
                                    user_id = parts[3].strip()
                                else:
                                    user_id = ''
                            else:
                                user_id = ''
                        else:
                            created_at = ''
                            link = ''
                            user_id = ''
                    else:
                        created_at = ''
                        link = ''
                        user_id = ''

                    # 获取互动数据
                    like_span = card.find('span', class_='woo-like-count')
                    attitudes_count = like_span.text.strip() if like_span else '0'

                    # 获取评论数
                    comment_a = card.find('a', {'action-type': 'feed_list_comment'})
                    comments_count = comment_a.text.strip() if comment_a else '0'

                    # 获取转发数
                    forward_a = card.find('a', {'action-type': 'feed_list_forward'})
                    reposts_count = forward_a.text.strip() if forward_a else '0'

                    # 获取微博内容
                    content_p = card.find('p', {'node-type': 'feed_list_content'})
                    text_raw = content_p.text.strip() if content_p else ''

                    # 获取用户名
                    name_div = card.find('div', class_='info')
                    if name_div:
                        name_a = name_div.find('a', {'nick-name': True})
                        screen_name = name_a.text.strip() if name_a else ''
                    else:
                        screen_name = ''

                    # 清理互动数据中的非数字字符
                    def clean_number(text):
                        import re
                        numbers = re.findall(r'\d+', text)
                        return numbers[0] if numbers else '0'

                    attitudes_count = clean_number(attitudes_count)
                    comments_count = clean_number(comments_count)
                    reposts_count = clean_number(reposts_count)

                    # 构建微博数据
                    weibo_item = {
                        'id': mid,
                        'text_raw': text_raw,
                        'created_at': created_at,
                        'attitudes_count': int(attitudes_count) if attitudes_count.isdigit() else 0,
                        'comments_count': int(comments_count) if comments_count.isdigit() else 0,
                        'reposts_count': int(reposts_count) if reposts_count.isdigit() else 0,
                        'user': {
                            'id': user_id,
                            'screen_name': screen_name
                        },
                        'link': f"https://weibo.com{link}" if link.startswith('/') else link
                    }

                    weibo_items.append(weibo_item)

                except Exception as e:
                    print(f"解析搜索结果条目失败: {e}")
                    continue

            print(f"搜索到 {len(weibo_items)} 条微博")
            return weibo_items

        except requests.exceptions.RequestException as e:
            print(f"搜索微博失败: {e}")
            return []
        except Exception as e:
            print(f"解析搜索结果失败: {e}")
            return []

    def get_weibo_detail(self, item: Dict) -> Dict:
        """提取微博详情信息"""
        weibo_info = {
            '微博ID': '',
            '微博内容': '',
            '发布时间': '',
            '点赞数': '',
            '评论数': '',
            '转发数': '',
            '阅读数': '',
            '微博链接': '',
            '是否原创': '',
            '来源': '',
            '话题': '',
            '图片数': '',
            '视频数': ''
        }

        try:
            # 如果是搜索结果的item，字段结构不同
            if 'link' in item:  # 搜索结果的item
                weibo_info.update({
                    '微博ID': str(self.safe_get(item, ['id'])),
                    '微博内容': self.safe_get(item, ['text_raw']),
                    '发布时间': self.safe_get(item, ['created_at']),
                    '点赞数': self.safe_get(item, ['attitudes_count']),
                    '评论数': self.safe_get(item, ['comments_count']),
                    '转发数': self.safe_get(item, ['reposts_count']),
                    '微博链接': self.safe_get(item, ['link']),
                    '是否原创': '未知',
                    '来源': '搜索',
                    '话题': ''
                })
            else:  # 热门时间线的item
                weibo_info.update({
                    '微博ID': str(self.safe_get(item, ['id'])),
                    '微博内容': self.safe_get(item, ['text_raw']),
                    '发布时间': self.convert_weekday_timezone(self.safe_get(item, ['created_at'])),
                    '点赞数': self.safe_get(item, ['attitudes_count']),
                    '评论数': self.safe_get(item, ['comments_count']),
                    '转发数': self.safe_get(item, ['reposts_count']),
                    '阅读数': self.safe_get(item, ['reads_count']),
                    '微博链接': f"https://weibo.com/{self.safe_get(item, ['user', 'id'])}/{self.safe_get(item, ['mblogid'])}",
                    '是否原创': '是' if not self.safe_get(item, ['retweeted_status']) else '否',
                    '来源': self.safe_get(item, ['source']),
                    '话题': ','.join(
                        [f"#{topic['topic_title']}#" for topic in self.safe_get(item, ['topic_struct'], [])]),
                    '图片数': len(self.safe_get(item, ['pic_ids'], [])),
                    '视频数': 1 if self.safe_get(item, ['page_info', 'type']) == 'video' else 0
                })

        except Exception as e:
            print(f"提取微博详情失败: {e}")

        return weibo_info

    def get_user_info(self, user_id: str) -> Dict:
        """获取用户信息"""
        user_info = {
            '用户ID': '',
            '用户名': '',
            '用户昵称': '',
            '个人简介': '',
            '粉丝数': '',
            '关注数': '',
            '微博数': '',
            '总评论数': '',
            '总点赞数': '',
            '总转发数': '',
            '总转赞数': '',
            '认证信息': '',
            '认证类型': '',
            '注册时间': '',
            '性别': '',
            '所在地': ''
        }

        if not user_id or user_id == '':
            return user_info

        url = "https://weibo.com/ajax/profile/info"
        params = {"uid": user_id}

        try:
            response = requests.get(url, headers=self.headers, cookies=self.cookies,
                                    params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            results = self.safe_get(data, ['data', 'user'], {})

            user_info.update({
                '用户ID': str(user_id),
                '用户名': self.safe_get(results, ['screen_name']),
                '用户昵称': self.safe_get(results, ['name']),
                '个人简介': self.safe_get(results, ['description']),
                '粉丝数': self.safe_get(results, ['followers_count']),
                '关注数': self.safe_get(results, ['friends_count']),
                '微博数': self.safe_get(results, ['statuses_count']),
                '总评论数': self.safe_get(results, ['status_total_counter', 'comment_cnt']),
                '总点赞数': self.safe_get(results, ['status_total_counter', 'like_cnt']),
                '总转发数': self.safe_get(results, ['status_total_counter', 'repost_cnt']),
                '总转赞数': self.safe_get(results, ['status_total_counter', 'total_cnt_format']),
                '认证信息': self.safe_get(results, ['verified_reason']),
                '认证类型': self.safe_get(results, ['verified_type']),
                '注册时间': self.convert_weekday_timezone(self.safe_get(results, ['created_at'])),
                '性别': self.safe_get(results, ['gender']),
                '所在地': self.safe_get(results, ['location'])
            })

            # 性别转换
            gender_map = {'m': '男', 'f': '女'}
            user_info['性别'] = gender_map.get(user_info['性别'], user_info['性别'])

            # 认证类型转换
            verified_type_map = {
                0: '个人认证',
                1: '政府认证',
                2: '企业认证',
                3: '媒体认证',
                5: '网站认证',
                7: '机构认证'
            }
            verified_type = user_info['认证类型']
            if isinstance(verified_type, int):
                user_info['认证类型'] = verified_type_map.get(verified_type, str(verified_type))

        except Exception as e:
            print(f"获取用户信息失败 {user_id}: {e}")

        return user_info

    def get_comments(self, weibo_id: str, user_id: str, count: int = 10) -> List[Dict]:
        """获取微博评论"""
        all_comments = []

        if not weibo_id or weibo_id == '':
            return all_comments

        url = "https://weibo.com/ajax/statuses/buildComments"
        params = {
            "flow": "0",
            "is_reload": "1",
            "id": weibo_id,
            "is_show_bulletin": "2",
            "is_mix": "0",
            "count": str(count),
            "uid": user_id if user_id and user_id != '' else weibo_id,
            "fetch_level": "0",
            "locale": "zh-CN"
        }

        try:
            response = requests.get(url, headers=self.headers, cookies=self.cookies,
                                    params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            comments = self.safe_get(data, ['data'], [])

            for comment in comments:
                comment_info = {
                    '评论ID': str(self.safe_get(comment, ['id'])),
                    '评论内容': self.safe_get(comment, ['text']),
                    '评论时间': self.convert_weekday_timezone(self.safe_get(comment, ['created_at'])),
                    '评论点赞数': self.safe_get(comment, ['like_counts']),
                    '评论用户ID': str(self.safe_get(comment, ['user', 'id'])),
                    '评论用户名': self.safe_get(comment, ['user', ['screen_name']]),
                    '评论用户昵称': self.safe_get(comment, ['user', 'name']),
                    '评论用户位置': self.safe_get(comment, ['user', 'location']),
                    '是否VIP': '是' if self.safe_get(comment, ['user', 'vip']) else '否',
                    '评论来源': self.safe_get(comment, ['source']),
                    '回复数': self.safe_get(comment, ['total_number'])
                }
                all_comments.append(comment_info)

        except Exception as e:
            print(f"获取评论失败 {weibo_id}: {e}")

        return all_comments

    def combine_data(self, weibo_info: Dict, user_info: Dict, comments: List[Dict]) -> List[Dict]:
        """组合所有数据，每条评论作为一行"""
        combined_rows = []

        # 如果没有评论，至少创建一行包含微博和用户信息
        if not comments:
            row = {}
            row.update(weibo_info)
            row.update(user_info)
            row.update({
                '评论ID': '',
                '评论内容': '',
                '评论时间': '',
                '评论点赞数': '',
                '评论用户ID': '',
                '评论用户名': '',
                '评论用户昵称': '',
                '评论用户位置': '',
                '是否VIP': '',
                '评论来源': '',
                '回复数': ''
            })
            combined_rows.append(row)
        else:
            for comment in comments:
                row = {}
                # 微博详情信息
                row.update(weibo_info)
                # 发帖用户信息
                row.update(user_info)
                # 评论信息
                row.update(comment)
                combined_rows.append(row)

        return combined_rows

    def scrape_hot(self, pages: int = 1, max_comments: int = 10) -> bool:
        """爬取热门微博（支持分页）

        Args:
            pages: 要爬取的页数
            max_comments: 每条微博最大评论数
        """
        print(f"开始获取微博热门时间线，共 {pages} 页...")

        total_weibos = 0

        # 使用生成器逐页获取数据
        for page_num, statuses in enumerate(self.get_hot_timeline(pages), 1):
            if not statuses:
                print(f"第 {page_num} 页没有数据")
                continue

            print(f"第 {page_num} 页找到 {len(statuses)} 条微博")

            # 处理当前页的每条微博
            for i, item in enumerate(statuses, 1):
                try:
                    print(f"\n处理第 {page_num} 页第 {i} 条热门微博...")

                    weibo_id = str(self.safe_get(item, ['id']))
                    user_id = str(self.safe_get(item, ['user', 'id']))

                    if not weibo_id or not user_id:
                        print(f"跳过微博，缺少ID信息")
                        continue

                    # 获取各种信息
                    weibo_info = self.get_weibo_detail(item)
                    user_info = self.get_user_info(user_id)
                    comments = self.get_comments(weibo_id, user_id, max_comments)

                    # 合并数据
                    combined_rows = self.combine_data(weibo_info, user_info, comments)
                    self.all_data.extend(combined_rows)

                    print(f"  微博ID: {weibo_id}")
                    print(f"  内容: {weibo_info.get('微博内容', '')[:50]}...")
                    print(f"  用户: {user_info.get('用户昵称', '')}")
                    print(f"  评论数: {len(comments)}")

                    total_weibos += 1

                    # 避免请求过快
                    time.sleep(0.5)

                except Exception as e:
                    print(f"处理热门微博时出错: {e}")
                    continue

            print(f"第 {page_num} 页处理完成")

        print(f"\n总共处理了 {total_weibos} 条微博")
        return total_weibos > 0

    def scrape_search(self, keyword: str, page: int = 1, max_comments: int = 10) -> bool:
        """爬取搜索结果微博"""
        print(f"开始搜索关键词: {keyword}")

        # 搜索微博
        search_items = self.search_weibo(keyword, page)
        if not search_items:
            print("未获取到搜索结果")
            return False

        print(f"找到 {len(search_items)} 条搜索结果")

        # 处理每条微博
        for i, item in enumerate(search_items):
            try:
                print(f"\n处理第 {i + 1} 条搜索结果...")

                weibo_id = str(self.safe_get(item, ['id']))
                user_id = str(self.safe_get(item, ['user', 'id']))

                if not weibo_id:
                    print(f"跳过微博，缺少ID信息")
                    continue

                # 获取各种信息
                weibo_info = self.get_weibo_detail(item)
                user_info = self.get_user_info(user_id)
                comments = self.get_comments(weibo_id, user_id, max_comments)

                # 合并数据
                combined_rows = self.combine_data(weibo_info, user_info, comments)
                self.all_data.extend(combined_rows)

                print(f"  微博ID: {weibo_id}")
                print(f"  内容: {weibo_info.get('微博内容', '')[:50]}...")
                print(f"  用户: {user_info.get('用户昵称', '')}")
                print(f"  评论数: {len(comments)}")

                # 避免请求过快
                time.sleep(1)

            except Exception as e:
                print(f"处理搜索结果时出错: {e}")
                continue

        return True

    def save_to_excel(self, filename: str, mode: str = 'w'):
        """保存数据到Excel文件

        Args:
            filename: 文件名
            mode: 'w' - 写入（覆盖）, 'a' - 追加
        """
        if not self.all_data:
            print("没有数据需要保存")
            return

        # 定义表头顺序（中文）
        headers_order = [
            # 微博信息
            '微博ID', '微博内容', '发布时间', '点赞数', '评论数', '转发数',
            '阅读数', '微博链接', '是否原创', '来源', '话题', '图片数', '视频数',
            # 用户信息
            '用户ID', '用户名', '用户昵称', '个人简介', '粉丝数', '关注数', '微博数',
            '总评论数', '总点赞数', '总转发数', '总转赞数', '认证信息', '认证类型',
            '注册时间', '性别', '所在地',
            # 评论信息
            '评论ID', '评论内容', '评论时间', '评论点赞数', '评论用户ID', '评论用户名',
            '评论用户昵称', '评论用户位置', '是否VIP', '评论来源', '回复数'
        ]

        # 确保所有行都有相同的列
        df_data = []
        for row in self.all_data:
            ordered_row = {}
            for header in headers_order:
                ordered_row[header] = row.get(header, '')
            df_data.append(ordered_row)

        df = pd.DataFrame(df_data, columns=headers_order)

        try:
            if mode == 'a' and os.path.exists(filename):
                # 追加模式：读取现有文件，追加新数据
                with pd.ExcelWriter(filename, engine='openpyxl', mode='a',
                                    if_sheet_exists='overlay') as writer:
                    # 尝试读取现有sheet
                    try:
                        existing_df = pd.read_excel(filename, sheet_name='微博数据')
                        combined_df = pd.concat([existing_df, df], ignore_index=True)
                    except:
                        # 如果sheet不存在，直接写入
                        combined_df = df

                    combined_df.to_excel(writer, index=False, sheet_name='微博数据')

                    # 调整列宽
                    worksheet = writer.sheets['微博数据']
                    for idx, col in enumerate(combined_df.columns):
                        column_length = max(
                            combined_df[col].astype(str).map(len).max(),
                            len(col)
                        ) + 2
                        column_width = min(column_length, 50)
                        column_letter = chr(65 + idx) if idx < 26 else chr(64 + idx // 26) + chr(65 + idx % 26)
                        worksheet.column_dimensions[column_letter].width = column_width

                    print(f"已追加数据到现有文件: {filename}")

            else:
                # 写入模式（覆盖）
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='微博数据')

                    # 调整列宽
                    worksheet = writer.sheets['微博数据']
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
            # 如果追加失败，尝试创建新文件
            if mode == 'a':
                print("尝试创建新文件...")
                self.save_to_excel(filename, mode='w')

    def clear_data(self):
        """清空已爬取的数据"""
        self.all_data = []
        print("已清空爬取的数据")


def main():
    """主函数"""
    scraper = WeiboScraper()

    print("微博爬虫程序")
    print("=" * 50)
    print("1. 爬取热门微博")
    print("2. 搜索关键词爬取")
    print("=" * 50)

    choice = input("请选择模式 (1 或 2): ").strip()

    if choice == '1':
        # 爬取热门微博
        weibo_page = int(input("请输入要爬取的微博页数 (默认1): ") or "1")
        comment_count = int(input("请输入每条微博获取的评论数 (默认5): ") or "5")

        scraper.scrape_hot(
            pages=weibo_page,
            max_comments=comment_count
        )

    elif choice == '2':
        # 搜索关键词爬取
        keyword = '美国斩杀线'
        if not keyword:
            print("关键词不能为空")
            return

        page = int(input("请输入搜索页数 (默认1): ") or "1")
        comment_count = int(input("请输入每条微博获取的评论数 (默认5): ") or "5")

        scraper.scrape_search(
            keyword=keyword,
            page=page,
            max_comments=comment_count
        )

    else:
        print("无效的选择")
        return

    # 保存数据
    if scraper.all_data:
        output_file = input("请输入输出文件名 (默认: 微博数据.xlsx): ").strip()
        if not output_file:
            output_file = "微博数据.xlsx"

        mode_choice = input("保存模式: 1.覆盖(w) 2.追加(a) (默认1): ").strip()
        mode = 'a' if mode_choice == '2' else 'w'

        scraper.save_to_excel(output_file, mode)
        print(f"\n数据已保存到: {output_file}")
        print(f"总数据行数: {len(scraper.all_data)}")
    else:
        print("没有成功抓取到数据")


if __name__ == '__main__':
    main()


# 美国斩杀线