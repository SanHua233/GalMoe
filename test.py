import requests
import json
import os

# 配置项（和你的app.py保持一致）
BANGUMI_API_BASE = os.getenv("BANGUMI_API_BASE", "https://api.bgm.tv").rstrip("/")
BANGUMI_API_TOKEN = os.getenv("BANGUMI_API_TOKEN", "")  # 有token的话直接赋值，如："your_token_here"

def search_bangumi_character(keyword):
    """
    完全复刻app.py中的API调用逻辑，搜索角色并打印所有返回内容
    :param keyword: 搜索关键词
    :return: None
    """
    if not keyword.strip():
        print("❌ 搜索关键词不能为空")
        return

    try:
        # 1. 复刻app.py中的API请求逻辑
        url = f"{BANGUMI_API_BASE}/v0/search/characters"
        payload = {
            "keyword": keyword.strip(),
            "limit": 20
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "GalMoe-Voting-System/1.0"
        }
        # 添加token认证（和你的代码逻辑一致）
        if BANGUMI_API_TOKEN:
            headers["Authorization"] = f"Bearer {BANGUMI_API_TOKEN}"
            print(f"🔑 使用Token认证: {BANGUMI_API_TOKEN[:10]}...")

        # 发送POST请求（和你的app.py完全一致）
        print(f"📡 正在请求API: {url}")
        print(f"📦 请求参数: {json.dumps(payload, ensure_ascii=False)}")
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()

        # 2. 打印API返回的完整原始数据（关键：排查所有字段）
        print("\n" + "="*80)
        print("📊 API返回的完整原始数据:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("="*80 + "\n")

        # 3. 复刻app.py中的数据提取逻辑
        characters = []
        for item in result.get("data", []):
            # 提取图片（优先large，其次medium）
            image_url = ""
            if item.get("images"):
                image_url = item["images"].get("large", item["images"].get("medium", ""))
            
            character_info = {
                "id": item.get("id"),
                "name": item.get("name", ""),
                "cn_name": item.get("name_cn", ""),
                "image": image_url
            }
            characters.append(character_info)

        # 4. 打印提取后的角色数据（和接口返回格式一致）
        print("🎭 提取后的角色数据（和/api/search_character返回格式一致）:")
        print(json.dumps({
            "success": True,
            "characters": characters
        }, ensure_ascii=False, indent=2))

        # 5. 单独打印每条角色的所有原始字段（重点排查name_cn）
        print("\n" + "-"*80)
        print("🔍 每条角色的原始字段详情:")
        for idx, item in enumerate(result.get("data", []), 1):
            print(f"\n--- 第{idx}条角色原始数据 ---")
            for key, value in item.items():
                print(f"字段名: {key:<15} 值: {json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value}")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Bangumi API请求错误: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"❌ 响应状态码: {e.response.status_code}")
            print(f"❌ 响应内容: {e.response.text}")
    except Exception as e:
        print(f"\n❌ 程序运行错误: {str(e)}")

if __name__ == "__main__":
    # ==================== 核心修改处 ====================
    # 直接修改这里的关键词，运行即可测试
    SEARCH_KEYWORD = "丛雨"  # 示例：可改为"路飞"、"桐人"、"哪吒"等
    # ==================================================
    print(f"🚀 开始搜索Bangumi角色: {SEARCH_KEYWORD}")
    search_bangumi_character(SEARCH_KEYWORD)