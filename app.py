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

# ==================== 小组赛 ====================

def _get_system_value(conn, data_name: str):
    cursor = conn.cursor()
    cursor.execute("SELECT data_value FROM system_data WHERE data_name = %s", (data_name,))
    row = cursor.fetchone()
    cursor.close()
    return row["data_value"] if row else None

def _fetch_group_stage_matches_with_scores(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            m.id AS match_id,
            m.group_name,
            m.match_order,
            m.char_a_id,
            m.char_b_id,
            a.name AS a_name,
            a.cn_name AS a_cn_name,
            a.image_url AS a_image_url,
            b.name AS b_name,
            b.cn_name AS b_cn_name,
            b.image_url AS b_image_url,
            COALESCE(SUM(CASE WHEN mv.voted_char_id = m.char_a_id THEN 1 ELSE 0 END), 0) AS score_a,
            COALESCE(SUM(CASE WHEN mv.voted_char_id = m.char_b_id THEN 1 ELSE 0 END), 0) AS score_b
        FROM matches m
        JOIN char_data a ON a.id = m.char_a_id
        JOIN char_data b ON b.id = m.char_b_id
        LEFT JOIN match_votes mv ON mv.match_id = m.id
        WHERE m.stage_name = '小组赛'
        GROUP BY m.id
        ORDER BY m.group_name ASC, m.match_order ASC, m.id ASC
    """)
    rows = cursor.fetchall()
    cursor.close()
    for r in rows:
        r["score_a"] = int(r["score_a"] or 0)
        r["score_b"] = int(r["score_b"] or 0)
    return rows

def _compute_group_stage_standings(match_rows):
    # group -> char_id -> stats
    standings = {}
    char_meta = {}

    for r in match_rows:
        a_id = int(r["char_a_id"])
        b_id = int(r["char_b_id"])
        char_meta[a_id] = {"id": a_id, "name": r["a_name"], "cn_name": r.get("a_cn_name") or "", "image_url": r.get("a_image_url") or ""}
        char_meta[b_id] = {"id": b_id, "name": r["b_name"], "cn_name": r.get("b_cn_name") or "", "image_url": r.get("b_image_url") or ""}

    def ensure(group_name, char_id):
        if group_name not in standings:
            standings[group_name] = {}
        if char_id not in standings[group_name]:
            standings[group_name][char_id] = {
                "played": 0,
                "wins": 0,
                "draws": 0,
                "losses": 0,
                "points": 0,
                "goals_for": 0,
                "goals_against": 0,
                "goal_diff": 0,
            }
        return standings[group_name][char_id]

    for r in match_rows:
        group_name = r.get("group_name")
        if not group_name:
            continue
        a_id = int(r["char_a_id"])
        b_id = int(r["char_b_id"])
        score_a = int(r["score_a"] or 0)
        score_b = int(r["score_b"] or 0)

        a = ensure(group_name, a_id)
        b = ensure(group_name, b_id)

        a["played"] += 1
        b["played"] += 1
        a["goals_for"] += score_a
        a["goals_against"] += score_b
        b["goals_for"] += score_b
        b["goals_against"] += score_a

        if score_a > score_b:
            a["wins"] += 1
            a["points"] += 3
            b["losses"] += 1
        elif score_b > score_a:
            b["wins"] += 1
            b["points"] += 3
            a["losses"] += 1
        else:
            a["draws"] += 1
            b["draws"] += 1
            a["points"] += 1
            b["points"] += 1

    # finalize goal diff and format for frontend
    result = {}
    for group_name, group_stats in standings.items():
        rows = []
        for char_id, s in group_stats.items():
            s["goal_diff"] = int(s["goals_for"]) - int(s["goals_against"])
            meta = char_meta.get(char_id, {"id": char_id, "name": "", "cn_name": "", "image_url": ""})
            rows.append({
                **meta,
                **s
            })

        rows.sort(key=lambda x: (-x["points"], -x["goal_diff"], -x["goals_for"], x["name"]))
        result[group_name] = rows
    return result

def _sync_group_stage_caches(conn, match_rows, standings_by_group):
    cursor = conn.cursor()
    try:
        # sync match scores
        cursor.executemany(
            "UPDATE matches SET score_a = %s, score_b = %s WHERE id = %s AND stage_name = '小组赛'",
            [(r["score_a"], r["score_b"], r["match_id"]) for r in match_rows],
        )

        # upsert standings
        upsert_sql = """
            INSERT INTO group_standings
                (group_name, char_id, played, wins, draws, losses, points, goal_diff, goals_for, goals_against)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                played = VALUES(played),
                wins = VALUES(wins),
                draws = VALUES(draws),
                losses = VALUES(losses),
                points = VALUES(points),
                goal_diff = VALUES(goal_diff),
                goals_for = VALUES(goals_for),
                goals_against = VALUES(goals_against)
        """
        payload = []
        for group_name, rows in standings_by_group.items():
            for r in rows:
                payload.append((
                    group_name,
                    r["id"],
                    r["played"],
                    r["wins"],
                    r["draws"],
                    r["losses"],
                    r["points"],
                    r["goal_diff"],
                    r["goals_for"],
                    r["goals_against"],
                ))
        if payload:
            cursor.executemany(upsert_sql, payload)
    finally:
        cursor.close()

@app.route("/api/group_stage/matches", methods=["GET"])
def get_group_stage_matches():
    """获取小组赛所有对战 + 实时票数（按组返回）"""
    conn = get_db()
    try:
        rows = _fetch_group_stage_matches_with_scores(conn)
        if not rows:
            return jsonify({"success": False, "message": "小组赛对战尚未生成，请联系管理员生成分组"}), 400

        groups = {}
        for r in rows:
            group_name = r["group_name"]
            groups.setdefault(group_name, []).append({
                "match_id": r["match_id"],
                "group_name": group_name,
                "match_order": r.get("match_order"),
                "char_a": {
                    "id": r["char_a_id"],
                    "name": r["a_name"],
                    "cn_name": r.get("a_cn_name") or "",
                    "image_url": r.get("a_image_url") or "",
                    "votes": r["score_a"],
                },
                "char_b": {
                    "id": r["char_b_id"],
                    "name": r["b_name"],
                    "cn_name": r.get("b_cn_name") or "",
                    "image_url": r.get("b_image_url") or "",
                    "votes": r["score_b"],
                },
            })

        ordered = {}
        for group_name in sorted(groups.keys()):
            ordered[group_name] = groups[group_name]
        return jsonify({"success": True, "groups": ordered})
    finally:
        conn.close()

@app.route("/api/group_stage/standings", methods=["GET"])
def get_group_stage_standings():
    """获取小组赛实时积分榜（按组返回）"""
    conn = get_db()
    try:
        match_rows = _fetch_group_stage_matches_with_scores(conn)
        if not match_rows:
            return jsonify({"success": False, "message": "小组赛对战尚未生成，请联系管理员生成分组"}), 400
        standings_by_group = _compute_group_stage_standings(match_rows)
        ordered = {}
        for group_name in sorted(standings_by_group.keys()):
            ordered[group_name] = standings_by_group[group_name]
        return jsonify({"success": True, "groups": ordered})
    finally:
        conn.close()

@app.route("/api/group_stage/user_votes", methods=["GET"])
def get_group_stage_user_votes():
    """获取当前登录用户在小组赛已投的对战（用于回显/禁用）"""
    if "user" not in session:
        return jsonify({"success": False, "message": "未登录"}), 401
    user_qq = session["user"]

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT mv.match_id, mv.voted_char_id
            FROM match_votes mv
            JOIN matches m ON m.id = mv.match_id
            WHERE m.stage_name = '小组赛' AND mv.user_qq = %s
        """, (user_qq,))
        rows = cursor.fetchall()
        votes = [{"match_id": r["match_id"], "voted_char_id": r["voted_char_id"]} for r in rows]
        return jsonify({"success": True, "has_voted": len(votes) > 0, "votes": votes})
    finally:
        cursor.close()
        conn.close()

