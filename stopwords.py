CHINESE_STOPWORDS = frozenset([
    "的", "了", "和", "是", "在", "我", "有", "就", "也", "都",
    "这", "那", "你", "他", "她", "它", "我们", "你们", "他们",
    "什么", "怎么", "为什么", "哪里", "吗", "呢", "吧", "啊", "呀",
    "嘛", "哦", "嗯", "把", "被", "让", "给", "向", "从", "到",
    "对", "为", "以", "及", "等", "之", "与", "或", "而", "又",
    "但", "但是", "因为", "所以", "如果", "虽然", "然而", "于是",
    "一个", "没有", "不", "很", "太", "最", "更", "还", "又",
    "上", "下", "里", "中", "外", "前", "后", "之间", "时候",
    "这是", "那是", "就是", "还是", "只是", "可以", "可能", "应该",
    "这个", "那个", "这些", "那些", "这样", "那样", "这里", "那里",
])

ENGLISH_STOPWORDS = frozenset([
    "the", "a", "an", "and", "or", "but", "if", "then", "else",
    "is", "are", "was", "were", "be", "been", "being",
    "of", "in", "on", "at", "to", "for", "with", "by", "from",
    "as", "into", "onto", "upon", "about", "over", "under",
    "i", "you", "he", "she", "it", "we", "they", "me", "him",
    "her", "us", "them", "my", "your", "his", "its", "our", "their",
    "this", "that", "these", "those", "there", "here",
    "not", "no", "nor", "so", "such", "very", "too", "just",
    "can", "will", "would", "should", "could", "may", "might",
    "do", "does", "did", "done", "have", "has", "had", "having",
    "what", "which", "who", "whom", "when", "where", "why", "how",
    "s", "t", "re", "ve", "ll", "d", "m",
])


def is_stopword(token):
    if not token:
        return True
    if token in ENGLISH_STOPWORDS:
        return True
    if token in CHINESE_STOPWORDS:
        return True
    if len(token) == 2 and all(ch in CHINESE_STOPWORDS for ch in token):
        return True
    return False
