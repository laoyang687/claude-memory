# 高考AI工具站 — 项目进度日志

## 2026-04-01 前端部署完成

### 修复的关键问题

#### 1. Vite构建不生效（根因）
- **现象**：修改App.tsx后构建产物不变，网站始终显示旧内容
- **根因**：`index.html` 直接引用了预构建JS文件 `/assets/index-B6hpTFah.js`，Vite没有编译React源码
- **修复**：将 `index.html` 的入口改为 `<script type="module" src="/src/main.tsx"></script>`
- **教训**：项目根目录 `assets/` 下有预构建文件，导致Vite跳过源码编译

#### 2. VIP弹窗空白
- **现象**：点击"开通VIP"后页面空白
- **根因**：API返回 `{ data: { products: [...] } }`，前端 `apiFetch` 取 `json.data` 得到对象，但代码当数组 `.map()` 使用，React崩溃
- **修复**：`handleOpenVipModal` 改用 `fetch` 直接获取，正确解析 `json.data.products`，并映射字段名（`price_yuan` → `price`，`duration` → `duration_days`）

#### 3. 验证码收不到
- **现象**：输入手机号后收不到短信验证码
- **根因**：后端 `send-code` 接口未接入短信API（TODO状态），生产环境不返回验证码
- **临时修复**：后端始终返回验证码，前端显示在登录弹窗的红色提示框中
- **待办**：接入阿里云短信API

### 修改的文件

#### 前端
| 文件 | 修改内容 |
|------|----------|
| `frontend/index.html` | 入口从预构建JS改为 `/src/main.tsx` |
| `frontend/src/App.tsx` | 添加React imports；修复VIP products API解析；验证码显示 |

#### 后端
| 文件 | 修改内容 |
|------|----------|
| `api/v1/auth.py` | send-code 始终返回验证码（临时方案） |

### 部署步骤（每次更新前端）
```bash
# 1. 本地构建
cd D:\yyc\gaokao-advisor-skill\frontend
npm run build

# 2. 上传dist到服务器
scp -r dist\* root@116.62.70.99:/var/www/gaokao-advisor-skill/frontend/dist/

# 3. 上传后端文件（如有修改）
scp api\v1\auth.py root@116.62.70.99:/var/www/gaokao-advisor-skill/api/v1/auth.py

# 4. SSH到服务器重启后端
ssh root@116.62.70.99
pkill -f gunicorn; sleep 2; cd /var/www/gaokao-advisor-skill && sudo -u gaokao venv/bin/gunicorn -c config/gunicorn.conf.py api.main:app -D
```

### 当前功能状态
- ✅ HTTPS/SSL（阿里云免费证书，有效期至2026-06-29）
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

### 待完成
- [ ] SEO优化（meta标签、结构化数据、sitemap）
- [ ] 移动端适配
- [ ] 接入阿里云短信API
- [ ] 内容营销（知乎、微信公众号引流）
- [ ] 百度收录提交
