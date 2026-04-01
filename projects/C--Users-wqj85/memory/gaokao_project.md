---
name: gaokao-project
description: 高考AI工具站项目 — gaokao-baoming.com 变现计划
type: project
---

# 高考AI工具站项目

## 项目概述
目标：把$100变成$10,000。用户（杨运才）出5%精力当代理人，Claude出95%执行力。

## 域名与部署
- **域名**：gaokao-baoming.com
- **阿里云服务器**：116.62.70.99（Ubuntu 22.04.5 LTS）
- **项目路径**：`/var/www/gaokao-advisor-skill/`
- **本地源码**：`D:\yyc\gaokao-advisor-skill\`
- **数据库**：47MB SQLite（`gaokao_advisor.db`）

---

## 聊天记录

### 2026-04-01 项目启动

#### 对话1：100美金变1万美金
用户提出挑战：给我100美金，你把它变成1万美金。

我的分析：
- 100→10000是100倍杠杆，核心不是钱，是时间和技能
- 我缺一双手和一个身份（不能注册账号、收钱、处理验证码）
- 需要用户当"代理人"，用户出5%精力，我出95%执行力
- 用户同意参与

#### 对话2：用户资源确认
通过问答确认：
- **目标市场**：交给我定（选了英文市场）
- **每日时间**：15分钟以内
- **已有资源**：GitHub账号、ChatGPT/Claude付费账号、域名gaokao-baoming.com

#### 对话3：市场调研
调研了英文市场AI工具方向，Top 3：
1. AI非营利组织补助金提案助手（推荐）
2. AI播客节目笔记生成器
3. AI简历+求职信定制工具

#### 对话4：方向调整
用户透露有域名gaokao-baoming.com（高考报名），方向调整为：
- **线1（优先）**：高考AI工具站，用现有域名，中国市场
- **线2（后续）**：英文AI Grant Proposal助手
- 用户选择"两个都做"

#### 对话5：产品方案设计
设计了高考AI志愿填报助手方案：
- 免费功能：基础推荐（前5所）、基础分析、限3次查询
- 付费功能（¥19.9-99）：完整推荐、深度分析、无限查询、AI对话
- 变现预估：高峰期月收入¥5000-50000
- 用户需要做的事：域名DNS（5分钟）+ 微信支付（15分钟）+ 分享（10分钟）

#### 对话6：服务器探索
登录阿里云服务器（116.62.70.99），发现项目已经开发了60%！

**现有架构：**
- 前端：React 19 + TypeScript + Vite（单文件App.tsx，952行）
- 后端：Python + FastAPI + Gunicorn（6个worker，端口8000）
- 数据库：SQLite（47MB，有大量数据）
- Web服务器：Nginx（反向代理）
- 爬虫：scrape_sequential.py 正在运行

**已完成的功能：**
1. 智能推荐（冲稳保方案）
2. 避坑检测（高/中/低风险分级）
3. 每日真相（教育真相卡片）
4. 分数↔排名双向转换
5. 一分一段表查询
6. 院校搜索+录取历史
7. 专业搜索+就业数据
8. 评论系统（后端）
9. 认证系统（JWT，后端）

**重大发现：支付系统已写好但未接入！**
- `modules/payment.py`（858行）：微信支付完整实现
- `api/payment_routes.py`（455行）：支付API路由已写好
- VIP会员系统：月VIP¥99、季VIP¥267、年VIP¥888
- 查询配额系统：免费10次/月，VIP无限
- **但**：`api/main.py`没有注册支付路由，认证只有微信小程序登录

**变现缺口更新：**
1. ✅ HTTPS/SSL — 已解决
2. ✅ 付费系统后端 — 已接入
3. ✅ 网站端登录 — 已添加手机号登录
4. 🔄 前端UI升级 — 开发中
5. [ ] SEO优化
6. [ ] 移动端适配

#### 对话7：执行计划确认
确定两步走策略：
- **第1步（1-2周）**：快速补齐变现能力 — HTTPS + 付费墙 + 微信支付 + 前端美化
- **第2步（高考前）**：引流增长 — SEO + 内容 + 社交媒体

用户确认"方向很好，继续"。

#### 对话8：HTTPS配置（踩坑记录）
**Let's Encrypt certbot失败：**
- 安装certbot + python3-certbot-nginx成功
- `certbot --nginx`失败（403错误，ACME验证路径被Nginx拦截）
- `certbot --standalone`也失败（ConnectionResetError）
- 原因：阿里云安全组可能阻断了Let's Encrypt服务器（国外IP）

**解决方案：阿里云免费SSL证书**
1. 阿里云控制台 → SSL证书 → 免费证书 → 申请
2. DNS验证：添加TXT记录 `_dnsauth.gaokao-baoming.com`
3. DNS验证需要在**云解析DNS**里添加（域名需使用阿里云DNS）
4. 审核通过后下载Nginx格式证书

**Nginx HTTPS配置踩坑：**
- 最初用heredoc写配置失败（终端格式化问题，Ctrl+C中断）
- 用Python写配置也失败（缩进错误）
- 最终方案：在本地D:\yyc写好配置文件，scp上传到服务器
- 配置文件路径：`/etc/nginx/sites-available/gaokao-advisor`
- 发现sites-enabled里有.bak备份文件导致冲突（重复server_name）
- 删除.bak后重启成功

**HTTPS配置完成：**
- 证书文件：`/etc/nginx/ssl/gaokao.pem` + `gaokao.key`
- HTTP自动301跳转到HTTPS
- SSL协议：TLSv1.2 + TLSv1.3
- 验证：`curl -I https://gaokao-baoming.com` 返回200 OK

