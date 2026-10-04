# 提取式中英文摘要小工具（text-summarizer-lite）

一个 **零第三方依赖** 的 Python 命令行摘要工具。默认走规则法提取式摘要；
当环境变量里配置了 OpenAI 兼容 API Key 时，可一键切换到 LLM 生成式摘要。

## 功能简介

- 中英文混合分句：自动识别中文 `。！？…` 与英文 `. ! ?` 句末标点；
- 分词打分：英文按单词、中文按字 bigram，去内置中英文停用词后统计词频；
- 句子打分：句内关键词词频之和按句长归一化；
- 按 `--ratio` 比例选出 top-n 句，**严格按原文顺序输出**；
- 可选 LLM 摘要：通过标准库 `urllib` 调用 OpenAI 兼容 `chat/completions`。

## 快速开始

环境要求：Python 3.10+（开发验证于 3.12）。无需 `pip install` 任何东西。

```bash
git clone https://github.com/ljiang9/text-summarizer-lite.git
cd text-summarizer-lite
```

## 使用示例

直接传文本：

```bash
python3 cli.py --text "人工智能正在快速发展。人工智能技术改变了很多行业。今天天气很好。我们去公园散步。人工智能在医疗领域也有重要应用。"
```

从文件读取并调整摘要比例：

```bash
python3 cli.py --file sample.txt --ratio 0.2
```

启用 LLM 摘要（需先配置环境变量）：

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="https://api.openai.com/v1"   # 可选，兼容任何 OpenAI 网关
export OPENAI_MODEL="gpt-4o-mini"                    # 可选
python3 cli.py --file sample.txt --ratio 0.3 --llm
```

## 无 API Key 如何运行

**完全不需要 Key**。只要不 `--llm`，工具自动使用内置规则法做提取式摘要，
开箱即用：

```bash
unset OPENAI_API_KEY
python3 cli.py --file sample.txt --ratio 0.3
```

LLM 调用失败（网络错误/鉴权失败）时也会自动降级回规则法，并打印 `[warn]`。

## 目录结构

```
text-summarizer-lite/
├── cli.py            # 命令行入口（argparse）
├── summarizer.py     # 分句 / 分词 / 打分 / 选句 / 可选 LLM
├── stopwords.py      # 内置中英文停用词表
├── sample.txt        # 示例输入
├── tests/
│   └── test_summarizer.py
├── README.md
├── LICENSE           # MIT
└── .gitignore
```

## 运行测试

```bash
python3 -m unittest discover -s tests
```

## 许可证

MIT License，见 [LICENSE](./LICENSE)。
