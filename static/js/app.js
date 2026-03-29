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
            preliminarySubmitting: false
        }
    },
    computed: {
        selectedCount() {
            return this.selectedCharacterIds.length;
        },
        rankedCharacters() {
            return [...this.preliminaryCharacters].sort((a, b) => b.vote_count - a.vote_count);
        },
        // 淘汰线位置：第32名（索引31），如果不足32名则返回最后一个索引
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
                // 如果当前在预选赛页面，刷新数据
                if (this.showPreliminaryPage) {
                    this.loadPreliminaryData();
                }
            } else {
                this.loginError = data.message;
            }
        },

        async logout() {
            await fetch("/logout", { method: "POST" });
            this.loggedIn = false;
            this.userQQ = "";
            // 如果当前在预选赛页面，重置状态
            if (this.showPreliminaryPage) {
                this.hasUserVotedInPreliminary = false;
                this.selectedCharacterIds = [];
                this.loadPreliminaryData();
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
            if (stage === '首页') {
                this.showNominationPage = false;
                this.showPreliminaryPage = false;
                this.currentStage = '首页';
            } else if (stage === '提名') {
                this.showNominationPage = true;
                this.showPreliminaryPage = false;
                this.currentStage = '提名';
                this.fetchCharacters();
            } else if (stage === '预选赛') {
                this.showNominationPage = false;
                this.showPreliminaryPage = true;
                this.currentStage = '预选赛';
                this.preliminaryActiveTab = 'vote';
                this.loadPreliminaryData();
            }
        },

        async loadPreliminaryData() {
            try {
                // 获取配置
                const configRes = await fetch("/api/preliminary/config");
                const configData = await configRes.json();
                this.preVotesPerUser = configData.max_votes_per_user || 20;

                // 获取角色列表及票数
                const charsRes = await fetch("/api/preliminary/characters");
                const charsData = await charsRes.json();
                this.preliminaryCharacters = charsData.characters;

                // 获取当前用户已投票列表
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

        isCharacterSelected(charId) {
            return this.selectedCharacterIds.includes(charId);
        },

        toggleSelectCharacter(charId) {
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

        searchCharacters() {
            if (!this.searchKeyword.trim()) {
                this.searchError = "请输入搜索关键词";
                return;
            }
            fetch("/api/search_character", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ keyword: this.searchKeyword.trim() })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    this.searchResults = data.characters;
                    this.searchError = "";
                    this.showSearchResult = true;
                } else {
                    this.searchError = data.message;
                    this.searchResults = [];
                }
            })
            .catch(e => {
                this.searchError = "网络错误，搜索失败";
                this.searchResults = [];
            });
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