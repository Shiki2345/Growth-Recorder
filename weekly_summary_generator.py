#!/usr/bin/env python3
"""
Automated Weekly Summary Generator for Product Internship

This script reads PDF files containing weekly work logs, generates structured
summaries using Claude AI, and updates the documentation system.

Priority hierarchy: Personal Thinking > Methodology > Work Tasks
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
import anthropic


def read_pdf_content(pdf_path: str) -> str:
    """
    Read PDF file content.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Extracted text content from PDF
    """
    try:
        import PyPDF2
    except ImportError:
        print("PyPDF2 not installed. Installing...")
        os.system("pip install PyPDF2")
        import PyPDF2

    pdf_text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                pdf_text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""

    return pdf_text


def generate_summary(client: anthropic.Anthropic, pdf_content: str, week_info: str) -> dict:
    """
    Generate a structured summary using Claude API.

    Args:
        client: Anthropic client instance
        pdf_content: Content extracted from PDF
        week_info: Information about the week (e.g., "Week 4" or date range)

    Returns:
        Dictionary containing the structured summary
    """

    system_prompt = """你是一个产品实习经验总结专家。你的任务是将工作文档转化为结构化的周报总结。

总结优先级（重要程度）：
1. 个人思考 - 反思、洞察、学到的东西、思维转变（最优先）
2. 方法论 - 可复用的框架、工具、最佳实践
3. 工作任务 - 具体完成的工作、进度、产出物

请按以下JSON格式输出总结（中文）：
{
  "personal_thinking": {
    "reflections": ["反思点1", "反思点2"],
    "insights": ["洞察1", "洞察2"],
    "learnings": ["学到的方法或框架1", "学到的方法或框架2"],
    "mindset_changes": "思维模式的改变描述"
  },
  "methodology": {
    "frameworks": ["框架1", "框架2"],
    "tools_and_tips": ["工具或技巧1"],
    "best_practices": ["最佳实践1"]
  },
  "work_tasks": {
    "main_tasks": [
      {
        "task": "任务名称",
        "completion_rate": "完成度",
        "output": "产出物"
      }
    ],
    "key_achievements": ["成就1", "成就2"]
  },
  "problem_review": {
    "issues": [
      {
        "problem": "问题描述",
        "root_cause": "根本原因",
        "solution": "解决方案",
        "prevention": "预防措施"
      }
    ]
  }
}"""

    user_message = f"""请为以下工作文档生成周报总结。

周期: {week_info}

文档内容:
{pdf_content[:8000]}  # 限制token数量