@app.route("/api/group_stage/vote", methods=["POST"])
def submit_group_stage_vote():
    """提交小组赛投票（每组至少投1场；允许部分对战弃票即不提交该场）"""
    if "user" not in session:
        return jsonify({"success": False, "message": "请先登录"}), 401
    user_qq = session["user"]

    data = request.json or {}
    votes = data.get("votes", [])
    if not isinstance(votes, list):
        return jsonify({"success": False, "message": "投票数据格式错误"}), 400
    if not votes:
        return jsonify({"success": False, "message": "请至少选择一场对战"}), 400

    # 去重 match_id，保留最后一次
    by_match = {}
    for item in votes:
        if not isinstance(item, dict):
            continue
        match_id = item.get("match_id")
        voted_char_id = item.get("voted_char_id")
        if match_id is None or voted_char_id is None:
            continue
        try:
            by_match[int(match_id)] = int(voted_char_id)
        except (TypeError, ValueError):
            continue

    if not by_match:
        return jsonify({"success": False, "message": "请至少选择一场对战"}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        cur_stage = _get_system_value(conn, "cur_stage")
        if cur_stage not in ("小组赛", "小组赛阶段"):
            return jsonify({"success": False, "message": "当前不在小组赛阶段，无法投票"}), 400

        # 已投过票：禁止再次提交（按“小组赛任意一票”判断）
        cursor.execute("""
            SELECT 1
            FROM match_votes mv
            JOIN matches m ON m.id = mv.match_id
            WHERE m.stage_name = '小组赛' AND mv.user_qq = %s
            LIMIT 1
        """, (user_qq,))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "您已完成小组赛投票，不能重复提交"}), 400

        match_ids = list(by_match.keys())
        placeholders = ",".join(["%s"] * len(match_ids))
        cursor.execute(f"""
            SELECT id, group_name, char_a_id, char_b_id
            FROM matches
            WHERE stage_name = '小组赛' AND id IN ({placeholders})
        """, match_ids)
        match_rows = cursor.fetchall()
        match_map = {int(r["id"]): r for r in match_rows}

        missing = [mid for mid in match_ids if mid not in match_map]
        if missing:
            return jsonify({"success": False, "message": f"存在无效对战ID: {missing}"}), 400

        # 校验：voted_char_id 必须属于该场对战双方
        votes_payload = []
        voted_groups = set()
        for match_id, voted_char_id in by_match.items():
            r = match_map[match_id]
            a_id = int(r["char_a_id"])
            b_id = int(r["char_b_id"])
            if voted_char_id not in (a_id, b_id):
                return jsonify({"success": False, "message": f"对战 {match_id} 的投票角色不合法"}), 400
            voted_groups.add(r["group_name"])
            votes_payload.append((match_id, user_qq, voted_char_id))

        # 校验：每组至少投 1 场
        cursor.execute("SELECT DISTINCT group_name FROM matches WHERE stage_name = '小组赛' ORDER BY group_name ASC")
        all_groups = [r["group_name"] for r in cursor.fetchall() if r.get("group_name")]
        missing_groups = [g for g in all_groups if g not in voted_groups]
        if missing_groups:
            return jsonify({"success": False, "message": f"每组至少投1场：缺少 {', '.join(missing_groups)} 组"}), 400

        try:
            cursor.executemany(
                "INSERT INTO match_votes (match_id, user_qq, voted_char_id) VALUES (%s, %s, %s)",
                votes_payload,
            )

            # 投票后同步冗余字段（matches.score_a/score_b + group_standings）
            match_rows_scored = _fetch_group_stage_matches_with_scores(conn)
            standings_by_group = _compute_group_stage_standings(match_rows_scored)
            _sync_group_stage_caches(conn, match_rows_scored, standings_by_group)

            conn.commit()
            return jsonify({"success": True, "message": "投票成功"})
        except Exception as e:
            conn.rollback()
            app.logger.error(f"提交小组赛投票失败: {str(e)}")
            return jsonify({"success": False, "message": f"投票失败: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

# ==================== 管理员后台 ====================

def admin_required(f):
    """装饰器：要求当前登录用户为管理员"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({"success": False, "message": "请先登录"}), 401
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE qq_number = %s", (session['user'],))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if not row or row['role'] != 'admin':
            return jsonify({"success": False, "message": "无权限访问"}), 403
        return f(*args, **kwargs)
    return decorated_function

def _fetch_stage_matches_with_scores(conn, stage_name: str):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            m.id AS match_id,
            m.stage_name,
            m.final_type,
            m.group_name,
            m.match_order,
            m.char_a_id,
            m.char_b_id,
            a.name AS a_name,
            a.cn_name AS a_cn_name,
            a.image_url AS a_image_url,
            b.name AS b_name,
            b.cn_name AS b_cn_name,
            b.image_url AS b_image_url,
            COALESCE(SUM(CASE WHEN mv.voted_char_id = m.char_a_id THEN 1 ELSE 0 END), 0) AS score_a,
            COALESCE(SUM(CASE WHEN mv.voted_char_id = m.char_b_id THEN 1 ELSE 0 END), 0) AS score_b
        FROM matches m
        JOIN char_data a ON a.id = m.char_a_id
        JOIN char_data b ON b.id = m.char_b_id
        LEFT JOIN match_votes mv ON mv.match_id = m.id
        WHERE m.stage_name = %s
        GROUP BY m.id
        ORDER BY
            CASE WHEN m.match_order IS NULL THEN 1 ELSE 0 END ASC,
            m.match_order ASC,
            m.id ASC
    """, (stage_name,))
    rows = cursor.fetchall()
    cursor.close()
    for r in rows:
        r["score_a"] = int(r["score_a"] or 0)
        r["score_b"] = int(r["score_b"] or 0)
    return rows

def _get_group_top_two(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            gs.group_name,
            gs.char_id,
            gs.points,
            gs.goal_diff,
            gs.goals_for,
            c.name,
            c.cn_name,
            c.image_url
        FROM group_standings gs
        JOIN char_data c ON c.id = gs.char_id
        ORDER BY
            gs.group_name ASC,
            gs.points DESC,
            gs.goal_diff DESC,
            gs.goals_for DESC,
            gs.char_id ASC
    """)
    rows = cursor.fetchall()
    cursor.close()

    top_two = {}
    for r in rows:
        g = r["group_name"]
        top_two.setdefault(g, [])
        if len(top_two[g]) >= 2:
            continue
        top_two[g].append(r)

    return top_two

@app.route('/admin')
@admin_required
def admin_index():
    """管理员后台页面"""
    return render_template('admin.html')

@app.route('/api/admin/current_stage', methods=['GET'])
@admin_required
def get_admin_current_stage():
    """获取当前阶段"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT data_value FROM system_data WHERE data_name = %s", ('cur_stage',))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify({"stage": row['data_value'] if row else "未开放"})

@app.route('/api/admin/update_stage', methods=['POST'])
@admin_required
def update_stage():
    """更新当前阶段"""
    data = request.json
    new_stage = data.get('stage')
    if not new_stage:
        return jsonify({"success": False, "message": "缺少阶段参数"}), 400
    valid_stages = ["（未开放）", "提名阶段", "预选赛阶段", "小组赛阶段", "淘汰赛（16进8）", "淘汰赛（8进4）", "半决赛", "总决赛", "（完赛）"]
    if new_stage not in valid_stages:
        return jsonify({"success": False, "message": "无效的阶段值"}), 400
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE system_data SET data_value = %s WHERE data_name = %s", (new_stage, 'cur_stage'))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "message": "阶段更新成功"})

@app.route('/api/admin/knockout/generate_preview', methods=['POST'])
@admin_required
def admin_generate_knockout_preview():
    """基于小组赛积分榜生成淘汰赛（16进8）对阵预览"""
    conn = get_db()
    try:
        # 必须已有小组积分数据
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM group_standings LIMIT 1")
        has_rows = cursor.fetchone()
        cursor.close()
        if not has_rows:
            return jsonify({"success": False, "message": "未找到小组赛积分数据，请先生成并完成小组赛投票"}), 400

        top_two = _get_group_top_two(conn)
        required_groups = [chr(65 + i) for i in range(8)]  # A-H
        missing = [g for g in required_groups if g not in top_two or len(top_two[g]) < 2]
        if missing:
            return jsonify({"success": False, "message": f"以下组别积分数据不足2名：{', '.join(missing)}"}), 400

        placements = {}
        for g in required_groups:
            placements[f"{g}1"] = top_two[g][0]
            placements[f"{g}2"] = top_two[g][1]

        pairs = [
            ("第1场", "A1", "B2"),
            ("第2场", "C1", "D2"),
            ("第3场", "E1", "F2"),
            ("第4场", "G1", "H2"),
            ("第5场", "B1", "A2"),
            ("第6场", "D1", "C2"),
            ("第7场", "F1", "E2"),
            ("第8场", "H1", "G2"),
        ]

        preview = []
        for idx, (label, left_key, right_key) in enumerate(pairs, start=1):
            left = placements[left_key]
            right = placements[right_key]
            preview.append({
                "match_order": idx,
                "label": label,
                "left_tag": left_key,
                "right_tag": right_key,
                "char_a": {
                    "id": left["char_id"],
                    "name": left["name"],
                    "cn_name": left.get("cn_name") or "",
                    "image_url": left.get("image_url") or "",
                    "points": int(left["points"]),
                    "goal_diff": int(left["goal_diff"]),
                    "goals_for": int(left["goals_for"]),
                },
                "char_b": {
                    "id": right["char_id"],
                    "name": right["name"],
                    "cn_name": right.get("cn_name") or "",
                    "image_url": right.get("image_url") or "",
                    "points": int(right["points"]),
                    "goal_diff": int(right["goal_diff"]),
                    "goals_for": int(right["goals_for"]),
                },
            })

        return jsonify({"success": True, "stage_name": "淘汰赛（16进8）", "matches": preview})
    finally:
        conn.close()

@app.route('/api/admin/knockout/confirm', methods=['POST'])
@admin_required
def admin_confirm_knockout_round16():
    """确认生成淘汰赛（16进8）对阵（写入 matches）"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 1 FROM matches WHERE stage_name = '淘汰赛（16进8）' LIMIT 1")
        if cursor.fetchone():
            return jsonify({"success": False, "message": "淘汰赛（16进8）对阵已存在，请勿重复生成"}), 400

        top_two = _get_group_top_two(conn)
        required_groups = [chr(65 + i) for i in range(8)]  # A-H
        missing = [g for g in required_groups if g not in top_two or len(top_two[g]) < 2]
        if missing:
            return jsonify({"success": False, "message": f"以下组别积分数据不足2名：{', '.join(missing)}"}), 400

        placements = {}
        for g in required_groups:
            placements[f"{g}1"] = int(top_two[g][0]["char_id"])
            placements[f"{g}2"] = int(top_two[g][1]["char_id"])

        pairs = [
            ("A1", "B2"),
            ("C1", "D2"),
            ("E1", "F2"),
            ("G1", "H2"),
            ("B1", "A2"),
            ("D1", "C2"),
            ("F1", "E2"),
            ("H1", "G2"),
        ]

        insert_payload = []
        for idx, (left_key, right_key) in enumerate(pairs, start=1):
            insert_payload.append((
                "淘汰赛（16进8）",
                None,
                idx,
                placements[left_key],
                placements[right_key],
                "pending",
            ))

        cursor.executemany("""
            INSERT INTO matches (stage_name, group_name, match_order, char_a_id, char_b_id, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, insert_payload)
        conn.commit()
        return jsonify({"success": True, "message": "淘汰赛（16进8）对阵已生成"})
    except Exception as e:
        conn.rollback()
        app.logger.error(f"生成淘汰赛（16进8）对阵失败: {str(e)}")
        return jsonify({"success": False, "message": f"操作失败: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

def _knockout_next_stage_name(stage_name: str):
    mapping = {
        "淘汰赛（16进8）": "淘汰赛（8进4）",
        "淘汰赛（8进4）": "半决赛",
        "半决赛": "总决赛",
        "总决赛": "（完赛）",
    }
    return mapping.get(stage_name)

def _knockout_build_next_matches(stage_name: str, matches_with_scores):
    # matches_with_scores must be ordered in bracket order.
    winners = []
    losers = []
    scored_preview = []

    for m in matches_with_scores:
        a_votes = int(m["score_a"])
        b_votes = int(m["score_b"])
        if a_votes == b_votes:
            scored_preview.append({**m, "result": "tie"})
            continue
        if a_votes > b_votes:
            winner_id = int(m["char_a_id"])
            loser_id = int(m["char_b_id"])
        else:
            winner_id = int(m["char_b_id"])
            loser_id = int(m["char_a_id"])
        winners.append(winner_id)
        losers.append(loser_id)
        scored_preview.append({**m, "winner_id": winner_id, "loser_id": loser_id, "result": "ok"})

    if any(x["result"] == "tie" for x in scored_preview):
        tied = [x["match_id"] for x in scored_preview if x["result"] == "tie"]
        return {"error": f"存在平票对战，无法结算：{tied}"}

    next_stage = _knockout_next_stage_name(stage_name)
    if not next_stage:
        return {"error": f"当前阶段不支持结算：{stage_name}"}

    next_matches = []
    if stage_name == "淘汰赛（16进8）":
        if len(winners) != 8:
            return {"error": "对阵数量不足，无法生成 8 进 4"}
        pairs = [(0, 1), (2, 3), (4, 5), (6, 7)]
        for idx, (i, j) in enumerate(pairs, start=1):
            next_matches.append({
                "match_order": idx,
                "char_a_id": winners[i],
                "char_b_id": winners[j],
            })
    elif stage_name == "淘汰赛（8进4）":
        if len(winners) != 4:
            return {"error": "对阵数量不足，无法生成半决赛"}
        pairs = [(0, 1), (2, 3)]
        for idx, (i, j) in enumerate(pairs, start=1):
            next_matches.append({
                "match_order": idx,
                "char_a_id": winners[i],
                "char_b_id": winners[j],
            })
    elif stage_name == "半决赛":
        if len(winners) != 2 or len(losers) != 2:
            return {"error": "对阵数量不足，无法生成总决赛/季军战"}
        # losers[0] is from match 13, losers[1] from match 14
        next_matches.append({
            "match_order": 1,
            "final_type": "third_place",
            "char_a_id": losers[0],
            "char_b_id": losers[1],
        })
        next_matches.append({
            "match_order": 2,
            "final_type": "championship",
            "char_a_id": winners[0],
            "char_b_id": winners[1],
        })
    elif stage_name == "总决赛":
        # 总决赛包含两场：季军战 + 冠军赛。结算后进入（完赛），不生成下一阶段对阵。
        if len(matches_with_scores) < 2:
            return {"error": "对阵数量不足，无法结算总决赛"}
        # winners/losers 已在上方计算
        if len(winners) != 2:
            return {"error": "总决赛存在平票或异常，无法结算"}

    return {"next_stage": next_stage, "current_scored": scored_preview, "next_matches": next_matches}

def _validate_knockout_stage_name(stage_name: str):
    allowed = {"淘汰赛（16进8）", "淘汰赛（8进4）", "半决赛", "总决赛"}
    return stage_name in allowed

@app.route('/api/results', methods=['GET'])
def get_results():
    """赛事结果：仅在（完赛）后提供前三名"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cur_stage = _get_system_value(conn, "cur_stage")
        if cur_stage != "（完赛）":
            return jsonify({"success": True, "finished": False})

        # 决赛（冠军赛）
        cursor.execute("""
            SELECT
                m.id,
                m.winner_id,
                m.char_a_id,
                m.char_b_id,
                m.score_a,
                m.score_b
            FROM matches m
            WHERE m.stage_name = '总决赛' AND m.final_type = 'championship'
            ORDER BY m.id DESC
            LIMIT 1
        """)
        final_match = cursor.fetchone()
        if not final_match or not final_match.get("winner_id"):
            return jsonify({"success": True, "finished": False})

        champion_id = int(final_match["winner_id"])
        a_id = int(final_match["char_a_id"])
        b_id = int(final_match["char_b_id"])
        runner_up_id = b_id if champion_id == a_id else a_id

        # 季军战
        cursor.execute("""
            SELECT
                m.id,
                m.winner_id,
                m.char_a_id,
                m.char_b_id,
                m.score_a,
                m.score_b
            FROM matches m
            WHERE m.stage_name = '总决赛' AND m.final_type = 'third_place'
            ORDER BY m.id DESC
            LIMIT 1
        """)
        third_match = cursor.fetchone()
        if not third_match or not third_match.get("winner_id"):
            return jsonify({"success": True, "finished": False})

        third_id = int(third_match["winner_id"])

        ids = [champion_id, runner_up_id, third_id]
        placeholders = ",".join(["%s"] * len(ids))
        cursor.execute(f"SELECT id, name, cn_name, image_url FROM char_data WHERE id IN ({placeholders})", ids)
        chars = {int(r["id"]): r for r in cursor.fetchall()}

        return jsonify({
            "success": True,
            "finished": True,
            "top3": {
                "champion": chars.get(champion_id),
                "runner_up": chars.get(runner_up_id),
                "third": chars.get(third_id),
            }
        })
    finally:
        cursor.close()
        conn.close()

@app.route('/api/knockout/matches', methods=['GET'])
def get_knockout_matches():
    """获取淘汰赛某阶段对阵 + 实时票数"""
    stage_name = (request.args.get("stage") or "").strip()
    if not _validate_knockout_stage_name(stage_name):
        return jsonify({"success": False, "message": "无效阶段参数"}), 400

    conn = get_db()
    try:
        rows = _fetch_stage_matches_with_scores(conn, stage_name)
        if not rows:
            return jsonify({"success": True, "stage_name": stage_name, "matches": []})

        matches = []
        for r in rows:
            matches.append({
                "match_id": r["match_id"],
                "stage_name": r["stage_name"],
                "final_type": r.get("final_type"),
                "match_order": r.get("match_order"),
                "char_a": {
                    "id": r["char_a_id"],
                    "name": r["a_name"],
                    "cn_name": r.get("a_cn_name") or "",
                    "image_url": r.get("a_image_url") or "",
                    "votes": int(r["score_a"] or 0),
                },
                "char_b": {
                    "id": r["char_b_id"],
                    "name": r["b_name"],
                    "cn_name": r.get("b_cn_name") or "",
                    "image_url": r.get("b_image_url") or "",
                    "votes": int(r["score_b"] or 0),
                },
            })
        return jsonify({"success": True, "stage_name": stage_name, "matches": matches})
    finally:
        conn.close()

@app.route('/api/knockout/user_votes', methods=['GET'])
def get_knockout_user_votes():
    """获取当前登录用户在淘汰赛某阶段已投的对战（用于回显/禁用）"""
    if "user" not in session:
        return jsonify({"success": False, "message": "未登录"}), 401
    stage_name = (request.args.get("stage") or "").strip()
    if not _validate_knockout_stage_name(stage_name):
        return jsonify({"success": False, "message": "无效阶段参数"}), 400

    user_qq = session["user"]
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT mv.match_id, mv.voted_char_id
            FROM match_votes mv
            JOIN matches m ON m.id = mv.match_id
            WHERE m.stage_name = %s AND mv.user_qq = %s
        """, (stage_name, user_qq))
        rows = cursor.fetchall()
        votes = [{"match_id": int(r["match_id"]), "voted_char_id": int(r["voted_char_id"])} for r in rows]
        return jsonify({"success": True, "votes": votes})
    finally:
        cursor.close()
        conn.close()

@app.route('/api/knockout/vote', methods=['POST'])
def submit_knockout_vote():
    """提交淘汰赛某阶段投票：必须每场选一方，不可弃票"""
    if "user" not in session:
        return jsonify({"success": False, "message": "请先登录"}), 401
    user_qq = session["user"]

    data = request.json or {}
    stage_name = (data.get("stage") or "").strip()
    votes = data.get("votes", [])

    if not _validate_knockout_stage_name(stage_name):
        return jsonify({"success": False, "message": "无效阶段参数"}), 400
    if not isinstance(votes, list):
        return jsonify({"success": False, "message": "投票数据格式错误"}), 400

    # 去重 match_id，保留最后一次
    by_match = {}
    for item in votes:
        if not isinstance(item, dict):
            continue
        match_id = item.get("match_id")
        voted_char_id = item.get("voted_char_id")
        if match_id is None or voted_char_id is None:
            continue
        try:
            by_match[int(match_id)] = int(voted_char_id)
        except (TypeError, ValueError):
            continue

    if not by_match:
        return jsonify({"success": False, "message": "请先完成本阶段所有对战选择"}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        cur_stage = _get_system_value(conn, "cur_stage")
        if cur_stage != stage_name:
            return jsonify({"success": False, "message": "当前不在该阶段，无法投票"}), 400

        # 查询本阶段所有对战
        cursor.execute("""
            SELECT id, char_a_id, char_b_id
            FROM matches
            WHERE stage_name = %s
            ORDER BY
                CASE WHEN match_order IS NULL THEN 1 ELSE 0 END ASC,
                match_order ASC,
                id ASC
        """, (stage_name,))
        stage_matches = cursor.fetchall()
        if not stage_matches:
            return jsonify({"success": False, "message": "本阶段对阵尚未生成"}), 400

        all_match_ids = [int(r["id"]) for r in stage_matches]
        if set(by_match.keys()) != set(all_match_ids):
            return jsonify({"success": False, "message": "必须对本阶段每场对战投票（不可弃票）"}), 400

        # 已投过票：禁止再次提交（按该阶段任意一票判断）
        placeholders = ",".join(["%s"] * len(all_match_ids))
        cursor.execute(f"""
            SELECT 1
            FROM match_votes
            WHERE user_qq = %s AND match_id IN ({placeholders})
            LIMIT 1
        """, [user_qq, *all_match_ids])
        if cursor.fetchone():
            return jsonify({"success": False, "message": "您已完成本阶段投票，不能重复提交"}), 400

        match_map = {int(r["id"]): r for r in stage_matches}
        payload = []
        for match_id, voted_char_id in by_match.items():
            r = match_map[match_id]
            a_id = int(r["char_a_id"])
            b_id = int(r["char_b_id"])
            if voted_char_id not in (a_id, b_id):
                return jsonify({"success": False, "message": f"对战 {match_id} 的投票角色不合法"}), 400
            payload.append((match_id, user_qq, voted_char_id))

        cursor.executemany(
            "INSERT INTO match_votes (match_id, user_qq, voted_char_id) VALUES (%s, %s, %s)",
            payload,
        )
        conn.commit()
        return jsonify({"success": True, "message": "投票成功"})
    except Exception as e:
        conn.rollback()
        app.logger.error(f"提交淘汰赛投票失败: {str(e)}")
        return jsonify({"success": False, "message": f"投票失败: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/admin/knockout/settle_preview', methods=['POST'])
@admin_required
def admin_knockout_settle_preview():
    """根据 system_data.cur_stage 统计票数并预览下一阶段对阵"""
    conn = get_db()
    try:
        cur_stage = _get_system_value(conn, "cur_stage")
        if not cur_stage:
            return jsonify({"success": False, "message": "未找到当前阶段（cur_stage）"}), 400

        stage_name = cur_stage
        if stage_name == "（完赛）":
            return jsonify({"success": False, "message": "赛事已完赛，无需结算"}), 400
        if stage_name == "小组赛阶段" or stage_name == "小组赛":
            return jsonify({"success": False, "message": "当前阶段为小组赛，不适用淘汰赛结算"}), 400

        rows = _fetch_stage_matches_with_scores(conn, stage_name)
        if not rows:
            return jsonify({"success": False, "message": f"未找到阶段「{stage_name}」的对阵数据"}), 400

        built = _knockout_build_next_matches(stage_name, rows)
        if built.get("error"):
            return jsonify({"success": False, "message": built["error"]}), 400

        # enrich preview with names for next stage matches（总决赛结算后 next_matches 为空）
        next_preview = []
        if built["next_matches"]:
            cursor = conn.cursor()
            ids = []
            for m in built["next_matches"]:
                ids.append(int(m["char_a_id"]))
                ids.append(int(m["char_b_id"]))
            placeholders = ",".join(["%s"] * len(ids))
            cursor.execute(f"SELECT id, name, cn_name, image_url FROM char_data WHERE id IN ({placeholders})", ids)
            chars = {int(r["id"]): r for r in cursor.fetchall()}
            cursor.close()

            for idx, m in enumerate(built["next_matches"], start=1):
                next_preview.append({
                    "match_order": m.get("match_order", idx),
                    "final_type": m.get("final_type"),
                    "char_a": chars.get(int(m["char_a_id"]), {"id": m["char_a_id"], "name": "", "cn_name": "", "image_url": ""}),
                    "char_b": chars.get(int(m["char_b_id"]), {"id": m["char_b_id"], "name": "", "cn_name": "", "image_url": ""}),
                })

        current_scored = []
        for m in built["current_scored"]:
            current_scored.append({
                "match_id": m["match_id"],
                "match_order": m.get("match_order"),
                "char_a": {"id": m["char_a_id"], "name": m["a_name"]},
                "char_b": {"id": m["char_b_id"], "name": m["b_name"]},
                "score_a": int(m["score_a"]),
                "score_b": int(m["score_b"]),
            })

        return jsonify({
            "success": True,
            "current_stage": stage_name,
            "next_stage": built["next_stage"],
            "current_matches": current_scored,
            "next_matches": next_preview,
        })
    finally:
        conn.close()

@app.route('/api/admin/knockout/settle_confirm', methods=['POST'])
@admin_required
def admin_knockout_settle_confirm():
    """结算当前淘汰赛阶段：写入胜者/比分，并生成下一阶段 matches"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cur_stage = _get_system_value(conn, "cur_stage")
        if not cur_stage:
            return jsonify({"success": False, "message": "未找到当前阶段（cur_stage）"}), 400

        stage_name = cur_stage
        next_stage = _knockout_next_stage_name(stage_name)
        if not next_stage:
            return jsonify({"success": False, "message": f"当前阶段不支持结算：{stage_name}"}), 400

        # 防重复（总决赛结算后不生成对阵，仅改阶段）
        if stage_name != "总决赛":
            cursor.execute("SELECT 1 FROM matches WHERE stage_name = %s LIMIT 1", (next_stage,))
            if cursor.fetchone():
                return jsonify({"success": False, "message": f"下一阶段「{next_stage}」对阵已存在，请勿重复结算"}), 400

        rows = _fetch_stage_matches_with_scores(conn, stage_name)
        if not rows:
            return jsonify({"success": False, "message": f"未找到阶段「{stage_name}」的对阵数据"}), 400

        built = _knockout_build_next_matches(stage_name, rows)
        if built.get("error"):
            return jsonify({"success": False, "message": built["error"]}), 400

        # 更新当前阶段 matches 的比分与胜者
        update_payload = []
        for m in built["current_scored"]:
            a_votes = int(m["score_a"])
            b_votes = int(m["score_b"])
            if a_votes == b_votes:
                return jsonify({"success": False, "message": "存在平票对战，无法结算"}), 400
            if a_votes > b_votes:
                winner_id = int(m["char_a_id"])
            else:
                winner_id = int(m["char_b_id"])
            update_payload.append((a_votes, b_votes, winner_id, "completed", m["match_id"]))

        cursor.executemany("""
            UPDATE matches
            SET score_a = %s, score_b = %s, winner_id = %s, status = %s, end_time = NOW()
            WHERE id = %s
        """, update_payload)

        # 插入下一阶段对阵（总决赛结算后不生成对阵）
        if stage_name != "总决赛":
            insert_payload = []
            for idx, m in enumerate(built["next_matches"], start=1):
                insert_payload.append((
                    built["next_stage"],
                    m.get("final_type"),
                    None,
                    m.get("match_order", idx),
                    int(m["char_a_id"]),
                    int(m["char_b_id"]),
                    "pending",
                ))

            cursor.executemany("""
                INSERT INTO matches (stage_name, final_type, group_name, match_order, char_a_id, char_b_id, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, insert_payload)

        # 自动推进阶段
        cursor.execute("UPDATE system_data SET data_value = %s WHERE data_name = %s", (next_stage, 'cur_stage'))

        conn.commit()
        if stage_name == "总决赛":
            return jsonify({"success": True, "message": "结算成功：赛事已完赛，当前阶段已更新为「（完赛）」"})
        return jsonify({"success": True, "message": f"结算成功：已生成下一阶段「{built['next_stage']}」对阵，并自动切换当前阶段"})
    except Exception as e:
        conn.rollback()
        app.logger.error(f"淘汰赛结算失败: {str(e)}")
        return jsonify({"success": False, "message": f"操作失败: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/admin/delete_user_votes', methods=['POST'])
@admin_required
def delete_user_votes():
    """删除指定用户的预选赛投票，并同步更新 char_data.pre_votes_total"""
    data = request.json
    user_qq = data.get('user_qq')
    if not user_qq:
        return jsonify({"success": False, "message": "QQ号不能为空"}), 400
    conn = get_db()
    cursor = conn.cursor()
    # 获取该用户投过的角色ID列表
    cursor.execute("SELECT char_id FROM pre_votes WHERE user_qq = %s", (user_qq,))
    votes = cursor.fetchall()
    if not votes:
        cursor.close()
        conn.close()
        return jsonify({"success": False, "message": f"用户 {user_qq} 没有预选赛投票记录"}), 404
    char_ids = [row['char_id'] for row in votes]
    try:
        # 删除投票记录
        cursor.execute("DELETE FROM pre_votes WHERE user_qq = %s", (user_qq,))
        # 更新每个角色的票数
        for char_id in char_ids:
            cursor.execute("UPDATE char_data SET pre_votes_total = pre_votes_total - 1 WHERE id = %s", (char_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True, "message": f"已删除用户 {user_qq} 的 {len(char_ids)} 条投票记录"})
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        app.logger.error(f"删除用户投票失败: {str(e)}")
        return jsonify({"success": False, "message": f"操作失败: {str(e)}"}), 500

@app.route('/api/admin/delete_user_group_votes', methods=['POST'])
@admin_required
def delete_user_group_votes():
    """删除指定用户的小组赛投票（match_votes.stage_name='小组赛'），并同步积分/比分缓存"""
    data = request.json or {}
    user_qq = data.get('user_qq')
    if not user_qq:
        return jsonify({"success": False, "message": "QQ号不能为空"}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT 1
            FROM match_votes mv
            JOIN matches m ON m.id = mv.match_id
            WHERE mv.user_qq = %s AND m.stage_name = '小组赛'
            LIMIT 1
        """, (user_qq,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "该用户当前阶段未投票"}), 400

        cursor.execute("""
            DELETE mv FROM match_votes mv
            JOIN matches m ON m.id = mv.match_id
            WHERE mv.user_qq = %s AND m.stage_name = '小组赛'
        """, (user_qq,))

        match_rows_scored = _fetch_group_stage_matches_with_scores(conn)
        standings_by_group = _compute_group_stage_standings(match_rows_scored)
        _sync_group_stage_caches(conn, match_rows_scored, standings_by_group)

        conn.commit()
        return jsonify({"success": True, "message": "已删除该用户小组赛投票"})
    except Exception as e:
        conn.rollback()
        app.logger.error(f"删除用户小组赛投票失败: {str(e)}")
        return jsonify({"success": False, "message": f"操作失败: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/admin/delete_user_knockout_votes', methods=['POST'])
@admin_required
def delete_user_knockout_votes():
    """删除指定用户的某一淘汰赛阶段投票（match_votes.stage_name=指定阶段）"""
    data = request.json or {}
    user_qq = data.get('user_qq')
    stage = (data.get('stage') or '').strip()
    if not user_qq:
        return jsonify({"success": False, "message": "QQ号不能为空"}), 400
    if stage not in {"淘汰赛（16进8）", "淘汰赛（8进4）", "半决赛", "总决赛"}:
        return jsonify({"success": False, "message": "无效的阶段参数"}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT 1
            FROM match_votes mv
            JOIN matches m ON m.id = mv.match_id
            WHERE mv.user_qq = %s AND m.stage_name = %s
            LIMIT 1
        """, (user_qq, stage))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "该用户当前阶段未投票"}), 400

        cursor.execute("""
            DELETE mv FROM match_votes mv
            JOIN matches m ON m.id = mv.match_id
            WHERE mv.user_qq = %s AND m.stage_name = %s
        """, (user_qq, stage))

        # 重新写回该阶段 matches.score_a/score_b（避免历史缓存影响展示/结算）
        scored = _fetch_stage_matches_with_scores(conn, stage)
        if scored:
            cursor.executemany(
                "UPDATE matches SET score_a = %s, score_b = %s WHERE id = %s AND stage_name = %s",
                [(m["score_a"], m["score_b"], m["match_id"], stage) for m in scored],
            )

        conn.commit()
        return jsonify({"success": True, "message": f"已删除该用户{stage}投票"})
    except Exception as e:
        conn.rollback()
        app.logger.error(f"删除用户淘汰赛投票失败: {str(e)}")
        return jsonify({"success": False, "message": f"操作失败: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/admin/generate_groups', methods=['POST'])
@admin_required
def generate_groups():
    """根据预选赛排名生成蛇形分组，返回分组预览数据"""
    conn = get_db()
    cursor = conn.cursor()
    # 获取所有角色按预选赛票数降序排列，取前32名
    cursor.execute("""
        SELECT id, name, pre_votes_total
        FROM char_data
        ORDER BY pre_votes_total DESC, id ASC
        LIMIT 32
    """)
    chars = cursor.fetchall()
    if len(chars) < 32:
        return jsonify({"success": False, "message": f"角色不足32人（当前{len(chars)}人），无法进行小组赛分组"}), 400
    # 蛇形分组：8组，每组4人
    # 分组逻辑：第1名->A1, 第2名->B1, ... 第8名->H1,
    # 第9名->H2, 第10名->G2, ... 第16名->A2,
    # 第17名->A3, ... 第24名->H3,
    # 第25名->H4, ... 第32名->A4
    groups = {chr(65+i): [] for i in range(8)}  # A-H
    for idx, char in enumerate(chars):
        # 索引从0开始
        row = idx // 8        # 0,1,2,3 对应第几轮（每组第几个）
        col = idx % 8         # 0-7 对应组号
        if row % 2 == 0:
            # 偶数轮（0,2）：正序分配组别
            group_name = chr(65 + col)
        else:
            # 奇数轮（1,3）：倒序分配组别
            group_name = chr(65 + (7 - col))
        groups[group_name].append({
            "id": char['id'],
            "name": char['name'],
            "vote_count": char['pre_votes_total']
        })
    # 构建返回数据：每个组按组内序号（即加入顺序）排序
    result = {}
    for group_name in sorted(groups.keys()):
        result[group_name] = groups[group_name]
    cursor.close()
    conn.close()
    return jsonify({"success": True, "groups": result})

@app.route('/api/admin/confirm_groups', methods=['POST'])
@admin_required
def confirm_groups():
    """确认分组，将分组信息写入 matches 和 group_standings 表"""
    # 首先检查是否已存在小组赛数据（避免重复生成）
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM matches WHERE stage_name = '小组赛' LIMIT 1")
    if cursor.fetchone():
        return jsonify({"success": False, "message": "小组赛已存在，请先清理数据后再生成"}), 400
    # 获取分组数据（实际可从请求体获取，但为了安全，重新生成一次）
    cursor.execute("""
        SELECT id, name, pre_votes_total
        FROM char_data
        ORDER BY pre_votes_total DESC, id ASC
        LIMIT 32
    """)
    chars = cursor.fetchall()
    if len(chars) < 32:
        return jsonify({"success": False, "message": f"角色不足32人（当前{len(chars)}人），无法进行小组赛分组"}), 400
    groups = {chr(65+i): [] for i in range(8)}
    for idx, char in enumerate(chars):
        row = idx // 8
        col = idx % 8
        if row % 2 == 0:
            group_name = chr(65 + col)
        else:
            group_name = chr(65 + (7 - col))
        groups[group_name].append(char['id'])
    try:
        # 1. 插入小组积分初始数据
        for group_name, char_ids in groups.items():
            for char_id in char_ids:
                cursor.execute("""
                    INSERT INTO group_standings (group_name, char_id, played, wins, draws, losses, points, goal_diff, goals_for, goals_against)
                    VALUES (%s, %s, 0, 0, 0, 0, 0, 0, 0, 0)
                """, (group_name, char_id))
        # 2. 生成小组赛比赛对阵（每组4人，循环赛，共6场）
        match_order = 1
        for group_name, char_ids in groups.items():
            # 生成该组所有两两组合
            for i in range(4):
                for j in range(i+1, 4):
                    cursor.execute("""
                        INSERT INTO matches (stage_name, group_name, match_order, char_a_id, char_b_id, status)
                        VALUES ('小组赛', %s, %s, %s, %s, 'pending')
                    """, (group_name, match_order, char_ids[i], char_ids[j]))
                    match_order += 1
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True, "message": "小组赛分组已生成"})
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        app.logger.error(f"生成小组赛分组失败: {str(e)}")
        return jsonify({"success": False, "message": f"操作失败: {str(e)}"}), 500

@app.route('/api/admin/clear_group_data', methods=['POST'])
@admin_required
def clear_group_data():
    """清空小组赛数据（比赛、积分、投票记录）"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        # 删除小组赛的投票记录
        cursor.execute("""
            DELETE FROM match_votes 
            WHERE match_id IN (SELECT id FROM (SELECT id FROM matches WHERE stage_name = '小组赛') AS tmp)
        """)
        # 删除小组赛比赛
        cursor.execute("DELETE FROM matches WHERE stage_name = '小组赛'")
        # 删除小组积分数据
        cursor.execute("DELETE FROM group_standings")
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True, "message": "小组赛数据已清空"})
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        app.logger.error(f"清空小组赛数据失败: {str(e)}")
        return jsonify({"success": False, "message": f"清空失败: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
