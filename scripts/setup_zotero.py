#!/usr/bin/env python3
"""
Zotero MCP 配置工具 — 包含安装、配置、检测三合一。

功能：
  默认模式：检测 Zotero MCP 状态并显示报告
  --install: 一键安装+配置 Zotero MCP
  --check  : JSON 格式输出检测结果（供脚本调用）
  --export : 输出环境变量配置命令

Usage:
  python3 scripts/setup_zotero.py             检测状态
  python3 scripts/setup_zotero.py --install   安装+配置
  python3 scripts/setup_zotero.py --check     JSON 输出
  python3 scripts/setup_zotero.py --export    输出 export 命令
"""
import sys, os, json, subprocess, shutil, configparser

PACKAGE_NAME = "zotero-mcp-server"
CONFIG_PATH = os.path.expanduser("~/.hermes/config.yaml")
HERMES_HOME = os.path.expanduser("~/.hermes")


# ── 检测函数 ──────────────────────────────────────────────

def check_installed():
    """检测 zotero-mcp-server pip 包是否已安装"""
    try:
        r = subprocess.run(
            [sys.executable, "-m", "pip", "show", PACKAGE_NAME],
            capture_output=True, text=True, timeout=10
        )
        if r.returncode == 0:
            for line in r.stdout.splitlines():
                if line.startswith("Version:"):
                    return True, line.split(":", 1)[1].strip()
        return False, None
    except Exception:
        return False, None


def check_env():
    """检测环境变量"""
    api_key = os.environ.get("ZOTERO_API_KEY", "")
    user_id = os.environ.get("ZOTERO_USER_ID", "")
    local = os.environ.get("ZOTERO_LOCAL", "").lower() in ["true", "yes", "1"]
    return api_key, user_id, local


def detect_mode():
    """检测当前 config.yaml 中 Zotero MCP 的运行模式"""
    if not os.path.exists(CONFIG_PATH):
        return None
    try:
        import yaml
        with open(CONFIG_PATH) as f:
            cfg = yaml.safe_load(f) or {}
        zot = cfg.get("mcp_servers", {}).get("zotero", {})
        env = zot.get("env", {})
        if env.get("ZOTERO_LOCAL", "").lower() in ["true", "yes", "1"]:
            return "local"
        if env.get("ZOTERO_API_KEY"):
            return "web"
        return None
    except Exception:
        return None


def check_mcp_registered():
    """检测 config.yaml 中是否有 zotero MCP 注册"""
    if not os.path.exists(CONFIG_PATH):
        return False
    try:
        import yaml
        with open(CONFIG_PATH) as f:
            cfg = yaml.safe_load(f)
        mcp = cfg.get("mcp_servers", {}) if isinstance(cfg, dict) else {}
        return "zotero" in mcp
    except Exception:
        return False


def check_zotero_local():
    """检测 Zotero 桌面端是否运行（本地 API 端口）"""
    try:
        import urllib.request
        r = urllib.request.urlopen(
            "http://127.0.0.1:23119/api/users/1/items?limit=1", timeout=3
        )
        return True
    except Exception:
        return False


def check_mcp_process():
    """通过 Hermes CLI 检测 MCP 是否存活"""
    for cmd in ["hermes", "openclaw"]:
        if shutil.which(cmd):
            try:
                r = subprocess.run(
                    [cmd, "mcp", "list"], capture_output=True, text=True, timeout=5
                )
                if "zotero" in r.stdout.lower():
                    return True
            except Exception:
                pass
    return False


# ── 安装与配置 ─────────────────────────────────────────────

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKAGES_DIR = os.path.join(SKILL_DIR, "scripts", "packages")


def find_local_wheel():
    """在 skill 的 packages/ 目录查找本地 wheel 文件"""
    if not os.path.isdir(PACKAGES_DIR):
        return None
    for f in os.listdir(PACKAGES_DIR):
        if f.startswith("zotero_mcp_server") and f.endswith(".whl"):
            return os.path.join(PACKAGES_DIR, f)
    return None


