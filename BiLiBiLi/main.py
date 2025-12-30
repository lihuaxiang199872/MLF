import time
import requests
import execjs
import pandas as pd
import os
from datetime import datetime
from typing import Dict, List, Any

# 使用你提供的headers和cookies
headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en-IE;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "origin": "https://search.bilibili.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://search.bilibili.com/all?keyword=AI&from_source=webtop_search&spm_id_from=333.1007&search_source=5&page=2&o=24",
    "sec-ch-ua": "\\Google",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\\Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}
cookies = {
    "buvid3": "6BB9C378-14FD-7CDF-A108-51AF288F929303281infoc",
    "b_nut": "1764834803",
    "_uuid": "AFA85643-2DFE-7CE7-3F2F-10783E5F87F6104142infoc",
    "CURRENT_QUALITY": "0",
    "buvid_fp": "e3376fa998e60cc87e3f5babb528a77c",
    "buvid4": "A9DCEDDA-E589-07EF-3B43-7BFC3294000904656-025120415-XDvCUQzBHeE0HE8/h43Ztg%3D%3D",
    "rpdid": "|(J|)YYJ~lJ~0J'u~YR)JR)|l",
    "bsource": "search_baidu",
    "b_lsid": "F75E12D5_19B4F163B53",
    "SESSDATA": "2a5b718a%2C1782110441%2C33f23%2Ac2CjBHpERBhsWzklI38F4yJt5Xvs5j_ABIelkkQ75YJq-vc9ktaFN6yR8njUx2yleOwfwSVmRYZmRDdlZyVlBZMkJMaXg2cFVsNFFaUUFMWUc1cm9HQXIxMlJ2S2ZpR1hIZG5JTUFLSS1QcnJTbkNzNm9zM3BLQUlyemdVVkpaV1VhODIxMWpxMzlnIIEC",
    "bili_jct": "54aa238902bc15cfd977ba5784e884e0",
    "DedeUserID": "3537118345300308",
    "DedeUserID__ckMd5": "9e0a26645d39c622",
    "CURRENT_FNVAL": "2000",
    "home_feed_column": "4",
    "browser_resolution": "853-911",
    "theme-tip-show": "SHOWED",
    "bili_ticket": "eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjY4MTc2NTksImlhdCI6MTc2NjU1ODM5OSwicGx0IjotMX0.DcigKfkbIiITSKfV1pf6mEqJJYSbD9-iWC1mbQWjCiI",
    "bili_ticket_expires": "1766817599",
    "sid": "ew8hvg4m"
}


