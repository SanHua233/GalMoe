from flask import Flask, render_template, request, jsonify, session
import pymysql
import requests
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config["SECRET_KEY"]

# 修改 Jinja2 定界符，避免与 Vue 冲突
app.jinja_env.variable_start_string = '{!'
app.jinja_env.variable_end_string = '!}'

BANGUMI_API_BASE = app.config.get("BANGUMI_API_BASE", "https://api.bgm.tv").rstrip("/")
BANGUMI_API_TOKEN = app.config.get("BANGUMI_API_TOKEN", "")

def get_db():
    return pymysql.connect(
        host=app.config["MYSQL_HOST"],
        user=app.config["MYSQL_USER"],
        password=app.config["MYSQL_PASSWORD"],
        database=app.config["MYSQL_DB"],
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/api/nominate_character", methods=["POST"])
def nominate_character():
    # 1. 校验登录状态
    if "user" not in session:
        return jsonify({"success": False, "message": "请先登录"}), 401
    
    # 2. 获取请求数据
    data = request.json
    name = data.get("name", "").strip()
    cn_name = data.get("cn_name", "").strip()
    image = data.get("image", "").strip()  # 前端传的图片链接，对应表的image_url
    
    if not name:
        return jsonify({"success": False, "message": "角色名称不能为空"}), 400
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # 3. 唯一性校验核心逻辑（仅使用表中存在的字段）
        # 3.1 先查询同名角色
        cursor.execute("SELECT id, image_url FROM char_data WHERE name = %s", (name,))
        same_name_chars = cursor.fetchall()
        
        if same_name_chars:
            # 3.2 有同名角色时，校验图片URL
            duplicate = False
            for char in same_name_chars:
                # 情况1：数据库中角色有图片URL，且和提名的图片URL一致 → 重复
                if char["image_url"] and image and char["image_url"] == image:
                    duplicate = True
                    break
                # 情况2：数据库中角色无图片URL，且提名的也无图片URL → 重复（同名且无图视为同一角色）
                elif not char["image_url"] and not image:
                    duplicate = True
                    break
            
            if duplicate:
                cursor.close()
                conn.close()
                return jsonify({"success": False, "message": "该角色已被提名，请勿重复提名"}), 400
        
        # 4. 插入新角色（仅插入表中存在的3个字段：name、cn_name、image_url）
        cursor.execute("""
            INSERT INTO char_data (name, cn_name, image_url)
            VALUES (%s, %s, %s)
        """, (name, cn_name, image))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "message": "提名成功"})
    
    except Exception as e:
        app.logger.error(f"提名角色错误: {str(e)}")
        return jsonify({"success": False, "message": f"提名失败：{str(e)}"}), 500
    

@app.route("/api/search_character", methods=["POST"])
def search_character():
    data = request.json
    keyword = data.get("keyword", "").strip()
    if not keyword:
        return jsonify({"success": False, "message": "搜索关键词不能为空"}), 400
    
    try:
        url = f"{BANGUMI_API_BASE}/v0/search/characters"
        payload = {
            "keyword": keyword,
            "limit": 20
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "GalMoe-Voting-System/1.0"
        }
        if BANGUMI_API_TOKEN:
            headers["Authorization"] = f"Bearer {BANGUMI_API_TOKEN}"
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        # 仅提取角色ID、名称、中文名称、图像
        characters = []
        for item in result.get("data", []):
            # 获取角色图片（优先large，其次medium）
            image_url = ""
            if item.get("images"):
                image_url = item["images"].get("large", item["images"].get("medium", ""))
            
            # ========== 核心修改：从infobox中提取简体中文名 ==========
            # 1. 先尝试从原有name_cn字段获取（兼容旧格式）
            cn_name = item.get("name_cn", "")
            # 2. 如果name_cn为空，从infobox数组中找「简体中文名」
            if not cn_name and item.get("infobox"):
                for info in item["infobox"]:
                    if info.get("key") == "简体中文名" and info.get("value"):
                        cn_name = info["value"]
                        break  # 找到后立即退出循环，提升效率
            
            characters.append({
                "id": item.get("id"),
                "name": item.get("name", ""),  # 原名（如：ムラサメ）
                "cn_name": cn_name,            # 简体中文名（如：丛雨）
                "image": image_url
            })
        
        return jsonify({
            "success": True,
            "characters": characters
        })
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Bangumi API请求错误: {str(e)}")
        return jsonify({"success": False, "message": f"API请求失败：{str(e)}"}), 500
    except Exception as e:
        app.logger.error(f"服务器错误: {str(e)}")
        return jsonify({"success": False, "message": f"服务器错误：{str(e)}"}), 500


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    qq_number = data.get("qq_number")

    if not qq_number:
        return jsonify({"success": False, "message": "QQ号不能为空"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE qq_number = %s", (qq_number,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        session["user"] = str(user["qq_number"])
        return jsonify({"success": True, "qq_number": str(user["qq_number"])})
    else:
        return jsonify({"success": False, "message": "账号不存在，请通过 @群bot 进行账号注册"})


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"success": True})


