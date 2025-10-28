#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import requests
import json
import time
from datetime import datetime
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Logger:
    """自定义日志类"""
    @staticmethod
    def info(msg):
        print(f"ℹ️ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [INFO] {msg}")

    @staticmethod
    def success(msg):
        print(f"✅ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [SUCCESS] {msg}")

    @staticmethod
    def warning(msg):
        print(f"⚠️ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [WARNING] {msg}")

    @staticmethod
    def error(msg):
        print(f"❌ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [ERROR] {msg}")


class MiniProgramCheckin:
    def __init__(self, token, activity_code, shop_code):
        self.base_url = "https://api.lzstack.com"
        self.token = token
        self.activity_code = activity_code
        self.shop_code = shop_code
        self.headers = {
            'Host': 'api.lzstack.com',
            'Connection': 'keep-alive',
            'app-version': '2.18.88',
            'x-http-token': self.token,
            'app-id': self.app_id,
            'client-name': 'mini-program',
            'xweb_xhr': '1',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://servicewechat.com/wxaa9a9e72172f63b4/5/page-frame.html',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate'
        }

    def check_in(self):
        """执行签到"""
        url = f"{self.base_url}/mall/v2/api/checkin/handler"

        payload = {
            "code": self.activity_code,
            "shopCode": self.shop_code,
            "startTime": datetime.now().strftime("%Y-%m-%d 00:00:00"),
            "endTime": datetime.now().strftime("%Y-%m-%d 23:59:59")
        }

        try:
            Logger.info("=" * 60)
            Logger.info(f"开始执行签到... 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=15,
                verify=False
            )

            result = response.json()
            Logger.info(f"响应状态码: {response.status_code}")
            Logger.info(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")

            code = result.get('code')
            message = result.get('message', '')

            if code == 200:
                data = result.get('data', {})
                activity_name = data.get('name', '未知活动')
                integral = data.get('giveIntegralNum', 0)
                coupons = data.get('couponGiveList', [])

                Logger.success(f"签到成功！活动: {activity_name}")
                Logger.success(f"获得积分: {integral}")

                if coupons:
                    Logger.success(f"获得优惠券: {len(coupons)}张")

                return True, f"签到成功！积分+{integral}"

            elif '已签到' in message or '已领取' in message:
                Logger.warning(message)
                return True, message

            else:
                Logger.error(f"签到失败: {message} (code: {code})")
                return False, f"签到失败: {message}"

        except Exception as e:
            Logger.error(f"异常: {str(e)}")
            import traceback
            Logger.error(traceback.format_exc())
            return False, f"异常: {str(e)}"
        finally:
            Logger.info("=" * 60)


class Notifier:
    """通知推送类"""

    @staticmethod
    def send_server_chan(sckey, title, content):
        """Server酱推送"""
        if not sckey:
            return
        try:
            response = requests.post(
                f"https://sctapi.ftqq.com/{sckey}.send",
                data={"title": title, "desp": content},
                timeout=10
            )
            if response.status_code == 200:
                Logger.success("Server酱通知发送成功")
            else:
                Logger.warning(f"Server酱通知发送失败: {response.text}")
        except Exception as e:
            Logger.warning(f"Server酱推送失败: {str(e)}")

    @staticmethod
    def send_pushplus(token, title, content):
        """PushPlus推送"""
        if not token:
            return
        try:
            response = requests.post(
                "http://www.pushplus.plus/send",
                json={
                    "token": token,
                    "title": title,
                    "content": content,
                    "template": "html"
                },
                timeout=10
            )
            if response.status_code == 200:
                Logger.success("PushPlus通知发送成功")
            else:
                Logger.warning(f"PushPlus通知发送失败: {response.text}")
        except Exception as e:
            Logger.warning(f"PushPlus推送失败: {str(e)}")

    @staticmethod
    def send_bark(url, title, content):
        """Bark推送（iOS）"""
        if not url:
            return
        try:
            bark_url = f"{url}/{title}/{content}"
            response = requests.get(bark_url, timeout=10)
            if response.status_code == 200:
                Logger.success("Bark通知发送成功")
            else:
                Logger.warning(f"Bark通知发送失败: {response.text}")
        except Exception as e:
            Logger.warning(f"Bark推送失败: {str(e)}")


def main():
    """主函数 - 从环境变量读取所有配置"""

    print("""
    ╔═══════════════════════════════════════╗
    ║   微信小程序自动签到 - GitHub版        ║
    ╚═══════════════════════════════════════╝
    """)

    # ========== 从环境变量读取配置 ==========
    TOKEN = os.getenv('CHECKIN_TOKEN')
    ACTIVITY_CODE = os.getenv('ACTIVITY_CODE', 'P151750060991850814')
    SHOP_CODE = os.getenv('SHOP_CODE', 'SC1008011')
    app_id = os.getenv('APP_ID')  # 默认小程序ID

    # 通知配置（可选）
    SCKEY = os.getenv('SCKEY')  # Server酱
    PUSHPLUS_TOKEN = os.getenv('PUSHPLUS_TOKEN')  # PushPlus
    BARK_URL = os.getenv('BARK_URL')  # Bark

    # ========== 验证必需参数 ==========
    if not TOKEN:
        Logger.error("❌ 未配置 CHECKIN_TOKEN 环境变量！")
        Logger.error("请在 GitHub Secrets 中添加 CHECKIN_TOKEN")
        sys.exit(1)

    Logger.info(f"✅ 读取到Token: {TOKEN[:20]}...{TOKEN[-10:]}")
    Logger.info(f"✅ 活动代码: {ACTIVITY_CODE}")
    Logger.info(f"✅ 店铺代码: {SHOP_CODE}")

    # ========== 执行签到 ==========
    checkin = MiniProgramCheckin(TOKEN, ACTIVITY_CODE, SHOP_CODE)
    success, message = checkin.check_in()

    # ========== 发送通知 ==========
    if success:
        title = "✅ 签到成功"
        content = f"""
        ### 签到成功 🎉

        **时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        **结果**: {message}
        **店铺**: {SHOP_CODE}
        **活动**: {ACTIVITY_CODE}
        """
    else:
        title = "❌ 签到失败"
        content = f"""
        ### 签到失败 ⚠️

        **时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        **错误**: {message}
        **建议**: 请检查Token是否过期
        """

    # 发送各类通知
    Notifier.send_server_chan(SCKEY, title, content)
    Notifier.send_pushplus(PUSHPLUS_TOKEN, title, content)
    Notifier.send_bark(BARK_URL, title, message)

    # ========== 设置退出码 ==========
    if not success:
        sys.exit(1)  # 失败时返回非0退出码，GitHub Actions会标记为失败


if __name__ == "__main__":
    main()
