import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from stopwords import is_stopword
from summarizer import (
    split_sentences,
    summarize_extractive,
    tokenize,
)


class TestSplitSentences(unittest.TestCase):
    def test_chinese_basic(self):
        text = "今天天气很好。我们去公园散步吧！你觉得怎么样？"
        sents = split_sentences(text)
        self.assertEqual(len(sents), 3)
        self.assertTrue(sents[0].endswith("。"))
        self.assertTrue(sents[1].endswith("！"))

    def test_english_basic(self):
        text = "Hello world. This is a test! Really?"
        sents = split_sentences(text)
        self.assertEqual(len(sents), 3)

    def test_mixed(self):
        text = "这是第一句。This is sentence two。第三句结束了。"
        sents = split_sentences(text)
        self.assertGreaterEqual(len(sents), 3)

    def test_empty(self):
        self.assertEqual(split_sentences(""), [])
        self.assertEqual(split_sentences("   "), [])

    def test_newline_split(self):
        text = "第一段第一句。第二段第一句。"
        sents = split_sentences(text)
        self.assertEqual(len(sents), 2)


class TestTokenize(unittest.TestCase):
    def test_english_lowercase(self):
        toks = tokenize("Hello World")
        self.assertIn("hello", toks)
        self.assertIn("world", toks)

    def test_chinese_bigram(self):
        toks = tokenize("人工智能")
        self.assertEqual(len(toks), 3)
        self.assertIn("人工", toks)
        self.assertIn("智能", toks)

    def test_mixed(self):
        toks = tokenize("AI 人工智能")
        self.assertIn("ai", toks)
        self.assertIn("人工", toks)


class TestStopwords(unittest.TestCase):
    def test_english_stopword(self):
        self.assertTrue(is_stopword("the"))
        self.assertTrue(is_stopword("is"))

    def test_chinese_stopword(self):
        self.assertTrue(is_stopword("的"))
        self.assertTrue(is_stopword("了"))

    def test_content_word(self):
        self.assertFalse(is_stopword("人工智能"))
        self.assertFalse(is_stopword("machine"))


class TestExtractiveSummary(unittest.TestCase):
    def setUp(self):
        self.text = (
            "人工智能正在快速发展。人工智能技术改变了很多行业。"
            "今天天气很好。我们去公园散步。"
            "人工智能在医疗领域也有重要应用。机器学习是人工智能的核心。"
        )

    def test_summary_not_empty(self):
        out = summarize_extractive(self.text, ratio=0.5)
        self.assertTrue(out.strip())

    def test_summary_length_ratio(self):
        sents = split_sentences(self.text)
        out = summarize_extractive(self.text, ratio=0.5)
        out_sents = split_sentences(out)
        self.assertEqual(len(out_sents), max(1, round(len(sents) * 0.5)))

    def test_summary_preserves_order(self):
        out = summarize_extractive(self.text, ratio=0.5)
        out_sents = split_sentences(out)
        orig = split_sentences(self.text)
        positions = [orig.index(s) for s in out_sents]
        self.assertEqual(positions, sorted(positions))

    def test_keyword_sentence_chosen(self):
        out = summarize_extractive(self.text, ratio=0.6)
        self.assertIn("人工智能", out)

    def test_single_sentence_returns_as_is(self):
        one = "只有一句话的文本。"
        self.assertEqual(summarize_extractive(one, ratio=0.5), one)

    def test_empty_returns_empty(self):
        self.assertEqual(summarize_extractive("", ratio=0.3), "")

    def test_invalid_ratio(self):
        with self.assertRaises(ValueError):
            summarize_extractive(self.text, ratio=0.0)
        with self.assertRaises(ValueError):
            summarize_extractive(self.text, ratio=1.5)


if __name__ == "__main__":
    unittest.main()