def install_package():
    """安装 zotero-mcp-server — 优先本地 wheel，跨平台编译包自动从 PyPI 补全"""
    local_wheel = find_local_wheel()

    if local_wheel:
        pkgs_dir = os.path.dirname(local_wheel)
        print(f"  发现本地包目录: {pkgs_dir} ({len(os.listdir(pkgs_dir))} 个 wheel)")
        print(f"  使用 --find-links 本地优先策略...")
        # --find-links: pip优先用本地wheel，缺的平台二进制自动降级到PyPI
        r = subprocess.run(
            [sys.executable, "-m", "pip", "install",
             "zotero-mcp-server",
             "--find-links", pkgs_dir,
             "-q"],
            capture_output=True, text=True, timeout=120
        )
        if r.returncode == 0:
            print(f"  ✅ zotero-mcp-server 安装成功")
            return True
        else:
            err = r.stderr.strip()
            if "find-links" in err.lower():
                print(f"  ⚠ --find-links 失败，尝试直接安装本地 wheel...")
                r2 = subprocess.run(
                    [sys.executable, "-m", "pip", "install",
                     local_wheel,
                     "--find-links", pkgs_dir,
                     "-q"],
                    capture_output=True, text=True, timeout=120
                )
                if r2.returncode == 0:
                    print(f"  ✅ zotero-mcp-server 安装成功")
                    return True
            print(f"  ❌ 安装失败，尝试从 PyPI 下载...")

    print(f"  从 PyPI 安装 {PACKAGE_NAME}（需联网）...")
    r = subprocess.run(
        [sys.executable, "-m", "pip", "install", PACKAGE_NAME, "-q"],
        capture_output=True, text=True, timeout=120
    )
    if r.returncode == 0:
        print(f"  ✅ {PACKAGE_NAME} 安装成功（PyPI）")
        return True
    else:
        print(f"  ❌ 安装失败: {r.stderr.strip()}")
        return False


def get_zotero_bin():
    """获取 zotero-mcp 可执行文件路径"""
    # 优先用 pip show 定位
    try:
        r = subprocess.run(
            [sys.executable, "-m", "pip", "show", PACKAGE_NAME],
            capture_output=True, text=True, timeout=10
        )
        for line in r.stdout.splitlines():
            if line.startswith("Location:"):
                site_pkgs = line.split(":", 1)[1].strip()
                # zotero-mcp 可执行文件通常在 bin/ 目录（同级或上一级）
                for candidate in [
                    os.path.join(os.path.dirname(site_pkgs), "bin", "zotero-mcp"),
                    os.path.join(site_pkgs, "bin", "zotero-mcp"),
                ]:
                    if os.path.exists(candidate):
                        return candidate
    except Exception:
        pass
    # fallback: which
    return shutil.which("zotero-mcp") or "zotero-mcp"


def configure_mcp(api_key="", user_id="", local_mode=False):
    """写入/更新 config.yaml 的 mcp_servers.zotero 节

    Args:
        api_key: Web API 模式时需要的 Zotero API Key
        user_id: Web API 模式时需要的 Zotero 用户数字 ID
        local_mode: True=本地模式（桌面端直连），False=Web API 模式
    """
    import yaml

    # 确保目录存在
    os.makedirs(HERMES_HOME, exist_ok=True)

    # 读取或创建配置
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            cfg = yaml.safe_load(f) or {}
    else:
        cfg = {}

    # 确保 mcp_servers 存在
    if "mcp_servers" not in cfg:
        cfg["mcp_servers"] = {}

    zotero_bin = get_zotero_bin()

    if local_mode:
        env = {
            "ZOTERO_LOCAL": "true",
            "no_proxy": "localhost,127.0.0.1,::1",
            "NO_PROXY": "localhost,127.0.0.1,::1",
        }
        print(f"  ✅ 模式: 本地 API（桌面端直连，仅读取）")
    else:
        env = {
            "ZOTERO_API_KEY": api_key,
            "ZOTERO_LIBRARY_ID": user_id,
            "no_proxy": "localhost,127.0.0.1,::1",
            "NO_PROXY": "localhost,127.0.0.1,::1",
        }
        print(f"  ✅ 模式: Web API（远程，支持读写）")

    cfg["mcp_servers"]["zotero"] = {
        "command": zotero_bin,
        "env": env,
        "enabled": True,
    }

    with open(CONFIG_PATH, "w") as f:
        yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True)

    print(f"  ✅ MCP 配置已写入 {CONFIG_PATH}")
    print(f"     command: {zotero_bin}")
    if local_mode:
        print(f"     ZOTERO_LOCAL: true（本地模式）")
    else:
        print(f"     library_id: {user_id}")
        print(f"     api_key: {'***' + api_key[-4:] if len(api_key) > 4 else '***'}")


