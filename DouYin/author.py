import requests
import json
import re

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en-IE;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://www.douyin.com/search/%E7%BE%8E%E5%9B%BD%E6%96%A9%E6%9D%80%E7%BA%BF?aid=fedc2cc8-31ea-4783-8665-b3ac735d6acc&type=general",
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
    "douyin.com": "",
    "enter_pc_once": "1",
    "UIFID_TEMP": "5bdad390e71fd6e6e69e3cafe6018169c2447c8bc0b8484cc0f203a274f99fdb860430424d4bd18d58929550fb4c694e5b3edb2b99ae5b50d93b9f0f983edd1ef3fdd95c18933d0d3abb4883d578dcdc",
    "x-web-secsdk-uid": "fbfea36c-59be-4f74-8e8e-3d5f94a7ebe1",
    "theme": "%22light%22",
    "s_v_web_id": "verify_mjm8l1t5_5MCtZHbR_VBVn_4bip_8jwE_Ox59tvlKx0wC",
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
    "__ac_nonce": "069522c9a00d0c8b41f73",
    "__ac_signature": "_02B4Z6wo00f01qIePSwAAIDBlfvZGYMeaI6iPjmAAMHhB1Rh1ku4RzDAEvfLFtJ5wSjCniaIr.k2NaL8A4XXVPMP1.4FmBlxw3dJBDLR2AHJ91Met0Lqqi7jQknUDJ2H7j94xQiiuRIDV--n95",
    "playRecommendGuideTagCount": "2",
    "totalRecommendGuideTagCount": "2",
    "gulu_source_res": "eyJwX2luIjoiMzRlYjBiNWI5YTNlY2RkMjY3ZGQzOTBkNjhjMjk1MGIzMjY2YmUyMDc3MWViYmZlMTIzNDM4ZDMxZmNkYTVjOCJ9",
    "stream_recommend_feed_params": "%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A24%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22",
    "FOLLOW_NUMBER_YELLOW_POINT_INFO": "%22MS4wLjABAAAA3Obav9vEpEDPRPhybOz7TiwNhSszqPku9iYXjlXzYQ0CdgiAD5nuKqG7duZhqpIv%2F1767024000000%2F0%2F1766994404267%2F0%22",
    "odin_tt": "e2c87e1c4c86671b980d559616f82adc5b45adfb84a02a381f4a7751316f5f8b3d3500089e803cddb8fb91dfdbd87f42d13189041ef29ad4aa6f960c4d8d5134",
    "biz_trace_id": "f2244a24",
    "sdk_source_info": "7e276470716a68645a606960273f276364697660272927676c715a6d6069756077273f276364697660272927666d776a68605a607d71606b766c6a6b5a7666776c7571273f275e58272927666a6b766a69605a696c6061273f27636469766027292762696a6764695a7364776c6467696076273f275e582729277672715a646971273f2763646976602729277f6b5a666475273f2763646976602729276d6a6e5a6b6a716c273f2763646976602729276c6b6f5a7f6367273f27636469766027292771273f273d3032333c31313c3c33333234272927676c715a75776a716a666a69273f2763646976602778",
    "bit_env": "4ScNPaHhffkZQv2Gvx0CTn3cp5BI_hUd41NsZZ1AMfJVp5oEdEdfelXhNbM9tCru4Zj_fkhLFusiFUmxqn7NK23-jhxIF3G-KfgWD-hS6W0ehXhpQpOsbGSPJlTRqUDVLMK0lFZNFYOwRBAqZnGvT0jQyeIBjo5UAbMmQ-8KRjXSqmG5LDqx2fA-QFozNBvvDYOaWMVeB4HMzECOZ0OWvKPndAs2vCDPegrlXr55upUrcdaOxFIC-GSLJYLY53VVDOMvTwNMS58tB5EaGE6R_opv1dexxmhfoE4ddD1kObPD4k8OQCRpkPpiOrtrnXTj5n7eiioMYBaUncSMA8odZ7ReFZvQtKdwCeDimtYmkY63oUBu6340e-sLhvsUjfO6Wke_u1Cd5iVu_M-4_zj0WLiSLZF1GGjDKTOmSyM0J2MvU98ch6myX_QwxWqolOTkyp8H91ih1iagyvoTqmJ5MzpvMugZskQEopodeqSGYqgOizWfSfaD_dwy9KIJCTSo",
    "passport_auth_mix_state": "x4j5uuo78ux0vw1xkxu9qjg5i45lnaw0c6onbojmks0yz9eg",
    "bd_ticket_guard_client_data": "eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCTHVNdDlUQWdpYThVY1lLdjVnTHVVM1l2Q2tYU2Q0TGFVVUhMRHJVRTV2d2psd1lWajY5NHVzL0NqdXp4RytYOXgzYUtJYkVUQmRiTlhFSG55Qzd1STQ9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D",
    "bd_ticket_guard_client_data_v2": "eyJyZWVfcHVibGljX2tleSI6IkJMdU10OVRBZ2lhOFVjWUt2NWdMdVUzWXZDa1hTZDRMYVVVSExEclVFNXZ3amx3WVZqNjk0dXMvQ2p1enhHK1g5eDNhS0liRVRCZGJOWEVIbnlDN3VJND0iLCJ0c19zaWduIjoidHMuMi45Y2MyMjRlNTRkOTY0NDgzZWI1ZjYwY2E5MzUxYzgwYTQxZGEwZDVmOWExYTFiNDE0Y2YyM2ViMzQyYWE2ZWNmYzRmYmU4N2QyMzE5Y2YwNTMxODYyNGNlZGExNDkxMWNhNDA2ZGVkYmViZWRkYjJlMzBmY2U4ZDRmYTAyNTc1ZCIsInJlcV9jb250ZW50Ijoic2VjX3RzIiwicmVxX3NpZ24iOiJncmR1NkRUMnRtdUNFV21XT2YxK1lYV0lyRVlIZzJIMmRxbWpsdXhCejZ3PSIsInNlY190cyI6IiNjWTI0d205TGtTWE5YcUJTQWtXS3FrcmladlhOUUlwdmZFM1ptVHBXWlBMM2lBRVBWVjNSY25zY2NJZEcifQ%3D%3D",
    "home_can_add_dy_2_desktop": "%221%22",
    "IsDouyinActive": "false"
}
def get_author_info(author_sec_uid):
    url = f"https://www.douyin.com/user/{author_sec_uid}"
    params = {
        "from_tab_name": "main"
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    def safe_unescape(s: str) -> str:
        if "\\u" in s or "\\x" in s:
            return bytes(s, "utf-8").decode("unicode_escape")
        return s

    # html = open("page.txt", "r", encoding="utf-8").read()

    pattern = re.compile(
        r'__pace_f\.push\(\[\s*\d+,\s*"(.+?)"\s*\]\)',
        re.S
    )

    blocks = pattern.findall(response.text)
    print("找到 pace 数据块数量:", len(blocks))

    parsed = []

    for raw in blocks:
        try:
            raw = safe_unescape(raw)

            if ":" in raw:
                raw = raw.split(":", 1)[1]

            data = json.loads(raw)

            if isinstance(data, list) and len(data) >= 4:
                obj = data[3]
                if isinstance(obj, dict):
                    parsed.append(obj)

        except Exception:
            pass
    def fix_mojibake(s: str) -> str:
        try:
            return s.encode("latin1").decode("utf-8")
        except Exception:
            return s
    print("成功解析 JSON 数量:", len(parsed))
    user = parsed[0]["user"]["user"]

    user["desc"] = fix_mojibake(user["desc"])
    user["nickname"] = fix_mojibake(user["nickname"])
    user['ipLocation'] = fix_mojibake(user['ipLocation'])
    user['country'] = fix_mojibake(user['country'])
    authon_followingCount = user['followingCount']
    author_desc = user["desc"]
    author_nickname = user["nickname"]
    awemeCount = user["awemeCount"]
    author_fans_count = user["mplatformFollowersCount"]
    author_like_count = user["totalFavorited"]
    author_ipLocation = user["ipLocation"]
    author_country = user["country"]
    author_uniqueId = user["uniqueId"]
    author_age = user["age"]
    return {
        'author_nickname': author_nickname,
        'author_desc': author_desc,
        'awemeCount': awemeCount,
        'author_fans_count': author_fans_count,
        'author_like_count': author_like_count,
        'authon_followingCount': authon_followingCount,
        'author_ipLocation': author_ipLocation,
        'author_country': author_country,
        'author_uniqueId': author_uniqueId,
        'author_age': author_age,
    }


if __name__ == '__main__':
    print(get_author_info('MS4wLjABAAAAUj_2j9toBPzDAuRFshoe8l-qI3Oxb-_OpH5m0njacyU'))