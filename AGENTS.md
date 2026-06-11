# digital-finance-ai-service — AI 开发代理规范

## 项目身份
- **名称**: 数字金融彩票 - AI 服务
- **端口**: 16081
- **技术栈**: Python 3 + FastAPI + Pydantic + httpx + uvicorn
- **包管理器**: pip

## 关键约定
- 遵循 `../.clinerules`（根 Rule）和本目录 `.clinerules`
- 异步优先: 使用 async/await 处理 I/O
- Pydantic BaseModel 用于请求/响应验证
- 统一响应格式: `{ "code": 0, "message": "success", "data": {} }`
- 外部 AI API 调用必须有超时和重试机制

## 快速命令
- `uvicorn app.main:app --reload --port 16081` — 启动开发服务器
- `ruff check .` — 代码检查
- `pytest` — 运行测试

## AI 调用规范
- 超时时间: 30 秒
- 熔断器模式: 连续失败 N 次后降级处理
- API Key 从环境变量加载
- 请求/响应日志脱敏记录

## 安全规范
- API Key 验证中间件
- 输入内容审核（防止 prompt injection）
- 输出内容过滤
- 请求频率限制

## 关联服务
- Go 后端: http://localhost:16080