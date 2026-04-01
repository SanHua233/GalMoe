const { createApp } = Vue;

createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            loggedIn: false,
            loginQQ: '',
            loginError: '',
            currentStage: '',
            selectedStage: '',
            stageOptions: ['（未开放）', '提名阶段', '预选赛阶段', '小组赛', '淘汰赛（16进8）', '淘汰赛（8进4）', '半决赛', '总决赛'],
            updatingStage: false,
            deleteUserQQ: '',
            deleting: false,
            deleteResult: '',
            groupsPreview: null,
            generatingPreview: false,
        }
    },
    mounted() {
        this.checkAdminLogin();
    },
    methods: {
        async adminLogin() {
            if (!this.loginQQ) {
                this.loginError = '请输入QQ号';
                return;
            }
            const res = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ qq_number: this.loginQQ })
            });
            const data = await res.json();
            if (data.success) {
                this.loggedIn = true;
                this.loginError = '';
                this.fetchCurrentStage();
            } else {
                this.loginError = data.message;
            }
        },
        async checkAdminLogin() {
            const res = await fetch('/me');
            const data = await res.json();
            if (data.logged_in) {
                // 检查是否是管理员
                const userRes = await fetch('/api/user/role'); // 需要新增这个接口，或者直接在后端判断
                // 简单起见，先假设登录即管理员，实际应请求一个检查权限的接口
                // 这里我们直接尝试访问 admin 页面，如果 403 则说明不是管理员
                const adminCheck = await fetch('/api/admin/current_stage');
                if (adminCheck.status === 403) {
                    this.loggedIn = false;
                    this.loginError = '您不是管理员，无权访问';
                } else {
                    this.loggedIn = true;
                    this.fetchCurrentStage();
                }
            }
        },
        async fetchCurrentStage() {
            const res = await fetch('/api/admin/current_stage');
            const data = await res.json();
            if (data.stage) {
                this.currentStage = data.stage;
                this.selectedStage = data.stage;
            }
        },
        async updateStage() {
            if (this.selectedStage === this.currentStage) {
                alert('阶段未改变');
                return;
            }
            this.updatingStage = true;
            try {
                const res = await fetch('/api/admin/update_stage', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ stage: this.selectedStage })
                });
                const data = await res.json();
                if (data.success) {
                    this.currentStage = this.selectedStage;
                    alert('阶段更新成功');
                } else {
                    alert(data.message);
                }
            } catch (e) {
                alert('请求失败');
            } finally {
                this.updatingStage = false;
            }
        },
        async deleteUserVotes() {
            if (!this.deleteUserQQ) {
                alert('请输入QQ号');
                return;
            }
            this.deleting = true;
            this.deleteResult = '';
            try {
                const res = await fetch('/api/admin/delete_user_votes', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_qq: this.deleteUserQQ })
                });
                const data = await res.json();
                this.deleteResult = data.message;
                if (data.success) {
                    // 可选：刷新分组预览等
                }
            } catch (e) {
                this.deleteResult = '请求失败';
            } finally {
                this.deleting = false;
            }
        },
        async generateGroupsPreview() {
            this.generatingPreview = true;
            try {
                const res = await fetch('/api/admin/generate_groups', {
                    method: 'POST'
                });
                const data = await res.json();
                if (data.success) {
                    this.groupsPreview = data.groups;
                } else {
                    alert(data.message);
                }
            } catch (e) {
                alert('请求失败');
            } finally {
                this.generatingPreview = false;
            }
        },
        cancelPreview() {
            this.groupsPreview = null;
        },
        async confirmGroups() {
            try {
                const res = await fetch('/api/admin/confirm_groups', {
                    method: 'POST'
                });
                const data = await res.json();
                if (data.success) {
                    alert(data.message);
                    this.groupsPreview = null;
                } else {
                    alert(data.message);
                }
            } catch (e) {
                alert('请求失败');
            }
        }
    }
}).mount('#app');