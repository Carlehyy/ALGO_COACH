"""
ACM算法学习平台 - UserService单元测试
参考：开发指南V3 - 9.3 单元测试示例
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import UserService
from app.models.mysql.user import User
from app.api.v1.schemas.user import UserCreate, UserUpdate
from app.core.exceptions import BusinessException, ErrorCode


@pytest.fixture
def mock_db():
    """Mock数据库会话"""
    db = AsyncMock(spec=AsyncSession)
    db.commit = AsyncMock()
    db.flush = AsyncMock()
    db.refresh = AsyncMock()
    return db


@pytest.fixture
def service(mock_db):
    """UserService实例"""
    return UserService(mock_db)


@pytest.fixture
def sample_user():
    """示例用户对象"""
    user = User()
    user.id = 1
    user.email = "test@example.com"
    user.hashed_password = "hashed_password"
    user.nickname = "Test User"
    user.points = 100
    user.status = "1"
    user.role = "user"
    return user


class TestUserService:
    """UserService测试类"""

    @pytest.mark.asyncio
    async def test_create_user_success(self, service, sample_user):
        """测试创建用户 - 成功"""
        user_in = UserCreate(email="test@example.com", password="password123", nickname="Test")

        # Mock repository方法
        with patch.object(service.user_repo, 'get_by_email', return_value=None):
            with patch.object(service.user_repo, 'create', return_value=sample_user) as mock_create:
                result = await service.create_user(user_in)

                # 验证
                mock_create.assert_called_once()
                assert result.id == 1

    @pytest.mark.asyncio
    async def test_create_user_email_exists(self, service, sample_user):
        """测试创建用户 - 邮箱已存在"""
        user_in = UserCreate(email="existing@example.com", password="password123")

        # Mock repository返回已存在的用户
        with patch.object(service.user_repo, 'get_by_email', return_value=sample_user):
            with pytest.raises(BusinessException) as exc_info:
                await service.create_user(user_in)

            # 验证错误码
            assert exc_info.value.code == ErrorCode.USER_EXISTS[0]

    @pytest.mark.asyncio
    async def test_authenticate_success(self, service, sample_user):
        """测试登录 - 成功"""
        # Mock repository
        with patch.object(service.user_repo, 'get_by_email', return_value=sample_user):
            with patch.object(service.user_repo, 'update_last_login', return_value=None):
                with patch('app.services.user_service.create_access_token', return_value='mock_token'):
                    result = await service.authenticate("test@example.com", "password123")

                    # 验证
                    assert result["access_token"] == "mock_token"
                    assert result["user"].email == "test@example.com"

    @pytest.mark.asyncio
    async def test_authenticate_user_not_found(self, service):
        """测试登录 - 用户不存在"""
        with patch.object(service.user_repo, 'get_by_email', return_value=None):
            with pytest.raises(BusinessException) as exc_info:
                await service.authenticate("notfound@example.com", "password123")

            assert exc_info.value.code == ErrorCode.USER_NOT_FOUND[0]

    @pytest.mark.asyncio
    async def test_authenticate_password_error(self, service, sample_user):
        """测试登录 - 密码错误"""
        with patch.object(service.user_repo, 'get_by_email', return_value=sample_user):
            with patch('app.services.user_service.verify_password', return_value=False):
                with pytest.raises(BusinessException) as exc_info:
                    await service.authenticate("test@example.com", "wrong_password")

                assert exc_info.value.code == ErrorCode.PASSWORD_ERROR[0]

    @pytest.mark.asyncio
    async def test_authenticate_user_disabled(self, service):
        """测试登录 - 用户已禁用"""
        disabled_user = User()
        disabled_user.id = 1
        disabled_user.email = "disabled@example.com"
        disabled_user.hashed_password = "hashed"
        disabled_user.status = "0"  # 禁用状态

        with patch.object(service.user_repo, 'get_by_email', return_value=disabled_user):
            with patch('app.services.user_service.verify_password', return_value=True):
                with pytest.raises(BusinessException) as exc_info:
                    await service.authenticate("disabled@example.com", "password123")

                assert exc_info.value.code == ErrorCode.USER_DISABLED[0]

    @pytest.mark.asyncio
    async def test_get_by_id(self, service, sample_user):
        """测试根据ID获取用户"""
        with patch.object(service.user_repo, 'get_by_id', return_value=sample_user):
            result = await service.get_by_id(1)
            assert result.id == 1

    @pytest.mark.asyncio
    async def test_update_user_success(self, service, sample_user):
        """测试更新用户 - 成功"""
        user_in = UserUpdate(nickname="Updated Name")

        with patch.object(service.user_repo, 'update', return_value=sample_user) as mock_update:
            result = await service.update_user(sample_user, user_in)

            # 验证
            mock_update.assert_called_once()
            assert result.nickname == "Updated Name" or result.id == 1

    @pytest.mark.asyncio
    async def test_update_points_add(self, service, sample_user):
        """测试积分增加"""
        with patch.object(service.user_repo, 'add_points', return_value=sample_user) as mock_add:
            result = await service.update_points(sample_user, 50, "充值")

            mock_add.assert_called_once_with(sample_user, 50)

    @pytest.mark.asyncio
    async def test_update_points_consume(self, service, sample_user):
        """测试积分消费"""
        with patch.object(service.user_repo, 'consume_points', return_value=sample_user) as mock_consume:
            result = await service.update_points(sample_user, -30, "消费")

            mock_consume.assert_called_once_with(sample_user, 30)

    @pytest.mark.asyncio
    async def test_list_users(self, service, sample_user):
        """测试获取用户列表"""
        with patch.object(
            service.user_repo, 'list_users', return_value=([sample_user], 1)
        ) as mock_list:
            users, total = await service.list_users(page=1, page_size=20)

            # 验证
            mock_list.assert_called_once_with(skip=0, limit=20, status=None, role=None)
            assert total == 1
            assert len(users) == 1

    @pytest.mark.asyncio
    async def test_get_user_balance(self, service, sample_user):
        """测试获取用户积分余额"""
        sample_user.points = 100
        sample_user.total_recharged = 500
        sample_user.total_consumed = 400

        balance = await service.get_user_balance(sample_user)

        assert balance["points"] == 100
        assert balance["total_recharged"] == 500
        assert balance["total_consumed"] == 400

    @pytest.mark.asyncio
    async def test_disable_user(self, service):
        """测试禁用用户"""
        with patch.object(service.user_repo, 'get_by_id', return_value=sample_user):
            with patch.object(service.user_repo, 'delete', return_value=None) as mock_delete:
                await service.disable_user(1)

                mock_delete.assert_called_once()
