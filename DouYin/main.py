import requests
import json
import re
import pandas as pd
import os
import time
from datetime import datetime
from typing import Dict, List, Any

# 使用你提供的headers和cookies
headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en-IE;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.douyin.com/search/%E5%8D%B0%E5%BA%A6%E5%86%9B%E6%BC%94?aid=68cb100f-1b00-4cd8-a5ab-27c22a6b9228&type=general",
    "sec-ch-ua": "\\Google",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\\Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "uifid": "5bdad390e71fd6e6e69e3cafe6018169c2447c8bc0b8484cc0f203a274f99fdb860430424d4bd18d58929550fb4c694e904c9c8222fb255bb21d445ba0f6de7186120c3f921178268037a817a9e65754c36694d234ccfa7ae0d1a7e3c95c83d0b913fe8540dbbc030746d9b9e77804a00bb0ce28623d1cfd8a61189608132081d5c455b1f0d4d8899dcb46b6b3350991315243f891444b9b65a733e58237078a",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}
cookies = {
    "enter_pc_once": "1",
    "UIFID_TEMP": "5bdad390e71fd6e6e69e3cafe6018169c2447c8bc0b8484cc0f203a274f99fdb860430424d4bd18d58929550fb4c694e5b3edb2b99ae5b50d93b9f0f983edd1ef3fdd95c18933d0d3abb4883d578dcdc",
    "x-web-secsdk-uid": "fbfea36c-59be-4f74-8e8e-3d5f94a7ebe1",
    "theme": "%22light%22",
    "s_v_web_id": "verify_mjm8l1t5_5MCtZHbR_VBVn_4bip_8jwE_Ox59tvlKx0wC",
    "douyin.com": "",
    "device_web_cpu_core": "24",
    "device_web_memory_size": "8",
    "architecture": "amd64",
    "hevc_supported": "true",
    "dy_swidth": "1920",
    "dy_sheight": "1080",
    "fpk1": "U2FsdGVkX1+siW6UucdetgJKVNLVhSJGXOuEywRSJ4n+D20B6fQ5J7vnbzJibUcH9kVamiUmdS1aHugb4tgOpA==",
    "fpk2": "89db729cfcdc129111f017b0e7ac324a",
    "UIFID": "5bdad390e71fd6e6e69e3cafe6018169c2447c8bc0b8484cc0f203a274f99fdb860430424d4bd18d58929550fb4c694e904c9c8222fb255bb21d445ba0f6de7186120c3f921178268037a817a9e65754c36694d234ccfa7ae0d1a7e3c95c83d0b913fe8540dbbc030746d9b9e77804a00bb0ce28623d1cfd8a61189608132081d5c455b1f0d4d8899dcb46b6b3350991315243f891444b9b65a733e58237078a",
    "is_dash_user": "1",
    "xgplayer_user_id": "979344606669",
    "stream_player_status_params": "%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22",
    "SEARCH_RESULT_LIST_TYPE": "%22single%22",
    "csrf_session_id": "f4abed7a211d8d8b72f2ef8d0a3da7de",
    "passport_csrf_token": "4e67b2108994e17da020b3d9bfb80921",
    "passport_csrf_token_default": "4e67b2108994e17da020b3d9bfb80921",
    "bd_ticket_guard_client_web_domain": "2",
    "strategyABtestKey": "%221766974713.9%22",
    "download_guide": "%223%2F20251229%2F1%22",
    "passport_mfa_token": "CjfvO9g%2FLx0YONzQC8Ju%2BIEtLEkQUqTA8EOg%2Buu7j9fmmHoqi3A7z2JTaj4dDqAUt2oGmRCXPv2FGkoKPAAAAAAAAAAAAABP470GB6XsoXJsHEyHtnVSWJx4mVIukNeH%2BgiG6v9cdG83pqTJ1qC0G9htJ8N0r58XERD2uYUOGPax0WwgAiIBA%2Bp47rU%3D",
    "d_ticket": "b9580e7421299386b51e21441f81d5e118667",
    "n_mh": "KqMGNgEFjJdMbP8U41qILlazIXtpnQF0sACDcby8Ak4",
    "is_staff_user": "false",
    "__security_server_data_status": "1",
    "publish_badge_show_info": "%220%2C0%2C0%2C1766974746691%22",
    "DiscoverFeedExposedAd": "%7B%7D",
    "SelfTabRedDotControl": "%5B%5D",
    "ttwid": "1%7C36mJvdoBFvcRWOk3PQ1d5a3XpcwYSo7RYM6dgTrdZHc%7C1766978447%7C500e9c9f188e0a30feb99035ae4347b0cb161a9ca1a362a51ad40559e252c7d6",
    "passport_assist_user": "CkHyfculhStV6YrxFCpqyJcN55fb0qCwvQvOn8BPevstrO0FZVAiv-IeI8kjwwsJPBiiMTpulIVVhqFVLdwLLs3O0xpKCjwAAAAAAAAAAAAAT-N5eVfUaPCuLefJsrLNgJ4suTSODkSSzxAQQQdPbX_FavJSDSSRBZ264lA0XXVu0NUQm7uFDhiJr9ZUIAEiAQPzz9F2",
    "sid_guard": "a46156a2b0e6480c2d23f4720dd21bd6%7C1766978470%7C5184000%7CFri%2C+27-Feb-2026+03%3A21%3A10+GMT",
    "uid_tt": "9afed20607f05bfa760648a810c45bb8",
    "uid_tt_ss": "9afed20607f05bfa760648a810c45bb8",
    "sid_tt": "a46156a2b0e6480c2d23f4720dd21bd6",
    "sessionid": "a46156a2b0e6480c2d23f4720dd21bd6",
    "sessionid_ss": "a46156a2b0e6480c2d23f4720dd21bd6",
    "session_tlb_tag": "sttt%7C10%7CpGFWorDmSAwtI_RyDdIb1v________-yf_8oKG6mNs99adsnlJYJaS8OyX18Q_MsCK7T4fff1XM%3D",
    "sid_ucp_v1": "1.0.0-KDY3YTUzMzcyNmRlNGZiYWI5OWYwNTgwZWRlNjJlMjZlY2YzMmMzM2IKIQiMwbCDlc2oBRCm58fKBhjvMSAMMMyN1KQGOAdA9AdIBBoCbGYiIGE0NjE1NmEyYjBlNjQ4MGMyZDIzZjQ3MjBkZDIxYmQ2",
    "ssid_ucp_v1": "1.0.0-KDY3YTUzMzcyNmRlNGZiYWI5OWYwNTgwZWRlNjJlMjZlY2YzMmMzM2IKIQiMwbCDlc2oBRCm58fKBhjvMSAMMMyN1KQGOAdA9AdIBBoCbGYiIGE0NjE1NmEyYjBlNjQ4MGMyZDIzZjQ3MjBkZDIxYmQ2",
    "_bd_ticket_crypt_cookie": "fcd2d6c2487d2744f21c8a4bd0742ef7",
    "__security_mc_1_s_sdk_sign_data_key_web_protect": "8c714a27-4d26-80b0",
    "__security_mc_1_s_sdk_cert_key": "bb3dbdb3-45d9-807a",
    "__security_mc_1_s_sdk_crypt_sdk": "39ed502d-4f79-97a1",
    "login_time": "1766978470829",
    "FOLLOW_LIVE_POINT_INFO": "%22MS4wLjABAAAA3Obav9vEpEDPRPhybOz7TiwNhSszqPku9iYXjlXzYQ0CdgiAD5nuKqG7duZhqpIv%2F1767024000000%2F0%2F1766978842046%2F0%22",
    "ttcid": "719eb28117f8418fab584e02957982b634",
    "tt_scid": "GpbKuHhelLJaTnieGsDOfOhkkJBM10cZMGSfEOSEwTu.zluZ.6MyI70PL2mN6kQ10985",
    "volume_info": "%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D",
    "playRecommendGuideTagCount": "2",
    "totalRecommendGuideTagCount": "2",
    "stream_recommend_feed_params": "%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A24%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22",
    "__ac_nonce": "0695324f200bf36bedf53",
    "__ac_signature": "_02B4Z6wo00f01qGGJrAAAIDBlmPCh5FiTmqhpiIAAME-8QiK05o6.VEfcutmcC93EsHXQ3eWwrvc-F2PhpSSAifYxRGCE8gu4d9I.h7GVsZqnwV.lGX98CPtDCRcg-1KKbOK7oPnvA9FYK-n06",
    "gulu_source_res": "eyJwX2luIjoiMzRlYjBiNWI5YTNlY2RkMjY3ZGQzOTBkNjhjMjk1MGIzMjY2YmUyMDc3MWViYmZlMTIzNDM4ZDMxZmNkYTVjOCJ9",
    "sdk_source_info": "7e276470716a68645a606960273f276364697660272927676c715a6d6069756077273f276364697660272927666d776a68605a607d71606b766c6a6b5a7666776c7571273f275e58272927666a6b766a69605a696c6061273f27636469766027292762696a6764695a7364776c6467696076273f275e582729277672715a646971273f2763646976602729277f6b5a666475273f2763646976602729276d6a6e5a6b6a716c273f2763646976602729276c6b6f5a7f6367273f27636469766027292771273f2733363c35373232303532333234272927676c715a75776a716a666a69273f2763646976602778",
    "bit_env": "mSXRUl-ufUzYH_e4xSF6rnKiFqkvl7kDX9ALcDJh2ftbuUJbS1xl_bZDR5CKFoTo8SlJ0Oi-ZfgspYaJZkmzB6XyMxprJVHdy0Uef_QcIrIocCnR_v5l6l93r4RoMXb5tMCtRSD8s22nugvB3Qa0pOW9pCBBY-7N7pZMqMX7xKvePZpkgUntTS-6x4xxCDt5-R8dlqq36CzfS6FiNNAIFjiVwxvQJ759JzdvDcm0O_N4MxaNiuTIbN_p2cW8f67p2fgBrQf0RkgWJKnoO7O-jT_dm3k-IwpPRLMCRzOtlIxb8Dcrd0MD9EALlNDT-0vV2bdKRFEjvAc1GpA_fFUdJgSScVNN5E9OkHnJ3tywsAq0dzV14jDQoAAnCFuiL4jAO4Jmgwftd0zguYvVH307miCPa12CDJVz2dgxpXoIW360CrHkwkEfnivGMa-g3oHZo5ftAuUgHGbulmjiMBk5cNtK94tGnMWtCuNAMswKUHu0oZ8YCtJuKS-8xa4Puqu7",
    "passport_auth_mix_state": "vf5sk1qyryotih4v4wpmvz3osv9x2vmk",
    "IsDouyinActive": "true",
    "bd_ticket_guard_client_data": "eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCTHVNdDlUQWdpYThVY1lLdjVnTHVVM1l2Q2tYU2Q0TGFVVUhMRHJVRTV2d2psd1lWajY5NHVzL0NqdXp4RytYOXgzYUtJYkVUQmRiTlhFSG55Qzd1STQ9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D",
    "FOLLOW_NUMBER_YELLOW_POINT_INFO": "%22MS4wLjABAAAA3Obav9vEpEDPRPhybOz7TiwNhSszqPku9iYXjlXzYQ0CdgiAD5nuKqG7duZhqpIv%2F1767110400000%2F0%2F0%2F1767059083409%22",
    "home_can_add_dy_2_desktop": "%221%22",
    "biz_trace_id": "3ca19741",
    "bd_ticket_guard_client_data_v2": "eyJyZWVfcHVibGljX2tleSI6IkJMdU10OVRBZ2lhOFVjWUt2NWdMdVUzWXZDa1hTZDRMYVVVSExEclVFNXZ3amx3WVZqNjk0dXMvQ2p1enhHK1g5eDNhS0liRVRCZGJOWEVIbnlDN3VJND0iLCJ0c19zaWduIjoidHMuMi45Y2MyMjRlNTRkOTY0NDgzZWI1ZjYwY2E5MzUxYzgwYTQxZGEwZDVmOWExYTFiNDE0Y2YyM2ViMzQyYWE2ZWNmYzRmYmU4N2QyMzE5Y2YwNTMxODYyNGNlZGExNDkxMWNhNDA2ZGVkYmViZWRkYjJlMzBmY2U4ZDRmYTAyNTc1ZCIsInJlcV9jb250ZW50Ijoic2VjX3RzIiwicmVxX3NpZ24iOiI2RDlhbG00bGJhdTNvcnFhekhMamdhYys4dk8xdzl2TUFTQUVWa0JlNDVnPSIsInNlY190cyI6IiM0dk12TWFlTlVCOFNpRHVXbm1admsraUI5bGt0bHBhTmY2aHhqZnZBOUdVdDV2L0FtcThXZjRIWTcyMHkifQ%3D%3D",
    "odin_tt": "231fbbb9c27187ef406af1755d5da767d23936d62bb01468292a4141e9d4666663bc26b8c66489f39fc8a3f76aafa2d73f9edc8ad7dd1b5002b0b3c030a3e03d04dd5137d48860511f6a0d05117836ad"
}


