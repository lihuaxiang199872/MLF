import requests
import pandas as pd
import os
import time
from typing import Dict, List, Any
from bs4 import BeautifulSoup

# 使用你提供的headers和cookies
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


class NeteaseNewsScraper:
    def __init__(self):
        self.headers = headers
        self.cookies = cookies
        self.all_data = []
        self.start_url_list = [
            'https://news.163.com/domestic/',
            'https://news.163.com/world/',
            'https://war.163.com/',
            'https://news.163.com/air/'
        ]

    def safe_get(self, soup, selector: str, attribute: str = None, default: Any = ""):
        """安全获取BeautifulSoup元素"""
        try:
            element = soup.select_one(selector)
            if element:
                if attribute:
                    return element.get(attribute, default)
                else:
                    return element.get_text(strip=True)
            return default
        except Exception:
            return default

    def safe_find(self, soup, tag: str, class_: str = None, attribute: str = None, default: Any = ""):
        """安全查找BeautifulSoup元素"""
        try:
            if class_:
                element = soup.find(tag, class_=class_)
            else:
                element = soup.find(tag)

            if element:
                if attribute:
                    return element.get(attribute, default)
                else:
                    return element.get_text(strip=True)
            return default
        except Exception:
            return default

    def get_column_news_urls(self, url: str) -> List[str]:
        """获取栏目新闻链接"""
        urls = []
        try:
            print(f"正在获取栏目链接: {url}")
            response = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            url_content = soup.find('div', class_='hidden')

            if url_content:
                links = url_content.find_all('a')
                for a in links:
                    href = a.get('href', '').strip()
                    if href and 'video' not in href:
                        urls.append(href)

            print(f"从 {url} 获取到 {len(urls)} 条新闻链接")

        except Exception as e:
            print(f"获取栏目链接失败 {url}: {e}")

        return urls

    def get_search_results(self, keyword: str) -> List[str]:
        """搜索新闻"""
        urls = []
        try:
            print(f"正在搜索关键词: {keyword}")
            url = "https://www.163.com/search"
            params = {"keyword": keyword}

            response = requests.get(url, headers=self.headers, cookies=self.cookies, params=params, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            keyword_divs = soup.find_all('div', class_='keyword_img')

            for div in keyword_divs:
                a_tag = div.find('a')
                if a_tag:
                    href = a_tag.get('href', '').strip()
                    if href and 'video' not in href:
                        urls.append(href)

            print(f"搜索到 {len(urls)} 条新闻链接")

        except Exception as e:
            print(f"搜索失败: {e}")

        return urls

    def get_news_detail(self, url: str) -> Dict:
        """获取新闻详情"""
        news_info = {
            '新闻链接': url,
            '新闻标题': '',
            '发布时间': '',
            '新闻内容': '',
            '图片链接': '',
            '来源': '',
            '栏目': '',
            '新闻ID': ''
        }

        try:
            print(f"正在获取新闻详情: {url}")
            response = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 获取新闻标题
            title = self.safe_find(soup, 'h1', 'post_title')
            if not title:
                title = self.safe_get(soup, 'h1[class*="title"]')

            # 获取发布时间和来源
            post_info = self.safe_find(soup, 'div', 'post_info')
            create_at = ''
            source = ''

            if post_info:
                if '来源' in post_info:
                    parts = post_info.split('来源')
                    create_at = parts[0].strip()
                    if len(parts) > 1:
                        source = parts[1].strip()
                else:
                    create_at = post_info.strip()

            # 获取新闻内容
            content_div = soup.find('div', class_='post_body')
            if not content_div:
                content_div = soup.find('div', {'id': 'content'})

            text = ''
            images = []

            if content_div:
                # 提取文本内容
                paragraphs = content_div.find_all('p')
                text_parts = []
                for p in paragraphs:
                    p_text = p.get_text(strip=True)
                    if p_text and not p_text.startswith('点击进入专题：'):
                        text_parts.append(p_text)
                text = '\n'.join(text_parts)

                # 提取图片链接
                img_tags = content_div.find_all('img')
                images = [img.get('src', '').strip() for img in img_tags if img.get('src')]

            # 提取新闻ID（从URL中）
            import re
            news_id_match = re.search(r'article/([A-Z0-9]+)', url)
            news_id = news_id_match.group(1) if news_id_match else ''

            # 判断栏目
            column = ''
            if 'domestic' in url:
                column = '国内'
            elif 'world' in url:
                column = '国际'
            elif 'war' in url:
                column = '军事'
            elif 'air' in url:
                column = '航空'

            news_info.update({
                '新闻标题': title,
                '发布时间': create_at,
                '新闻内容': text,
                '图片链接': ','.join(images) if images else '',
                '来源': source,
                '栏目': column,
                '新闻ID': news_id
            })

            print(f"  标题: {title[:50]}...")

        except Exception as e:
            print(f"获取新闻详情失败 {url}: {e}")

        return news_info

    def scrape_columns(self, max_news_per_column: int = 10) -> bool:
        """爬取栏目新闻

        Args:
            max_news_per_column: 每个栏目最多爬取的新闻数量
        """
        print(f"开始爬取网易新闻栏目，每个栏目最多 {max_news_per_column} 条新闻...")

        total_processed = 0

        for column_url in self.start_url_list:
            try:
                print(f"\n处理栏目: {column_url}")

                # 获取栏目新闻链接
                news_urls = self.get_column_news_urls(column_url)
                if not news_urls:
                    print(f"该栏目没有新闻链接")
                    continue

                # 限制处理数量
                news_urls = news_urls[:max_news_per_column]

                # 处理每条新闻
                for i, url in enumerate(news_urls, 1):
                    try:
                        print(f"  处理第 {i}/{len(news_urls)} 条新闻...")

                        # 获取新闻详情
                        news_info = self.get_news_detail(url)
                        self.all_data.append(news_info)

                        total_processed += 1

                        # 避免请求过快
                        if i < len(news_urls):
                            time.sleep(0.5)

                    except Exception as e:
                        print(f"  处理新闻失败 {url}: {e}")
                        continue

                print(f"栏目 {column_url} 处理完成")

            except Exception as e:
                print(f"处理栏目失败 {column_url}: {e}")
                continue

        print(f"\n总共处理了 {total_processed} 条新闻")
        return total_processed > 0

    def scrape_search(self, keyword: str, max_results: int = 10) -> bool:
        """搜索新闻

        Args:
            keyword: 搜索关键词
            max_results: 最大结果数量
        """
        print(f"开始搜索新闻，关键词: {keyword}，最多 {max_results} 条结果...")

        # 获取搜索结果
        news_urls = self.get_search_results(keyword)
        if not news_urls:
            print("没有找到搜索结果")
            return False

        # 限制处理数量
        news_urls = news_urls[:max_results]
        total_processed = 0

        # 处理每条新闻
        for i, url in enumerate(news_urls, 1):
            try:
                print(f"处理第 {i}/{len(news_urls)} 条搜索结果...")

                # 获取新闻详情
                news_info = self.get_news_detail(url)
                self.all_data.append(news_info)

                total_processed += 1

                # 避免请求过快
                if i < len(news_urls):
                    time.sleep(0.5)

            except Exception as e:
                print(f"处理搜索结果失败 {url}: {e}")
                continue

        print(f"\n总共处理了 {total_processed} 条搜索结果")
        return total_processed > 0

    def save_to_excel(self, filename: str = "网易新闻.xlsx", mode: str = 'w'):
        """保存数据到Excel文件

        Args:
            filename: 文件名
            mode: 'w' - 写入（覆盖）, 'a' - 追加
        """
        if not self.all_data:
            print("没有数据需要保存")
            return

        # 定义表头顺序
        headers_order = [
            '新闻ID', '新闻标题', '发布时间', '新闻内容', '图片链接',
            '来源', '栏目', '新闻链接'
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
                        existing_df = pd.read_excel(filename, sheet_name='网易新闻')
                        combined_df = pd.concat([existing_df, df], ignore_index=True)
                    except:
                        combined_df = df

                    combined_df.to_excel(writer, index=False, sheet_name='网易新闻')

                    # 调整列宽
                    worksheet = writer.sheets['网易新闻']
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
                    df.to_excel(writer, index=False, sheet_name='网易新闻')

                    # 调整列宽
                    worksheet = writer.sheets['网易新闻']
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
        print("网易新闻数据采集程序")
        print("=" * 50)
        print("1. 采集栏目新闻（国内、国际、军事、航空）")
        print("2. 搜索关键词采集")
        print("=" * 50)

        choice = input("请选择模式 (1 或 2): ").strip()

        if choice == '1':
            # 采集栏目新闻
            max_news = int(input("请输入每个栏目最大新闻数 (默认10): ") or "10")

            print("\n开始采集栏目新闻...")
            success = self.scrape_columns(max_news_per_column=max_news)

        elif choice == '2':
            # 搜索关键词采集
            keyword = input("请输入搜索关键词: ").strip()
            if not keyword:
                print("关键词不能为空")
                return

            max_results = int(input("请输入最大结果数 (默认10): ") or "10")

            print(f"\n开始搜索关键词: {keyword}")
            success = self.scrape_search(keyword=keyword, max_results=max_results)

        else:
            print("无效的选择")
            return

        # 保存数据
        if self.all_data:
            output_file = input("请输入输出文件名 (默认: 网易新闻.xlsx): ").strip()
            if not output_file:
                output_file = "网易新闻.xlsx"

            mode_choice = input("保存模式: 1.覆盖(w) 2.追加(a) (默认1): ").strip()
            mode = 'a' if mode_choice == '2' else 'w'

            self.save_to_excel(output_file, mode)
            print(f"\n数据已保存到: {output_file}")
            print(f"总数据行数: {len(self.all_data)}")
        else:
            print("没有成功抓取到数据")


def main():
    """主函数"""
    scraper = NeteaseNewsScraper()

    # 方法1：直接调用
    # 采集栏目新闻
    # success = scraper.scrape_columns(max_news_per_column=5)

    # 或者搜索新闻
    # success = scraper.scrape_search(keyword="AI", max_results=5)

    # 保存数据
    # scraper.save_to_excel("网易新闻.xlsx")

    # 方法2：交互式运行
    scraper.run_scraper()


if __name__ == '__main__':
    main()

# 网易手机数据.xlsx
# 网易美国斩杀线数据.xlsx