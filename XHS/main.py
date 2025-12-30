import json
import re
from datetime import datetime

import requests
import pandas as pd
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional

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
    "webBuild": "5.3.0",
    "websectiga": "2a3d3ea002e7d92b5c9743590ebd24010cf3710ff3af8029153751e41a6af4a3",
    "sec_poison_id": "d51f3224-4156-4284-8a91-568540b222eb",
    "acw_tc": "0ad62b1517669705749163803e7454b8dc92950e6b0d2eef0929c46ff082ca",
    "web_session": "040069b6aced5b79a3ef499d643b4b8daf505f",
    "id_token": "VjEAALG/FOn9ITUOTvlhf+TLZB+o0RK5k6sPnaky6dh8mrggozJuN0Q+KJax3zSHwOk8x4dnBQrc7KaPW0sYuY1T50J0z/hfFn9jaYnhLTtbRKSakLHRUmva+/vuyxqDMMEyPoK7",
    "loadts": "1766970675371",
    "unread": "{%22ub%22:%22693561af000000001e00eec9%22%2C%22ue%22:%2269307175000000001e0103ed%22%2C%22uc%22:31}"
}


class XHSScraper:
    # 需要定期更新cookie
    def __init__(self):
        self.headers = headers
        self.cookies = cookies
        self.all_data = []

    def safe_get(self, data: Dict, keys: List[str], default: Any = "") -> Any:
        """安全获取嵌套字典的值"""
        try:
            for key in keys:
                data = data[key]
            return data
        except (KeyError, TypeError, IndexError):
            return default

    def get_search_results(self, keyword: str = "", page: int = 1, page_size: int = 20) -> List[Dict]:
        """获取搜索结果"""
        url = "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes"
        data = {
            "keyword": keyword,
            "page": page,
            "page_size": page_size,
            "search_id": "2fqatpwkvfwuny7gamfvz",
            "sort": "general",
            "note_type": 0,
            "ext_flags": [],
            "geo": "",
            "image_formats": ["jpg", "webp", "avif"]
        }

        try:
            response = requests.post(url, headers=self.headers, cookies=self.cookies, json=data, timeout=10)
            response.raise_for_status()
            items = self.safe_get(response.json(), ['data', 'items'], [])
            return items
        except Exception as e:
            print(f"搜索失败: {e}")
            return []

    def get_detail(self, x_id: str, xsec_token: str) -> Dict:
        """获取笔记详情"""
        url = f"https://www.xiaohongshu.com/explore/{x_id}"
        params = {
            "xsec_token": xsec_token,
            "xsec_source": "pc_search",
            "source": "unknown"
        }

        detail_info = {
            '笔记ID': '',
            '标题': '',
            '描述': '',
            '类型': '',
            '媒体信息': '',
            '发布时间': '',
            '收藏数': '',
            '点赞数': '',
            '评论数': '',
            '分享数': '',
            '网页链接':''
        }

        try:
            response = requests.get(url, params=params, headers=self.headers, cookies=self.cookies, timeout=10)
            response.raise_for_status()

            # 提取笔记数据
            pattern = r'"note"\s*:\s*(.*?)\s*"nioStore"\s*:'
            result = re.search(pattern, response.text, re.S)

            if result:
                content = result.group(1)
                if content[-1] == ',':
                    content = content[:-1]

                data_json = json.loads(content)
                firstNoteId = self.safe_get(data_json, ['firstNoteId'])
                note_detail = self.safe_get(data_json, ['noteDetailMap', firstNoteId, 'note'], {})

                # 获取互动数据
                interactions = self.safe_get(note_detail, ['interactInfo'], {})
                post_time = self.safe_get(note_detail, ['time'])
                post_time = datetime.fromtimestamp(int(post_time) / 1000).strftime("%Y-%m-%d %H:%M:%S")
                detail_info.update({
                    '网页链接': response.url,
                    '笔记ID': x_id,
                    '标题': self.safe_get(note_detail, ['title']),
                    '描述': self.safe_get(note_detail, ['desc']),
                    '类型': self.safe_get(note_detail, ['type']),
                    '发布时间': post_time,
                    '收藏数': self.safe_get(interactions, ['collectedCount']),
                    '点赞数': self.safe_get(interactions, ['likedCount']),
                    '评论数': self.safe_get(interactions, ['commentCount']),
                    '分享数': self.safe_get(interactions, ['shareCount']),
                })

                # 处理媒体信息
                note_type = detail_info['类型']
                if note_type == 'video':
                    media_url = self.safe_get(note_detail, ['video', 'media', 'stream', 'h265', 0, 'masterUrl'])
                    detail_info['媒体信息'] = media_url if media_url else ''
                else:
                    image_list = self.safe_get(note_detail, ['imageList'], [])
                    media_urls = [self.safe_get(img, ['urlPre']) for img in image_list if
                                  self.safe_get(img, ['urlPre'])]
                    detail_info['媒体信息'] = ','.join(media_urls) if media_urls else ''

        except Exception as e:
            print(f"获取详情失败 {x_id}: {e}")

        return detail_info

    def get_comments(self, x_id: str, xsec_token: str) -> List[Dict]:
        """获取评论信息"""
        all_comments = []
        url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/page"
        params = {
            "note_id": x_id,
            "cursor": "",
            "top_comment_id": "",
            "image_formats": "jpg,webp,avif",
            "xsec_token": xsec_token
        }

        try:
            response = requests.get(url, headers=self.headers, cookies=self.cookies, params=params, timeout=10)
            response.raise_for_status()
            comments = self.safe_get(response.json(), ['data', 'comments'], [])
            for com in comments:
                comment_time = self.safe_get(com, ['create_time'])
                comment_time = datetime.fromtimestamp(int(comment_time)/1000).strftime("%Y-%m-%d %H:%M:%S")
                comment_info = {
                    '评论ID': self.safe_get(com, ['id']),
                    '评论内容': self.safe_get(com, ['content']),
                    '评论时间': comment_time,
                    '点赞数': self.safe_get(com, ['like_count']),
                    '回复数': self.safe_get(com, ['sub_comment_count']),
                    '用户ID': self.safe_get(com, ['user_info', 'user_id']),
                    '用户名': self.safe_get(com, ['user_info', 'nickname']),
                    '用户IP': self.safe_get(com, ['ip_location'])
                }
                all_comments.append(comment_info)

        except Exception as e:
            print(f"获取评论失败 {x_id}: {e}")

        return all_comments

    def get_user_info(self, user_id: str, xsec_token: str) -> Dict:
        """获取用户信息"""
        user_info = {
            '用户ID': '',
            '用户名': '',
            '小红书号': '',
            '用户IP': '',
            '个人简介': '',
            '笔记数': '',
            '粉丝数': '',
            '获赞收藏数': ''
        }

        url = f"https://www.xiaohongshu.com/user/profile/{user_id}"
        params = {
            "xsec_token": xsec_token,
            "xsec_source": "pc_note"
        }

        try:
            response = requests.get(url, headers=self.headers, cookies=self.cookies, params=params, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # 提取用户信息
            user_name_elem = soup.find('div', class_='user-name')
            user_redId_elem = soup.find('span', class_='user-redId')
            user_ip_elem = soup.find('span', class_='user-IP')
            user_desc_elem = soup.find('div', class_='user-desc')
            user_image = soup.find('img',class_='user-image')
            user_info.update({
                '用户ID': user_id,
                '用户名': user_name_elem.text.strip() if user_name_elem else '',
                '小红书号': user_redId_elem.text.strip() if user_redId_elem else '',
                '用户IP': user_ip_elem.text.strip() if user_ip_elem else '',
                '个人简介': user_desc_elem.text.strip() if user_desc_elem else '',
                '用户头像': user_image.get('src') if user_image else ''
            })

            # 提取互动数据
            interaction_spans = soup.find_all('span', class_='count')
            if len(interaction_spans) >= 3:
                user_info['笔记数'] = interaction_spans[0].text.strip() if interaction_spans[0] else ''
                user_info['粉丝数'] = interaction_spans[1].text.strip() if interaction_spans[1] else ''
                user_info['获赞收藏数'] = interaction_spans[2].text.strip() if interaction_spans[2] else ''

        except Exception as e:
            print(f"获取用户信息失败 {user_id}: {e}")

        return user_info

    def combine_data(self, note_info: Dict, detail_info: Dict, user_info: Dict, comments: List[Dict]) -> List[Dict]:
        """组合所有数据，每条评论作为一行"""
        combined_rows = []

        # 如果没有评论，至少创建一行包含笔记和用户信息
        if not comments:
            row = {}
            row.update(detail_info)
            row.update(user_info)
            row.update({
                '评论ID': '',
                '评论内容': '',
                '评论时间': '',
                '评论点赞数': '',
                '评论回复数': '',
                '评论用户ID': '',
                '评论用户名': '',
                '评论用户IP': ''
            })
            combined_rows.append(row)
        else:
            for comment in comments:
                row = {}
                # 笔记详情信息
                row.update(detail_info)
                # 用户信息
                row.update(user_info)
                # 评论信息（重命名避免冲突）
                row.update({
                    '评论ID': comment.get('评论ID', ''),
                    '评论内容': comment.get('评论内容', ''),
                    '评论时间': comment.get('评论时间', ''),
                    '评论点赞数': comment.get('点赞数', ''),
                    '评论回复数': comment.get('回复数', ''),
                    '评论用户ID': comment.get('用户ID', ''),
                    '评论用户名': comment.get('用户名', ''),
                    '评论用户IP': comment.get('用户IP', '')
                })
                combined_rows.append(row)

        return combined_rows

    def scrape_and_save(self, keyword: str = "", max_items: int = 10, output_file: str = "xhs_data.xlsx"):
        """主函数：爬取数据并保存到Excel"""
        print(f"开始搜索关键词: {keyword}")

        # 获取搜索结果
        search_items = self.get_search_results(keyword)
        if not search_items:
            print("未找到搜索结果")
            return

        print(f"找到 {len(search_items)} 条笔记")

        # 处理每条笔记
        for i, item in enumerate(search_items[:max_items]):
            try:
                print(f"\n处理第 {i + 1} 条笔记...")

                x_id = self.safe_get(item, ['id'])
                xsec_token = self.safe_get(item, ['xsec_token'])
                user_id = self.safe_get(item, ['note_card', 'user', 'user_id'])
                user_xsec_token = self.safe_get(item, ['note_card', 'user', 'xsec_token'])

                if not all([x_id, xsec_token, user_id, user_xsec_token]):
                    print(f"跳过笔记 {x_id}，缺少必要参数")
                    continue

                # 获取各种信息
                detail_info = self.get_detail(x_id, xsec_token)
                user_info = self.get_user_info(user_id, user_xsec_token)
                comments = self.get_comments(x_id, xsec_token)

                # 合并数据
                combined_rows = self.combine_data(item, detail_info, user_info, comments)
                self.all_data.extend(combined_rows)

                print(f"  笔记ID: {x_id}")
                print(f"  标题: {detail_info.get('标题', '')[:50]}...")
                print(f"  用户: {user_info.get('用户名', '')}")
                print(f"  评论数: {len(comments)}")

            except Exception as e:
                print(f"处理笔记时出错: {e}")
                continue

        # 保存到Excel
        if self.all_data:
            self.save_to_excel(output_file)
            print(f"\n数据已保存到: {output_file}")
            print(f"总数据行数: {len(self.all_data)}")
        else:
            print("没有成功抓取到数据")

    def save_to_excel(self, filename: str):
        """保存数据到Excel文件"""
        if not self.all_data:
            print("没有数据需要保存")
            return

        # 定义表头顺序（中文）
        headers_order = [
            '网页链接','笔记ID', '标题', '描述', '类型', '媒体信息', '发布时间',
            '收藏数', '点赞数', '评论数', '分享数',
            '用户ID', '用户名', '小红书号', '用户IP', '个人简介','用户头像',
            '关注数', '粉丝数', '获赞收藏数',
            '评论ID', '评论内容', '评论时间', '评论点赞数', '评论回复数',
            '评论用户ID', '评论用户名', '评论用户IP'
        ]

        # 确保所有行都有相同的列
        df_data = []
        for row in self.all_data:
            ordered_row = {}
            for header in headers_order:
                ordered_row[header] = row.get(header, '')
            df_data.append(ordered_row)

        df = pd.DataFrame(df_data, columns=headers_order)

        # 保存到Excel
        with pd.ExcelWriter(filename,mode='w', engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='小红书数据')

            # 调整列宽
            # worksheet = writer.sheets['小红书数据']
            # for idx, col in enumerate(df.columns):
            #     column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
            #     worksheet.column_dimensions[chr(65 + idx)].width = min(column_width, 50)


def main():
    """主函数"""
    scraper = XHSScraper()

    # 配置参数
    keyword = "华为"  # 搜索关键词
    max_items = 10  # 最大处理笔记数（建议先测试少量）
    output_file = "小红书数据.xlsx"  # 输出文件名

    # 开始爬取
    scraper.scrape_and_save(keyword, max_items, output_file)


if __name__ == '__main__':
    main()