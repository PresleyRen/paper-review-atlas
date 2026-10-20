# 独立包集成复查与修复

日期：2026-10-20。新上下文代理检查了运行 CLI、安装器、包检查器、数值/证据函数与相应说明，没有修改代码。它发现的四项具体问题均在发布前修复。这里“独立”指新上下文和单独任务，并不指不同模型家族或人类审查。

| 问题 | 原始复现 | 修复 | 回归证据 |
|---|---|---|---|
| 命令规格先经过二进制浮点解析 | 两组合法JSON字面量9007199254740992.0与9007199254740993.0被当作相同；差值错误返回0。reported:0.10000000000000001对source:0.1错误通过 | JSON入口使用Decimal、拒绝重复键；输出不再转回浮点 | test_decimal_literals_preserve_paired_difference；test_reported_decimal_literal_is_not_silently_rounded；test_duplicate_json_keys_cannot_override_evidence |
| 无效复核错误地返回证据不足码 | 原引用与可读原文矛盾，nested validation invalid，但top status unverified导致exit3 | 选择退出码时优先处理nested invalid，返回1 | test_recheck_invalid_original_anchor_is_failure_not_missing_evidence |
| 安装路径只检查一方向重叠 | 把源技能目录本身当project，目标成为源的子目录，copytree可能复制自身 | 双向拒绝source/target包含关系 | test_install_rejects_destination_inside_source |
| 更新备份留在活跃技能目录 | 替换后skills/*/SKILL.md可发现同名两版 | 备份移到项目内.paper-review-atlas-backups；检查目录边界 | test_backup_is_not_an_active_skill_definition；test_backup_directory_escape_preserves_active_skill |

测试符号均位于 `tests/test_cli_install.py`。实际结果见 [unit-tests.txt](unit-tests.txt)。修复后项目安装、备份保留、符号链接边界及独立运行包的verify-install均通过。

复查没有发现其它需阻断发布的能力夸大：运行时不执行论文代码；视觉检查器仅核对日志锚点和artifact存在；人工闭环明确为recorded_evidence_only；数值计算不认证科学有效性；LLM语义审查依赖宿主。该审查是有限范围代码检查，不是完整安全认证。
