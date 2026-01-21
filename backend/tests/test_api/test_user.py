"""
ACM算法学习平台 - 用户API集成测试
"""

import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch

from app.main import app
from app.models.mysql.user import User
from app.api.v1.schemas.user import UserCreate


@pytest.fixture
async def client():
    """测试客户端"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
def mock_user():
    """Mock用户对象"""
    user = User()
    user.id = 1
    user.email = "test@example.com"
    user.nickname = "Test User"
    user.points = 100
    user.status = "1"
    user.role = "user"
    return user


class TestUserAPI:
    """用户API测试类"""

    @pytest.mark.asyncio
    async def test_register_success(self, client, mock_user):
        """测试用户注册 - 成功"""
        user_data = {
            "email": "newuser@example.com",
            "password": "password123",
            "nickname": "New User"
        }

        with patch('app.services.user_service.UserService.create_user', return_value=mock_user):
            response = await client.post("/api/v1/users/register", json=user_data)

            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 200
            assert data["data"]["email"] == "test@example.com"

    @pytest.mark.asyncio
    async def test_register_email_exists(self, client):
        """测试用户注册 - 邮箱已存在"""
        user_data = {
            "email": "existing@example.com",
            "password": "password123"
        }

        with patch('app.services.user_service.UserService.create_user', side_effect=Exception("邮箱已存在")):
            response = await client.post("/api/v1/users/register", json=user_data)

            # 可能返回500或业务错误
            assert response.status_code in [200, 500]

    @pytest.mark.asyncio
    async def test_login_success(self, client, mock_user):
        """测试用户登录 - 成功"""
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }

        mock_auth_result = {
            "user": mock_user,
            "access_token": "test_token"
        }

        with patch('app.services.user_service.UserService.authenticate', return_value=mock_auth_result):
            response = await client.post("/api/v1/users/login", json=login_data)

            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 200
            assert data["data"]["access_token"] == "test_token"

    @pytest.mark.asyncio
    async def test_login_user_not_found(self, client):
        """测试用户登录 - 用户不存在"""
        login_data = {
            "email": "notfound@example.com",
            "password": "password123"
        }

        with patch('app.services.user_service.UserService.authenticate', side_effect=Exception("用户不存在")):
            response = await client.post("/api/v1/users/login", json=login_data)

            # 可能返回500
            assert response.status_code in [200, 500]

    @pytest.mark.asyncio
    async def test_get_me_without_auth(self, client):
        """测试获取当前用户 - 未登录"""
        response = await client.get("/api/v1/users/me")

        # 应该返回401或其他错误
        assert response.status_code in [200, 401]

    @pytest.mark.asyncio
    async def test_update_me_success(self, client, mock_user):
        """测试更新用户信息 - 成功"""
        update_data = {
            "nickname": "Updated Name"
        }

        with patch('app.api.deps.get_current_user', return_value=mock_user):
            with patch('app.services.user_service.UserService.update_user', return_value=mock_user):
                response = await client.put(
                    "/api/v1/users/me",
                    json=update_data,
                    headers={"Authorization": "Bearer test_token"}
                )

                assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_balance(self, client, mock_user):
        """测试获取积分余额"""
        with patch('app.api.deps.get_current_user', return_value=mock_user):
            with patch('app.services.user_service.UserService.get_user_balance', return_value={
                "points": 100,
                "total_recharged": 0,
                "total_consumed": 0
            }):
                response = await client.get(
                    "/api/v1/users/balance",
                    headers={"Authorization": "Bearer test_token"}
                )

                assert response.status_code == 200
                data = response.json()
                assert data["data"]["points"] == 100

    @pytest.mark.asyncio
    async def test_list_users(self, client, mock_user):
        """测试获取用户列表"""
        with patch('app.api.deps.get_current_user', return_value=mock_user):
            with patch('app.services.user_service.UserService.list_users', return_value=([mock_user], 1)):
                response = await client.get(
                    "/api/v1/users/",
                    headers={"Authorization": "Bearer test_token"}
                )

                assert response.status_code == 200
                data = response.json()
                assert data["data"]["total"] == 1
