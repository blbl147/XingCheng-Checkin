# ✨ Actions-Checkin

<div align="center">

[![GitHub Stars](https://img.shields.io/github/stars/yourusername/Actions-Checkin?style=flat-square)](https://github.com/yourusername/Actions-Checkin/stargazers)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![GitHub Actions](https://img.shields.io/badge/GitHub-Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)](https://github.com/features/actions)

**Actions 的自动签到**

支持平台：龙空 | 星城

[快速开始](#-快速开始) · [常见问题](#-常见问题)

</div>

---

## 📋 目录

- [支持平台](#-支持平台)
- [快速开始](#-快速开始)
- [运行测试](#-运行测试)
- [常见问题](#-常见问题)
- [开发计划](#-开发计划)
- [贡献指南](#-贡献指南)
- [许可证](#-许可证)

---

## 🎯 支持平台

| 平台 | 状态 | 说明 |
|------|------|------|
| 🐉 龙空 | ✅ 支持 | 基于 Cookie 认证 |
| 🌟 星城 | ✅ 支持 | 基于 Token 认证 |

---

## 🚀 快速开始

### 1. Fork 本仓库

点击右上角 **Fork** 按钮，将项目复制到你的账户下。

### 2. 配置 Secrets

进入你 Fork 的仓库，点击：

```
Settings → Secrets and variables → Actions → New repository secret
```

### 3. 启用 Actions

进入 **Actions** 标签页，点击 **I understand my workflows, go ahead and enable them**。

### 4. 手动触发测试

在 **Actions** 页面选择对应的 Workflow，点击 **Run workflow** 进行测试。

---

## ⚙️ 配置说明

### 🐉 龙空签到配置

#### 获取 Cookie

1. 使用浏览器登录 [龙空](https://www.lkong.com/)
2. 按 `F12` 打开开发者工具
3. 切换到 **Network（网络）** 标签
4. 刷新页面，点击任意请求
5. 在 **Headers（请求头）** 中找到 `Cookie` 字段
6. 复制完整的 Cookie 值

#### 添加到 Secrets

| Secret Name | 说明 | 示例 |
|-------------|------|------|
| `LKONG_COOKIE` | 龙空网站的 Cookie | `123456` |

---

### 🌟 星城签到配置

#### 获取 Token 和 App ID

1. 打开微信小程序：`#小程序://星城/rD4FdKj2vw6Fo0o`
2. 使用抓包工具（如 Charles、Fiddler）或小程序调试工具
3. 查找请求 URL：`https://api.lzstack.com/mall/v2/api/checkin/handler`
4. 在 **请求标头（Request Headers）** 中找到以下字段：
   - `token` - 用户认证令牌
   - `app-id` - 应用标识符

#### 添加到 Secrets

| Secret Name | 说明 | 示例 |
|-------------|------|------|
| `CHECKIN_TOKEN` | 星城 API 的 Token | `123456...` |
| `APP_ID` | 星城应用的 App ID | `wx1234567890abcdef` |

---

## 🧪 运行测试

配置完成后，可以通过以下方式测试：

### 手动触发

```
Actions → 选择 Workflow → Run workflow
```

### 查看日志

点击运行记录，查看详细的执行日志，确认签到是否成功。

---

## ❓ 常见问题

<details>
<summary><b>Q1: 如何修改签到时间？</b></summary>

编辑 `.github/workflows/*.yml` 文件中的 `cron` 表达式：

```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # 每天 UTC 00:00（北京时间 08:00）
```

</details>

<details>
<summary><b>Q2: Cookie/Token 过期怎么办？</b></summary>

重新获取并更新 GitHub Secrets 中的对应值。

</details>

<details>
<summary><b>Q3: Actions 没有自动运行？</b></summary>

检查以下几点：
- 确保已启用 Actions
- 检查 Workflow 文件语法是否正确
- 仓库需要有提交活动（Fork 后至少有一次 Commit）

</details>

<details>
<summary><b>Q4: 如何添加通知推送？</b></summary>

可以集成以下服务：
- Server酱
- Bark
- Telegram Bot
- 企业微信/钉钉机器人

</details>

---

## 📅 开发计划

- [ ] 添加更多平台支持
- [ ] 支持多账户签到
- [ ] 集成消息通知服务
- [ ] 添加签到失败重试机制
- [ ] 提供 Docker 部署方案

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送到分支：`git push origin feature/AmazingFeature`
5. 提交 Pull Request

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---

## ⚠️ 免责声明

本项目仅供学习交流使用，请勿用于商业用途。使用本项目所产生的一切后果由使用者自行承担。

---

## 💖 支持项目

如果这个项目对你有帮助，欢迎：

- ⭐ Star 本项目
- 🐛 提交 Issue 反馈问题
- 🔀 提交 PR 贡献代码
- 📢 分享给更多人

---

<div align="center">

**Made with ❤️ by cecil(blbl147)**

</div>
