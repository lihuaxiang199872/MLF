import json
import requests
import pandas as pd
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import time

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
    # 需要定期更新cookie
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

    def get_hot_timeline(self, count: int = 10) -> List[Dict]:
        """获取热门时间线微博"""
        url = "https://weibo.com/ajax/feed/hottimeline"
        params = {
            "since_id": "0",
            "refresh": "0",
            "group_id": "102803600343",
            "containerid": "102803_ctg1_600343_-_ctg1_600343",
            "extparam": "discover|new_feed",
            "max_id": "0",
            "count": str(count)
        }

        try:
            response = requests.get(url, headers=self.headers, cookies=self.cookies,
                                    params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            if 'statuses' in data:
                return data['statuses'][:count]
            else:
                print("未找到微博数据")
                return []

        except requests.exceptions.RequestException as e:
            print(f"获取热门时间线失败: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
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
                '话题': ','.join([f"#{topic['topic_title']}#" for topic in self.safe_get(item, ['topic_struct'], [])]),
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
                '0': '个人认证',
                '1': '政府认证',
                '2': '企业认证',
                '3': '媒体认证',
                '4': '校园认证',
                '5': '网站认证',
                '6': '应用认证',
                '7': '机构认证'
            }
            verified_type = str(user_info['认证类型'])
            user_info['认证类型'] = verified_type_map.get(verified_type, verified_type)

        except Exception as e:
            print(f"获取用户信息失败 {user_id}: {e}")

        return user_info

    def get_comments(self, weibo_id: str, user_id: str, count: int = 10) -> List[Dict]:
        """获取微博评论"""
        all_comments = []
        url = "https://weibo.com/ajax/statuses/buildComments"
        params = {
            "flow": "0",
            "is_reload": "1",
            "id": weibo_id,
            "is_show_bulletin": "2",
            "is_mix": "0",
            "count": str(count),
            "uid": user_id,
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
                    '评论用户名': self.safe_get(comment, ['user', 'screen_name']),
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

    def scrape_and_save(self, count: int = 10, max_comments: int = 10,
                        output_file: str = "微博数据.xlsx", mode: str = 'w'):
        """主函数：爬取数据并保存到Excel

        Args:
            count: 获取微博数量
            max_comments: 每条微博最大评论数
            output_file: 输出文件名
            mode: 'w' - 写入（覆盖）, 'a' - 追加
        """
        print(f"开始获取微博热门时间线...")

        # 获取热门微博
        statuses = self.get_hot_timeline(count)
        if not statuses:
            print("未获取到微博数据")
            return

        print(f"找到 {len(statuses)} 条微博")

        # 处理每条微博
        for i, item in enumerate(statuses):
            try:
                print(f"\n处理第 {i + 1} 条微博...")

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

                # 避免请求过快
                time.sleep(1)

            except Exception as e:
                print(f"处理微博时出错: {e}")
                continue

        # 保存到Excel
        if self.all_data:
            self.save_to_excel(output_file, mode)
            print(f"\n数据已保存到: {output_file}")
            print(f"总数据行数: {len(self.all_data)}")
        else:
            print("没有成功抓取到数据")

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


def main():
    """主函数"""
    scraper = WeiboScraper()

    # 配置参数
    weibo_count = 10  # 获取微博数量（建议先测试少量）
    comment_count = 10  # 每条微博获取评论数
    output_file = "微博数据_2025_12_29.xlsx"  # 输出文件名
    mode = 'w'  # 'w' - 写入（覆盖）, 'a' - 追加

    # 开始爬取
    scraper.scrape_and_save(
        count=weibo_count,
        max_comments=comment_count,
        output_file=output_file,
        mode=mode
    )


if __name__ == '__main__':
    main()