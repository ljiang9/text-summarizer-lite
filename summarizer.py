from __future__ import annotations

import json
import os
import re
import urllib.request
from collections import Counter

from stopwords import is_stopword

_SENT_END = "。！？!?…."


def split_sentences(text):
    if not text or not text.strip():
        return []

    chunks = []
    for raw_line in re.split(r"[\r\n]+", text):
        line = raw_line.strip()
        if line:
            chunks.append(line)

    sentences = []
    for chunk in chunks:
        parts = re.findall(rf"[^{_SENT_END}]+[{_SENT_END}]*", chunk)
        for p in parts:
            p = p.strip()
            if p:
                sentences.append(p)
    return sentences


_EN_WORD_RE = re.compile(r"[A-Za-z]+(?:['\-][A-Za-z]+)*")
_CJK_RUN_RE = re.compile(r"[\u4e00-\u9fff]+")


def tokenize(sentence):
    tokens = []
    for w in _EN_WORD_RE.findall(sentence):
        tokens.append(w.lower())
    for run in _CJK_RUN_RE.findall(sentence):
        if len(run) == 1:
            tokens.append(run)
        else:
            for i in range(len(run) - 1):
                tokens.append(run[i:i + 2])
    return tokens


def _score_sentence(sentence, freq):
    tokens = [t for t in tokenize(sentence) if not is_stopword(t)]
    if not tokens:
        return 0.0
    score = sum(freq.get(t, 0) for t in tokens)
    return score / (len(tokens) ** 0.5)


def summarize_extractive(text, ratio=0.3):
    if not text or not text.strip():
        return ""
    if not (0.0 < ratio <= 1.0):
        raise ValueError("ratio 必须在 (0, 1] 之间")

    sentences = split_sentences(text)
    if len(sentences) <= 1:
        return text.strip()

    counter = Counter()
    for sent in sentences:
        for t in tokenize(sentence=sent):
            if not is_stopword(t):
                counter[t] += 1
    freq = dict(counter)

    scored = [(idx, _score_sentence(s, freq)) for idx, s in enumerate(sentences)]
    n = max(1, round(len(sentences) * ratio))
    n = min(n, len(sentences))

    top = sorted(scored, key=lambda x: x[1], reverse=True)[:n]
    chosen_indices = sorted(idx for idx, _ in top)

    return "".join(sentences[i] for i in chosen_indices)


def summarize_llm(text, ratio=0.3, api_key=None, base_url=None, model=None):
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    base_url = (base_url or os.environ.get("OPENAI_BASE_URL")
                or "https://api.openai.com/v1").rstrip("/")
    model = model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    if not api_key:
        raise RuntimeError("未设置 OPENAI_API_KEY，无法使用 LLM 摘要")

    max_chars = max(1, int(len(text) * ratio))
    prompt = ("请用不超过约 " + str(max_chars) + " 字对下面文本做简洁摘要，直接输出摘要正文：\n\n" + text)
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "你是一个简洁的中文摘要助手。"},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }
    req = urllib.request.Request(
        base_url + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"].strip()


def summarize(text, ratio=0.3, use_llm=True):
    if use_llm and os.environ.get("OPENAI_API_KEY"):
        try:
            return summarize_llm(text, ratio=ratio)
        except Exception as exc:
            print("[warn] LLM 摘要失败，降级为提取式：" + str(exc))
    return summarize_extractive(text, ratio=ratio)
