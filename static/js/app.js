const { createApp } = Vue;

createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            theme: 'light',
            currentStage: '首页',
            dbStage: '',
            stages: [
                "首页",
                "提名",
                "预选赛",
                "小组赛",
                "淘汰赛",
                "最终决赛"
            ],
            showRules: false,
            showLogin: false,
            loginQQ: "",
            loginError: "",
            loggedIn: false,
            userQQ: "",
            characters: [],
            searchKeyword: "",
            showNominationPage: false,
            showSearchResult: false,
            searchResults: [],
            searchError: "",
            showConfirmNomination: false,
            selectedCharacter: {},
            nominationMessage: "",
            nominationSuccess: false,
            // 预选赛相关数据
            showPreliminaryPage: false,
            preliminaryActiveTab: 'vote',
            preliminaryCharacters: [],
            selectedCharacterIds: [],
            preVotesPerUser: 20,
            hasUserVotedInPreliminary: false,
            preliminarySubmitting: false,

            // 小组赛相关数据
            showGroupStagePage: false,
            groupStageActiveTab: 'vote',
            groupStageGroups: {},
            groupStageStandings: {},
            groupStageSelections: {},
            groupStageHasVoted: false,
            groupStageSubmitting: false,
            showGroupVoteConfirm: false,
            groupStageRefreshTimer: null
        }
    },
    computed: {
        selectedCount() {
            return this.selectedCharacterIds.length;
        },
        rankedCharacters() {
            return [...this.preliminaryCharacters].sort((a, b) => b.vote_count - a.vote_count);
        },
        eliminationLineIndex() {
            const total = this.rankedCharacters.length;
            if (total === 0) return -1;
            if (total >= 32) {
                return 31; // 第32名的索引
            } else {
                return total - 1; // 最后一名索引
            }
        }
    },
    mounted() {
        document.body.classList.add(this.theme);
        this.checkLogin();
        this.fetchCurrentStage();
        this.fetchCharacters();
    },
    methods: {
        toggleTheme() {
            document.body.classList.remove(this.theme);
            this.theme = this.theme === 'light' ? 'dark' : 'light';
            document.body.classList.add(this.theme);
        },

        goToCurrentStage() {
            if (this.dbStage === '提名阶段') {
                this.navigateTo('提名');
            } else if (this.dbStage === '预选赛阶段') {
                this.navigateTo('预选赛');
            } else if (this.dbStage === '小组赛阶段') {
                this.navigateTo('小组赛');
            } else {
                alert('未开放阶段，请等待后台更新');
            }
        },


        async login() {
            const res = await fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ qq_number: this.loginQQ })
            });
            const data = await res.json();
            if (data.success) {
                this.loggedIn = true;
                this.userQQ = data.qq_number;
                this.showLogin = false;
                this.loginError = "";
                if (this.showPreliminaryPage) {
                    this.loadPreliminaryData();
                }
                if (this.showGroupStagePage) {
                    this.loadGroupStageData();
                }
            } else {
                this.loginError = data.message;
            }
        },

        async logout() {
            await fetch("/logout", { method: "POST" });
            this.loggedIn = false;
            this.userQQ = "";
            if (this.showPreliminaryPage) {
                this.hasUserVotedInPreliminary = false;
                this.selectedCharacterIds = [];
                this.loadPreliminaryData();
            }
            if (this.showGroupStagePage) {
                this.groupStageHasVoted = false;
                this.groupStageSelections = {};
                this.loadGroupStageData();
            }
        },

        async checkLogin() {
            const res = await fetch("/me");
            const data = await res.json();
            if (data.logged_in) {
                this.loggedIn = true;
                this.userQQ = data.qq_number;
                if (this.showPreliminaryPage) {
                    this.loadPreliminaryData();
                }
                if (this.showGroupStagePage) {
                    this.loadGroupStageData();
                }
            } else {
                this.loggedIn = false;
                this.userQQ = "";
            }
        },

        async fetchCurrentStage() {
            const res = await fetch("/get_current_stage");
            const data = await res.json();
            if (data.current_stage) {
                this.dbStage = data.current_stage;
            }
        },

        async fetchCharacters() {
            try {
                const res = await fetch("/get_characters");
                const data = await res.json();
                if (data.characters) {
                    this.characters = data.characters;
                } else if (data.error) {
                    alert(data.error);
                }
            } catch (e) {
                alert("获取角色列表失败：" + e.message);
            }
        },

        navigateTo(stage) {
            // 先刷新阶段信息（异步）
            this.fetchCurrentStage().then(() => {
                if (stage === '首页') {
                    this.stopGroupStageAutoRefresh();
                    this.showNominationPage = false;
                    this.showPreliminaryPage = false;
                    this.showGroupStagePage = false;
                    this.currentStage = '首页';
                } else if (stage === '提名') {
                    this.stopGroupStageAutoRefresh();
                    this.showNominationPage = true;
                    this.showPreliminaryPage = false;
                    this.showGroupStagePage = false;
                    this.currentStage = '提名';
                    this.fetchCharacters();
                } else if (stage === '预选赛') {
                    this.stopGroupStageAutoRefresh();
                    this.showNominationPage = false;
                    this.showPreliminaryPage = true;
                    this.showGroupStagePage = false;
                    this.currentStage = '预选赛';
                    this.preliminaryActiveTab = 'vote';
                    this.loadPreliminaryData();
                } else if (stage === '小组赛') {
                    this.showNominationPage = false;
                    this.showPreliminaryPage = false;
                    this.showGroupStagePage = true;
                    this.currentStage = '小组赛';
                    this.groupStageActiveTab = 'vote';
                    this.loadGroupStageData();
                }
            });
        },

        setGroupStageTab(tab) {
            this.groupStageActiveTab = tab;
            if (this.showGroupStagePage) {
                if (tab === 'rank') {
                    this.fetchGroupStageStandings();
                } else if (tab === 'vote') {
                    this.fetchGroupStageMatches();
                }
            }
        },

        async loadPreliminaryData() {
            try {
                const configRes = await fetch("/api/preliminary/config");
                const configData = await configRes.json();
                this.preVotesPerUser = configData.max_votes_per_user || 20;

                const charsRes = await fetch("/api/preliminary/characters");
                const charsData = await charsRes.json();
                this.preliminaryCharacters = charsData.characters;

                if (this.loggedIn) {
                    const votesRes = await fetch("/api/preliminary/user_votes");
                    if (votesRes.status === 401) {
                        this.hasUserVotedInPreliminary = false;
                        this.selectedCharacterIds = [];
                    } else {
                        const votesData = await votesRes.json();
                        if (votesData.voted_ids) {
                            this.hasUserVotedInPreliminary = votesData.voted_ids.length > 0;
                            if (this.hasUserVotedInPreliminary) {
                                this.selectedCharacterIds = [];
                            } else {
                                this.selectedCharacterIds = votesData.voted_ids;
                            }
                        } else {
                            this.hasUserVotedInPreliminary = false;
                            this.selectedCharacterIds = [];
                        }
                    }
                } else {
                    this.hasUserVotedInPreliminary = false;
                    this.selectedCharacterIds = [];
                }
            } catch (error) {
                console.error("加载预选赛数据失败:", error);
            }
        },

        startGroupStageAutoRefresh() {
            if (this.groupStageRefreshTimer) return;
            this.groupStageRefreshTimer = setInterval(() => {
                if (!this.showGroupStagePage) return;
                if (this.groupStageActiveTab === 'rank') {
                    this.fetchGroupStageStandings();
                } else {
                    this.fetchGroupStageMatches();
                }
            }, 10000);
        },

        stopGroupStageAutoRefresh() {
            if (!this.groupStageRefreshTimer) return;
            clearInterval(this.groupStageRefreshTimer);
            this.groupStageRefreshTimer = null;
        },

        async loadGroupStageData() {
            try {
                await this.fetchGroupStageMatches();
                if (this.groupStageActiveTab === 'rank') {
                    await this.fetchGroupStageStandings();
                }
                if (this.loggedIn) {
                    await this.fetchGroupStageUserVotes();
                } else {
                    this.groupStageHasVoted = false;
                    this.groupStageSelections = {};
                }
                this.startGroupStageAutoRefresh();
            } catch (e) {
                console.error("加载小组赛数据失败:", e);
            }
        },

        async fetchGroupStageMatches() {
            const res = await fetch("/api/group_stage/matches");
            const data = await res.json();
            if (data.success) {
                this.groupStageGroups = data.groups || {};
            } else {
                this.groupStageGroups = {};
            }
        },

        async fetchGroupStageStandings() {
            const res = await fetch("/api/group_stage/standings");
            const data = await res.json();
            if (data.success) {
                this.groupStageStandings = data.groups || {};
            } else {
                this.groupStageStandings = {};
            }
        },

        async fetchGroupStageUserVotes() {
            const res = await fetch("/api/group_stage/user_votes");
            if (res.status === 401) {
                this.groupStageHasVoted = false;
                this.groupStageSelections = {};
                return;
            }
            const data = await res.json();
            if (data.success) {
                this.groupStageHasVoted = !!data.has_voted;
                if (this.groupStageHasVoted) {
                    const mapping = {};
                    for (const v of (data.votes || [])) {
                        mapping[v.match_id] = v.voted_char_id;
                    }
                    this.groupStageSelections = mapping;
                } else {
                    this.groupStageSelections = {};
                }
            }
        },

        isGroupStageOpen() {
            return this.dbStage === '小组赛阶段' || this.dbStage === '小组赛';
        },

        isGroupStageSelected(matchId, charId) {
            return this.groupStageSelections[matchId] === charId;
        },

        toggleGroupStageSelect(matchId, charId) {
            if (!this.isGroupStageOpen()) {
                alert('当前不在小组赛阶段，无法投票');
                return;
            }
            if (this.groupStageHasVoted) {
                alert('不可投票：您已完成小组赛投票');
                return;
            }
            if (!this.loggedIn) {
                alert("请先登录后再进行投票");
                this.showLogin = true;
                return;
            }
            const current = this.groupStageSelections[matchId];
            if (current === charId) {
                // 再次点击取消选择（弃票）
                const next = { ...this.groupStageSelections };
                delete next[matchId];
                this.groupStageSelections = next;
            } else {
                this.groupStageSelections = { ...this.groupStageSelections, [matchId]: charId };
            }
        },

        clearGroupStageSelect(matchId) {
            if (this.groupStageHasVoted) return;
            const next = { ...this.groupStageSelections };
            delete next[matchId];
            this.groupStageSelections = next;
        },

        getGroupStageMissingGroups() {
            const missing = [];
            for (const groupName of Object.keys(this.groupStageGroups || {})) {
                const matches = this.groupStageGroups[groupName] || [];
                const hasAny = matches.some(m => this.groupStageSelections[m.match_id]);
                if (!hasAny) missing.push(groupName);
            }
            return missing;
        },

        openGroupStageVoteConfirm() {
            if (!this.isGroupStageOpen()) {
                alert('当前不在小组赛阶段，无法投票');
                return;
            }
            if (!this.loggedIn) {
                alert("请先登录");
                this.showLogin = true;
                return;
            }
            if (this.groupStageHasVoted) {
                alert('不可投票：您已完成小组赛投票');
                return;
            }
            if (!this.groupStageGroups || Object.keys(this.groupStageGroups).length === 0) {
                alert('小组赛对战尚未生成，请联系管理员生成分组');
                return;
            }
            const missing = this.getGroupStageMissingGroups();
            if (missing.length > 0) {
                alert(`每组至少投1场：缺少 ${missing.join('、')} 组`);
                return;
            }
            this.showGroupVoteConfirm = true;
        },

        closeGroupStageVoteConfirm() {
            this.showGroupVoteConfirm = false;
        },

        async submitGroupStageVote() {
            if (!this.isGroupStageOpen()) {
                alert('当前不在小组赛阶段，无法投票');
                return;
            }
            if (!this.loggedIn) {
                alert("请先登录");
                this.showLogin = true;
                return;
            }
            if (this.groupStageHasVoted) {
                alert('不可投票：您已完成小组赛投票');
                return;
            }
            if (!this.groupStageGroups || Object.keys(this.groupStageGroups).length === 0) {
                alert('小组赛对战尚未生成，请联系管理员生成分组');
                return;
            }
            const missing = this.getGroupStageMissingGroups();
            if (missing.length > 0) {
                alert(`每组至少投1场：缺少 ${missing.join('、')} 组`);
                return;
            }

            const votes = Object.entries(this.groupStageSelections).map(([match_id, voted_char_id]) => ({
                match_id: Number(match_id),
                voted_char_id: Number(voted_char_id)
            }));

            this.groupStageSubmitting = true;
            try {
                const res = await fetch("/api/group_stage/vote", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ votes })
                });
                const data = await res.json();
                if (data.success) {
                    alert("投票成功！");
                    this.showGroupVoteConfirm = false;
                    await this.loadGroupStageData();
                    this.groupStageHasVoted = true;
                } else {
                    alert("投票失败：" + data.message);
                }
            } catch (e) {
                console.error("提交小组赛投票出错:", e);
                alert("网络错误，请稍后重试");
            } finally {
                this.groupStageSubmitting = false;
            }
        },

        isCharacterSelected(charId) {
            return this.selectedCharacterIds.includes(charId);
        },

        toggleSelectCharacter(charId) {
            // 阶段检测
            if (this.dbStage !== '预选赛阶段') {
                alert('当前不在预选赛阶段，无法投票');
                return;
            }
            if (this.hasUserVotedInPreliminary) {
                alert("您已完成投票，无法修改");
                return;
            }
            if (!this.loggedIn) {
                alert("请先登录后再进行投票");
                this.showLogin = true;
                return;
            }
            const index = this.selectedCharacterIds.indexOf(charId);
            if (index === -1) {
                if (this.selectedCharacterIds.length >= this.preVotesPerUser) {
                    alert(`您最多只能投${this.preVotesPerUser}票，已达到上限`);
                    return;
                }
                this.selectedCharacterIds.push(charId);
            } else {
                this.selectedCharacterIds.splice(index, 1);
            }
        },

        async submitPreliminaryVote() {
            // 阶段检测
            if (this.dbStage !== '预选赛阶段') {
                alert('当前不在预选赛阶段，无法投票');
                return;
            }
            if (!this.loggedIn) {
                alert("请先登录");
                this.showLogin = true;
                return;
            }
            if (this.hasUserVotedInPreliminary) {
                alert("您已经投过票，不能重复提交");
                return;
            }
            if (this.selectedCharacterIds.length === 0) {
                alert("请至少选择一个角色");
                return;
            }
            if (this.selectedCharacterIds.length > this.preVotesPerUser) {
                alert(`最多只能投${this.preVotesPerUser}票`);
                return;
            }
            this.preliminarySubmitting = true;
            try {
                const res = await fetch("/api/preliminary/vote", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ vote_ids: this.selectedCharacterIds })
                });
                const data = await res.json();
                if (data.success) {
                    alert("投票成功！");
                    this.hasUserVotedInPreliminary = true;
                    await this.loadPreliminaryData();
                } else {
                    alert("投票失败：" + data.message);
                }
            } catch (error) {
                console.error("提交投票出错:", error);
                alert("网络错误，请稍后重试");
            } finally {
                this.preliminarySubmitting = false;
            }
        },

        handlePrelimImageError(charId) {
            const char = this.preliminaryCharacters.find(c => c.id === charId);
            if (char) char.image_url = "";
        },

        handleGroupStageImageError(matchId, side) {
            for (const groupName of Object.keys(this.groupStageGroups || {})) {
                const matches = this.groupStageGroups[groupName] || [];
                const m = matches.find(x => Number(x.match_id) === Number(matchId));
                if (!m) continue;
                if (side === 'a') m.char_a.image_url = "";
                if (side === 'b') m.char_b.image_url = "";
                break;
            }
        },

        async searchCharacters() {
            // 阶段检测
            if (this.dbStage !== '提名阶段') {
                alert('当前不在提名阶段，无法搜索');
                return;
            }
            if (!this.searchKeyword.trim()) {
                this.searchError = "请输入搜索关键词";
                return;
            }
            try {
                const res = await fetch("/api/search_character", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ keyword: this.searchKeyword.trim() })
                });
                const data = await res.json();
                if (data.success) {
                    this.searchResults = data.characters;
                    this.searchError = "";
                    this.showSearchResult = true;
                } else {
                    this.searchError = data.message;
                    this.searchResults = [];
                }
            } catch (e) {
                this.searchError = "网络错误，搜索失败";
                this.searchResults = [];
            }
        },

        openConfirmNominationModal(character) {
            this.selectedCharacter = character;
            this.showConfirmNomination = true;
            this.nominationMessage = "";
            this.nominationSuccess = false;
        },

        closeConfirmNominationModal() {
            this.showConfirmNomination = false;
            this.selectedCharacter = {};
        },

        async confirmNomination() {
            if (!this.loggedIn) {
                alert("请先登录后再进行提名");
                this.showConfirmNomination = false;
                this.showLogin = true;
                return;
            }
            const nominationData = {
                name: this.selectedCharacter.name || "",
                cn_name: this.selectedCharacter.cn_name || "无中文名",
                image: this.selectedCharacter.image || ""
            };
            try {
                const res = await fetch("/api/nominate_character", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(nominationData)
                });
                const data = await res.json();
                if (data.success) {
                    this.nominationMessage = data.message;
                    this.nominationSuccess = true;
                    this.closeConfirmNominationModal();
                    this.fetchCharacters();
                    alert(data.message);
                } else {
                    this.nominationMessage = data.message;
                    this.nominationSuccess = false;
                    alert(data.message);
                }
            } catch (e) {
                this.nominationMessage = "网络错误，提名失败";
                this.nominationSuccess = false;
                alert(this.nominationMessage + "：" + e.message);
            }
        },

        handleImageError(index) {
            this.characters[index].image_url = "";
        },
        handleResultImageError(index) {
            this.searchResults[index].image = "";
        },
        handleConfirmImageError() {
            this.selectedCharacter.image = "";
        }
    }
}).mount('#app');