def prompt_and_install():
    """交互式安装流程"""
    print("=" * 55)
    print("  Zotero MCP 一键安装与配置")
    print("=" * 55)

    # 1. 安装包
    installed, ver = check_installed()
    if installed:
        print(f"\n✅ zotero-mcp-server (v{ver}) 已安装，跳过安装步骤。")
    else:
        print(f"\n⏳ {PACKAGE_NAME} 未安装，开始安装...")
        if not install_package():
            print("\n❌ pip 安装失败。请手动执行:")
            print(f"   pip install {PACKAGE_NAME}")
            return False

    # 2. 选择连接模式
    current_mode = detect_mode()
    if current_mode:
        mode_hint = "本地" if current_mode == "local" else "Web API"
        print(f"\n当前已配置模式: {mode_hint}")
        try:
            val = input("  是否切换模式？(y/n, 默认 n): ").strip().lower()
            if val == "y":
                current_mode = None  # 强制进入选择流程
        except (EOFError, KeyboardInterrupt):
            print("   [跳过]")
            return True

    if not current_mode:
        print("\n请选择 Zotero 连接模式：")
        print("  1) Web API（远程连接 zotero.org，支持读写操作）")
        print("     需要 API Key，不需要 Zotero 桌面端运行")
        print("  2) 本地 API（直连 Zotero 桌面端，无需 API Key）")
        print("     仅支持读取，需要 Zotero 桌面端保持运行")
        print()
        try:
            choice = input("  请输入 1 或 2（默认 1）: ").strip()
        except (EOFError, KeyboardInterrupt):
            choice = ""

        local_mode = (choice == "2")

        if local_mode:
            # 本地模式 — 不需要 API Key
            print(f"\n📋 本地模式配置")
            if not check_zotero_local():
                print("  ⚠ 未检测到 Zotero 桌面端运行。")
                print("    请先启动 Zotero 桌面端，然后重新运行本脚本。")
                print("    或继续配置，稍后启动 Zotero。")
            configure_mcp(local_mode=True)
        else:
            # Web API 模式 — 需要 API Key 和 User ID
            print(f"\n📋 Web API 模式配置")
            api_key, user_id, _ = check_env()
            if not api_key:
                print("\n请输入你的 Zotero API Key：")
                print("  （打开 https://www.zotero.org/settings/keys 创建）")
                try:
                    val = input("   ZOTERO_API_KEY: ").strip()
                    if val:
                        api_key = val
                except (EOFError, KeyboardInterrupt):
                    print("   [跳过输入]")

            if not user_id:
                print("\n请输入你的 Zotero 用户数字 ID：")
                print("  （打开 zotero.org/settings/keys，URL 中可找到数字 ID）")
                try:
                    val = input("   ZOTERO_USER_ID: ").strip()
                    if val:
                        user_id = val
                except (EOFError, KeyboardInterrupt):
                    print("   [跳过输入]")

            if api_key and user_id:
                configure_mcp(api_key=api_key, user_id=user_id)
            else:
                print("\n⚠  API Key 或 User ID 不完整，跳过配置写入。")
                print("   可稍后手动编辑 ~/.hermes/config.yaml 补全。")
                return False
    else:
        print(f"  保持当前配置不变。")

    # 4. 验证
    print("\n" + "=" * 55)
    print("  安装完成！重启 Hermes 后生效。")
    print("  验证命令：")
    print("    hermes mcp list          # 查看 MCP 列表")
    print("    python3 setup_zotero.py  # 运行本脚本检测状态")
    print("=" * 55)
    return True


