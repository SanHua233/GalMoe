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
            stageOptions: ['（未开放）', '提名阶段', '预选赛阶段', '小组赛阶段', '淘汰赛（16进8）', '淘汰赛（8进4）', '半决赛', '总决赛', '（完赛）'],
            updatingStage: false,
            deleteUserQQ: '',
            deleting: false,
            deleteResult: '',
            groupsPreview: null,
            generatingPreview: false,
            clearingGroup: false,

            // 淘汰赛
            knockoutPreview: null,
            generatingKnockout: false,
            confirmingKnockout: false,
            settlePreview: null,
            settlingPreview: false,
            settlingConfirm: false,

            // 新增功能数据
            deleteCharName: '',
            deletingChar: false,
            deleteCharResult: '',

            showResetModal: false,
            resetConfirmText: '',
            resettingAll: false,

            showAddUserModal: false,
            newUserQQ: '',
            newUserNickname: '',
            addUserResult: '',
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
                }
            } catch (e) {
                this.deleteResult = '请求失败';
            } finally {
                this.deleting = false;
            }
        },
        async deleteUserGroupVotes() {
            if (!this.deleteUserQQ) {
                alert('请输入QQ号');
                return;
            }
            if (!confirm('确认删除该用户小组赛投票吗？')) return;
            this.deleting = true;
            this.deleteResult = '';
            try {
                const res = await fetch('/api/admin/delete_user_group_votes', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_qq: this.deleteUserQQ })
                });
                const data = await res.json();
                this.deleteResult = data.message;
                if (!data.success) alert(data.message);
            } catch (e) {
                this.deleteResult = '请求失败';
            } finally {
                this.deleting = false;
            }
        },
        async deleteUserKnockoutVotes(stage) {
            if (!this.deleteUserQQ) {
                alert('请输入QQ号');
                return;
            }
            if (!confirm(`确认删除该用户「${stage}」投票吗？`)) return;
            this.deleting = true;
            this.deleteResult = '';
            try {
                const res = await fetch('/api/admin/delete_user_knockout_votes', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_qq: this.deleteUserQQ, stage })
                });
                const data = await res.json();
                this.deleteResult = data.message;
                if (!data.success) alert(data.message);
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
        cancelKnockoutPreview() {
            this.knockoutPreview = null;
        },
        cancelSettlePreview() {
            this.settlePreview = null;
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
        },
        async clearGroupData() {
            if (!confirm('该操作将清空所有小组赛数据（包括比赛、积分和投票记录），是否继续？')) return;
            this.clearingGroup = true;
            try {
                const res = await fetch('/api/admin/clear_group_data', {
                    method: 'POST'
                });
                const data = await res.json();
                if (data.success) {
                    alert(data.message);
                    this.groupsPreview = null;
                } else {
                    alert('清空失败：' + data.message);
                }
            } catch (e) {
                alert('请求失败：' + e.message);
            } finally {
                this.clearingGroup = false;
            }
        },

        async generateKnockoutPreview() {
            this.generatingKnockout = true;
            this.knockoutPreview = null;
            try {
                const res = await fetch('/api/admin/knockout/generate_preview', { method: 'POST' });
                const data = await res.json();
                if (data.success) {
                    this.knockoutPreview = data;
                } else {
                    alert(data.message);
                }
            } catch (e) {
                alert('请求失败：' + e.message);
            } finally {
                this.generatingKnockout = false;
            }
        },

        async confirmKnockout() {
            if (!this.knockoutPreview) return;
            if (!confirm('确认生成淘汰赛（16进8）对阵吗？生成后将写入数据库。')) return;
            this.confirmingKnockout = true;
            try {
                const res = await fetch('/api/admin/knockout/confirm', { method: 'POST' });
                const data = await res.json();
                if (data.success) {
                    alert(data.message);
                    this.knockoutPreview = null;
                } else {
                    alert(data.message);
                }
            } catch (e) {
                alert('请求失败：' + e.message);
            } finally {
                this.confirmingKnockout = false;
            }
        },

        async settleKnockoutPreview() {
            this.settlingPreview = true;
            this.settlePreview = null;
            try {
                await this.fetchCurrentStage();
                const res = await fetch('/api/admin/knockout/settle_preview', { method: 'POST' });
                const data = await res.json().catch(() => ({ success: false, message: '服务器返回非JSON（可能500错误），请查看后端日志' }));
                if (data.success) {
                    this.settlePreview = data;
                } else {
                    alert(data.message);
                }
            } catch (e) {
                alert('请求失败：' + e.message);
            } finally {
                this.settlingPreview = false;
            }
        },

        async confirmSettleKnockout() {
            if (!this.settlePreview) return;
            const msg = `当前阶段：${this.settlePreview.current_stage}\n将生成：${this.settlePreview.next_stage}\n\n确认结算并生成下一阶段对阵吗？`;
            if (!confirm(msg)) return;
            this.settlingConfirm = true;
            try {
                const res = await fetch('/api/admin/knockout/settle_confirm', { method: 'POST' });
                const data = await res.json();
                if (data.success) {
                    alert(data.message);
                    this.settlePreview = null;
                    await this.fetchCurrentStage();
                } else {
                    alert(data.message);
                }
            } catch (e) {
                alert('请求失败：' + e.message);
            } finally {
                this.settlingConfirm = false;
            }
        },

        // ===== 新增功能方法 =====
        async deleteCharacter() {
            const name = this.deleteCharName.trim();
            if (!name) {
                alert('请输入需要删除的角色名（日文或中文）');
                return;
            }
            if (!confirm(`确定要删除角色“${name}”吗？此操作不可恢复！`)) return;
            this.deletingChar = true;
            this.deleteCharResult = '';
            try {
                const res = await fetch('/api/admin/delete_character', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name: name })
                });
                const data = await res.json();
                this.deleteCharResult = data.message;
                if (data.success) {
                    alert(data.message);
                    this.deleteCharName = '';
                } else {
                    alert(data.message);
                }
            } catch (e) {
                alert('请求失败：' + e.message);
            } finally {
                this.deletingChar = false;
            }
        },

        async executeResetAll() {
            if (this.resetConfirmText !== '确认清除') return;
            if (!confirm('最终确认：即将清空所有角色、投票、比赛数据。此操作不可恢复！')) return;
            this.resettingAll = true;
            try {
                const res = await fetch('/api/admin/reset_all', { method: 'POST' });
                const data = await res.json();
                if (data.success) {
                    alert(data.message);
                    this.showResetModal = false;
                    this.resetConfirmText = '';
                    this.fetchCurrentStage();
                } else {
                    alert('重置失败：' + data.message);
                }
            } catch (e) {
                alert('请求失败：' + e.message);
            } finally {
                this.resettingAll = false;
            }
        },

        async submitAddUser() {
            if (!this.newUserQQ) return;
            this.addUserResult = '';
            try {
                const res = await fetch('/api/admin/add_user', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        qq_number: this.newUserQQ,
                        nickname: this.newUserNickname.trim() || null
                    })
                });
                const data = await res.json();
                this.addUserResult = data.message;
                if (data.success) {
                    alert(data.message);
                    this.showAddUserModal = false;
                    this.newUserQQ = '';
                    this.newUserNickname = '';
                } else {
                    alert(data.message);
                }
            } catch (e) {
                alert('请求失败：' + e.message);
            }
        },
    }
}).mount('#app');