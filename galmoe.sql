/*
 Navicat Premium Data Transfer

 Source Server         : MySQL
 Source Server Type    : MySQL
 Source Server Version : 80042
 Source Host           : localhost:3306
 Source Schema         : galmoe

 Target Server Type    : MySQL
 Target Server Version : 80042
 File Encoding         : 65001

 Date: 22/04/2026 00:08:04
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for char_data
-- ----------------------------
DROP TABLE IF EXISTS `char_data`;
CREATE TABLE `char_data`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cn_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `image_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `pre_votes_total` int NOT NULL DEFAULT 0 COMMENT '预选赛总得票数（实时更新）',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 39 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of char_data
-- ----------------------------
INSERT INTO `char_data` VALUES (3, '二階堂ヒロ', '二阶堂希罗', 'https://lain.bgm.tv/pic/crt/l/b7/80/154882_crt_CDcuA.jpg', 2);
INSERT INTO `char_data` VALUES (4, '桜羽エマ', '樱羽艾玛', 'https://lain.bgm.tv/pic/crt/l/4f/66/154881_crt_udaOq.jpg', 2);
INSERT INTO `char_data` VALUES (5, 'ムラサメ', '丛雨', 'https://lain.bgm.tv/pic/crt/l/6f/34/39362_crt_oM36R.jpg', 1);
INSERT INTO `char_data` VALUES (6, '纳西妲', '布耶尔', 'https://lain.bgm.tv/pic/crt/l/b8/b2/112644_crt_zhh2S.jpg?r=1666590070', 0);
INSERT INTO `char_data` VALUES (7, '綾地寧々', '绫地宁宁', 'https://lain.bgm.tv/pic/crt/l/4e/eb/27371_crt_z99iG.jpg', 1);
INSERT INTO `char_data` VALUES (8, '二階堂真紅', '二阶堂真红', 'https://lain.bgm.tv/pic/crt/l/52/65/12234_crt_wYtk4.jpg', 1);
INSERT INTO `char_data` VALUES (9, '乙津夢', '乙津梦', 'https://lain.bgm.tv/pic/crt/l/77/b1/11015_crt_eJL2l.jpg', 3);
INSERT INTO `char_data` VALUES (10, 'メア=S=エフェメラル', '梅娅·S·艾菲梅拉尔', 'https://lain.bgm.tv/pic/crt/l/e3/0e/11014_crt_Sa0Hh.jpg', 2);
INSERT INTO `char_data` VALUES (11, 'ベアトリーチェ', '贝阿朵莉切', 'https://lain.bgm.tv/pic/crt/l/54/39/944_crt_FYVzB.jpg?r=1677396175', 2);
INSERT INTO `char_data` VALUES (12, '鑑純夏', '鉴纯夏', 'https://lain.bgm.tv/pic/crt/l/d8/37/16868_crt_lI0Fn.jpg', 1);
INSERT INTO `char_data` VALUES (13, 'ルルティエ', '露露缇耶', 'https://lain.bgm.tv/pic/crt/l/c6/78/35099_crt_U3gKx.jpg', 1);
INSERT INTO `char_data` VALUES (14, 'クオン', '久远', 'https://lain.bgm.tv/pic/crt/l/78/80/33173_crt_5Dr0d.jpg', 2);
INSERT INTO `char_data` VALUES (15, '隠杏珠', '隐杏珠', 'https://lain.bgm.tv/pic/crt/l/80/1d/177392_crt_nQNQ9.jpg?r=1750858577', 0);
INSERT INTO `char_data` VALUES (16, '白河ほたる', '白河萤', 'https://lain.bgm.tv/pic/crt/l/03/b4/12967_crt_3Jg7b.jpg', 0);
INSERT INTO `char_data` VALUES (17, '四季ナツメ', '四季夏目', 'https://lain.bgm.tv/pic/crt/l/04/1c/71524_crt_79Fww.jpg?r=1574872110', 1);
INSERT INTO `char_data` VALUES (18, 'メアリー・ハーカー', '玛丽·哈卡', 'https://lain.bgm.tv/pic/crt/l/ad/39/56364_crt_edIaD.jpg', 0);
INSERT INTO `char_data` VALUES (19, '織部こころ', '织部心', 'https://lain.bgm.tv/pic/crt/l/97/48/39703_crt_TZI1Z.jpg', 1);
INSERT INTO `char_data` VALUES (20, '柳木詩夢', '柳木诗梦', 'https://lain.bgm.tv/pic/crt/l/1b/bf/176735_crt_yw5Wn.jpg?r=1748488049', 1);
INSERT INTO `char_data` VALUES (21, '倉木鈴菜', '仓木铃菜', 'https://lain.bgm.tv/pic/crt/l/b8/f0/21408_crt_Q31VY.jpg', 1);
INSERT INTO `char_data` VALUES (22, '陽坂美都子', '阳坂美都子', 'https://lain.bgm.tv/pic/crt/l/33/33/22260_crt_bPPPo.jpg', 1);
INSERT INTO `char_data` VALUES (23, '鳴河千歳', '鸣河千岁', 'https://lain.bgm.tv/pic/crt/l/4b/0d/33508_crt_L7G7R.jpg', 1);
INSERT INTO `char_data` VALUES (24, '橘観美', '橘观美', 'https://lain.bgm.tv/pic/crt/l/68/ce/33509_crt_u6mp4.jpg', 1);
INSERT INTO `char_data` VALUES (25, '天ノ川沙夜', '天之川沙夜', 'https://lain.bgm.tv/pic/crt/l/95/70/34203_crt_pzHDF.jpg', 2);
INSERT INTO `char_data` VALUES (26, 'シーラ・ヘルマン', '希拉·赫尔曼', 'https://lain.bgm.tv/pic/crt/l/02/55/36559_crt_nw5h7.jpg', 2);
INSERT INTO `char_data` VALUES (27, '見当かなみ', '见当加奈美', 'https://lain.bgm.tv/pic/crt/l/cf/0a/22097_crt_l6R2O.jpg', 1);
INSERT INTO `char_data` VALUES (28, '桜来瑞花', '樱来瑞花', 'https://lain.bgm.tv/pic/crt/l/35/d6/115390_crt_4q700.jpg', 1);
INSERT INTO `char_data` VALUES (29, '八坂愛乃亜', '八坂爱乃亚', 'https://lain.bgm.tv/pic/crt/l/74/16/115391_crt_8qCoW.jpg', 1);
INSERT INTO `char_data` VALUES (30, '月社妃', '月社妃', 'https://lain.bgm.tv/pic/crt/l/81/f3/26422_crt_0XoSm.jpg', 1);
INSERT INTO `char_data` VALUES (31, '日向かなた', '日向彼方', 'https://lain.bgm.tv/pic/crt/l/46/10/26424_crt_hPZeu.jpg', 1);
INSERT INTO `char_data` VALUES (32, '鳶沢みさき', '鸢泽美咲', 'https://lain.bgm.tv/pic/crt/l/b8/82/22881_crt_FG9mm.jpg?r=1459502612', 1);
INSERT INTO `char_data` VALUES (33, '牧瀬紅莉栖', '牧濑红莉栖', 'https://lain.bgm.tv/pic/crt/l/f7/2a/12393_crt_SS7II.jpg?r=1531372585', 1);
INSERT INTO `char_data` VALUES (34, '夏咲詠', '夏咲咏', 'https://lain.bgm.tv/pic/crt/l/18/f5/19302_crt_yAo3H.jpg', 1);
INSERT INTO `char_data` VALUES (35, 'フィア', '菲娅', 'https://lain.bgm.tv/pic/crt/l/12/93/49049_crt_2GWP0.jpg', 1);
INSERT INTO `char_data` VALUES (36, 'ユナギ・シャイエ', '无中文名', 'https://lain.bgm.tv/pic/crt/l/a7/e1/64332_crt_iI55l.jpg', 1);
INSERT INTO `char_data` VALUES (37, '散華礼弥', '散华礼弥', 'https://lain.bgm.tv/pic/crt/l/2c/67/15499_crt_z9TNj.jpg', 1);
INSERT INTO `char_data` VALUES (38, '菲比', '无中文名', 'https://lain.bgm.tv/pic/crt/l/2f/f3/167269_crt_L1aep.jpg?r=1754886594', 1);

-- ----------------------------
-- Table structure for group_standings
-- ----------------------------
DROP TABLE IF EXISTS `group_standings`;
CREATE TABLE `group_standings`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_name` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '组别 A~H',
  `char_id` int NOT NULL COMMENT '角色ID',
  `played` tinyint NOT NULL DEFAULT 0 COMMENT '已赛场次',
  `wins` tinyint NOT NULL DEFAULT 0 COMMENT '胜场',
  `draws` tinyint NOT NULL DEFAULT 0 COMMENT '平场',
  `losses` tinyint NOT NULL DEFAULT 0 COMMENT '负场',
  `points` tinyint NOT NULL DEFAULT 0 COMMENT '积分（胜3平1负0）',
  `goal_diff` int NOT NULL DEFAULT 0 COMMENT '得票差（得票-失票）',
  `goals_for` int NOT NULL DEFAULT 0 COMMENT '总得票数',
  `goals_against` int NOT NULL DEFAULT 0 COMMENT '总失票数',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_group_char`(`group_name` ASC, `char_id` ASC) USING BTREE,
  INDEX `idx_char`(`char_id` ASC) USING BTREE,
  INDEX `idx_group_points`(`group_name` ASC, `points` DESC, `goal_diff` DESC, `goals_for` DESC) USING BTREE,
  CONSTRAINT `fk_standings_char` FOREIGN KEY (`char_id`) REFERENCES `char_data` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 65 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '小组赛积分榜（冗余，每场比赛后更新）' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of group_standings
-- ----------------------------
INSERT INTO `group_standings` VALUES (33, 'A', 9, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (34, 'A', 20, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (35, 'A', 21, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (36, 'A', 38, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (37, 'B', 3, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (38, 'B', 19, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (39, 'B', 22, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (40, 'B', 37, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (41, 'C', 4, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (42, 'C', 17, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (43, 'C', 23, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (44, 'C', 36, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (45, 'D', 10, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (46, 'D', 13, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (47, 'D', 24, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (48, 'D', 35, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (49, 'E', 11, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (50, 'E', 12, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (51, 'E', 27, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (52, 'E', 34, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (53, 'F', 14, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (54, 'F', 8, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (55, 'F', 28, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (56, 'F', 33, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (57, 'G', 25, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (58, 'G', 7, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (59, 'G', 29, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (60, 'G', 32, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (61, 'H', 26, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (62, 'H', 5, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (63, 'H', 30, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO `group_standings` VALUES (64, 'H', 31, 0, 0, 0, 0, 0, 0, 0, 0);

-- ----------------------------
-- Table structure for match_votes
-- ----------------------------
DROP TABLE IF EXISTS `match_votes`;
CREATE TABLE `match_votes`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `match_id` int NOT NULL COMMENT '比赛ID',
  `user_qq` bigint NOT NULL COMMENT '用户QQ号',
  `voted_char_id` int NOT NULL COMMENT '用户投票支持的角色ID（必须是char_a_id或char_b_id之一）',
  `vote_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_match_user`(`match_id` ASC, `user_qq` ASC) USING BTREE,
  INDEX `idx_match`(`match_id` ASC) USING BTREE,
  INDEX `idx_user`(`user_qq` ASC) USING BTREE,
  INDEX `fk_match_votes_char`(`voted_char_id` ASC) USING BTREE,
  CONSTRAINT `fk_match_votes_char` FOREIGN KEY (`voted_char_id`) REFERENCES `char_data` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_match_votes_match` FOREIGN KEY (`match_id`) REFERENCES `matches` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `fk_match_votes_user` FOREIGN KEY (`user_qq`) REFERENCES `users` (`qq_number`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '用户对比赛（小组赛/淘汰赛）的投票' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of match_votes
-- ----------------------------

-- ----------------------------
-- Table structure for matches
-- ----------------------------
DROP TABLE IF EXISTS `matches`;
CREATE TABLE `matches`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `stage_name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '阶段名称：小组赛,十六强赛,八强赛,半决赛,决赛',
  `final_type` enum('championship','third_place') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '决赛类型：championship-冠军赛, third_place-季军赛（仅stage_name=决赛时使用）',
  `group_name` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '小组赛阶段使用：A~H',
  `match_order` tinyint NULL DEFAULT NULL COMMENT '小组赛内比赛序号（1-6）',
  `char_a_id` int NOT NULL COMMENT '角色A的ID',
  `char_b_id` int NOT NULL COMMENT '角色B的ID',
  `winner_id` int NULL DEFAULT NULL COMMENT '胜者角色ID（淘汰赛必填，小组赛平局时为NULL）',
  `score_a` int NULL DEFAULT NULL COMMENT '角色A得票数',
  `score_b` int NULL DEFAULT NULL COMMENT '角色B得票数',
  `status` enum('pending','ongoing','completed') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'pending' COMMENT '比赛状态',
  `start_time` datetime NULL DEFAULT NULL,
  `end_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_stage`(`stage_name` ASC) USING BTREE,
  INDEX `idx_group`(`group_name` ASC) USING BTREE,
  INDEX `idx_chars`(`char_a_id` ASC, `char_b_id` ASC) USING BTREE,
  INDEX `fk_matches_char_b`(`char_b_id` ASC) USING BTREE,
  INDEX `fk_matches_winner`(`winner_id` ASC) USING BTREE,
  CONSTRAINT `fk_matches_char_a` FOREIGN KEY (`char_a_id`) REFERENCES `char_data` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_matches_char_b` FOREIGN KEY (`char_b_id`) REFERENCES `char_data` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_matches_winner` FOREIGN KEY (`winner_id`) REFERENCES `char_data` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 97 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '所有比赛（小组赛+淘汰赛）' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of matches
-- ----------------------------
INSERT INTO `matches` VALUES (49, '小组赛', NULL, 'A', 1, 9, 20, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (50, '小组赛', NULL, 'A', 2, 9, 21, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (51, '小组赛', NULL, 'A', 3, 9, 38, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (52, '小组赛', NULL, 'A', 4, 20, 21, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (53, '小组赛', NULL, 'A', 5, 20, 38, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (54, '小组赛', NULL, 'A', 6, 21, 38, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (55, '小组赛', NULL, 'B', 7, 3, 19, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (56, '小组赛', NULL, 'B', 8, 3, 22, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (57, '小组赛', NULL, 'B', 9, 3, 37, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (58, '小组赛', NULL, 'B', 10, 19, 22, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (59, '小组赛', NULL, 'B', 11, 19, 37, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (60, '小组赛', NULL, 'B', 12, 22, 37, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (61, '小组赛', NULL, 'C', 13, 4, 17, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (62, '小组赛', NULL, 'C', 14, 4, 23, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (63, '小组赛', NULL, 'C', 15, 4, 36, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (64, '小组赛', NULL, 'C', 16, 17, 23, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (65, '小组赛', NULL, 'C', 17, 17, 36, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (66, '小组赛', NULL, 'C', 18, 23, 36, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (67, '小组赛', NULL, 'D', 19, 10, 13, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (68, '小组赛', NULL, 'D', 20, 10, 24, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (69, '小组赛', NULL, 'D', 21, 10, 35, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (70, '小组赛', NULL, 'D', 22, 13, 24, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (71, '小组赛', NULL, 'D', 23, 13, 35, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (72, '小组赛', NULL, 'D', 24, 24, 35, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (73, '小组赛', NULL, 'E', 25, 11, 12, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (74, '小组赛', NULL, 'E', 26, 11, 27, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (75, '小组赛', NULL, 'E', 27, 11, 34, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (76, '小组赛', NULL, 'E', 28, 12, 27, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (77, '小组赛', NULL, 'E', 29, 12, 34, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (78, '小组赛', NULL, 'E', 30, 27, 34, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (79, '小组赛', NULL, 'F', 31, 14, 8, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (80, '小组赛', NULL, 'F', 32, 14, 28, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (81, '小组赛', NULL, 'F', 33, 14, 33, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (82, '小组赛', NULL, 'F', 34, 8, 28, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (83, '小组赛', NULL, 'F', 35, 8, 33, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (84, '小组赛', NULL, 'F', 36, 28, 33, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (85, '小组赛', NULL, 'G', 37, 25, 7, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (86, '小组赛', NULL, 'G', 38, 25, 29, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (87, '小组赛', NULL, 'G', 39, 25, 32, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (88, '小组赛', NULL, 'G', 40, 7, 29, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (89, '小组赛', NULL, 'G', 41, 7, 32, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (90, '小组赛', NULL, 'G', 42, 29, 32, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (91, '小组赛', NULL, 'H', 43, 26, 5, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (92, '小组赛', NULL, 'H', 44, 26, 30, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (93, '小组赛', NULL, 'H', 45, 26, 31, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (94, '小组赛', NULL, 'H', 46, 5, 30, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (95, '小组赛', NULL, 'H', 47, 5, 31, NULL, NULL, NULL, 'pending', NULL, NULL);
INSERT INTO `matches` VALUES (96, '小组赛', NULL, 'H', 48, 30, 31, NULL, NULL, NULL, 'pending', NULL, NULL);

-- ----------------------------
-- Table structure for pre_votes
-- ----------------------------
DROP TABLE IF EXISTS `pre_votes`;
CREATE TABLE `pre_votes`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_qq` bigint NOT NULL COMMENT '用户QQ号',
  `char_id` int NOT NULL COMMENT '角色ID',
  `vote_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_user_char`(`user_qq` ASC, `char_id` ASC) USING BTREE,
  INDEX `idx_char_id`(`char_id` ASC) USING BTREE,
  CONSTRAINT `fk_pre_votes_char` FOREIGN KEY (`char_id`) REFERENCES `char_data` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `fk_pre_votes_user` FOREIGN KEY (`user_qq`) REFERENCES `users` (`qq_number`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 65 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '预选赛投票记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pre_votes
-- ----------------------------
INSERT INTO `pre_votes` VALUES (4, 123456789, 3, '2026-03-29 17:25:39');
INSERT INTO `pre_votes` VALUES (5, 123456789, 5, '2026-03-29 17:25:39');
INSERT INTO `pre_votes` VALUES (6, 123456789, 8, '2026-03-29 17:25:39');
INSERT INTO `pre_votes` VALUES (7, 123456789, 9, '2026-03-29 17:25:39');
INSERT INTO `pre_votes` VALUES (8, 123456789, 10, '2026-03-29 17:25:39');
INSERT INTO `pre_votes` VALUES (9, 123456789, 11, '2026-03-29 17:25:39');
INSERT INTO `pre_votes` VALUES (10, 123456789, 12, '2026-03-29 17:25:39');
INSERT INTO `pre_votes` VALUES (31, 514, 32, '2026-04-01 15:19:01');
INSERT INTO `pre_votes` VALUES (32, 514, 33, '2026-04-01 15:19:01');
INSERT INTO `pre_votes` VALUES (33, 514, 34, '2026-04-01 15:19:01');
INSERT INTO `pre_votes` VALUES (34, 514, 35, '2026-04-01 15:19:01');
INSERT INTO `pre_votes` VALUES (35, 514, 4, '2026-04-01 15:19:01');
INSERT INTO `pre_votes` VALUES (36, 514, 9, '2026-04-01 15:19:01');
INSERT INTO `pre_votes` VALUES (37, 514, 14, '2026-04-01 15:19:01');
INSERT INTO `pre_votes` VALUES (38, 514, 25, '2026-04-01 15:19:01');
INSERT INTO `pre_votes` VALUES (39, 514, 26, '2026-04-01 15:19:01');
INSERT INTO `pre_votes` VALUES (40, 514, 29, '2026-04-01 15:19:01');
INSERT INTO `pre_votes` VALUES (41, 514, 30, '2026-04-01 15:19:01');
INSERT INTO `pre_votes` VALUES (42, 1, 17, '2026-04-01 15:43:04');
INSERT INTO `pre_votes` VALUES (43, 1, 37, '2026-04-01 15:43:04');
INSERT INTO `pre_votes` VALUES (44, 114, 3, '2026-04-01 16:01:41');
INSERT INTO `pre_votes` VALUES (45, 114, 4, '2026-04-01 16:01:41');
INSERT INTO `pre_votes` VALUES (46, 114, 7, '2026-04-01 16:01:41');
INSERT INTO `pre_votes` VALUES (47, 114, 9, '2026-04-01 16:01:41');
INSERT INTO `pre_votes` VALUES (48, 114, 10, '2026-04-01 16:01:41');
INSERT INTO `pre_votes` VALUES (49, 114, 11, '2026-04-01 16:01:41');
INSERT INTO `pre_votes` VALUES (50, 114, 13, '2026-04-01 16:01:41');
INSERT INTO `pre_votes` VALUES (51, 114, 14, '2026-04-01 16:01:41');
INSERT INTO `pre_votes` VALUES (52, 114, 19, '2026-04-01 16:01:41');
INSERT INTO `pre_votes` VALUES (53, 114, 20, '2026-04-01 16:01:41');
INSERT INTO `pre_votes` VALUES (54, 114, 21, '2026-04-01 16:01:41');
INSERT INTO `pre_votes` VALUES (55, 114, 22, '2026-04-01 16:01:41');
INSERT INTO `pre_votes` VALUES (56, 114, 23, '2026-04-01 16:01:41');
INSERT INTO `pre_votes` VALUES (57, 114, 24, '2026-04-01 16:01:41');
INSERT INTO `pre_votes` VALUES (58, 114, 25, '2026-04-01 16:01:41');
INSERT INTO `pre_votes` VALUES (59, 114, 26, '2026-04-01 16:01:41');
INSERT INTO `pre_votes` VALUES (60, 114, 27, '2026-04-01 16:01:41');
INSERT INTO `pre_votes` VALUES (61, 114, 28, '2026-04-01 16:01:41');
INSERT INTO `pre_votes` VALUES (62, 114, 31, '2026-04-01 16:01:41');
INSERT INTO `pre_votes` VALUES (63, 114, 36, '2026-04-01 16:01:41');
INSERT INTO `pre_votes` VALUES (64, 429, 38, '2026-04-01 16:58:16');

-- ----------------------------
-- Table structure for system_data
-- ----------------------------
DROP TABLE IF EXISTS `system_data`;
CREATE TABLE `system_data`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `data_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `data_value` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of system_data
-- ----------------------------
INSERT INTO `system_data` VALUES (1, 'cur_stage', '小组赛');
INSERT INTO `system_data` VALUES (2, 'pre_votes_per_user', '20');
INSERT INTO `system_data` VALUES (3, 'group_size', '4');
INSERT INTO `system_data` VALUES (4, 'groups_count', '8');
INSERT INTO `system_data` VALUES (5, 'advance_per_group', '2');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `qq_number` bigint NOT NULL,
  `nickname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `role` enum('user','admin') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'user',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`qq_number`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, NULL, 'user', '2026-04-01 15:42:54');
INSERT INTO `users` VALUES (114, NULL, 'user', '2026-04-01 15:00:22');
INSERT INTO `users` VALUES (429, '散华', 'admin', '2026-04-01 15:58:50');
INSERT INTO `users` VALUES (514, NULL, 'user', '2026-04-01 15:00:33');
INSERT INTO `users` VALUES (123456789, NULL, 'user', '2026-03-03 16:03:10');

SET FOREIGN_KEY_CHECKS = 1;
