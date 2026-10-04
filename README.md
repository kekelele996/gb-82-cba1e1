# 系统监控大屏

系统资源监控数据可视化大屏，实时展示 CPU、内存、磁盘、网络等指标。

## 主要功能

- **实时仪表盘**：CPU 使用率实时折线图、内存使用率仪表盘、磁盘使用率进度条、网络流量折线图，每 5 秒自动刷新
- **历史数据查看**：支持选择最近 1 小时、6 小时、24 小时的历史数据，图表展示趋势，支持缩放查看细节
- **告警阈值配置**：可配置 CPU、内存、磁盘告警阈值，超过阈值时图表对应区域变红，告警列表记录触发时间
- **进程监控**：表格展示 TOP 10 进程，包含 PID、名称、CPU 使用率、内存使用率，每 5 秒刷新
- **数据导出**：支持导出监控数据为 CSV 格式

## 快速启动（Docker Compose）

### 一键启动

```bash
# 复制环境变量配置
cp .env.example .env

# 构建并启动所有服务
docker compose up -d --build
```

### 访问地址

- 前端页面：http://localhost:8113
- 后端 API：http://localhost:3113
- API 健康检查：http://localhost:3113/api/health/

### 常用命令

```bash
# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f

# 停止服务
docker compose down

# 停止服务并删除数据卷（清空数据库）
docker compose down -v
```

## 本地开发方式

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

前端开发服务器地址：http://localhost:3000

### 后端启动

```bash
cd backend

# 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行数据库迁移
python manage.py migrate

# 生成种子数据
python seeders/seed_data.py

# 启动开发服务器
python manage.py runserver
```

后端开发服务器地址：http://localhost:8000

## 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| 前端框架 | Vue.js | 3.x |
| 前端构建 | Vite | 5.x |
| 图表库 | ECharts | 5.x |
| 状态管理 | Pinia | 2.x |
| 后端框架 | Django | 4.2 |
| REST API | Django REST Framework | 3.14 |
| 任务调度 | APScheduler | 3.10 |
| 数据库 | PostgreSQL | 15 |
| 缓存 | Redis | 7 |

## 项目目录结构

```
gb-82/
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── components/      # Vue 组件
│   │   ├── api/             # API 请求封装
│   │   ├── store/           # Pinia 状态管理
│   │   ├── types/           # TypeScript 类型定义
│   │   ├── assets/          # 静态资源和样式
│   │   └── App.vue          # 根组件
│   ├── Dockerfile           # 前端 Docker 镜像配置
│   ├── nginx.conf           # Nginx 配置
│   └── package.json         # 前端依赖配置
├── backend/                  # 后端项目
│   ├── monitoring/          # 监控应用
│   │   ├── models.py        # 数据模型
│   │   ├── views.py         # API 视图
│   │   ├── serializers.py   # 序列化器
│   │   ├── scheduler.py     # 定时任务调度
│   │   └── admin.py         # 管理后台配置
│   ├── core/                # Django 项目配置
│   ├── seeders/             # 种子数据脚本
│   ├── Dockerfile           # 后端 Docker 镜像配置
│   ├── entrypoint.sh        # 容器启动脚本
│   └── requirements.txt     # Python 依赖
├── docker-compose.yml       # Docker Compose 编排配置
├── .env.example             # 环境变量示例
└── README.md                # 项目说明文档
```

## 环境变量说明

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DJANGO_SECRET_KEY` | Django 密钥 | - |
| `DEBUG` | 是否开启调试模式 | False |
| `DB_NAME` | PostgreSQL 数据库名 | monitoring_db |
| `DB_USER` | PostgreSQL 用户名 | monitoring_user |
| `DB_PASSWORD` | PostgreSQL 密码 | monitoring_password |
| `DB_HOST` | PostgreSQL 主机 | localhost |
| `DB_PORT` | PostgreSQL 端口 | 5613 |
| `REDIS_HOST` | Redis 主机 | localhost |
| `REDIS_PORT` | Redis 端口 | 6513 |
| `FRONTEND_PORT` | 前端服务端口 | 8113 |
| `BACKEND_PORT` | 后端服务端口 | 3113 |

## Docker 部署说明

### 端口映射

| 服务 | 容器内部端口 | 主机映射端口 | 说明 |
|------|-------------|-------------|------|
| 前端 (Nginx) | 80 | 8113 | 访问监控大屏页面 |
| 后端 (Django) | 8000 | 3113 | REST API 服务 |
| PostgreSQL | 5432 | 5613 | 数据库服务 |
| Redis | 6379 | 6513 | 缓存服务 |

### 数据卷

| 数据卷名称 | 说明 |
|-----------|------|
| monitoring_postgres_data | PostgreSQL 数据持久化 |
| monitoring_redis_data | Redis 数据持久化 |

### 常见问题

**Q: 如何重新生成种子数据？**

```bash
docker compose exec backend python seeders/seed_data.py
```

**Q: 如何查看后端日志？**

```bash
docker compose logs -f backend
```

**Q: 数据库连接失败怎么办？**

确保 PostgreSQL 服务健康：
```bash
docker compose ps postgres
```

如果状态不是 healthy，重启数据库服务：
```bash
docker compose restart postgres
```

**Q: 如何进入 Django Admin 管理后台？**

首先创建超级用户：
```bash
docker compose exec backend python manage.py createsuperuser
```

然后访问：http://localhost:3113/admin/

## License

MIT