# ── 状态报告 ──────────────────────────────────────────────

def print_status():
    """打印人类可读的状态报告"""
    installed, ver = check_installed()
    api_key, user_id, local_env = check_env()
    mode = detect_mode()
    registered = check_mcp_registered()
    alive = check_mcp_process()
    local_ok = check_zotero_local()

    print("=" * 50)
    print("  Zotero MCP 环境检测")
    print("=" * 50)

    # 1. 包安装
    if installed:
        print(f"\n📦 zotero-mcp-server  v{ver}  ✅ 已安装")
    else:
        print(f"\n📦 zotero-mcp-server     ❌ 未安装")
        print("   执行 python3 setup_zotero.py --install 一键安装")

    # 2. 模式
    mode_text = {"web": "Web API（远程读写）", "local": "本地 API（桌面端只读）"}
    if registered and mode:
        print(f"🔌 连接模式:           {mode_text.get(mode, mode)}")
    else:
        print(f"🔌 连接模式:           未配置")

    # 3. 可执行文件
    zotero_bin = get_zotero_bin()
    if zotero_bin and os.path.exists(zotero_bin):
        print(f"🔧 可执行文件:         {zotero_bin}")
    else:
        print(f"🔧 可执行文件:         未找到")

    # 4. 配置注册
    if registered:
        print(f"⚙️  config.yaml 注册:    ✅ 已配置")
    else:
        print(f"⚙️  config.yaml 注册:    ❌ 未配置")

    # 5. 环境变量
    if mode == "web":
        print(f"🔑 ZOTERO_API_KEY:     {'✅ 已设置' if api_key else '❌ 未设置'}")
        print(f"👤 ZOTERO_LIBRARY_ID:  {'✅ 已设置 (' + user_id + ')' if user_id else '❌ 未设置'}")
    elif mode == "local":
        print(f"🔑 ZOTERO_LOCAL:       ✅ true（本地模式）")

    # 6. 进程存活
    if alive:
        print(f"🚀 MCP 进程:            ✅ 运行中")
    else:
        print(f"🚀 MCP 进程:            ⏸️  未启动（重启 Hermes 后生效）")

    # 7. Zotero 桌面端
    if local_ok:
        print(f"💻 Zotero 桌面端:        ✅ 运行中")
    else:
        print(f"💻 Zotero 桌面端:        ⏹️  未检测到")

    # 总结
    print()
    if installed and registered and (mode == "local" or api_key):
        print("🎯 状态：就绪，Zotero MCP 可正常使用")
    elif installed and not registered:
        print("💡 提示：包已安装，执行 --install 完成配置写入")
    else:
        print("💡 提示：执行 python3 setup_zotero.py --install 一键配置")
    print()


# ── 主入口 ──────────────────────────────────────────────

if __name__ == "__main__":
    if "--install" in sys.argv:
        prompt_and_install()
    elif "--check" in sys.argv:
        installed, ver = check_installed()
        api_key, user_id, local_env = check_env()
        mode = detect_mode()
        result = {
            "installed": installed,
            "version": ver,
            "mode": mode,
            "api_key_set": bool(api_key),
            "user_id_set": bool(user_id),
            "local_mode": local_env,
            "mcp_registered": check_mcp_registered(),
            "mcp_alive": check_mcp_process(),
            "local_running": check_zotero_local(),
            "binary": get_zotero_bin(),
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif "--export" in sys.argv:
        print("# Zotero MCP 环境变量（二选一）")
        print("#")
        print("# 选项 A: Web API 模式（远程，支持读写）")
        print('export ZOTERO_API_KEY="你的_API_KEY"')
        print('export ZOTERO_USER_ID="你的_USER_ID"')
        print("#")
        print("# 选项 B: 本地模式（桌面端直连，仅读取）")
        print("# export ZOTERO_LOCAL=true")
        print("#")
        print("# 查看完整配置：python3 setup_zotero.py")
    else:
        print_status()
