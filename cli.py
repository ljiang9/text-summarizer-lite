from __future__ import annotations

import argparse
import sys

from summarizer import summarize, summarize_extractive


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="text-summarizer-lite",
        description="零依赖的中英文提取式摘要工具（可选 LLM 增强）",
    )
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="直接传入待摘要文本")
    src.add_argument("--file", help="从文本文件读取待摘要内容")
    p.add_argument("--ratio", type=float, default=0.3,
                   help="摘要句数占原句数的比例，默认 0.3")
    p.add_argument("--llm", action="store_true",
                   help="尝试调用 LLM 摘要（需环境变量 OPENAI_API_KEY）")
    p.add_argument("--no-llm", action="store_true",
                   help="强制只使用规则提取式摘要")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = args.text or ""

    use_llm = args.llm and not args.no_llm
    result = summarize(text, ratio=args.ratio, use_llm=use_llm)

    print("=== 摘要结果 ===")
    print(result if result else "(空)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