@app.route("/me")
def me():
    if "user" in session:
        return jsonify({"logged_in": True, "qq_number": session["user"]})
    else:
        return jsonify({"logged_in": False})


@app.route("/get_current_stage", methods=["GET"])
def get_current_stage():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT data_value FROM system_data WHERE data_name = %s", ('cur_stage',))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return jsonify({"current_stage": result["data_value"]})
    return jsonify({"error": "Current stage not found"}), 404


@app.route("/get_characters", methods=["GET"])
def get_characters():
    try:
        conn = get_db()
        cursor = conn.cursor()
        # 直接查询char_data表的所有字段（匹配name/cn_name/image_url）
        cursor.execute("SELECT name, cn_name, image_url FROM char_data")
        characters = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"characters": characters})
    except Exception as e:
        app.logger.error(f"获取角色列表失败：{str(e)}")
        return jsonify({"error": f"获取角色失败：{str(e)}"}), 500


@app.route("/update_current_stage", methods=["POST"])
def update_current_stage():
    data = request.json
    new_stage = data.get("cur_stage")
    if new_stage:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE system_data SET data_value = %s WHERE data_name = %s", (new_stage, 'cur_stage'))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True})
    return jsonify({"error": "Missing 'cur_stage' data"}), 400

@app.route("/api/preliminary/config", methods=["GET"])
def get_preliminary_config():
    """获取预选赛配置（每人最大票数）"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT data_value FROM system_data WHERE data_name = %s", ('pre_votes_per_user',))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    max_votes = int(result["data_value"]) if result else 20
    return jsonify({"max_votes_per_user": max_votes})

@app.route("/api/preliminary/characters", methods=["GET"])
def get_preliminary_characters():
    """获取所有角色及其当前得票数（从 char_data.pre_votes_total 读取）"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, cn_name, image_url, pre_votes_total as vote_count
        FROM char_data
        ORDER BY pre_votes_total DESC, id ASC
    """)
    characters = cursor.fetchall()
    cursor.close()
    conn.close()
    for char in characters:
        char["vote_count"] = int(char["vote_count"])
    return jsonify({"characters": characters})

@app.route("/api/preliminary/user_votes", methods=["GET"])
def get_user_preliminary_votes():
    """获取当前登录用户已经投了哪些角色（返回角色ID列表）"""
    if "user" not in session:
        return jsonify({"success": False, "message": "未登录"}), 401
    user_qq = session["user"]
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT char_id FROM pre_votes WHERE user_qq = %s", (user_qq,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    voted_ids = [row["char_id"] for row in rows]
    return jsonify({"voted_ids": voted_ids})

@app.route("/api/preliminary/vote", methods=["POST"])
def submit_preliminary_vote():
    if "user" not in session:
        return jsonify({"success": False, "message": "请先登录"}), 401
    user_qq = session["user"]
    data = request.json
    vote_ids = data.get("vote_ids", [])
    if not isinstance(vote_ids, list):
        return jsonify({"success": False, "message": "投票数据格式错误"}), 400
    
    vote_ids = list(set(vote_ids))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 获取最大票数配置
    cursor.execute("SELECT data_value FROM system_data WHERE data_name = %s", ('pre_votes_per_user',))
    config_row = cursor.fetchone()
    max_votes = int(config_row["data_value"]) if config_row else 20
    
    if len(vote_ids) > max_votes:
        return jsonify({"success": False, "message": f"最多只能投{max_votes}票"}), 400
    
    # 检查是否已经投过票
    cursor.execute("SELECT 1 FROM pre_votes WHERE user_qq = %s LIMIT 1", (user_qq,))
    if cursor.fetchone():
        return jsonify({"success": False, "message": "您已经投过票，不能重复提交"}), 400
    
    # 检查角色ID是否存在
    if vote_ids:
        placeholders = ','.join(['%s'] * len(vote_ids))
        cursor.execute(f"SELECT id FROM char_data WHERE id IN ({placeholders})", vote_ids)
        existing_ids = {row["id"] for row in cursor.fetchall()}
        invalid_ids = set(vote_ids) - existing_ids
        if invalid_ids:
            return jsonify({"success": False, "message": f"存在无效角色ID: {invalid_ids}"}), 400
    else:
        return jsonify({"success": False, "message": "请至少选择一个角色"}), 400
    
    try:
        # 插入投票记录
        insert_sql = "INSERT INTO pre_votes (user_qq, char_id) VALUES (%s, %s)"
        for char_id in vote_ids:
            cursor.execute(insert_sql, (user_qq, char_id))
        
        # 更新 char_data 中的冗余票数字段
        update_sql = "UPDATE char_data SET pre_votes_total = pre_votes_total + 1 WHERE id = %s"
        for char_id in vote_ids:
            cursor.execute(update_sql, (char_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True, "message": "投票成功"})
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        app.logger.error(f"提交投票失败: {str(e)}")
        return jsonify({"success": False, "message": f"投票失败: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