#### 对话9：支付系统接入 + 手机号登录

**后端修改：**
1. `api/main.py`：添加import payment_router, vip_router + include_router
2. `api/v1/auth.py`：添加手机号登录端点
   - `POST /api/v1/auth/send-code` — 发送验证码（60秒频率限制，5分钟过期）
   - `POST /api/v1/auth/phone-login` — 手机号+验证码登录（自动注册新用户）
   - 验证码存储在内存（生产环境应用Redis）
   - 开发模式DEBUG=true时直接返回验证码
3. `api/config.py`：CORS添加gaokao-baoming.com域名

**踩坑：**
- 第一次上传auth.py后gunicorn启动失败：`NameError: name 'Session' is not defined`
- 原因：添加了`session: Session = Depends(get_db)`但没导入Session
- 修复：添加`from sqlalchemy.orm import Session`

**验证成功：**
- `GET /api/v1/payment/products` — 返回3个VIP产品 ✅
- `POST /api/v1/auth/send-code` — 发送验证码成功 ✅

**新增API端点汇总：**
- `POST /api/v1/auth/send-code` — 发送短信验证码
- `POST /api/v1/auth/phone-login` — 手机号登录
- `GET /api/v1/payment/products` — VIP产品列表
- `POST /api/v1/payment/create` — 创建支付订单
- `POST /api/v1/payment/notify` — 微信支付回调
- `GET /api/v1/payment/orders` — 用户订单列表
- `GET /api/v1/payment/status/{order_no}` — 订单状态
- `POST /api/v1/payment/refund` — 申请退款
- `GET /api/v1/vip/status` — VIP状态
- `GET /api/v1/vip/benefits` — VIP权益说明

---

## 任务清单

### 待执行
- [ ] 前端UI升级（开发中，后台Agent处理中）
  - 登录弹窗（手机号+验证码）
  - VIP会员购买弹窗
  - 用户信息显示（头像、昵称、剩余次数）
  - 查询配额提示
- [ ] 前端构建+部署到服务器
- [ ] SEO优化和内容引流

### 已完成
- [x] 市场调研
- [x] 产品方案设计
- [x] 服务器探索和现状分析
- [x] 执行计划制定
- [x] 把项目源码拉到本地（D:\yyc\gaokao-advisor-skill\）
- [x] 配置HTTPS/SSL证书（2026-04-01完成）
  - Let's Encrypt certbot失败（阿里云安全组阻断）
  - 改用阿里云免费SSL证书 + DNS验证成功
  - Nginx配置HTTPS + HTTP自动跳转HTTPS
  - 证书文件：/etc/nginx/ssl/gaokao.pem + gaokao.key
- [x] 接入支付路由到main.py（2026-04-01完成）
  - 支付API、VIP API全部注册到生产入口
- [x] 添加网站端手机号登录（2026-04-01完成）
  - send-code + phone-login 端点
  - 修复Session import bug

---

## 用户资源
- GitHub账号（已有）
- ChatGPT/Claude付费账号（已有）
- 域名gaokao-baoming.com（已有，部署在阿里云）
- 阿里云服务器 116.62.70.99（Ubuntu 22.04，98GB磁盘）
- 每天可投入时间：15分钟以内

## 关键时间节点
- 2026-04-01：项目启动，HTTPS完成，支付API上线，手机号登录完成
- 4月：前端UI升级 + 部署
- 5月：SEO优化 + 内容积累
- 6-7月：高考季流量高峰，重点变现

## 技术笔记
- **服务器操作方式**：用户SSH登录后手动执行命令（我无法直接SSH）
- **文件上传方式**：本地写好文件 → scp上传到服务器
- **PowerShell限制**：多行bash命令在PowerShell中会被分行执行，需要一行一条
- **Nginx配置文件**：`/etc/nginx/sites-available/gaokao-advisor`（符号链接到sites-enabled）
- **Gunicorn配置**：`/var/www/gaokao-advisor-skill/config/gunicorn.conf.py`
- **重启后端命令**：`pkill -f gunicorn; sleep 2; cd /var/www/gaokao-advisor-skill && sudo -u gaokao venv/bin/gunicorn -c config/gunicorn.conf.py api.main:app -D`
- **Gunicorn日志**：`/var/log/gaokao_advisor/error.log`
