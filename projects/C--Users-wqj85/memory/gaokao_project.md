---
name: gaokao-project
description: 高考AI工具站项目 — gaokao-baoming.com 变现计划
type: project
---

# 高考AI工具站项目

## 项目概述
目标：把$100变成$10,000。用户（杨运才）出5%精力当代理人，Claude出95%执行力。

## 域名与部署
- **域名**：gaokao-baoming.com（不带www，SSL证书只覆盖裸域名）
- **阿里云服务器**：116.62.70.99（Ubuntu 22.04.5 LTS）
- **项目路径**：`/var/www/gaokao-advisor-skill/`
- **本地源码**：`D:\yyc\gaokao-advisor-skill\`
- **数据库**：47MB SQLite（`gaokao_advisor.db`）

---

## 2026-04-01 完整开发日志

### 对话1-5：项目启动与方向确定
- 用户提出$100→$10,000挑战
- 确认资源：GitHub账号、域名gaokao-baoming.com、阿里云服务器
- 方向调整为中国高考市场（利用现有域名）
- 设计产品方案：免费+VIP付费模式

### 对话6：服务器探索
发现项目已开发60%，前后端架构完整：
- 前端：React 19 + TypeScript + Vite
- 后端：Python + FastAPI + Gunicorn
- 数据库：SQLite（47MB）
- 支付系统已写好但未接入（payment.py 858行）

### 对话7-9：HTTPS + 支付接入 + 手机号登录
- Let's Encrypt失败（阿里云安全组阻断），改用阿里云免费SSL证书
- Nginx HTTPS配置完成（/etc/nginx/ssl/gaokao.pem + gaokao.key）
- 接入支付路由到main.py
- 添加手机号登录API（send-code + phone-login）

### 对话10：前端部署（重大踩坑）

**根因：Vite构建不生效**
- **现象**：修改App.tsx后构建产物不变
- **根因**：`index.html` 直接引用预构建JS `/assets/index-B6hpTFah.js`，Vite没有编译React源码
- **修复**：入口改为 `<script type="module" src="/src/main.tsx"></script>`
- **教训**：项目根目录 `assets/` 下有预构建文件，导致Vite跳过源码编译

**VIP弹窗空白**
- **根因**：API返回 `{ data: { products: [...] } }`，前端取 `json.data` 得到对象但当数组 `.map()` 使用
- **修复**：直接用fetch解析 `json.data.products`，映射字段名

**验证码收不到**
- **根因**：后端未接入短信API
- **临时方案**：后端始终返回验证码，前端显示在登录弹窗

### 对话11：SEO技术优化
- Meta标签（title/description/keywords 针对高考志愿搜索词）
- Open Graph社交分享标签
- JSON-LD结构化数据（WebApplication类型）
- robots.txt + sitemap.xml
- 移动端适配增强

### 对话12：SEO内容文章
创建3篇攻略HTML页面：
1. `gaokao-zhiyuan-tianbao-zhinan.html` — 2026高考志愿填报完全指南
2. `yifen-yiduan-biao-zenme-kan.html` — 一分一段表怎么看
3. `pingxing-zhiyuan-tianbao-jiqiao.html` — 平行志愿填报技巧
- 主站底部添加文章链接（内链SEO）

### 对话13：百度站长平台
- HTML标签验证失败（百度服务器连不上HTTPS）
- 文件验证成功（不带www域名）
- 提交4个URL到百度收录

---

## 当前功能清单
- ✅ 智能推荐（冲稳保方案）
- ✅ 避坑检测（高/中/低风险分级）
- ✅ 每日真相（教育真相卡片）
- ✅ 分数↔排名双向转换
- ✅ 一分一段表查询
- ✅ 院校搜索+录取历史
- ✅ 专业搜索+就业数据
- ✅ 手机号登录（验证码显示在页面上）
- ✅ VIP会员购买弹窗（月¥99/季¥267/年¥888）
- ✅ 用户信息显示（头像、昵称、剩余次数）
- ✅ SEO元数据+结构化数据+robots.txt+sitemap.xml
- ✅ 3篇SEO攻略文章
- ✅ 百度站长平台验证+URL提交

## 待完成
- [ ] 短信API接入（替换临时验证码方案）
- [ ] 外链引流（知乎、小红书等）
- [ ] 百度收录后监控排名
- [ ] 更多SEO文章（每周2-3篇）
- [ ] 百度统计/Google Analytics接入

---

## API端点汇总
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

## 部署流程
1. 本地构建：`cd D:\yyc\gaokao-advisor-skill\frontend && npm run build`
2. 上传dist：`scp -r dist\* root@116.62.70.99:/var/www/gaokao-advisor-skill/frontend/dist/`
3. 上传后端（如有修改）：`scp api\v1\auth.py root@116.62.70.99:/var/www/gaokao-advisor-skill/api/v1/auth.py`
4. 重启后端：`pkill -f gunicorn; sleep 2; cd /var/www/gaokao-advisor-skill && sudo -u gaokao venv/bin/gunicorn -c config/gunicorn.conf.py api.main:app -D`
5. 清理旧JS：删除dist/assets/下不再被index.html引用的旧文件

---

## 关键时间节点
- 2026-04-01：项目启动，全栈上线，SEO+百度提交完成
- 4月：内容积累，每周2-3篇SEO文章
- 5月：外链引流，知乎/小红书推广
- 6-7月：高考季流量高峰，重点变现

## 技术笔记
- **服务器操作方式**：用户SSH登录后手动执行命令（我无法直接SSH）
- **文件上传方式**：本地写好文件 → scp上传到服务器
- **PowerShell限制**：多行bash命令会被分行执行，需一行一条
- **SSL证书**：阿里云免费证书，只覆盖gaokao-baoming.com（不含www），有效期至2026-06-29
- **百度站长**：已验证，站点URL为 https://gaokao-baoming.com（不带www）
- **Nginx配置**：`/etc/nginx/sites-available/gaokao-advisor`（符号链接到sites-enabled）
- **Gunicorn配置**：`/var/www/gaokao-advisor-skill/config/gunicorn.conf.py`
- **重启后端命令**：`pkill -f gunicorn; sleep 2; cd /var/www/gaokao-advisor-skill && sudo -u gaokao venv/bin/gunicorn -c config/gunicorn.conf.py api.main:app -D`
- **Gunicorn日志**：`/var/log/gaokao_advisor/error.log`
- **Vite构建注意**：index.html必须用 `/src/main.tsx` 入口，不能用预构建JS文件
