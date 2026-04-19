#!/usr/bin/env python3
"""
快速启动脚本 - 互动式周报生成

使用方式: python quick_start.py
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime


def setup_api_key():
    """检查并设置API key"""
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        print("⚠️  未检测到 ANTHROPIC_API_KEY 环境变量\n")
        print("请输入你的 Anthropic API key:")
        print("(从 https://console.anthropic.com 获取)\n")

        api_key = input("API Key: ").strip()

        if not api_key:
            print("❌ API Key 不能为空")
            return False

        # 临时设置
        os.environ["ANTHROPIC_API_KEY"] = api_key
        print(f"✅ API Key 已设置 (临时)\n")

        # 提供永久设置建议
        print("💡 建议：设置环境变量以避免每次输入")
        print("   Windows: setx ANTHROPIC_API_KEY \"你的key\"")
        print("   Linux/Mac: export ANTHROPIC_API_KEY='你的key'\n")

    return True


def select_pdf():
    """让用户选择PDF文件"""
    print("📁 选择PDF文件\n")

    # 列出当前目录的PDF文件
    pdf_files = list(Path(".").glob("*.pdf"))

    if not pdf_files:
        print("❌ 当前目录没有找到PDF文件\n")
        print("请手动输入PDF路径:")
        pdf_path = input("PDF 路径: ").strip()

        if not Path(pdf_path).exists():
            print(f"❌ 文件不存在: {pdf_path}")
            return None

        return pdf_path

    if len(pdf_files) == 1:
        print(f"✅ 检测到PDF: {pdf_files[0].name}")
        use_it = input("使用这个文件? (y/n): ").strip().lower()

        if use_it == 'y':
            return str(pdf_files[0])

    print("找到以下PDF文件:\n")
    for i, pdf in enumerate(pdf_files, 1):
        print(f"{i}. {pdf.name}")

    print(f"{len(pdf_files) + 1}. 手动输入路径\n")

    choice = input("选择 (输入序号): ").strip()

    try:
        choice_num = int(choice)

        if 1 <= choice_num <= len(pdf_files):
            return str(pdf_files[choice_num - 1])
        elif choice_num == len(pdf_files) + 1:
            pdf_path = input("PDF 路径: ").strip()
            if Path(pdf_path).exists():
                return pdf_path
            else:
                print(f"❌ 文件不存在: {pdf_path}")
                return None
        else:
            print("❌ 选择无效")
            return None
    except ValueError:
        print("❌ 请输入有效的序号")
        return None


def input_week_info():
    """获取周期信息"""
    print("\n📅 周期信息\n")
    print("输入格式示例:")
    print("  - 第4周")
    print("  - 2026-04-18 至 2026-04-25")
    print("  - W4")

    default_week = f"第{datetime.now().isocalendar()[1]}周"
    week_info = input(f"周期 (默认: {default_week}): ").strip()

    if not week_info:
        week_info = default_week

    return week_info


def confirm_settings(pdf_path, week_info):
    """确认设置"""
    print("\n✅ 确认设置\n")
    print(f"📄 PDF 文件: {pdf_path}")
    print(f"📅 周期: {week_info}")
    print(f"🤖 模型: claude-opus-4-6")
    print(f"💾 输出目录: ./每周总结/\n")

    confirm = input("开始生成? (y/n): ").strip().lower()

    return confirm == 'y'


def run_generator(pdf_path, week_info):
    """运行生成器"""
    print("\n" + "="*50)
    print("🚀 开始生成周报...")
    print("="*50 + "\n")

    try:
        # 检查脚本是否存在
        if not Path("weekly_summary_generator.py").exists():
            print("❌ 找不到 weekly_summary_generator.py")
            print("   请确保在正确的目录下运行此脚本")
            return False

        # 运行主脚本
        result = subprocess.run(
            [sys.executable, "weekly_summary_generator.py", pdf_path, week_info],
            capture_output=False,
            text=True
        )

        if result.returncode == 0:
            print("\n" + "="*50)
            print("✨ 周报生成成功!")
            print("="*50)

            # 提示查看输出
            print("\n📂 查看结果:")
            print("  1. 周报: 每周总结/")
            print("  2. 索引: 每周日志索引.md")
            print("  3. 日志: 已读文档日志.md")

            return True
        else:
            print("\n❌ 生成失败")
            return False

    except Exception as e:
        print(f"\n❌ 出错: {e}")
        return False


def main():
    """主函数"""
    print("""
╔════════════════════════════════════════╗
║     📝 产品实习周报自动生成器           ║
║                                        ║
║  一键生成结构化周报总结                 ║
║  优先级: 个人思考 > 方法论 > 工作任务  ║
╚════════════════════════════════════════╝
    """)

    # Step 1: 检查 API Key
    if not setup_api_key():
        return

    # Step 2: 选择 PDF
    pdf_path = select_pdf()
    if not pdf_path:
        return

    # Step 3: 输入周期
    week_info = input_week_info()

    # Step 4: 确认设置
    if not confirm_settings(pdf_path, week_info):
        print("\n❌ 已取消")
        return

    # Step 5: 运行生成器
    success = run_generator(pdf_path, week_info)

    if success:
        print("\n💡 下次使用: python quick_start.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⛔ 已取消")
    except Exception as e:
        print(f"\n❌ 程序出错: {e}")
        sys.exit(1)
