import requests


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

def get_search_url(keyword,num):
    url = "https://www.douyin.com/aweme/v1/web/general/search/single/"
    for i in range(0,num):
        params = {
            "aid": "6383",
            "browser_language": "zh-CN",
            "browser_name": "Chrome",
            "browser_online": "true",
            "browser_platform": "Win32",
            "browser_version": "143.0.0.0",
            "channel": "channel_pc_web",
            "cookie_enabled": "true",
            "count": "10",
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
            "offset": f"{0*num}",
            "os_name": "Windows",
            "os_version": "10",
            "pc_client_type": "1",
            "pc_libra_divert": "Windows",
            "pc_search_top_1_params": {"enable_ai_search_top_1":1},
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
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        results = response.json()['data']
        for result in results:
            type = result['type']
            if type == 1:
                desc = result['aweme_info']['desc']
                aweme_id = result['aweme_info']['aweme_id']
                create_time = result['aweme_info']['create_time']
                author_nickname = result['aweme_info']['author']['nickname']
                author_sec_uid = result['aweme_info']['author']['sec_uid']
                author_user_id = result['aweme_info']['author_user_id']
                collect_count = result['aweme_info']['statistics']['collect_count']
                comment_count = result['aweme_info']['statistics']['comment_count']
                digg_count = result['aweme_info']['statistics']['digg_count']
                share_count = result['aweme_info']['statistics']['share_count']
                video_url = result['aweme_info']['video']['play_addr']['url_list'][-1]
                print(video_url)
if __name__ == '__main__':
    get_search_url('美国斩杀线',2)