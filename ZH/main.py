import pandas as pd
import os
import time
from datetime import datetime
from typing import Dict, List, Any, Generator
import requests
from bs4 import BeautifulSoup

# 使用你提供的headers和cookies
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

class ZhihuScraper:
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

    def get_recommend_feed(self, num: int = 1) -> Generator[List[Dict], None, None]:
        """获取知乎推荐内容（生成器版本）

        Args:
            num: 要获取的页数

        Yields:
            每页的推荐内容
        """
        for page_num in range(num):
            print(f"正在获取第 {page_num + 1} 页推荐内容...")

            url = "https://www.zhihu.com/api/v3/feed/topstory/recommend"
            params = {
                "action": "down",
                "ad_interval": "-10",
                "after_id": str(page_num * 10 + 1),
                "desktop": "true",
                "end_offset": str(page_num * 10 + 10),
                "page_number": page_num + 1,
                "session_token": "db7b1af3511b06c17325a8e6116de1cc"
            }

            try:
                response = requests.get(url, headers=self.headers, cookies=self.cookies,
                                        params=params, timeout=15)
                response.raise_for_status()
                data = response.json()

                results = self.safe_get(data, ['data'], [])
                if not results:
                    print(f"第 {page_num + 1} 页没有更多数据")
                    break

                yield results

                # 避免请求过快
                time.sleep(1)

            except Exception as e:
                print(f"获取第 {page_num + 1} 页推荐内容失败: {e}")
                break

    def extract_question_info(self, result: Dict) -> Dict:
        """提取问题/回答信息"""
        try:
            target = self.safe_get(result, ['target'])

            # 获取时间戳并转换
            created_time = self.safe_get(result, ['created_time'])
            if created_time:
                created_at = datetime.fromtimestamp(int(created_time)).strftime('%Y-%m-%d %H:%M:%S')
            else:
                created_at = ''
            question_id = self.safe_get(target, ['question', 'id'])
            answer_id = str(self.safe_get(target, ['id']))
            return {
                '标题': self.safe_get(target, ['question', 'title']),
                '内容': self.change_content(self.safe_get(target, ['content'])),
                '创建时间': created_at,
                '作者姓名': self.safe_get(target, ['author', 'name']),
                '作者头像': self.safe_get(target, ['author', 'avatar_url']),
                '作者签名': self.safe_get(target, ['author', 'headline']),
                '作者类型': self.safe_get(target, ['author', 'user_type']),
                '评论数': self.safe_get(target, ['comment_count']),
                '回答ID': answer_id,
                '内容链接': f'https://www.zhihu.com/question/{question_id}/answer/{answer_id}',
                '赞同数': self.safe_get(target, ['voteup_count'])
            }
        except Exception as e:
            print(f"提取问题信息失败: {e}")
            return {}

    def get_comments(self, answer_id: str, expected_comments_count: int) -> List[Dict]:
        """获取回答评论（根据评论数判断是否需要重试）

        Args:
            answer_id: 回答ID
            expected_comments_count: 预期的评论数（从问题信息中获取）
            limit: 评论数量限制

        Returns:
            评论列表，如果获取失败则返回空列表
        """
        all_comments = []

        # 如果没有评论或者没有回答ID，直接返回空列表
        if not answer_id or answer_id == '' or expected_comments_count <= 0:
            print(f"回答 {answer_id} 没有评论（预期评论数: {expected_comments_count}），跳过获取")
            return all_comments

        print(f"回答 {answer_id} 有 {expected_comments_count} 条评论，开始获取...")

        url = f"https://www.zhihu.com/api/v4/comment_v5/answers/{answer_id}/root_comment"
        params = {
            "order_by": "score",
            "limit": "20",
            "offset": ""
        }

        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                # 重试时增加延迟
                if retry_count > 0:
                    delay = retry_count * 1  # 1, 2, 3秒
                    print(f"第 {retry_count} 次重试，等待 {delay} 秒...")
                    time.sleep(delay)

                print(f"尝试获取评论 (第 {retry_count + 1} 次)...")

                response = requests.get(url, headers=self.headers, cookies=self.cookies,
                                        params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                # 解析评论数据
                comments = data['data']
                # 尝试不同的数据路径
                if 'data' in data:
                    comments_data = data['data']

                    if isinstance(comments_data, dict) and 'data' in comments_data:
                        comments = comments_data['data']
                    elif isinstance(comments_data, list):
                        comments = comments_data
                    elif isinstance(comments_data, dict) and 'comments' in comments_data:
                        comments = comments_data['comments']

                print(f"解析到 {len(comments)} 条评论数据")

                # 处理评论数据
                for comment in comments:
                    # 获取评论内容
                    content = self.safe_get(comment, ['content'])
                    if not content:
                        # 尝试其他可能的字段名
                        content = self.safe_get(comment, ['text'])
                        if not content:
                            print(f"评论数据缺少内容字段: {comment}")
                            continue

                    # 获取评论时间
                    comment_time = self.safe_get(comment, ['created_time'])
                    if comment_time:
                        comment_created_at = datetime.fromtimestamp(int(comment_time)).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        comment_created_at = ''

                    # 获取作者信息
                    comment_author_name = ''
                    author = self.safe_get(comment, ['author'])
                    if author:
                        comment_author_name = self.safe_get(author, ['name'])
                        if not comment_author_name:
                            comment_author_name = self.safe_get(author, ['name'])

                    # 获取点赞数
                    vote_count = self.safe_get(comment, ['like_count'], 0)

                    comment_info = {
                        '评论内容': self.change_content(content),
                        '评论时间': comment_created_at,
                        '评论者姓名': comment_author_name,
                        '评论点赞数': vote_count
                    }
                    all_comments.append(comment_info)

                # 判断是否需要重试
                if len(all_comments) > 0:
                    # 成功获取到评论
                    print(f"成功获取到 {len(all_comments)} 条评论内容")
                    return all_comments
                elif len(comments) > 0:
                    # 有评论数据但解析失败
                    print(f"解析失败：有 {len(comments)} 条评论数据但无法解析内容")
                    retry_count += 1
                else:
                    # 没有评论数据
                    print(f"没有评论数据，响应状态码: {response.status_code}")

                    # 如果预期有评论但获取不到，可能是API问题或数据延迟
                    retry_count += 1

            except requests.exceptions.Timeout:
                print(f"请求超时，准备重试...")
                retry_count += 1
                continue
            except requests.exceptions.RequestException as e:
                print(f"网络请求失败: {e}，准备重试...")
                retry_count += 1
                continue
            except Exception as e:
                print(f"获取评论时发生错误: {e}")
                retry_count += 1
                continue

        # 重试次数用完
        print(f"回答 {answer_id} 获取评论失败，已达到最大重试次数 {max_retries}")
        return all_comments

    def combine_data(self, question_info: Dict, comments: List[Dict]) -> List[Dict]:
        """组合所有数据，每条评论作为一行"""
        combined_rows = []

        # 如果没有评论，至少创建一行包含问题信息
        if not comments:
            row = question_info.copy()
            row.update({
                '评论内容': '',
                '评论时间': '',
                '评论者姓名': '',
                '评论点赞数': ''
            })
            combined_rows.append(row)
        else:
            for comment in comments:
                row = question_info.copy()
                row.update(comment)
                combined_rows.append(row)

        return combined_rows

    def scrape_zhihu(self, pages: int = 1, max_comments: int = 20) -> bool:
        """爬取知乎推荐内容

        Args:
            pages: 要爬取的页数
            max_comments: 每条回答最大评论数
        """
        print(f"开始获取知乎推荐内容，共 {pages} 页...")

        total_items = 0

        # 使用生成器逐页获取数据
        for page_num, items in enumerate(self.get_recommend_feed(pages), 1):
            if not items:
                print(f"第 {page_num} 页没有数据")
                continue

            print(f"第 {page_num} 页找到 {len(items)} 条内容")

            # 处理当前页的每条内容
            for i, item in enumerate(items, 1):
                try:
                    print(f"\n处理第 {page_num} 页第 {i} 条内容...")

                    # 提取问题信息
                    question_info = self.extract_question_info(item)

                    if not question_info:
                        continue

                    # 获取评论数
                    comment_count = question_info.get('评论数', 0)
                    if isinstance(comment_count, str):
                        try:
                            comment_count = int(comment_count)
                        except:
                            comment_count = 0

                    # 获取评论（根据评论数决定是否获取）
                    answer_id = question_info.get('回答ID', '')
                    comments = []

                    if comment_count > 0:
                        print(f"该回答有 {comment_count} 条评论，开始获取...")
                        # 在获取评论前等待，避免请求过快
                        time.sleep(1)

                        # 根据预期的评论数来获取
                        comments = self.get_comments(
                            answer_id=answer_id,
                            expected_comments_count=comment_count,
                        )

                        # 检查获取到的评论数
                        if len(comments) == 0:
                            print(f"⚠️ 警告：该回答显示有 {comment_count} 条评论，但获取到 0 条")
                        else:
                            print(f"✅ 成功获取到 {len(comments)} 条评论")
                    else:
                        print(f"该回答没有评论，跳过获取")

                    # 合并数据
                    combined_rows = self.combine_data(question_info, comments)
                    self.all_data.extend(combined_rows)

                    print(f"  标题: {question_info.get('标题', '')[:50]}...")
                    print(f"  作者: {question_info.get('作者姓名', '')}")
                    print(f"  获取到的评论数: {len(comments)} / 总评论数: {comment_count}")

                    total_items += 1

                    # 处理下一条内容前的延迟
                    if i < len(items):
                        time.sleep(0.5)

                except Exception as e:
                    print(f"处理内容时出错: {e}")
                    continue

            print(f"第 {page_num} 页处理完成")

            # 页与页之间的延迟
            if page_num < pages:
                time.sleep(2)

        print(f"\n总共处理了 {total_items} 条内容")
        print(f"成功获取评论的回答数: {sum(1 for item in self.all_data if item.get('评论内容'))}")
        return total_items > 0

    def save_to_excel(self, filename: str = "知乎数据.xlsx", mode: str = 'w'):
        """保存数据到Excel文件

        Args:
            filename: 文件名
            mode: 'w' - 写入（覆盖）, 'a' - 追加
        """
        if not self.all_data:
            print("没有数据需要保存")
            return

        # 定义表头顺序（只保留你原有的字段）
        headers_order = [
            # 问题信息
            '标题', '内容', '创建时间', '作者姓名', '作者头像', '作者签名',
            '作者类型', '评论数', '回答ID', '内容链接', '赞同数',
            # 评论信息
            '评论内容', '评论时间', '评论者姓名', '评论点赞数'
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
                        existing_df = pd.read_excel(filename, sheet_name='知乎数据')
                        combined_df = pd.concat([existing_df, df], ignore_index=True)
                    except:
                        combined_df = df

                    combined_df.to_excel(writer, index=False, sheet_name='知乎数据')

                    # 调整列宽
                    worksheet = writer.sheets['知乎数据']
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
                    df.to_excel(writer, index=False, sheet_name='知乎数据')

                    # 调整列宽
                    worksheet = writer.sheets['知乎数据']
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

    def search_zhihu_content(self, keyword: str, pages: int = 1) -> Generator[List[Dict], None, None]:
        """搜索知乎内容（生成器版本）

        Args:
            keyword: 搜索关键词
            pages: 要获取的页数（每页20条）

        Yields:
            每页的搜索结果
        """
        for page_num in range(pages):
            print(f"正在搜索关键词 '{keyword}'，第 {page_num + 1} 页...")

            url = "https://www.zhihu.com/api/v4/search_v3"
            params = {
                "gk_version": "gz-gaokao",
                "t": "general",
                "q": keyword,
                "correction": "1",
                "offset": str(page_num * 20),  # 每页20条
                "limit": "20",
                "filter_fields": "",
                "lc_idx": "0",
                "show_all_topics": "0",
                "search_source": "Normal"
            }

            try:
                response = requests.get(url, headers=self.headers, cookies=self.cookies,
                                        params=params, timeout=15)
                response.raise_for_status()
                data = response.json()

                results = self.safe_get(data, ['data'], [])
                if not results:
                    print(f"第 {page_num + 1} 页没有更多搜索结果")
                    break

                yield results

                # 避免请求过快
                time.sleep(1)

            except Exception as e:
                print(f"搜索第 {page_num + 1} 页失败: {e}")
                break

    def extract_search_result_info(self, result: Dict) -> Dict:
        """提取搜索结果信息"""
        try:
            obj = self.safe_get(result, ['object'])
            result_type = self.safe_get(result, ['type'])

            # 只处理search_result类型
            if result_type != 'search_result':
                return {}

            # 获取内容ID和类型
            content_id = str(self.safe_get(obj, ['id']))
            content_type = self.safe_get(obj, ['type'])

            # 构建内容链接
            content_url = ''
            if content_type == 'answer':
                question_id = self.safe_get(obj, ['question', 'id'])
                content_url = f'https://www.zhihu.com/question/{question_id}/answer/{content_id}'
            elif content_type == 'article':
                content_url = f'https://zhuanlan.zhihu.com/p/{content_id}'

            # 获取时间戳并转换
            created_time = self.safe_get(obj, ['created_time'])
            if created_time:
                created_at = datetime.fromtimestamp(int(created_time)).strftime('%Y-%m-%d %H:%M:%S')
            else:
                created_at = ''

            return {
                '标题': self.safe_get(obj, ['title']),
                '内容': self.change_content(self.safe_get(obj, ['content'])),
                '创建时间': created_at,
                '作者姓名': self.safe_get(obj, ['author', 'name']),
                '作者头像': self.safe_get(obj, ['author', 'avatar_url']),
                '作者签名': self.safe_get(obj, ['author', 'headline']),
                '作者类型': self.safe_get(obj, ['author', 'user_type']),
                '评论数': self.safe_get(obj, ['comment_count']),
                '回答ID': content_id,
                '内容类型': content_type,
                '内容链接': content_url,
                '赞同数': self.safe_get(obj, ['voteup_count'])
            }
        except Exception as e:
            print(f"提取搜索结果信息失败: {e}")
            return {}

    def scrape_search(self, keyword: str, pages: int = 1, max_comments: int = 20) -> bool:
        """爬取搜索结果

        Args:
            keyword: 搜索关键词
            pages: 要爬取的页数
            max_comments: 每条回答最大评论数
        """
        print(f"开始搜索知乎内容，关键词: {keyword}，共 {pages} 页...")

        total_items = 0

        # 使用生成器逐页获取搜索结果
        for page_num, items in enumerate(self.search_zhihu_content(keyword, pages), 1):
            if not items:
                print(f"第 {page_num} 页没有搜索结果")
                continue

            print(f"第 {page_num} 页找到 {len(items)} 条搜索结果")

            # 处理当前页的每条结果
            for i, item in enumerate(items, 1):
                try:
                    print(f"\n处理第 {page_num} 页第 {i} 条搜索结果...")

                    # 提取搜索结果信息
                    search_info = self.extract_search_result_info(item)

                    if not search_info:
                        continue

                    # 获取评论数
                    comment_count = search_info.get('评论数', 0)
                    if isinstance(comment_count, str):
                        try:
                            comment_count = int(comment_count)
                        except:
                            comment_count = 0

                    # 获取评论（只获取回答类型的评论，文章可能没有）
                    answer_id = search_info.get('回答ID', '')
                    content_type = search_info.get('内容类型', '')
                    comments = []

                    if comment_count > 0 and content_type == 'answer':
                        print(f"该回答有 {comment_count} 条评论，开始获取...")
                        time.sleep(1)

                        comments = self.get_comments(
                            answer_id=answer_id,
                            expected_comments_count=comment_count,
                        )

                        if len(comments) == 0:
                            print(f"⚠️ 警告：该回答显示有 {comment_count} 条评论，但获取到 0 条")
                        else:
                            print(f"✅ 成功获取到 {len(comments)} 条评论")
                    else:
                        if content_type != 'answer':
                            print(f"内容类型为 {content_type}，跳过获取评论")
                        else:
                            print(f"该回答没有评论，跳过获取")

                    # 合并数据
                    combined_rows = self.combine_data(search_info, comments)
                    self.all_data.extend(combined_rows)

                    print(f"  标题: {search_info.get('标题', '')[:50]}...")
                    print(f"  作者: {search_info.get('作者姓名', '')}")
                    print(f"  类型: {search_info.get('内容类型', '')}")
                    print(f"  获取到的评论数: {len(comments)} / 总评论数: {comment_count}")

                    total_items += 1

                    # 处理下一条内容前的延迟
                    if i < len(items):
                        time.sleep(0.5)

                except Exception as e:
                    print(f"处理搜索结果时出错: {e}")
                    continue

            print(f"第 {page_num} 页处理完成")

            # 页与页之间的延迟
            if page_num < pages:
                time.sleep(2)

        print(f"\n总共处理了 {total_items} 条搜索结果")
        print(f"成功获取评论的回答数: {sum(1 for item in self.all_data if item.get('评论内容'))}")
        return total_items > 0

    def run_scraper(self):
        """运行爬虫程序（交互式）"""
        print("=" * 50)
        print("知乎数据采集程序")
        print("=" * 50)
        print("1. 采集推荐内容")
        print("2. 搜索关键词采集")
        print("=" * 50)

        choice = input("请选择模式 (1 或 2): ").strip()

        if choice == '1':
            # 采集推荐内容
            pages = int(input("请输入要采集的页数 (默认1): ") or "1")
            max_comments = int(input("请输入每条回答最大评论数 (默认10): ") or "10")

            print("\n开始采集推荐内容...")
            success = self.scrape_zhihu(pages=pages, max_comments=max_comments)

        elif choice == '2':
            # 搜索关键词采集
            keyword = input("请输入搜索关键词: ").strip()
            if not keyword:
                print("关键词不能为空")
                return

            pages = int(input("请输入要采集的页数 (默认1): ") or "1")
            max_comments = int(input("请输入每条回答最大评论数 (默认10): ") or "10")

            print(f"\n开始搜索关键词: {keyword}")
            success = self.scrape_search(keyword=keyword, pages=pages, max_comments=max_comments)

        else:
            print("无效的选择")
            return

        # 保存数据
        if self.all_data:
            output_file = input("请输入输出文件名 (默认: 知乎数据.xlsx): ").strip()
            if not output_file:
                output_file = "知乎数据.xlsx"

            mode_choice = input("保存模式: 1.覆盖(w) 2.追加(a) (默认1): ").strip()
            mode = 'a' if mode_choice == '2' else 'w'

            self.save_to_excel(output_file, mode)
            print(f"\n数据已保存到: {output_file}")
            print(f"总数据行数: {len(self.all_data)}")
        else:
            print("没有成功抓取到数据")


def main():
    """主函数"""
    scraper = ZhihuScraper()

    # 运行交互式爬虫
    scraper.run_scraper()


if __name__ == '__main__':
    main()

#美国斩杀线