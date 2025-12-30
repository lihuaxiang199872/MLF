import json
import requests
import re
import pandas as pd
import os
import time
from datetime import datetime
from typing import Dict, List, Any
from bs4 import BeautifulSoup

# 使用你提供的headers和cookies
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en-IE;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
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
    "__snaker__id": "Gckc3E8JvNixsd6a",
    "SESSIONID": "ktXlBk3OFJHa3CqcvErkM0a64gIAORvqrClysR7TT83",
    "JOID": "Wl8WC083sBeoNFKzA0zBiJn5QjMTU8BEyHo2hEd99VvCCx3NZHoKWME3WbwEc2IerqjPpRz5Vj_sX_2SZH64E2g=",
    "osd": "UlATA04_vxKgNVq8BkTAgJb8SjIbXMVMyXI5gU98_VTHAxzFa38CWck4XLQFe20bpqnHqhnxVzfjWvWTbHG9G2k=",
    "_xsrf": "QLIWlrnwhUNK6y7zMw4z5AhmfwWGs8DO",
    "_zap": "ba83ebc2-0b02-49c3-b316-e493c3fef6ab",
    "d_c0": "HOZT1qO16RqPTp2HbVi8mk26q2ovTs6Xc3E=|1755140579",
    "Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49": "1755140581,1756880226",
    "DATE": "1765432136091",
    "crystal": "U2FsdGVkX18xQsH7xtIfqBCMGxLkG765+XH0OnBt9QEDatgOLX5T63QKmvEioBHOcvCNZ0zfCzaDoq27cmhZsOIFg/2n92JqxEey4Z0THpU2H0aMuqnTVYMaXBFNHFRjhP1cRa2292nRJNfIE1Gz5CCS5oSuXrXdAiu2INWFWNu/0BUjgsEsKHk3pkWAmBN+w2DlA7f45oOYlfKQz0URc1YENCfA3pVTDPVMpxHWu9I+cGidegVAJsF7ZCoW+GqD",
    "vmce9xdq": "U2FsdGVkX19PGL1JO3OV06svokZGkIUVHkd6pjtLA0y5Okn6Z34iZj3/IOES0W8Zm1o+0eHKvzKwYyw9u+5LPWmDiHatYGthjRjOvWh7sq/tlEt7sAAIkCa0RiDoagwBZHqzzS0J5UYxh5oKLWnsCw==",
    "captcha_session_v2": "2|1:0|10:1766040148|18:captcha_session_v2|88:MHpsbXZCMC9vZU9TMXdnMkJoRTNtSkhvQ21SYlZBY3ZUTXNXanRGN0pOVC9xWld2WmxxKzZQZjBIeGtlZk0zTQ==|f76f53ecf9d97db95341bf3c754721b4e886738be3504b37c5f0a15e469e92e8",
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
    "__zse_ck": "004_2KdvWiVLWbwgt4TAaFv7lXhozircdoc=/BYqpLC4a2i0I0nrt8svQAM=OL8iP/RGq06eXEsVOB7F7jpllf5HgASaVib3A75NVWjPvGJ09JH7KcyQfCngmriyygMDgAxO-z354fVun8Tp8GlyVoXBXdGmmNUbtfK9YKPzOBgnaDISAxZhB0niArc0OjmLR2xSEHlXsoG8e4WrOOf1L/uGaMaPqbw8dQ038i6c/rtPMrwykX0F33fgIvLx6qw7P5Dqg",
    "BEC": "1eb0fb512bb6053f407f0a7771f545e9"
}


