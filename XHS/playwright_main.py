from playwright.sync_api import sync_playwright
import time


def simple_cookie_usage():
    # 你的原始cookie字典（保持原样）
    cookie_dict = {
        "abRequestId": "6b7017a3-16c5-53e2-87fa-4fa56980442e",
        "xsecappid": "xhs-pc-web",
        "a1": "19b262d5370a14z23ula914kdb6bajisd8oizgkv050000523902",
        "webId": "340e907e3bff6105d7cddb92cacb6756",
        "gid": "yjDJKJfK2if4yjDJKJf2qYkTW80y4uJq710jlh8y4TfDK328D0V3Mu8882Jqj8J8WWid4D8i",
        "web_session": "040069b443fd5e4a2c40b059743b4b9515608e",
        "unread": "{%22ub%22:%22693d01c5000000001e0338f0%22%2C%22ue%22:%2269411bed000000001e0332d7%22%2C%22uc%22:23}",
        "webBuild": "5.0.7",
        "loadts": "1765878724565",
        "acw_tc": "0a4a3e3517659325857748428ef123be40d359e4494963622a29afc091cf8b",
        "websectiga": "984412fef754c018e472127b8effd174be8a5d51061c991aadd200c69a2801d6",
        "sec_poison_id": "efcda492-9f15-4671-9118-27b5da463506"
    }
    # 转换为Playwright需要的格式
    cookies = []
    for name, value in cookie_dict.items():
        cookies.append({
            "name": name,
            "value": value,
            "domain": ".xiaohongshu.com",  # 关键：设置正确的域名
            "path": "/"
        })

    with sync_playwright() as p:
        # 启动浏览器（设为可见以便调试）
        browser = p.chromium.launch(headless=False)

        # 创建context并设置cookies
        context = browser.new_context()
        context.add_cookies(cookies)

        # 创建页面
        page = context.new_page()

        # 访问小红书
        print("正在访问小红书...")
        page.goto("https://www.xiaohongshu.com/explore/6941fe1e000000001e02e3a1?xsec_token=ABSeBrWJzwSPn7YO5vJQZKuSiJwmMutc_yPIm2ijvHs2k=&xsec_source=pc_search&source=unknown")

        # 等待页面加载完成
        page.wait_for_load_state('networkidle')

        # 检查页面标题或内容，确认是否成功
        title = page.title()
        print(f"页面标题: {title}")

        # 查找登录后的特征元素
        # 小红书登录后常见的元素选择器
        login_indicators = [
            ".user-name",
            ".user-avatar",
            "[data-testid='user-avatar']",
            "text=我的",
            "text=消息"
        ]

        for indicator in login_indicators:
            if page.locator(indicator).count() > 0:
                print(f"✅ 检测到登录元素: {indicator}")
                print("🎉 Cookie有效，登录成功！")
                break
        else:
            print("⚠️  未检测到登录状态，Cookie可能已过期")

        # 打印当前URL
        print(f"当前URL: {page.url}")

        # 截图保存
        page.screenshot(path="result.png")
        print("截图已保存为 result.png")

        # 保持浏览器打开10秒以便查看
        print("\n浏览器将保持打开10秒...")
        time.sleep(10)

        browser.close()


if __name__ == "__main__":
    simple_cookie_usage()