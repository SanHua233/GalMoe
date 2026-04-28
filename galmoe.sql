/*
 Navicat Premium Dump SQL

 Source Server         : MySQL97
 Source Server Type    : MySQL
 Source Server Version : 90700 (9.7.0)
 Source Host           : localhost:3306
 Source Schema         : galmoe

 Target Server Type    : MySQL
 Target Server Version : 90700 (9.7.0)
 File Encoding         : 65001

 Date: 28/04/2026 14:38:59
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
) ENGINE = InnoDB AUTO_INCREMENT = 38 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of char_data
-- ----------------------------
INSERT INTO `char_data` VALUES (1, '菲比', '无中文名', 'https://lain.bgm.tv/pic/crt/l/2f/f3/167269_crt_L1aep.jpg?r=1754886594', 0);
INSERT INTO `char_data` VALUES (2, '卜灵', '无中文名', 'https://lain.bgm.tv/pic/crt/l/e2/2d/177796_crt_74snX.jpg', 0);
INSERT INTO `char_data` VALUES (3, '爱弥斯', '无中文名', 'https://lain.bgm.tv/pic/crt/l/6d/5b/195805_crt_7exx8.jpg?r=1769918549', 0);
INSERT INTO `char_data` VALUES (4, '漂泊者', '漂泊者（女）', 'https://lain.bgm.tv/pic/crt/l/42/d2/158082_crt_ia6Px.jpg?r=1716565615', 0);
INSERT INTO `char_data` VALUES (5, '卡提希娅', '无中文名', 'https://lain.bgm.tv/pic/crt/l/5a/ed/169357_crt_9C5r2.jpg?r=1754886697', 0);
INSERT INTO `char_data` VALUES (6, '洛可可', '无中文名', 'https://lain.bgm.tv/pic/crt/l/4a/8f/167270_crt_zc0rI.jpg?r=1754886545', 0);
INSERT INTO `char_data` VALUES (7, '西格莉卡', '无中文名', 'https://lain.bgm.tv/pic/crt/l/fa/d6/191861_crt_eGDNY.jpg?r=1773990691', 0);
INSERT INTO `char_data` VALUES (8, '琳奈', '无中文名', 'https://lain.bgm.tv/pic/crt/l/9e/de/191863_crt_bSZrp.jpg?r=1766287208', 0);
INSERT INTO `char_data` VALUES (9, '莫宁', '无中文名', 'https://lain.bgm.tv/pic/crt/l/09/c9/191859_crt_9n90C.jpg?r=1768103974', 0);
INSERT INTO `char_data` VALUES (10, '达妮娅', '无中文名', 'https://lain.bgm.tv/pic/crt/l/ea/e0/205122_crt_weYde.jpg?r=1774496699', 0);
INSERT INTO `char_data` VALUES (11, '绯雪', '无中文名', 'https://lain.bgm.tv/pic/crt/l/6f/93/205121_crt_js3Dj.jpg?r=1777173616', 0);
INSERT INTO `char_data` VALUES (12, '千咲', '朽叶千咲', 'https://lain.bgm.tv/pic/crt/l/a1/fa/176899_crt_5uy1D.jpg?r=1763265672', 0);
INSERT INTO `char_data` VALUES (13, '桃祈', '无中文名', 'https://lain.bgm.tv/pic/crt/l/a0/0d/158088_crt_PpExP.jpg?r=1716567539', 0);
INSERT INTO `char_data` VALUES (14, '丹瑾', '无中文名', 'https://lain.bgm.tv/pic/crt/l/69/41/158090_crt_xbmX3.jpg?r=1716567377', 0);
INSERT INTO `char_data` VALUES (15, '散华', '无中文名', 'https://lain.bgm.tv/pic/crt/l/ca/9b/158093_crt_284Zz.jpg?r=1716567129', 0);
INSERT INTO `char_data` VALUES (16, '炽霞', '马小芳', 'https://lain.bgm.tv/pic/crt/l/d5/16/158095_crt_ph0RP.jpg?r=1758256604', 0);
INSERT INTO `char_data` VALUES (17, '白芷', '无中文名', 'https://lain.bgm.tv/pic/crt/l/6e/72/158094_crt_2D5Yx.jpg?r=1758257114', 0);
INSERT INTO `char_data` VALUES (18, '秧秧', '无中文名', 'https://lain.bgm.tv/pic/crt/l/f3/99/158096_crt_1QZBn.jpg?r=1758256542', 0);
INSERT INTO `char_data` VALUES (19, '灯灯', '无中文名', 'https://lain.bgm.tv/pic/crt/l/13/52/164249_crt_X2dvX.jpg', 0);
INSERT INTO `char_data` VALUES (20, '安可', '无中文名', 'https://lain.bgm.tv/pic/crt/l/cb/01/158097_crt_a1rfa.jpg?r=1716567817', 0);
INSERT INTO `char_data` VALUES (21, '维里奈', '无中文名', 'https://lain.bgm.tv/pic/crt/l/6b/11/158086_crt_4464R.jpg?r=1716567742', 0);
INSERT INTO `char_data` VALUES (22, '鉴心', '无中文名', 'https://lain.bgm.tv/pic/crt/l/a9/5d/158087_crt_wV2B9.jpg?r=1716567299', 0);
INSERT INTO `char_data` VALUES (23, '吟霖', '无中文名', 'https://lain.bgm.tv/pic/crt/l/3b/9f/158715_crt_sRSSN.jpg?r=1720342718', 0);
INSERT INTO `char_data` VALUES (24, '今汐', '今汐', 'https://lain.bgm.tv/pic/crt/l/8c/f7/158713_crt_lAN9E.jpg?r=1720340556', 0);
INSERT INTO `char_data` VALUES (25, '长离', '无中文名', 'https://lain.bgm.tv/pic/crt/l/61/f5/158714_crt_d8dKP.jpg?r=1721678258', 0);
INSERT INTO `char_data` VALUES (26, '折枝', '无中文名', 'https://lain.bgm.tv/pic/crt/l/1c/f4/161487_crt_MSs54.jpg?r=1723470125', 0);
INSERT INTO `char_data` VALUES (27, '椿', '无中文名', 'https://lain.bgm.tv/pic/crt/l/14/51/164113_crt_5Ph65.jpg?r=1726205669', 0);
INSERT INTO `char_data` VALUES (28, '守岸人', '无中文名', 'https://lain.bgm.tv/pic/crt/l/43/2c/162418_crt_19ZK7.jpg?r=1722911403', 0);
INSERT INTO `char_data` VALUES (29, '珂莱塔', '珂莱塔·莫塔里', 'https://lain.bgm.tv/pic/crt/l/ac/cb/167287_crt_xjm7g.jpg?r=1754886453', 0);
INSERT INTO `char_data` VALUES (30, '坎特蕾拉', '坎特蕾拉·翡萨烈', 'https://lain.bgm.tv/pic/crt/l/f0/a5/171681_crt_0dPV8.jpg?r=1754886628', 0);
INSERT INTO `char_data` VALUES (31, '弗洛洛', '无中文名', 'https://lain.bgm.tv/pic/crt/l/e1/cb/164646_crt_i6T55.jpg?r=1754886756', 0);
INSERT INTO `char_data` VALUES (32, '露帕', '无中文名', 'https://lain.bgm.tv/pic/crt/l/62/61/175541_crt_4QJMN.jpg?r=1754886728', 0);
INSERT INTO `char_data` VALUES (33, '夏空', '夏空·托卡塔', 'https://lain.bgm.tv/pic/crt/l/70/98/173088_crt_XOiJQ.jpg?r=1754886677', 0);
INSERT INTO `char_data` VALUES (34, '尤诺', '尤诺·西比尔', 'https://lain.bgm.tv/pic/crt/l/1c/49/176906_crt_66o1f.jpg?r=1757737664', 0);
INSERT INTO `char_data` VALUES (35, '奥古斯塔', '无中文名', 'https://lain.bgm.tv/pic/crt/l/11/4f/176907_crt_a8R1u.jpg?r=1756011737', 0);
INSERT INTO `char_data` VALUES (36, '嘉贝莉娜', '无中文名', 'https://lain.bgm.tv/pic/crt/l/61/d5/176903_crt_3K4N0.jpg?r=1759635680', 0);
INSERT INTO `char_data` VALUES (37, '赞妮', '无中文名', 'https://lain.bgm.tv/pic/crt/l/91/97/167283_crt_P4Ddz.jpg?r=1754886646', 0);

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
) ENGINE = InnoDB AUTO_INCREMENT = 130 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '小组赛积分榜（冗余，每场比赛后更新）' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of group_standings
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 140 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '用户对比赛（小组赛/淘汰赛）的投票' ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 161 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '所有比赛（小组赛+淘汰赛）' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of matches
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 65 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '预选赛投票记录' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of pre_votes
-- ----------------------------

-- ----------------------------
-- Table structure for system_data
-- ----------------------------
DROP TABLE IF EXISTS `system_data`;
CREATE TABLE `system_data`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `data_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `data_value` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of system_data
-- ----------------------------
INSERT INTO `system_data` VALUES (1, 'cur_stage', '预选赛阶段');
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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (20260429, '管理员ouo', 'admin', '2026-04-28 14:36:28');

SET FOREIGN_KEY_CHECKS = 1;