class ZhihuHotScraper:
    def __init__(self):
        self.headers = headers
        self.cookies = cookies
        self.all_data = []
    def change_content(self, html_content):
        """转换HTML内容为纯文本"""
        if not html_content:
            return ""

        if '</p>' in html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            texts = []
            for p in soup.find_all('p'):
                text = p.get_text(strip=True)
                if text:
                    texts.append(text)
            full_text = '\n'.join(texts)
            return full_text
        else:
            return html_content

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

    def timestamp_to_datetime(self, timestamp: Any) -> str:
        """时间戳转换为日期时间字符串"""
        try:
            if not timestamp:
                return ""
            if isinstance(timestamp, str):
                timestamp = int(timestamp)
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError):
            return ""

    def get_hot_list_urls(self) -> List[str]:
        """获取热搜榜问题链接"""
        print("正在获取知乎热搜榜...")

        urls = []
        try:
            url = "https://www.zhihu.com/hot"
            response = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            hot_items = soup.find_all('div', class_='HotItem-content')

            for div in hot_items:
                try:
                    a_tag = div.find('a')
                    if a_tag and a_tag.get('href'):
                        href = a_tag.get('href')
                        # 确保是完整的URL
                        if href.startswith('http'):
                            urls.append(href)
                        else:
                            urls.append(f"https://www.zhihu.com{href}")
                except Exception as e:
                    print(f"解析热搜项目失败: {e}")
                    continue

            print(f"获取到 {len(urls)} 个热搜问题链接")

        except Exception as e:
            print(f"获取热搜榜失败: {e}")

        return urls

    def parse_detail_url(self, text: str) -> Dict:
        """解析页面中的JSON数据"""
        try:
            pattern = r'<script id="js-initialData" type="text/json">(.*?)</script>'
            match = re.search(pattern, text, re.S | re.I)

            if match:
                json_text = match.group(1).strip()
                return json.loads(json_text)
        except Exception as e:
            print(f"解析JSON数据失败: {e}")

        return {}

    def get_question_detail(self, url: str) -> List[Dict]:
        """获取问题详情和回答信息"""
        all_rows = []

        print(f"正在处理问题: {url}")

        try:
            response = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=15)
            response.raise_for_status()

            data = self.parse_detail_url(response.text)
            if not data:
                print(f"无法解析页面数据: {url}")
                return all_rows

            # 获取问题数据
            questions_data = self.safe_get(data, ['initialState', 'entities', 'questions'], {})
            answers_data = self.safe_get(data, ['initialState', 'entities', 'answers'], {})

            # 处理每个问题
            for question_id, question_value in questions_data.items():
                try:
                    # 基础问题信息
                    question_info = {
                        '问题ID': question_id,
                        '问题标题': self.safe_get(question_value, ['title']),
                        '问题创建时间': self.timestamp_to_datetime(self.safe_get(question_value, ['created'])),
                        '问题链接': self.safe_get(question_value, ['url']),
                        '问题详情': self.change_content(self.safe_get(question_value, ['detail'])),
                        '回答数': self.safe_get(question_value, ['answerCount']),
                        '浏览次数': self.safe_get(question_value, ['visitCount']),
                        '问题评论数': self.safe_get(question_value, ['commentCount']),
                        '关注者数': self.safe_get(question_value, ['followerCount']),
                        '问题点赞数': self.safe_get(question_value, ['voteupCount']),
                        '问题作者姓名': self.safe_get(question_value, ['author', 'name']),
                        '问题作者签名': self.safe_get(question_value, ['author', 'headline'])
                    }

                    # 处理该问题的回答
                    for answer_id, answer_value in answers_data.items():
                        try:
                            # 检查是否属于当前问题
                            answer_question_id = self.safe_get(answer_value, ['question', 'id'])
                            if answer_question_id != question_id:
                                continue

                            # 回答信息
                            answer_info = {
                                '回答ID': answer_id,
                                '回答内容': self.change_content(self.safe_get(answer_value, ['content'])),
                                '回答作者姓名': self.safe_get(answer_value, ['author', 'name']),
                                '回答作者签名': self.safe_get(answer_value, ['author', 'headline']),
                                '回答作者粉丝数': self.safe_get(answer_value, ['author', 'followerCount'])
                            }

                            # 合并问题信息和回答信息
                            row = {**question_info, **answer_info}
                            all_rows.append(row)

                        except Exception as e:
                            print(f"处理回答失败 {answer_id}: {e}")
                            continue

                    # 如果没有回答，也保存问题信息
                    if not all_rows:
                        row = question_info.copy()
                        # 添加空的回答字段
                        row.update({
                            '回答ID': '',
                            '回答内容': '',
                            '回答作者姓名': '',
                            '回答作者签名': '',
                            '回答作者粉丝数': ''
                        })
                        all_rows.append(row)

                except Exception as e:
                    print(f"处理问题失败 {question_id}: {e}")
                    continue

        except Exception as e:
            print(f"获取问题详情失败 {url}: {e}")

        return all_rows

    def scrape_hot_list(self, max_urls: int = 10) -> bool:
        """爬取热搜榜数据

        Args:
            max_urls: 最大处理的问题数量
        """
        print(f"开始爬取知乎热搜榜，最多处理 {max_urls} 个问题...")

        # 获取热搜链接
        urls = self.get_hot_list_urls()
        if not urls:
            print("没有获取到热搜链接")
            return False

        # 限制处理数量
        urls = urls[:max_urls]
        total_processed = 0

        for i, url in enumerate(urls, 1):
            try:
                print(f"\n处理第 {i}/{len(urls)} 个热搜问题...")

                # 获取问题详情
                rows = self.get_question_detail(url)
                self.all_data.extend(rows)

                total_processed += 1

                print(f"  获取到 {len(rows)} 条数据")

                # 避免请求过快
                if i < len(urls):
                    time.sleep(1)

            except Exception as e:
                print(f"处理热搜问题失败 {url}: {e}")
                continue

        print(f"\n总共处理了 {total_processed} 个热搜问题")
        print(f"总数据行数: {len(self.all_data)}")
        return total_processed > 0

    def save_to_excel(self, filename: str = "知乎热搜榜.xlsx", mode: str = 'w'):
        """保存数据到Excel文件

        Args:
            filename: 文件名
            mode: 'w' - 写入（覆盖）, 'a' - 追加
        """
        if not self.all_data:
            print("没有数据需要保存")
            return

        # 定义表头顺序（使用你原有的字段）
        headers_order = [
            # 问题信息
            '问题ID', '问题标题', '问题创建时间', '问题链接', '问题详情',
            '回答数', '浏览次数', '问题评论数', '关注者数', '问题点赞数',
            '问题作者姓名', '问题作者签名',
            # 回答信息
            '回答ID', '回答内容', '回答作者姓名', '回答作者签名', '回答作者粉丝数'
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
                        existing_df = pd.read_excel(filename, sheet_name='知乎热搜')
                        combined_df = pd.concat([existing_df, df], ignore_index=True)
                    except:
                        combined_df = df

                    combined_df.to_excel(writer, index=False, sheet_name='知乎热搜')

                    # 调整列宽
                    worksheet = writer.sheets['知乎热搜']
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
                    df.to_excel(writer, index=False, sheet_name='知乎热搜')

                    # 调整列宽
                    worksheet = writer.sheets['知乎热搜']
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


def main():
    """主函数"""
    scraper = ZhihuHotScraper()

    # 配置参数
    max_urls = 5  # 最多处理5个热搜问题（可以先测试少量）

    print("开始爬取知乎热搜榜...")

    # 开始爬取
    success = scraper.scrape_hot_list(max_urls=max_urls)

    if success:
        # 保存数据
        output_file = "知乎热搜榜数据.xlsx"
        scraper.save_to_excel(output_file, mode='w')
        print(f"\n数据已保存到: {output_file}")
        print(f"总数据行数: {len(scraper.all_data)}")
    else:
        print("没有成功抓取到数据")


if __name__ == '__main__':
    main()