class DouyinScraper:
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

    def fix_mojibake(self, s: str) -> str:
        """修复乱码"""
        if not s:
            return ""
        try:
            return s.encode("latin1").decode("utf-8")
        except Exception:
            return s

    def parse_user_page(self, html_text: str) -> Dict:
        """解析用户页面数据"""
        user_info = {
            '作者名称': '',
            '作者描述': '',
            '作品数': '',
            '作者粉丝数': '',
            '作者点赞数': '',
            '作者关注数': '',
            '作者IP': '',
            '作者所在城市': '',
            '作者编号': '',
            '作者年龄': ''
        }

        try:
            # 使用正则表达式提取数据
            pattern = re.compile(
                r'__pace_f\.push\(\[\s*\d+,\s*"(.+?)"\s*\]\)',
                re.S
            )

            blocks = pattern.findall(html_text)

            for raw in blocks:
                try:
                    # 处理Unicode转义
                    if "\\u" in raw or "\\x" in raw:
                        raw = bytes(raw, "utf-8").decode("unicode_escape")

                    if ":" in raw:
                        raw = raw.split(":", 1)[1]

                    data = json.loads(raw)

                    if isinstance(data, list) and len(data) >= 4:
                        obj = data[3]
                        if isinstance(obj, dict) and "user" in obj:
                            user = obj["user"]["user"]

                            user_info.update({
                                '作者名称': self.fix_mojibake(self.safe_get(user, ['nickname'])),
                                '作者描述': self.fix_mojibake(self.safe_get(user, ['desc'])),
                                '作品数': self.safe_get(user, ['awemeCount']),
                                '作者粉丝数': self.safe_get(user, ['mplatformFollowersCount']),
                                '作者点赞数': self.safe_get(user, ['totalFavorited']),
                                '作者关注数': self.safe_get(user, ['followingCount']),
                                '作者IP': self.fix_mojibake(self.safe_get(user, ['ipLocation'])),
                                '作者所在城市': self.fix_mojibake(self.safe_get(user, ['country'])),
                                '作者编号': self.safe_get(user, ['uniqueId']),
                                '作者年龄': self.safe_get(user, ['age'])
                            })
                            break

                except Exception:
                    continue

        except Exception as e:
            print(f"解析用户页面失败: {e}")

        return user_info

    def get_author_info(self, author_sec_uid: str) -> Dict:
        """获取作者信息"""
        print(f"获取作者信息: {author_sec_uid}")

        try:
            url = f"https://www.douyin.com/user/{author_sec_uid}"
            params = {"from_tab_name": "main"}

            response = requests.get(url, headers=self.headers, cookies=self.cookies,
                                    params=params, timeout=15)
            response.raise_for_status()

            return self.parse_user_page(response.text)

        except Exception as e:
            print(f"获取作者信息失败 {author_sec_uid}: {e}")
            return {}

    def get_comments(self, aweme_id: str, count: int = 10) -> List[Dict]:
        """获取评论"""
        all_comments = []

        try:
            print(f"获取视频 {aweme_id} 的评论...")

            url = "https://www.douyin.com/aweme/v1/web/comment/list/"
            params = {
                "device_platform": "webapp",
                "aid": "6383",
                "channel": "channel_pc_web",
                "aweme_id": aweme_id,
                "cursor": "0",
                "count": str(count),
                "item_type": "0",
                "insert_ids": "",
                "whale_cut_token": "",
                "cut_version": "1",
                "rcFT": "",
                "update_version_code": "170400",
                "pc_client_type": "1",
                "pc_libra_divert": "Windows",
                "support_h265": "1",
                "support_dash": "1",
                "cpu_core_num": "24",
                "version_code": "170400",
                "version_name": "17.4.0",
                "cookie_enabled": "true",
                "screen_width": "1920",
                "screen_height": "1080",
                "browser_language": "zh-CN",
                "browser_platform": "Win32",
                "browser_name": "Chrome",
                "browser_version": "143.0.0.0",
                "browser_online": "true",
                "engine_name": "Blink",
                "engine_version": "143.0.0.0",
                "os_name": "Windows",
                "os_version": "10",
                "device_memory": "8",
                "platform": "PC",
                "downlink": "10",
                "effective_type": "4g",
                "round_trip_time": "0",
                "webid": "7586931630573536822",
                "uifid": "5bdad390e71fd6e6e69e3cafe6018169c2447c8bc0b8484cc0f203a274f99fdb860430424d4bd18d58929550fb4c694e904c9c8222fb255bb21d445ba0f6de7186120c3f921178268037a817a9e65754c36694d234ccfa7ae0d1a7e3c95c83d0b913fe8540dbbc030746d9b9e77804a00bb0ce28623d1cfd8a61189608132081d5c455b1f0d4d8899dcb46b6b3350991315243f891444b9b65a733e58237078a",
                "msToken": "b3xiKUNtKcHNh5XLTLs57kYQnvibdiU1ZYmoLGOmN0oiWAwTpIu5ECkCywBqD-gaPR0npBBie7ZdP4Oh_EDmzHZGzqbTH-YAbjbC3aWuOqhRlv5c6rtaJuSL23jy826768OiW05Vq6haaj07OYaYXhSkFnEBxyo-n2lKHjncxvIZlTv7GXUvtA==",
                "a_bogus": "Y645h7XiQqmRcd/b8KOjHv1U9UxMrs8ynPTdWeOUexqkcXec8mPs/aclbxKtteevLuBhwHVHkdBMbdnbsGtsZqrpumpvuoU6oT2VIwvoZZiZYskgXNfLCGGxwiPGUW4YmAIVi/4RWsMC2dOWINCwAB17L/vNmRDdMq-GVMTjT9KsUWujwo/Ia3EZFhlz"
            }

            response = requests.get(url, headers=self.headers, cookies=self.cookies,
                                    params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            results = self.safe_get(data, ['comments'], [])

            for result in results:
                create_time = self.safe_get(result, ['create_time'])
                if create_time:
                    comment_create_time = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    comment_create_time = ''

                comment_info = {
                    '评论者名称': self.safe_get(result, ['user', 'nickname']),
                    '评论内容': self.safe_get(result, ['text']),
                    '评论时间': comment_create_time,
                    '评论IP': self.safe_get(result, ['ip_label'])
                }
                all_comments.append(comment_info)

            print(f"获取到 {len(all_comments)} 条评论")

        except Exception as e:
            print(f"获取评论失败 {aweme_id}: {e}")

        return all_comments

    def search_videos(self, keyword: str, pages: int = 1, max_per_page: int = 10) -> List[Dict]:
        """搜索视频"""
        print(f"搜索抖音视频，关键词: {keyword}，共 {pages} 页...")

        all_videos = []

        for page_num in range(pages):
            try:
                print(f"获取第 {page_num + 1} 页搜索结果...")

                url = "https://www.douyin.com/aweme/v1/web/general/search/single/"
                params = {
                    "aid": "6383",
                    "browser_language": "zh-CN",
                    "browser_name": "Chrome",
                    "browser_online": "true",
                    "browser_platform": "Win32",
                    "browser_version": "143.0.0.0",
                    "channel": "channel_pc_web",
                    "cookie_enabled": "true",
                    "count": str(max_per_page),
                    "cpu_core_num": "24",
                    "device_memory": "8",
                    "device_platform": "webapp",
                    "disable_rs": "0",
                    "downlink": "10",
                    "effective_type": "4g",
                    "enable_history": "1",
                    "engine_name": "Blink",
                    "engine_version": "143.0.0.0",
                    "from_group_id": "",
                    "is_filter_search": "0",
                    "keyword": keyword,
                    "list_type": "single",
                    "need_filter_settings": "1",
                    "offset": str(page_num * max_per_page),
                    "os_name": "Windows",
                    "os_version": "10",
                    "pc_client_type": "1",
                    "pc_libra_divert": "Windows",
                    "pc_search_top_1_params": '{"enable_ai_search_top_1":1}',
                    "platform": "PC",
                    "query_correct_type": "1",
                    "round_trip_time": "50",
                    "screen_height": "1080",
                    "screen_width": "1920",
                    "search_channel": "aweme_general",
                    "search_source": "normal_search",
                    "support_dash": "1",
                    "support_h265": "1",
                    "uifid": "5bdad390e71fd6e6e69e3cafe6018169c2447c8bc0b8484cc0f203a274f99fdb860430424d4bd18d58929550fb4c694e904c9c8222fb255bb21d445ba0f6de7186120c3f921178268037a817a9e65754c36694d234ccfa7ae0d1a7e3c95c83d0b913fe8540dbbc030746d9b9e77804a00bb0ce28623d1cfd8a61189608132081d5c455b1f0d4d8899dcb46b6b3350991315243f891444b9b65a733e58237078a",
                    "update_version_code": "0",
                    "version_code": "190600",
                    "version_name": "19.6.0",
                    "webid": "7586931630573536822",
                    "msToken": "2It3N8OvyOulG_v_B51N5HJsM5iePU2yEgoF8mtXjY6ZyKH2yTklGDAYcDglTH4-cIsH7kA7FTEkYUe4yGh2Yg1dg6I2HQG5Cj8lpLQKEnXC0Y1XK6kTNjis6YSJDYC4BTLB8w42RDV9RGYIBGsBqM8xfitk923vntiaw6zORSLo-TM9XG8_tg==",
                    "a_bogus": "QvsnDw7yOZmbKdKGuOGF76dlw8IlrTuy3MTQRPKlSOqkcHzP4mNhQPcQJxu95AQ6p8pwwqI7efMlYdncsz7sZq9kLmkvSEJRw02AISmLMq7sb-JZvNRDCjbxFiPG0CTY85IniZ4Rls0eIxcWnN9hAB37L/3rmbEdBH-UVMYjP9usUWujix/5a3jdYwtqbE=="
                }

                response = requests.get(url, headers=self.headers, cookies=self.cookies,
                                        params=params, timeout=15)
                response.raise_for_status()
                data = response.json()

                results = self.safe_get(data, ['data'], [])

                for result in results:
                    try:
                        result_type = self.safe_get(result, ['type'])
                        if result_type != 1:
                            continue

                        aweme_info = self.safe_get(result, ['aweme_info'], {})

                        create_time = self.safe_get(aweme_info, ['create_time'])
                        if create_time:
                            create_time_str = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            create_time_str = ''

                        video_info = {
                            '视频ID': self.safe_get(aweme_info, ['aweme_id']),
                            '视频描述': self.safe_get(aweme_info, ['desc']),
                            '创建时间': create_time_str,
                            '作者ID': self.safe_get(aweme_info, ['author_user_id']),
                            '作者sec_uid': self.safe_get(aweme_info, ['author', 'sec_uid']),
                            '收藏数': self.safe_get(aweme_info, ['statistics', 'collect_count']),
                            '评论数': self.safe_get(aweme_info, ['statistics', 'comment_count']),
                            '点赞数': self.safe_get(aweme_info, ['statistics', 'digg_count']),
                            '分享数': self.safe_get(aweme_info, ['statistics', 'share_count']),
                            '视频链接': aweme_info['video']['play_addr']['url_list'][-1],
                            '来源': '搜索'
                        }
                        all_videos.append(video_info)

                    except Exception as e:
                        print(f"解析视频信息失败: {e}")
                        continue

                print(f"第 {page_num + 1} 页获取到 {len([r for r in results if r.get('type') == 1])} 个视频")

                # 避免请求过快
                if page_num < pages - 1:
                    time.sleep(1)

            except Exception as e:
                print(f"获取第 {page_num + 1} 页失败: {e}")
                break

        print(f"总共获取到 {len(all_videos)} 个视频")
        return all_videos

    def get_recommend_videos(self, pages: int = 1, max_per_page: int = 20) -> List[Dict]:
        """获取推荐视频"""
        print(f"获取抖音推荐视频，共 {pages} 页...")

        all_videos = []

        for page_num in range(1, pages + 1):
            try:
                print(f"获取第 {page_num} 页推荐...")

                url = "https://www.douyin.com/aweme/v2/web/module/feed/"
                params = {
                    "device_platform": "webapp",
                    "aid": "6383",
                    "channel": "channel_pc_web",
                    "module_id": "3003101",
                    "count": str(max_per_page),
                    "filterGids": "",
                    "presented_ids": "",
                    "refresh_index": page_num,
                    "refer_id": "",
                    "refer_type": "10",
                    "pull_type": "2",
                    "awemePcRecRawData": '{"is_xigua_user":0,"danmaku_switch_status":1,"is_client":"false"}',
                    "Seo-Flag": "0",
                    "install_time": "1766470183",
                    "tag_id": "",
                    "active_id": "",
                    "is_active_tab": "false",
                    "use_lite_type": "0",
                    "xigua_user": "0",
                    "pc_client_type": "1",
                    "pc_libra_divert": "Windows",
                    "update_version_code": "170400",
                    "support_h265": "1",
                    "support_dash": "1",
                    "version_code": "170400",
                    "version_name": "17.4.0",
                    "cookie_enabled": "true",
                    "screen_width": "1920",
                    "screen_height": "1080",
                    "browser_language": "zh-CN",
                    "browser_platform": "Win32",
                    "browser_name": "Chrome",
                    "browser_version": "143.0.0.0",
                    "browser_online": "true",
                    "engine_name": "Blink",
                    "engine_version": "143.0.0.0",
                    "os_name": "Windows",
                    "os_version": "10",
                    "cpu_core_num": "24",
                    "device_memory": "8",
                    "platform": "PC",
                    "downlink": "10",
                    "effective_type": "4g",
                    "round_trip_time": "50",
                    "webid": "7586931630573536822",
                    "uifid": "5bdad390e71fd6e6e69e3cafe6018169c2447c8bc0b8484cc0f203a274f99fdb860430424d4bd18d58929550fb4c694e904c9c8222fb255bb21d445ba0f6de7186120c3f921178268037a817a9e65754c36694d234ccfa7ae0d1a7e3c95c83d0b913fe8540dbbc030746d9b9e77804a00bb0ce28623d1cfd8a61189608132081d5c455b1f0d4d8899dcb46b6b3350991315243f891444b9b65a733e58237078a",
                    "msToken": "y4l37IJsDxcAhCocTNrc7NT5M5lYtWYfjNCvxMnn_IS5qO_yvY_pFG5pDJ71T6SnokxL7tLQVYNkLKY-gEa1aEjowASm1iQnD8XQyeYue-Rt_H1-F-yrHT6BZyLr7JATQcMAPqfDeqUVMY_dzSHVZDYogQiG5KXHumeE5tMdyJb8p79T4IHMj1c%3D",
                    "a_bogus": "D70VhtWJdoRccVKGYKxbHWMlX0I%2FrT8yh-ToSNBTePYtc1lcUYNi%2FNelaxuufzMviYpkwe57pdMMYDdbTzUkZorkzmpvSKJRZt%2FIIwso%2FHh6TBiZXqfLCbtxziTGUAGY85ICiMWR6sMFIEcWVrChApVHK%2FvNRcEdMq-GV%2FujY9uRUWujio%2Fna5jsYhwqiE%3D%3D",
                    "verifyFp": "verify_mjm8l1t5_5MCtZHbR_VBVn_4bip_8jwE_Ox59tvlKx0wC",
                    "fp": "verify_mjm8l1t5_5MCtZHbR_VBVn_4bip_8jwE_Ox59tvlKx0wC"
                }

                response = requests.post(url, headers=self.headers, cookies=self.cookies,
                                         params=params, timeout=15)
                response.raise_for_status()
                data = response.json()

                results = self.safe_get(data, ['aweme_list'], [])

                for result in results:
                    try:
                        create_time = self.safe_get(result, ['create_time'])
                        if create_time:
                            create_time_str = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            create_time_str = ''

                        video_info = {
                            '视频ID': self.safe_get(result, ['aweme_id']),
                            '视频描述': self.safe_get(result, ['desc']),
                            '创建时间': create_time_str,
                            '作者sec_uid': self.safe_get(result, ['author', 'sec_uid']),
                            '作者ID': self.safe_get(result, ['author', 'uid']),
                            '收藏数': self.safe_get(result, ['statistics', 'collect_count']),
                            '评论数': self.safe_get(result, ['statistics', 'comment_count']),
                            '点赞数': self.safe_get(result, ['statistics', 'digg_count']),
                            '分享数': self.safe_get(result, ['statistics', 'share_count']),
                            '视频链接': self.safe_get(result, ['video', 'play_addr', 'url_list', -1]),
                            '来源': '推荐'
                        }
                        all_videos.append(video_info)

                    except Exception as e:
                        print(f"解析推荐视频信息失败: {e}")
                        continue

                print(f"第 {page_num} 页获取到 {len(results)} 个推荐视频")

                # 避免请求过快
                if page_num < pages:
                    time.sleep(1)

            except Exception as e:
                print(f"获取第 {page_num} 页推荐失败: {e}")
                break

        print(f"总共获取到 {len(all_videos)} 个推荐视频")
        return all_videos

    def combine_data(self, video_info: Dict, author_info: Dict, comments: List[Dict]) -> List[Dict]:
        """组合数据，每条评论作为一行"""
        combined_rows = []

        # 合并视频信息和作者信息
        base_info = {**video_info, **author_info}

        # 如果没有评论，至少创建一行
        if not comments:
            row = base_info.copy()
            row.update({
                '评论者名称': '',
                '评论内容': '',
                '评论时间': '',
                '评论IP': ''
            })
            combined_rows.append(row)
        else:
            for comment in comments:
                row = base_info.copy()
                row.update(comment)
                combined_rows.append(row)

        return combined_rows

    def scrape_search(self, keyword: str, pages: int = 1,
                      max_comments_per_video: int = 10) -> bool:
        """爬取搜索结果"""
        print(f"开始爬取抖音搜索结果，关键词: {keyword}...")

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
                print(f"  描述: {video['视频描述'][:50]}..." if video['视频描述'] else "  无描述")

                # 获取作者信息
                author_sec_uid = video.get('作者sec_uid', '')
                author_info = {}
                if author_sec_uid:
                    author_info = self.get_author_info(author_sec_uid)

                # 获取评论
                video_id = video.get('视频ID', '')
                comments = self.get_comments(video_id, max_comments_per_video)

                # 合并数据
                combined_rows = self.combine_data(video, author_info, comments)
                self.all_data.extend(combined_rows)

                print(f"  获取到 {len(comments)} 条评论")

                total_processed += 1

                # 避免请求过快
                if i < len(videos):
                    time.sleep(2)

            except Exception as e:
                print(f"处理视频失败: {e}")
                continue

        print(f"\n总共处理了 {total_processed} 个视频")
        return total_processed > 0

    def scrape_recommend(self, pages: int = 1,
                         max_comments_per_video: int = 10) -> bool:
        """爬取推荐视频"""
        print("开始爬取抖音推荐视频...")

        # 获取推荐视频
        videos = self.get_recommend_videos(pages=pages)
        if not videos:
            print("没有获取到推荐视频")
            return False

        total_processed = 0

        # 处理每个视频
        for i, video in enumerate(videos, 1):
            try:
                print(f"\n处理第 {i}/{len(videos)} 个推荐视频...")
                print(f"  描述: {video['视频描述'][:50]}..." if video['视频描述'] else "  无描述")

                # 获取作者信息
                author_sec_uid = video.get('作者sec_uid', '')
                author_info = {}
                if author_sec_uid:
                    author_info = self.get_author_info(author_sec_uid)

                # 获取评论
                video_id = video.get('视频ID', '')
                comments = self.get_comments(video_id, max_comments_per_video)

                # 合并数据
                combined_rows = self.combine_data(video, author_info, comments)
                self.all_data.extend(combined_rows)

                print(f"  获取到 {len(comments)} 条评论")

                total_processed += 1

                # 避免请求过快
                if i < len(videos):
                    time.sleep(2)

            except Exception as e:
                print(f"处理推荐视频失败: {e}")
                continue

        print(f"\n总共处理了 {total_processed} 个推荐视频")
        return total_processed > 0

    def save_to_excel(self, filename: str = "抖音数据.xlsx", mode: str = 'w'):
        """保存数据到Excel文件"""
        if not self.all_data:
            print("没有数据需要保存")
            return

        # 定义表头顺序
        headers_order = [
            # 视频信息
            '视频ID', '视频描述', '创建时间', '视频链接', '来源',
            '作者ID', '作者sec_uid','收藏数', '评论数', '点赞数', '分享数',
            # 作者信息
            '作者名称', '作者描述', '作品数', '作者粉丝数',
            '作者点赞数', '作者关注数', '作者IP',
            '作者所在城市', '作者编号', '作者年龄',
            # 评论信息
            '评论者名称', '评论内容', '评论时间', '评论IP'
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
                        existing_df = pd.read_excel(filename, sheet_name='抖音数据')
                        combined_df = pd.concat([existing_df, df], ignore_index=True)
                    except:
                        combined_df = df

                    combined_df.to_excel(writer, index=False, sheet_name='抖音数据')

                    # 调整列宽
                    worksheet = writer.sheets['抖音数据']
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
                    df.to_excel(writer, index=False, sheet_name='抖音数据')

                    # 调整列宽
                    worksheet = writer.sheets['抖音数据']
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
        print("抖音数据采集程序")
        print("=" * 50)
        print("1. 采集推荐视频")
        print("2. 搜索关键词采集")
        print("=" * 50)

        choice = input("请选择模式 (1 或 2): ").strip()

        if choice == '1':
            # 采集推荐视频
            pages = int(input("请输入采集页数 (默认1): ") or "1")
            max_comments = int(input("请输入每个视频最大评论数 (默认10): ") or "10")

            print("\n开始采集推荐视频...")
            success = self.scrape_recommend(pages=pages, max_comments_per_video=max_comments)

        elif choice == '2':
            # 搜索关键词采集
            keyword = input("请输入搜索关键词: ").strip()
            if not keyword:
                print("关键词不能为空")
                return

            pages = int(input("请输入搜索页数 (默认1): ") or "1")
            max_comments = int(input("请输入每个视频最大评论数 (默认10): ") or "10")

            print(f"\n开始搜索关键词: {keyword}")
            success = self.scrape_search(keyword=keyword, pages=pages,
                                         max_comments_per_video=max_comments)

        else:
            print("无效的选择")
            return

        # 保存数据
        if self.all_data:
            output_file = input("请输入输出文件名 (默认: 抖音数据.xlsx): ").strip()
            if not output_file:
                output_file = "抖音数据.xlsx"

            mode_choice = input("保存模式: 1.覆盖(w) 2.追加(a) (默认1): ").strip()
            mode = 'a' if mode_choice == '2' else 'w'

            self.save_to_excel(output_file, mode)
            print(f"\n数据已保存到: {output_file}")
            print(f"总数据行数: {len(self.all_data)}")
        else:
            print("没有成功抓取到数据")


def main():
    """主函数"""
    scraper = DouyinScraper()

    # 方法1：直接调用
    # 采集推荐视频
    # scraper.scrape_recommend(pages=1, max_comments_per_video=5)

    # 或者搜索视频
    # scraper.scrape_search(keyword="AI", pages=1, max_comments_per_video=5)

    # 保存数据
    # scraper.save_to_excel("抖音数据.xlsx")

    # 方法2：交互式运行
    scraper.run_scraper()


if __name__ == '__main__':
    main()

# 美国斩杀线