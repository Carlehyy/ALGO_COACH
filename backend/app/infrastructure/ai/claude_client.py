"""
Claude API客户端（Mock实现）
实际使用时替换为真实Claude API调用
"""

from typing import List, Dict, Optional, AsyncIterator
from loguru import logger
import time
import random


class MockClaudeClient:
    """Mock Claude客户端 - 用于开发和测试"""

    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.model = "claude-3-5-sonnet-20241022"
        self.max_tokens = 4096

    async def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
    ) -> Dict:
        """
        普通对话（非流式）

        Args:
            messages: 消息列表 [{"role": "user", "content": "..."}]
            max_tokens: 最大token数

        Returns:
            {"content": "...", "input_tokens": 10, "output_tokens": 20}
        """
        # 模拟API延迟
        await self._simulate_delay()

        user_message = messages[-1]["content"] if messages else ""

        # 根据用户消息生成模拟回复
        mock_response = self._generate_mock_response(user_message)

        logger.info(f"[MockClaude] 普通对话: input_tokens={len(user_message)//4}")
        return {
            "content": mock_response,
            "input_tokens": len(user_message) // 4,
            "output_tokens": len(mock_response) // 4,
        }

    async def chat_stream(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
    ) -> AsyncIterator[str]:
        """
        流式对话（SSE）

        Args:
            messages: 消息列表
            max_tokens: 最大token数

        Yields:
            文本片段
        """
        user_message = messages[-1]["content"] if messages else ""
        mock_response = self._generate_mock_response(user_message)

        # 模拟流式输出
        words = mock_response.split()
        for i, word in enumerate(words):
            if i > 0:
                yield " "
            yield word
            # 模拟打字延迟
            await self._simulate_delay(0.02)

    async def count_tokens(self, text: str) -> int:
        """估算token数量"""
        # 简单估算：1 token ≈ 4 字符（英文）
        return len(text) // 4

    async def _simulate_delay(self, base_delay: float = 0.5) -> None:
        """模拟API延迟"""
        delay = base_delay + random.uniform(0, 0.3)
        await asyncio.sleep(delay)

    def _generate_mock_response(self, user_message: str) -> str:
        """生成模拟回复"""
        user_lower = user_message.lower()

        # 根据关键词生成回复
        if "时间复杂度" in user_message or "time complexity" in user_lower:
            return """时间复杂度是衡量算法运行时间随输入规模增长的度量。

**常见时间复杂度（从快到慢）：**
1. O(1) - 常数时间：哈希表查找
2. O(log n) - 对数时间：二分查找
3. O(n) - 线性时间：简单遍历
4. O(n log n)：归并排序、快速排序
5. O(n²)：冒泡排序、插入排序
6. O(2ⁿ)：指数时间：暴力搜索
7. O(n!)：阶乘时间：全排列

**分析技巧：**
- 忽略常数项和低阶项
- 关注最高阶的增长项
- 最坏情况 vs 平均情况

需要详细讲解某个具体的复杂度吗？"""

        elif "二分查找" in user_message or "binary search" in user_lower:
            return """**二分查找**是一种在有序数组中查找目标元素的高效算法。

**算法思想：**
1. 维护左右指针 left 和 right
2. 每次取中间位置 mid = (left + right) / 2
3. 比较目标值与中间值：
   - 相等：找到目标
   - 目标值更大：在右半区查找（left = mid + 1）
   - 目标值更小：在左半区查找（right = mid - 1）
4. 重复直到找到或 left > right

**时间复杂度：** O(log n)
**空间复杂度：** O(1)

**适用条件：**
- 数组必须有序
- 适合静态数据（频繁查询、少量插入删除）

需要看代码实现吗？"""

        elif "动态规划" in user_message or "dp" in user_lower or "dynamic programming" in user_lower:
            return """**动态规划**是通过分解问题为子问题来解决复杂问题的算法思想。

**核心要素：**
1. **最优子结构**：问题的最优解包含子问题的最优解
2. **重叠子问题**：子问题会重复出现
3. **状态定义**：用数组/表格记录子问题解
4. **状态转移方程**：描述状态之间的关系

**经典问题：**
- 背包问题：0-1背包、完全背包
- 序列问题：LCS、LIS
- 区间DP：矩阵链乘法
- 状态压缩DP：旅行商问题

**解题步骤：**
1. 定义状态（dp数组的含义）
2. 找出状态转移方程
3. 确定初始条件和边界
4. 确定计算顺序

你想深入了解哪个具体问题？"""

        elif "链表" in user_message or "linked list" in user_lower:
            return """**链表**是一种常见的线性数据结构。

**链表 vs 数组：**
| 特性 | 数组 | 链表 |
|------|------|------|
| 内存 | 连续 | 分散 |
| 访问 | O(1) | O(n) |
| 插入/删除 | O(n) | O(1) |
| 大小 | 固定 | 动态 |

**链表类型：**
1. **单向链表**：每个节点指向下一个
2. **双向链表**：每个节点同时有前驱和后继
3. **循环链表**：首尾相连

**常用技巧：**
- 快慢指针：找中点、检测环
- 虚拟头节点：简化边界处理
- 递归：反转链表

需要讲解具体的链表操作吗？"""

        else:
            # 通用回复
            responses = [
                """这是一个很好的算法问题！让我来帮你分析一下。

建议从以下几个方面来理解：
1. **问题分析**：明确输入输出和约束条件
2. **算法思路**：思考可能的解决方案
3. **复杂度分析**：评估时间和空间复杂度
4. **代码实现**：编写清晰的代码
5. **测试验证**：考虑边界情况

你具体想了解哪部分呢？""",
                """理解算法需要多练习！这里有一些建议：

**学习路径：**
1. 掌握基础数据结构（数组、链表、栈、队列）
2. 学习基本算法（排序、搜索、递归）
3. 练习经典问题（LeetCode 前200题）
4. 总结解题模式和技巧

**推荐资源：**
- 《算法导论》- 理论基础
- LeetCode - 刷题平台
- 《算法图解》- 可视化理解

有什么具体问题想讨论吗？""",
                f"""关于"{user_message[:20]}..."这个话题：

这是一个值得深入学习的内容。建议你：
1. 先理解基本概念
2. 做几道相关练习题
3. 总结常见考点和陷阱

我可以为你详细讲解这个知识点，或者帮你分析相关的题目。你想从哪里开始？"""
            ]
            return random.choice(responses)


# 全局Mock客户端实例
_mock_client: Optional[MockClaudeClient] = None


def get_mock_claude_client() -> MockClaudeClient:
    """获取Mock Claude客户端单例"""
    global _mock_client
    if _mock_client is None:
        _mock_client = MockClaudeClient()
    return _mock_client


# 导入asyncio
import asyncio


# 真实Claude客户端（待实现）
class ClaudeClient:
    """真实Claude API客户端"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        # TODO: 初始化真实的Claude API

    async def chat(self, messages, max_tokens=None):
        """调用Claude API"""
        # TODO: 实现真实的API调用
        pass

    async def chat_stream(self, messages, max_tokens=None):
        """流式调用Claude API"""
        # TODO: 实现真实的流式API调用
        pass
