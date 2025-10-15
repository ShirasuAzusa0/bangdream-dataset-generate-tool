"""
 downloader.py
 用于下载邦邦所有的 event-story 文件
 获取文件列表：https://bestdori.com/api/explorer/cn/assets/scenario/eventstory/event{n}.json
 下载文件：https://bestdori.com/assets/cn/scenario/eventstory/event{n}_rip/{filename}
 bestdori上提供的asset里Scenarioevent1.asset这一个似乎有点问题，无论是选择哪个服务器，下载下来都是日文的
 SERVER 和 CATEGORY 可按需更改，具体使用方法请参照 README 以及下面的注释
"""

import os
import requests
from tqdm import tqdm

# configs
SERVERS = ["cn", "jp", "en", "tw", "kr"]        # 可选服务器
CATEGORIES = [                                  # 可选分类
    "eventstory/event",                         # 事件剧情（包含大多数剧情，首选，其他为补充按需选择）
    "actionset/group",                          # 地图内小对话
    "afterlivetalk/group",                      # live结束后小对话
    "band",                                     # 按乐队分的主线剧情
    "birthdaystory"                             # 角色生日剧情
]
BAND_CAT = [                                    # 若分类选择目标选了 band 记得还要选 BAND_CAT，例如 "band/001"
    "001",                                      # Poppin'Party
    "002",                                      # AfterGlow
    "003",                                      # Hello、Happy World
    "004",                                      # Pastel*Palettes
    "005",                                      # Roselia
    "018",                                      # RAISE A SUILEN
    "021",                                      # Morfonica
    "045"                                       # Is MyGo!!!!!
]
MAX_EVENT_ID = 1000                             # 最大 event 序号，程序会自动跳过不存在的
MAX_THREADS = 8                                 # 并发下载线程数

SERVER = "cn"                                   # 当前下载目标（可改）
CATEGORY = "eventstory/event"                   # 当前分类选择目标（可改）

BASE_API = f"https://bestdori.com/api/explorer/{SERVER}/assets/scenario/{CATEGORY}"
BASE_ASSET = f"https://bestdori.com/assets/{SERVER}/scenario/{CATEGORY}"
DOWNLOAD_DIR = "Downloaded_Stories"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# tool functions
# 获取 event{n} 对应的 asset 文件列表
def fetch_event_list(event_id:int):
    # 获取所有 story 分类的子目录（eventID）
    url = f"{BASE_API}{event_id}.json"
    # 下面这个版本在你选择 band 或 birthdaystory 的时候使用
    # url = f"{BASE_API}.json"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception:
        return None

# 下载单个 asset 文件
def download_asset(event_id:int, filename:str):
    url = f"{BASE_ASSET}{event_id}_rip/{filename}"
    # 下面这个版本在你选择 band 或 birthdaystory 的时候使用
    # url = f"{BASE_ASSET}_rip/{filename}"
    local_path = os.path.join(DOWNLOAD_DIR, f"event{event_id}", filename)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    # 断点续传（已存在的文件直接跳过）
    if os.path.exists(local_path):
        return

    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        if resp.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(resp.content)
                f.close()
        else:
            print(f"❌ Failed {url} ({resp.status_code})")
    except Exception as e:
        print(f"⚠️ Error downloading {url}: {e}")

def main():
    print("🔍 Scanning for available event story assets...")

    for event_id in range(0, 999):
        asset_list = fetch_event_list(event_id)
        if not asset_list:
            continue

        print(f"\n📘 Found event{event_id} with {len(asset_list)} assets.")
        for filename in tqdm(asset_list, desc=f"⬇️ event{event_id}", unit="file"):
            download_asset(event_id, filename)

    print("\n✅ All available BangDream event assets downloaded.")


if __name__ == "__main__":
    main()