请生成JSON格式的完整总结。"""

    try:
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            system=system_prompt
        )

        # Extract JSON from response
        response_text = message.content[0].text

        # Try to parse JSON
        try:
            # Find JSON in response (Claude might add extra text)
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                summary = json.loads(json_str)
            else:
                raise ValueError("No JSON found in response")
        except json.JSONDecodeError as e:
            print(f"Error parsing Claude's response as JSON: {e}")
            print(f"Raw response: {response_text[:500]}")
            return {"error": str(e), "raw_response": response_text}

        return summary

    except Exception as e:
        print(f"Error calling Claude API: {e}")
        return {"error": str(e)}


def format_summary_to_markdown(summary: dict, week_info: str) -> str:
    """
    Convert structured summary to Markdown format.

    Args:
        summary: Structured summary dictionary
        week_info: Week information

    Returns:
        Markdown formatted summary
    """

    if "error" in summary:
        return f"# 周报生成失败\n\n错误: {summary['error']}"

    markdown = f"# {week_info} 产品实习总结 - {datetime.now().strftime('%Y年%m月%d日')}\n\n"

    # Personal Thinking
    markdown += "## 🧠 个人思考与洞察\n\n"
    if "personal_thinking" in summary:
        pt = summary["personal_thinking"]

        if pt.get("reflections"):
            markdown += "### 反思\n"
            for reflection in pt["reflections"]:
                markdown += f"- {reflection}\n"
            markdown += "\n"

        if pt.get("insights"):
            markdown += "### 洞察\n"
            for insight in pt["insights"]:
                markdown += f"- {insight}\n"
            markdown += "\n"

        if pt.get("learnings"):
            markdown += "### 学到的内容\n"
            for learning in pt["learnings"]:
                markdown += f"- {learning}\n"
            markdown += "\n"

        if pt.get("mindset_changes"):
            markdown += f"### 思维转变\n{pt['mindset_changes']}\n\n"

    # Methodology
    markdown += "## 🛠️ 方法论提炼\n\n"
    if "methodology" in summary:
        meth = summary["methodology"]

        if meth.get("frameworks"):
            markdown += "### 框架\n"
            for framework in meth["frameworks"]:
                markdown += f"- {framework}\n"
            markdown += "\n"

        if meth.get("tools_and_tips"):
            markdown += "### 工具与技巧\n"
            for tool in meth["tools_and_tips"]:
                markdown += f"- {tool}\n"
            markdown += "\n"

        if meth.get("best_practices"):
            markdown += "### 最佳实践\n"
            for practice in meth["best_practices"]:
                markdown += f"- {practice}\n"
            markdown += "\n"

    # Work Tasks
    markdown += "## 📊 本周工作要点\n\n"
    if "work_tasks" in summary:
        work = summary["work_tasks"]

        if work.get("main_tasks"):
            markdown += "### 主要任务\n\n"
            markdown += "| 任务 | 完成度 | 产出 |\n"
            markdown += "|-----|------|------|\n"
            for task in work["main_tasks"]:
                markdown += f"| {task.get('task', '')} | {task.get('completion_rate', '')} | {task.get('output', '')} |\n"
            markdown += "\n"

        if work.get("key_achievements"):
            markdown += "### 关键成就\n"
            for achievement in work["key_achievements"]:
                markdown += f"- ✅ {achievement}\n"
            markdown += "\n"

    # Problem Review
    markdown += "## ⚠️ 问题复盘\n\n"
    if "problem_review" in summary and summary["problem_review"].get("issues"):
        markdown += "| 问题 | 根本原因 | 解决方案 | 预防措施 |\n"
        markdown += "|-----|---------|---------|----------|\n"
        for issue in summary["problem_review"]["issues"]:
            markdown += f"| {issue.get('problem', '')} | {issue.get('root_cause', '')} | {issue.get('solution', '')} | {issue.get('prevention', '')} |\n"
        markdown += "\n"

    return markdown


def update_summary_files(summary_content: str, week_info: str, base_path: str = ".") -> bool:
    """
    Update the weekly summary files in the documentation system.

    Args:
        summary_content: Markdown formatted summary
        week_info: Week information (used for filename)
        base_path: Base path for the documentation

    Returns:
        True if successful, False otherwise
    """

    base_path = Path(base_path)
    summary_dir = base_path / "每周总结"

    # Ensure directory exists
    summary_dir.mkdir(parents=True, exist_ok=True)

    # Create filename (e.g., "第二周总结.md" or "2026-04-18_总结.md")
    if "周" in week_info:
        filename = f"{week_info}总结.md"
    else:
        filename = f"{week_info}_总结.md"

    summary_file = summary_dir / filename

    try:
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        print(f"✅ 周报已保存到: {summary_file}")

        # Update the main index file
        index_file = base_path / "每周日志索引.md"
        update_index(index_file, week_info, filename)

        return True
    except Exception as e:
        print(f"❌ 保存周报失败: {e}")
        return False


def update_index(index_file: Path, week_info: str, summary_filename: str) -> None:
    """
    Update the main index file with the new summary entry.

    Args:
        index_file: Path to the index file
        week_info: Week information
        summary_filename: Name of the summary file
    """

    try:
        if not index_file.exists():
            print(f"⚠️ 索引文件不存在: {index_file}")
            return

        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add new entry to the summary list (simple approach)
        # This is a placeholder - you might want more sophisticated index management
        new_entry = f"- **[{week_info} 总结](./每周总结/{summary_filename})** - {datetime.now().strftime('%Y-%m-%d')} 更新\n"

        # Find the position to insert (after the summary list header)
        if "## 📅 总结列表" in content:
            insert_pos = content.find("## 📅 总结列表") + len("## 📅 总结列表")
            # Find the next line
            next_line_pos = content.find("\n", insert_pos)
            if next_line_pos != -1:
                content = content[:next_line_pos + 1] + new_entry + content[next_line_pos + 1:]

        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ 索引已更新: {index_file}")

    except Exception as e:
        print(f"⚠️ 更新索引时出错: {e}")


def log_reading(pdf_path: str, week_info: str, base_path: str = ".") -> None:
    """
    Log the reading of a document in the readings log.

    Args:
        pdf_path: Path to the PDF file
        week_info: Week information
        base_path: Base path for documentation
    """

    log_file = Path(base_path) / "已读文档日志.md"

    if not log_file.exists():
        print(f"⚠️ 已读日志文件不存在: {log_file}")
        return

    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n| {len(pdf_path)} | {Path(pdf_path).name} | {datetime.now().strftime('%Y.%m.%d')} | PDF | {week_info} | ✅ 已处理 |\n")

        print(f"✅ 文档日志已更新")
    except Exception as e:
        print(f"⚠️ 更新文档日志时出错: {e}")


def main():
    """Main function to orchestrate the summary generation process."""

    # Configuration
    if len(sys.argv) < 2:
        print("用法: python weekly_summary_generator.py <pdf_path> [week_info]")
        print("例如: python weekly_summary_generator.py ./工作总结.pdf '第4周'")
        sys.exit(1)

    pdf_path = sys.argv[1]
    week_info = sys.argv[2] if len(sys.argv) > 2 else f"第{datetime.now().isocalendar()[1]}周"

    # Validate PDF exists
    if not os.path.exists(pdf_path):
        print(f"❌ 文件不存在: {pdf_path}")
        sys.exit(1)

    print(f"📖 开始处理文档: {pdf_path}")
    print(f"📅 周期: {week_info}\n")

    # Read PDF
    print("正在提取PDF内容...")
    pdf_content = read_pdf_content(pdf_path)

    if not pdf_content:
        print("❌ 无法提取PDF内容")
        sys.exit(1)

    print(f"✅ 成功提取 {len(pdf_content)} 字符\n")

    # Initialize Claude client
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ 未设置 ANTHROPIC_API_KEY 环境变量")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # Generate summary
    print("🤖 使用Claude生成总结...")
    summary = generate_summary(client, pdf_content, week_info)

    if "error" in summary:
        print(f"❌ 生成总结失败: {summary['error']}")
        sys.exit(1)

    print("✅ 总结生成成功\n")

    # Format to Markdown
    print("📝 格式化为Markdown...")
    markdown_summary = format_summary_to_markdown(summary, week_info)

    # Save summary files
    print("💾 保存文件...")
    base_path = Path(pdf_path).parent
    update_summary_files(markdown_summary, week_info, base_path)
    log_reading(pdf_path, week_info, base_path)

    print("\n✨ 周报生成完成!")
    print("\n" + "="*50)
    print(markdown_summary)
    print("="*50)


if __name__ == "__main__":
    main()
