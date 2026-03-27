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
            // 新增确认提名相关数据
            showConfirmNomination: false,
            selectedCharacter: {},
            // 新增提名结果提示
            nominationMessage: "",
            nominationSuccess: false
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
            } else {
                this.loginError = data.message;
            }
        },

        async logout() {
            await fetch("/logout", { method: "POST" });
            this.loggedIn = false;
            this.userQQ = "";
        },

        async checkLogin() {
            const res = await fetch("/me");
            const data = await res.json();
            if (data.logged_in) {
                this.loggedIn = true;
                this.userQQ = data.qq_number;
            }
        },

        async fetchCurrentStage() {
            const res = await fetch("/get_current_stage");
            const data = await res.json();
            if (data.current_stage) {
                this.dbStage = data.current_stage;
            }
        },

        // ========== 调整：获取角色列表（匹配新字段） ==========
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
                this.currentStage = '首页';
            } else if (stage === '提名') {
                this.showNominationPage = true;
                this.currentStage = '提名';
                // 切换到提名页时重新加载角色列表
                this.fetchCharacters();
            }
        },

        async searchCharacters() {
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

        // 新增：打开确认提名弹窗
        openConfirmNominationModal(character) {
            this.selectedCharacter = character;
            this.showConfirmNomination = true;
            // 清空之前的提名提示
            this.nominationMessage = "";
            this.nominationSuccess = false;
        },

        // 新增：关闭确认提名弹窗（仅关闭当前弹窗）
        closeConfirmNominationModal() {
            this.showConfirmNomination = false;
            this.selectedCharacter = {};
        },

        // ========== 核心新增：调用提名接口 ==========
        async confirmNomination() {
            // 验证登录状态
            if (!this.loggedIn) {
                alert("请先登录后再进行提名");
                this.showConfirmNomination = false;
                this.showLogin = true;
                return;
            }

            // 构造提名数据（匹配数据库字段）
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
                    // 关闭弹窗 + 刷新角色列表
                    this.closeConfirmNominationModal();
                    this.fetchCharacters();
                    // 提示成功
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

        // 新增：图片加载失败处理
        handleImageError(index) {
            // 将失败的图片URL置空，触发占位图显示
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