class BilibiliScraper:
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

    def get_w_rid(self, mid: str, wts: str) -> str:
        """获取w_rid参数（需要w_rid.js文件）"""
        try:
            # 读取JS文件
            with open('w_rid.js', 'r', encoding='utf-8') as f:
                js_code = f.read()

            # 创建JS环境
            ctx = execjs.compile(js_code)

            # 调用函数
            a = "ea1db124af3c7062474693fa704f4ff8"
            v = f"mode=3&oid={mid}&pagination_str=%7B%22offset%22%3A%22%22%7D&plat=1&seek_rpid=&type=1&web_location=1315875&wts={wts}"

            w_rid = ctx.call('Qe.exports', v + a)
            return w_rid

        except FileNotFoundError:
            print("错误：找不到 w_rid.js 文件")
            return ""
        except Exception as e:
            print(f"生成w_rid失败: {e}")
            return ""

    def search_videos(self, keyword: str, pages: int = 1, page_size: int = 20) -> List[Dict]:
        """搜索视频"""
        print(f"正在搜索B站视频，关键词: {keyword}，共 {pages} 页...")

        all_videos = []

        for page_num in range(1, pages + 1):
            try:
                print(f"获取第 {page_num} 页...")

                url = "https://api.bilibili.com/x/web-interface/wbi/search/type"
                params = {
                    "category_id": "",
                    "search_type": "video",
                    "ad_resource": "5654",
                    "__refresh__": "true",
                    "_extra": "",
                    "context": "",
                    "page": page_num,
                    "page_size": "42",
                    # 'order':'pubdate',  #pubdate表示最新发布  click表示播放量最高
                    "pubtime_begin_s": "0",
                    "pubtime_end_s": "0",
                    "from_source": "",
                    "from_spmid": "333.337",
                    "platform": "pc",
                    "highlight": "1",
                    "single_column": "0",
                    "keyword": keyword,
                    "qv_id": "PvsGcO2h6nNmCHsbqum0XWx52drQ71LZ",
                    "source_tag": "3",
                    "gaia_vtoken": "",
                    "dynamic_offset": "24",
                    "web_roll_page": "1",
                    "web_location": "1430654",
                    "w_rid": "d933408047329da0165e068f333c7cc1",
                    "wts": "1766558489"
                }

                response = requests.get(url, headers=self.headers, cookies=self.cookies,
                                        params=params, timeout=15)
                response.raise_for_status()
                data = response.json()

                results = self.safe_get(data, ['data', 'result'], [])

                for result in results:
                    try:
                        pubdate = self.safe_get(result, ['pubdate'])
                        if pubdate:
                            pubdate_str = datetime.fromtimestamp(pubdate).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            pubdate_str = ''

                        video_info = {
                            '视频ID': str(self.safe_get(result, ['id'])),
                            '视频标题': self.safe_get(result, ['title']),
                            '视频链接': self.safe_get(result, ['arcurl']),
                            '作者': self.safe_get(result, ['author']),
                            '播放量': self.safe_get(result, ['play']),
                            '弹幕数': self.safe_get(result, ['video_review']),
                            '点赞数': self.safe_get(result, ['like']),
                            '评论数': self.safe_get(result, ['review']),
                            '收藏数': self.safe_get(result, ['favorites']),
                            '硬币数': self.safe_get(result, ['coins']),
                            '分享数': self.safe_get(result, ['share']),
                            '视频时长': self.safe_get(result, ['duration']),
                            '视频描述': self.safe_get(result, ['description']),
                            '发布时间': pubdate_str,
                            '封面图': self.safe_get(result, ['pic']),
                            'UP主ID': str(self.safe_get(result, ['mid']))
                        }
                        all_videos.append(video_info)

                    except Exception as e:
                        print(f"解析视频信息失败: {e}")
                        continue

                print(f"第 {page_num} 页获取到 {len(results)} 个视频")

                # 避免请求过快
                if page_num < pages:
                    time.sleep(1)

            except Exception as e:
                print(f"获取第 {page_num} 页失败: {e}")
                break

        print(f"总共获取到 {len(all_videos)} 个视频")
        return all_videos

    def get_video_comments(self, mid: str, max_comments: int = 20) -> List[Dict]:
        """获取视频评论"""
        all_comments = []

        if not mid or mid == '':
            return all_comments

        try:
            wts = str(int(time.time()))
            w_rid = self.get_w_rid(mid, wts)

            if not w_rid:
                print(f"无法生成w_rid参数，跳过获取评论")
                return all_comments

            url =f"https://api.bilibili.com/x/v2/reply/wbi/main?oid={mid}&type=1&mode=3&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&web_location=1315875&w_rid={w_rid}&wts={wts}"

            print(f"获取视频 {mid} 的评论...")
            response = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=10)
            response.raise_for_status()
            data = response.json()

            replies = self.safe_get(data, ['data', 'replies'], [])

            for i, reply in enumerate(replies[:max_comments]):
                try:
                    ctime = self.safe_get(reply, ['ctime'])
                    if ctime:
                        comment_time = datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        comment_time = ''

                    comment_info = {
                        '评论ID': str(self.safe_get(reply, ['rpid'])),
                        '评论者昵称': self.safe_get(reply, ['member', 'uname']),
                        '评论者ID': str(self.safe_get(reply, ['member', 'mid'])),
                        '评论者头像': self.safe_get(reply, ['member', 'avatar']),
                        '评论内容': self.safe_get(reply, ['content', 'message']),
                        '评论时间': comment_time,
                        '评论点赞数': self.safe_get(reply, ['like']),
                        '评论回复数': self.safe_get(reply, ['count'])
                    }
                    all_comments.append(comment_info)

                except Exception as e:
                    print(f"解析评论失败: {e}")
                    continue

            print(f"获取到 {len(all_comments)} 条评论")

        except Exception as e:
            print(f"获取评论失败 {mid}: {e}")

        return all_comments

    def combine_data(self, video_info: Dict, comments: List[Dict]) -> List[Dict]:
        """组合数据，每条评论作为一行"""
        combined_rows = []

        # 如果没有评论，至少创建一行包含视频信息
        if not comments:
            row = video_info.copy()
            row.update({
                '评论ID': '',
                '评论者昵称': '',
                '评论者ID': '',
                '评论者头像': '',
                '评论内容': '',
                '评论时间': '',
                '评论点赞数': '',
                '评论回复数': ''
            })
            combined_rows.append(row)
        else:
            for comment in comments:
                row = video_info.copy()
                row.update(comment)
                combined_rows.append(row)

        return combined_rows

    def scrape_search(self, keyword: str, pages: int = 1,
                      max_comments_per_video: int = 10) -> bool:
        """爬取搜索结果

        Args:
            keyword: 搜索关键词
            pages: 搜索页数
            max_comments_per_video: 每个视频最大评论数
        """
        print(f"开始爬取B站搜索结果，关键词: {keyword}...")

        # 搜索视频
        videos = self.search_videos(keyword, pages=pages)
        if not videos:
            print("没有搜索到视频")
            return False

        total_processed = 0

        # 处理每个视频
        for i, video in enumerate(videos, 1):
            try:
                print(f"\n处理第 {i}/{len(videos)} 个视频...")
                print(f"  标题: {video['视频标题'][:50]}...")

                # 获取视频评论
                video_id = video.get('视频ID', '')
                comments = self.get_video_comments(video_id, max_comments_per_video)

                # 合并数据
                combined_rows = self.combine_data(video, comments)
                self.all_data.extend(combined_rows)

                print(f"  获取到 {len(comments)} 条评论")

                total_processed += 1

                # 避免请求过快
                if i < len(videos):
                    time.sleep(1)

            except Exception as e:
                print(f"处理视频失败: {e}")
                continue

        print(f"\n总共处理了 {total_processed} 个视频")
        print(f"总数据行数: {len(self.all_data)}")
        return total_processed > 0

    def save_to_excel(self, filename: str = "B站数据.xlsx", mode: str = 'w'):
        """保存数据到Excel文件"""
        if not self.all_data:
            print("没有数据需要保存")
            return

        # 定义表头顺序
        headers_order = [
            # 视频信息
            '视频ID', '视频标题', '视频链接', '作者', '播放量', '弹幕数',
            '点赞数', '评论数', '收藏数', '硬币数', '分享数', '视频时长',
            '视频描述', '发布时间', '封面图', 'UP主ID',
            # 评论信息
            '评论ID', '评论者昵称', '评论者ID', '评论者头像', '评论内容',
            '评论时间', '评论点赞数', '评论回复数'
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
                        existing_df = pd.read_excel(filename, sheet_name='B站数据')
                        combined_df = pd.concat([existing_df, df], ignore_index=True)
                    except:
                        combined_df = df

                    combined_df.to_excel(writer, index=False, sheet_name='B站数据')

                    # 调整列宽
                    worksheet = writer.sheets['B站数据']
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
                    df.to_excel(writer, index=False, sheet_name='B站数据')

                    # 调整列宽
                    worksheet = writer.sheets['B站数据']
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
        print("B站数据采集程序")
        print("=" * 50)

        keyword = input("请输入搜索关键词: ").strip()
        if not keyword:
            print("关键词不能为空")
            return

        pages = int(input("请输入搜索页数 (默认1): ") or "1")
        max_comments = int(input("请输入每个视频最大评论数 (默认10): ") or "10")

        print(f"\n开始搜索关键词: {keyword}")
        success = self.scrape_search(
            keyword=keyword,
            pages=pages,
            max_comments_per_video=max_comments
        )

        # 保存数据
        if self.all_data:
            output_file = input("请输入输出文件名 (默认: B站数据.xlsx): ").strip()
            if not output_file:
                output_file = "B站数据.xlsx"

            mode_choice = input("保存模式: 1.覆盖(w) 2.追加(a) (默认1): ").strip()
            mode = 'a' if mode_choice == '2' else 'w'

            self.save_to_excel(output_file, mode)
            print(f"\n数据已保存到: {output_file}")
            print(f"总数据行数: {len(self.all_data)}")

            # 统计信息
            unique_videos = len(set(row['视频ID'] for row in self.all_data if row.get('视频ID')))
            comments_count = sum(1 for row in self.all_data if row.get('评论内容'))
            print(f"视频数: {unique_videos}")
            print(f"评论数: {comments_count}")
        else:
            print("没有成功抓取到数据")


def main():
    """主函数"""
    scraper = BilibiliScraper()

    # 检查w_rid.js文件是否存在
    if not os.path.exists('w_rid.js'):
        print("警告：找不到 w_rid.js 文件，评论功能可能无法使用")
        print("请确保 w_rid.js 文件与脚本在同一目录下")

    # 方法1：直接调用
    # scraper.scrape_search(keyword="AI", pages=1, max_comments_per_video=5)
    # scraper.save_to_excel("B站搜索结果.xlsx")

    # 方法2：交互式运行
    scraper.run_scraper()


if __name__ == '__main__':
    main()

# 印度军演
# B站印度军演数据.xlsx
