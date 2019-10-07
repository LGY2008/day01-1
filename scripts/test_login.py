import unittest
import requests
from requests import Session
from api.login import LoginApi


class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_api = LoginApi()

    def setUp(self):
        self.session = Session()

    def tearDown(self):
        self.session.close()

    # 登录成功
    def test_login_success(self):
        # 获取验证码
        response = self.login_api.get_login_verify_code(self.session)
        # 判断是否为图片类型
        self.assertIn("image", response.headers.get("Content-Type"))
        # 登录
        response = self.login_api.login(self.session, "13012345678", "123456", "8888")
        result = response.json()
        print("login response data=", result)
        # 断言
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, result.get("status"))
        self.assertEqual("登陆成功", result.get("msg"))

    # 账号不存在
    def test_login_username_not_exist(self):
        # 获取验证码
        response = self.login_api.get_login_verify_code(self.session)
        # 判断是否为图片类型
        self.assertIn("image", response.headers.get("Content-Type"))
        # 登录
        response = self.login_api.login(self.session, "13088888888", "123456", "8888")
        result = response.json()
        print("login response data=", result)
        # 断言
        self.assertEqual(200, response.status_code)
        self.assertEqual(-1, result.get("status"))
        self.assertIn("账号不存在", result.get("msg"))

    # 密码错误
    def test_login_password_is_error(self):
        # 获取验证码
        response = self.login_api.get_login_verify_code(self.session)
        # 判断是否为图片类型
        self.assertIn("image", response.headers.get("Content-Type"))
        # 登录
        response = self.login_api.login(self.session, "13012345678", "error", "8888")
        result = response.json()
        print("login response data=", result)
        # 断言
        self.assertEqual(200, response.status_code)
        self.assertEqual(-2, result.get("status"))
        self.assertIn("密码错误", result.get("msg"))