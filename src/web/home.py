import streamlit as st

from src.util.svn_util import SvnUtil
from src.util.token_util import TokenUtil


class Home:

    @staticmethod
    def init():
        # print("session username : " + st.session_state['username'])
        print(st.session_state)

        if TokenUtil.check_token():
            Home.svn_table()
        else:
            Home.login()
        pass

    @staticmethod
    def login():
        st.title("登录页面")
        # 创建 session state 键（如果它们不存在）
        if 'username' not in st.session_state:
            st.session_state['username'] = ''
        if 'password' not in st.session_state:
            st.session_state['password'] = ''

        # 建立表单用来输入认证详情
        with st.form(key='login_form'):
            username = st.text_input('账号', value=st.session_state['username'])
            password = st.text_input('密码', type='password', value=st.session_state['password'])
            remember_me = st.checkbox('记住密码')

            # 表单提交按钮
            login_attempted = st.form_submit_button(label='登录')
            # 点击登录
            if login_attempted:
                # 认证 账号密码
                authentication_succeeded = SvnUtil.check_connection(username, password)
                #  认证成功
                if authentication_succeeded:
                    # 用户选择记住密码，更新session state
                    if remember_me:
                        st.session_state['username'] = username
                        st.session_state['password'] = password

                    st.success('登录成功！')
                    # 简单处理 token 信息
                    token = TokenUtil.generate_token(username)
                    print("token: " + token)
                    st.session_state['token'] = token
                    # 跳转到新页面
                    st.rerun()
                    # Home.init()
                else:
                    # 禁止记住密码，清除session state
                    if not remember_me:
                        st.session_state['username'] = ''
                        st.session_state['password'] = ''

                    st.error('登录失败。请检查您的用户名和密码。')
                    # 如果Streamlit直接支持刷新页面，则可调用刷新页面的操作
                    # 否则，你可能需要手动重置状态或告诉用户重新加载页面

    @staticmethod
    def svn_table():
        user_info_col, logout_btn_col = st.columns(2)
        with user_info_col:
            st.write(f"欢迎用户 {TokenUtil.get_token_user()}")
        with logout_btn_col:
            logout_btn = st.button("退出登录", type="primary")
            if logout_btn:
                # 清除Session State中的token信息
                # del st.session_state['token']
                # 重载页面，这将导致再次运行脚本
                st.rerun()
        st.title("SVN 🔒 数据")

        pass


if __name__ == "__main__":
    if 'token' in st.session_state and TokenUtil.check_token():
        # 如果 token 有效，在这儿调用显示应用主内容的函数
        Home.svn_table()
    else:
        # 显示登录页面
        Home.login()
