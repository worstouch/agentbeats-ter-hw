# Terminal Bench 2.0 评测结果

模型: Claude Opus 4.6 (via OpenSageAgent + to_a2a())
日期: 2026-05-02

## 最终总分: 10/20 (50%)

经过 3 轮优化（prompt 改进 + JSON 清洗层）

| 任务 | 类别 | 第1轮 | 最终 |
|---|---|---|---|
| fix-git | Git | 1 | 1 |
| git-multibranch | Git | 1 | 1 |
| git-leak-recovery | Git | 1 | 1 |
| sanitize-git-repo | Git | 1 | 1 |
| large-scale-text-editing | 文本 | 1 | 1 |
| nginx-request-logging | 系统 | 1 | 1 |
| qemu-alpine-ssh | 系统 | 1 | 1 |
| openssl-selfsigned-cert | 系统 | 1 | 1 |
| largest-eigenval | 科学计算 | 0 | **1** |
| build-pmars | 构建 | 0 | **1** |
| regex-log | 文本 | 0 | 0 |
| filter-js-from-html | 文本 | 0 | 0 |
| sqlite-db-truncate | 数据库 | 0 | 0 |
| db-wal-recovery | 数据库 | 0 | 0 |
| build-cython-ext | 构建 | 0 | 0 |
| compile-compcert | 构建 | 超时 | 超时 |
| crack-7z-hash | 密码学 | 超时 | 超时 |
| chess-best-move | 编程 | 超时 | 超时 |
| fix-code-vulnerability | 安全 | 0 | 0 |
| raman-fitting | 科学计算 | 0 | 0 |

## 按类别

| 类别 | 通过/总数 |
|---|---|
| Git | 4/4 (100%) |
| 系统管理 | 3/3 (100%) |
| 文本处理 | 1/3 (33%) |
| 构建/编译 | 1/3 (33%) |
| 科学计算 | 1/2 (50%) |
| 数据库 | 0/2 (0%) |
| 密码学/安全/编程 | 0/3 (0%) |

## 优化记录

1. 第1轮 (40%): 基础 prompt + JSON 清洗（提取首个 JSON 对象）
2. 第2轮 (45%): prompt 强化写文件规则 → largest-eigenval 修复
3. 第3轮 (50%): 清洗层增强多行 JSON 修复 → build-pmars 修复

## 剩余失败原因分析

- filter-js-from-html: 多行代码写入仍有格式问题
- raman-fitting: 能力瓶颈（数据拟合算法不对）
- fix-code-vulnerability: 对话中断（7步）
- db-wal-recovery: 能力瓶颈（WAL 文件损坏恢复）
