import spacy
from translate import Translator
from spacy.vocab import Vocab
translator = Translator(to_lang="vi")
vocab = Vocab(strings=["hello", "world"])
tobe = ["’m", "’re", "’s", "’ve", "’ll", "’d", "’ve", "n’t",
        "'m", "'re", "'s", "'ve", "'ll", "'d", "'ve", "n't"]
symbols = ['.', ',', '?', '!', ':', ';',
           '[', ']', '{', '}', '"', "'", '’', '“', '”', '‘', '’', '…', '� ',
           "’m", "’re", "’s", "’ve", "’ll", "’d", "’ve", "n’t",
           "'m", "'re", "'s", "'ve", "'ll", "'d", "'ve", "n't"]
# Tải mô hình ngôn ngữ tiếng Anh từ spaCy
nlp = spacy.load("en_core_web_sm")


def text_to_word(sentence):
    # Phân tích câu với spaCy
    doc = nlp(sentence)

    # Tạo danh sách để lưu trữ các cụm động từ đã gộp lại
    merged_verb_phrases = []

    # Biến để lưu trữ cụm động từ tạm thời
    current_verb_phrase = []

    i = 0
    # for i in range(len(doc)):
    #     print(doc[i].text, doc[i].pos_)

    skip_iterations = 0
    # Lặp qua các token trong câu
    for i in range(len(doc)):
        if skip_iterations > 0:
            skip_iterations -= 1
            i += 1
            continue

        token = doc[i]
        # print(token.text, token.pos_)
        # Kiểm tra nếu token là động từ (VERB)
        if token.pos_ == "VERB":
            # Kiểm tra xem có một đại từ (PRON) ở vị trí sau VERB không
            if i < len(doc) - 1 and doc[i + 1].pos_ == "PRON":
                # Nếu có, thêm VERB, PRON và ADP vào cụm động từ
                if i + 2 < len(doc) and doc[i + 2].pos_ == "ADP":
                    current_verb_phrase.append(token.text)
                    current_verb_phrase.append(doc[i + 1].text)
                    current_verb_phrase.append(doc[i + 2].text)
                    if i + 3 < len(doc) and doc[i + 3].text in symbols:
                        merged_verb_phrases.append(
                            {'text': " ".join(current_verb_phrase) + doc[i + 3].text, "type": "PHRASAL VERB"})
                        current_verb_phrase = []
                        skip_iterations += 3
                    else:
                        merged_verb_phrases.append({"text":
                                                    " ".join(current_verb_phrase), "type": "PHRASAL VERB"})
                        current_verb_phrase = []
                        skip_iterations += 2
                else:
                    if i + 1 < len(doc) and doc[i + 1].text in symbols:
                        current_verb_phrase.append(token.text)
                        current_verb_phrase.append(doc[i + 1].text)
                        merged_verb_phrases.append({"text":
                                                    "".join(current_verb_phrase), "type": "PHRASAL VERB"})
                        current_verb_phrase = []
                        skip_iterations += 1
                    else:
                        merged_verb_phrases.append(
                            {"text": token.text, "type": "VERB"})
            # Kiểm tra xem có một trạng từ (ADV) ở vị trí sau VERB không
            elif i < len(doc) - 1 and doc[i + 1].pos_ == "ADV":
                current_verb_phrase.append(token.text)
                # Nếu có, thêm VERB và ADV vào cụm động từ
                if i + 2 < len(doc) and doc[i + 2].pos_ == "ADP":
                    if i + 3 < len(doc) and doc[i + 3].text in symbols:
                        current_verb_phrase.append(doc[i + 1].text)
                        merged_verb_phrases.append({"text":
                                                    " ".join(current_verb_phrase) + doc[i + 3].text, "type": "PHRASAL VERB"})
                        current_verb_phrase = []
                        skip_iterations += 3
                    else:
                        current_verb_phrase.append(doc[i + 1].text)
                        merged_verb_phrases.append({"text":
                                                    " ".join(current_verb_phrase), "type": "PHRASAL VERB"})
                        current_verb_phrase = []
                        skip_iterations += 1
                else:
                    if i + 1 < len(doc) and doc[i + 1].text in symbols:
                        merged_verb_phrases.append({"text":
                                                    " ".join(current_verb_phrase) + doc[i + 1].text, "type": "PHRASAL VERB"})
                        current_verb_phrase = []
                        skip_iterations += 1
                    else:
                        merged_verb_phrases.append({'text':
                                                    " ".join(current_verb_phrase), "type": "VERB"})
                        current_verb_phrase = []
            # Nếu không có PRON sau VERB, kiểm tra xem có một giới từ (ADP) ở vị trí sau VERB không
            elif i < len(doc) - 1 and doc[i + 1].pos_ == "ADP":
                if i + 2 < len(doc) and doc[i + 2].text in symbols:
                    current_verb_phrase.append(token.text)
                    current_verb_phrase.append(doc[i + 1].text)
                    merged_verb_phrases.append({"text":
                                                " ".join(current_verb_phrase) + doc[i + 2].text, "type": "PHRASAL VERB"})
                    current_verb_phrase = []
                    skip_iterations += 1
                else:
                    current_verb_phrase.append(token.text)
                    current_verb_phrase.append(doc[i + 1].text)
                    merged_verb_phrases.append(
                        {"text": " ".join(current_verb_phrase), "type": "PHRASAL VERB"})
                    current_verb_phrase = []
                    skip_iterations += 1
            elif i < len(doc) - 1 and doc[i + 1].text == '-':
                current_verb_phrase.append(token.text)
                current_verb_phrase.append(doc[i + 1].text)
                if i + 2 < len(doc):
                    current_verb_phrase.append(doc[i + 2].text)
                if i + 3 < len(doc) and doc[i + 3].text in symbols:
                    merged_verb_phrases.append(
                        {"text": "".join(current_verb_phrase) + doc[i + 3].text, "type": "PHRASAL VERB"})
                    current_verb_phrase = []
                    skip_iterations += 3
                else:
                    merged_verb_phrases.append(
                        {"text": "".join(current_verb_phrase), "type": "PHRASAL VERB"})
                    current_verb_phrase = []
                    skip_iterations += 2
            elif i < len(doc) - 1 and doc[i + 1].text in tobe:
                if i + 2 < len(doc) and doc[i + 2].text in symbols:
                    current_verb_phrase.append(token.text)
                    current_verb_phrase.append(doc[i + 1].text)
                    merged_verb_phrases.append(
                        {"text": "".join(current_verb_phrase) + doc[i + 2].text, "type": "PHRASAL VERB"})
                    current_verb_phrase = []
                    skip_iterations += 2
                else:
                    current_verb_phrase.append(token.text)
                    current_verb_phrase.append(doc[i + 1].text)
                    merged_verb_phrases.append(
                        {"text": "".join(current_verb_phrase), "type": "PHRASAL VERB"})
                    current_verb_phrase = []
                    skip_iterations += 1
            else:
                # Nếu không có PRON hoặc ADP sau VERB, thêm VERB vào cụm động từ
                if i + 1 < len(doc) and doc[i + 1].text in symbols:
                    current_verb_phrase.append(token.text)
                    current_verb_phrase.append(doc[i + 1].text)
                    merged_verb_phrases.append(
                        {"text": "".join(current_verb_phrase), "type": "VERB"})
                    current_verb_phrase = []
                    skip_iterations += 1
                else:
                    merged_verb_phrases.append(
                        {"text": token.text, "type": "VERB"})
        elif token.pos_ == "NOUN":
            if i < len(doc) - 1 and doc[i + 1].text == '-':
                current_verb_phrase.append(token.text)
                current_verb_phrase.append(doc[i + 1].text)
                if i + 2 < len(doc):
                    current_verb_phrase.append(doc[i + 2].text)
                    merged_verb_phrases.append(
                        {"text": "".join(current_verb_phrase), "type": "PHRASAL NOUN"})
                    if i + 3 < len(doc) and doc[i + 3].text in symbols:
                        merged_verb_phrases.append({"text":
                                                    "".join(current_verb_phrase) + doc[i + 3].text, "type": "PHRASAL NOUN"})
                        current_verb_phrase = []
                        skip_iterations += 3
                    else:
                        current_verb_phrase = []
                        skip_iterations += 2
            elif i < len(doc) - 1 and doc[i + 1].pos_ == "NOUN":
                # Nếu có, thêm NOUN và NOUN vào cụm động từ
                current_verb_phrase.append(token.text)
                current_verb_phrase.append(doc[i + 1].text)
                if i + 2 < len(doc) and doc[i + 2].pos_ == "NOUN":
                    if i + 3 < len(doc) and doc[i + 3].text in symbols:
                        merged_verb_phrases.append({"text":
                                                    " ".join(current_verb_phrase) + doc[i + 3].text, "type": "PHRASAL NOUN"})
                        current_verb_phrase = []
                        skip_iterations += 3
                    else:
                        current_verb_phrase.append(doc[i + 2].text)
                        merged_verb_phrases.append({"text":
                                                    " ".join(current_verb_phrase), "type": "PHRASAL NOUN"})
                        current_verb_phrase = []
                        skip_iterations += 2
                else:
                    if i + 2 < len(doc) and doc[i + 2].text in symbols:
                        merged_verb_phrases.append({"text":
                                                    " ".join(current_verb_phrase) + doc[i + 2].text, "type": "PHRASAL NOUN"})
                        current_verb_phrase = []
                        skip_iterations += 2
                    else:
                        merged_verb_phrases.append({"text":
                                                    " ".join(current_verb_phrase), "type": "PHRASAL NOUN"})
                        current_verb_phrase = []
                        skip_iterations += 1
            else:
                if i + 1 < len(doc) and doc[i + 1].text in symbols:
                    current_verb_phrase.append(token.text)
                    current_verb_phrase.append(doc[i + 1].text)
                    merged_verb_phrases.append(
                        {"text": "".join(current_verb_phrase), "type": "NOUN"})
                    current_verb_phrase = []
                    skip_iterations += 1
                else:
                    merged_verb_phrases.append(
                        {"text": token.text, "type": "NOUN"})
        elif token.pos_ == "DET" and token.text in ["the", "The"]:
            if i < len(doc) - 1 and doc[i + 1].pos_ in ["NOUN", "NUM"]:
                if i + 2 < len(doc) and doc[i + 2].pos_ == "NOUN":
                    if i + 3 < len(doc) and doc[i + 3].text in symbols:
                        current_verb_phrase.append(token.text)
                        current_verb_phrase.append(doc[i + 1].text)
                        current_verb_phrase.append(doc[i + 2].text)
                        merged_verb_phrases.append({"text":
                                                    " ".join(current_verb_phrase) + doc[i + 3].text, "type": "PHRASAL NOUN"})
                        current_verb_phrase = []
                        skip_iterations += 3
                    else:
                        current_verb_phrase.append(token.text)
                        current_verb_phrase.append(doc[i + 1].text)
                        current_verb_phrase.append(doc[i + 2].text)
                        merged_verb_phrases.append({"text":
                                                    " ".join(current_verb_phrase), "type": "PHRASAL NOUN"})
                        current_verb_phrase = []
                        skip_iterations += 2
                else:
                    if i + 2 < len(doc) and doc[i + 2].text in symbols:
                        current_verb_phrase.append(token.text)
                        current_verb_phrase.append(doc[i + 1].text)
                        merged_verb_phrases.append({"text":
                                                    " ".join(current_verb_phrase) + doc[i + 2].text, "type": "PHRASAL NOUN"})
                        current_verb_phrase = []
                        skip_iterations += 2
                    else:
                        current_verb_phrase.append(token.text)
                        current_verb_phrase.append(doc[i + 1].text)
                        merged_verb_phrases.append({"text":
                                                    " ".join(current_verb_phrase), "type": "PHRASAL NOUN"})
                        current_verb_phrase = []
                        skip_iterations += 1
            else:
                if i + 1 < len(doc) and doc[i + 1].text in symbols:
                    current_verb_phrase.append(token.text)
                    current_verb_phrase.append(doc[i + 1].text)
                    merged_verb_phrases.append(
                        {"text": "".join(current_verb_phrase), "type": token.pos_})
                    current_verb_phrase = []
                    skip_iterations += 1
                else:
                    merged_verb_phrases.append(
                        {"text": token.text, "type": token.pos_})
        elif token.pos_ == "AUX":
            if i < len(doc) - 1 and doc[i + 1].pos_ == "AUX":
                if i + 2 < len(doc) and doc[i + 2].text in symbols:
                    current_verb_phrase.append(token.text)
                    current_verb_phrase.append(doc[i + 1].text)
                    merged_verb_phrases.append({"text":
                                                " ".join(current_verb_phrase) + doc[i + 2].text, "type": "AUX"})
                    current_verb_phrase = []
                    skip_iterations += 2
                else:
                    current_verb_phrase.append(token.text)
                    current_verb_phrase.append(doc[i + 1].text)
                    merged_verb_phrases.append(
                        {"text": " ".join(current_verb_phrase), "type": "AUX"})
                    current_verb_phrase = []
                    skip_iterations += 1
            else:
                if i + 1 < len(doc) and doc[i + 1].text in symbols:
                    current_verb_phrase.append(token.text)
                    current_verb_phrase.append(doc[i + 1].text)
                    merged_verb_phrases.append(
                        {"text": "".join(current_verb_phrase), "type": token.pos_})
                    current_verb_phrase = []
                    skip_iterations += 1
                else:
                    merged_verb_phrases.append(
                        {"text": token.text, "type": token.pos_})
        elif token.pos_ == "ADJ":
            if i < len(doc) - 1 and doc[i + 1].pos_ == "NOUN":
                if i + 2 < len(doc) and doc[i + 2].text in symbols:
                    current_verb_phrase.append(token.text)
                    current_verb_phrase.append(doc[i + 1].text)
                    merged_verb_phrases.append({"text":
                                                " ".join(current_verb_phrase) + doc[i + 2].text, "type": "PHRASAL NOUN"})
                    current_verb_phrase = []
                    skip_iterations += 2
                else:
                    current_verb_phrase.append(token.text)
                    current_verb_phrase.append(doc[i + 1].text)
                    merged_verb_phrases.append(
                        {"text": " ".join(current_verb_phrase), "type": "PHRASAL NOUN"})
                    current_verb_phrase = []
                    skip_iterations += 1
            elif i < len(doc) - 1 and doc[i + 1].text == '-':
                current_verb_phrase.append(token.text)
                current_verb_phrase.append(doc[i + 1].text)
                if i + 2 < len(doc):
                    current_verb_phrase.append(doc[i + 2].text)
                    if doc[i + 3].text == '-':
                        current_verb_phrase.append(doc[i + 3].text)
                        if i + 4 < len(doc):
                            current_verb_phrase.append(doc[i + 4].text)
                            merged_verb_phrases.append({"text":
                                                        "".join(current_verb_phrase), "type": "PHRASAL NOUN"})
                            if doc[i + 5].text in symbols:
                                merged_verb_phrases.append({"text":
                                                            "".join(current_verb_phrase) + doc[i + 5].text, "type": "PHRASAL NOUN"})
                                current_verb_phrase = []
                                skip_iterations += 5
                            else:
                                current_verb_phrase = []
                                skip_iterations += 4
                        else:
                            current_verb_phrase = []
                            skip_iterations += 3
                    elif doc[i + 3].text in symbols:
                        merged_verb_phrases.append({"text":
                                                    "".join(current_verb_phrase) + doc[i + 3].text, "type": "PHRASAL NOUN"})
                        current_verb_phrase = []
                        skip_iterations += 3
                    else:
                        merged_verb_phrases.append({"text":
                                                    "".join(current_verb_phrase), "type": "PHRASAL NOUN"})
                        current_verb_phrase = []
                        skip_iterations += 2
            else:
                if i + 1 < len(doc) and doc[i + 1].text in symbols:
                    current_verb_phrase.append(token.text)
                    current_verb_phrase.append(doc[i + 1].text)
                    merged_verb_phrases.append(
                        {"text": "".join(current_verb_phrase), "type": token.pos_})
                    current_verb_phrase = []
                    skip_iterations += 1
                else:
                    merged_verb_phrases.append(
                        {"text": token.text, "type": token.pos_})
        elif token.pos_ == "CCONJ":
            if i < len(doc) - 1 and doc[i + 1].pos_ == "VERB":
                if (i + 2 < len(doc) and doc[i - 1].pos_ == "NOUN"):
                    if i + 3 < len(doc) and doc[i + 1].text in symbols:
                        current_verb_phrase.append(token.text)
                        merged_verb_phrases.append({"text":
                                                    " ".join(current_verb_phrase), "type": token.pos_})
                        current_verb_phrase = []
                        current_verb_phrase.append(doc[i + 1].text)
                        current_verb_phrase.append(doc[i + 2].text)
                        merged_verb_phrases.append({"text":
                                                    " ".join(current_verb_phrase) + doc[i + 3].text, "type": "PHRASAL NOUN"})
                        current_verb_phrase = []
                        skip_iterations += 3
                    else:
                        current_verb_phrase.append(token.text)
                        merged_verb_phrases.append({"text":
                                                    " ".join(current_verb_phrase), "type": token.pos_})
                        current_verb_phrase = []
                        current_verb_phrase.append(doc[i + 1].text)
                        current_verb_phrase.append(doc[i + 2].text)
                        merged_verb_phrases.append({"text":
                                                    " ".join(current_verb_phrase), "type": "PHRASAL NOUN"})
                        current_verb_phrase = []
                        skip_iterations += 2
                else:
                    merged_verb_phrases.append(
                        {"text": token.text, "type": token.pos_})
            else:
                merged_verb_phrases.append(
                    {"text": token.text, "type": token.pos_})
        elif token.pos_ == "ADV":
            if i < len(doc) - 1 and doc[i + 1].pos_ == "ADJ":
                if i + 2 < len(doc) and doc[i + 2].text in symbols:
                    current_verb_phrase.append(token.text)
                    current_verb_phrase.append(doc[i + 1].text)
                    merged_verb_phrases.append({"text":
                                                " ".join(current_verb_phrase) + doc[i + 2].text, "type": "PHRASAL ADJ"})
                    current_verb_phrase = []
                    skip_iterations += 2
                else:
                    current_verb_phrase.append(token.text)
                    current_verb_phrase.append(doc[i + 1].text)
                    merged_verb_phrases.append(
                        {"text": " ".join(current_verb_phrase), "type": "PHRASAL ADJ"})
                    current_verb_phrase = []
                    skip_iterations += 1
            else:
                if i + 1 < len(doc) and doc[i + 1].text in symbols:
                    current_verb_phrase.append(token.text)
                    merged_verb_phrases.append({"text":
                                                " ".join(current_verb_phrase) + doc[i + 1].text, "type": token.pos_})
                    current_verb_phrase = []
                    skip_iterations += 1
                else:
                    merged_verb_phrases.append(
                        {"text": token.text, "type": token.pos_})
        else:
            # Nếu token không phải là VERB, thêm token vào cụm động từ
            if i < len(doc) - 1 and doc[i + 1].text == '-':
                current_verb_phrase.append(token.text)
                current_verb_phrase.append(doc[i + 1].text)
                if i + 3 < len(doc):
                    current_verb_phrase.append(doc[i + 2].text)
                    if doc[i + 3].text == '-':
                        current_verb_phrase.append(doc[i + 3].text)
                        if i + 4 < len(doc):
                            current_verb_phrase.append(doc[i + 4].text)
                            merged_verb_phrases.append({"text":
                                                        "".join(current_verb_phrase), "type": token.pos_})
                            if i + 5 < len(doc) and doc[i + 5].text in symbols:
                                merged_verb_phrases.append({"text":
                                                            "".join(current_verb_phrase) + doc[i + 5].text, "type": token.pos_})
                                current_verb_phrase = []
                                skip_iterations += 5
                            else:
                                current_verb_phrase = []
                                skip_iterations += 4
                        else:
                            current_verb_phrase = []
                            skip_iterations += 3
                    elif doc[i + 3].text in symbols:
                        merged_verb_phrases.append({"text":
                                                    "".join(current_verb_phrase), "type": token.pos_})
                        merged_verb_phrases.append({"text":
                                                    "".join(current_verb_phrase) + doc[i + 3].text, "type": token.pos_})
                        current_verb_phrase = []
                        skip_iterations += 3
                    else:
                        merged_verb_phrases.append({"text":
                                                    "".join(current_verb_phrase), "type": token.pos_})
                        current_verb_phrase = []
                        skip_iterations += 2
            elif i < len(doc) - 1 and doc[i + 1].text in tobe:
                if i + 2 < len(doc) and doc[i + 2].text in symbols:
                    current_verb_phrase.append(token.text)
                    current_verb_phrase.append(doc[i + 1].text)
                    merged_verb_phrases.append({"text":
                                                "".join(current_verb_phrase) + doc[i + 2].text, "type": token.pos_})
                    current_verb_phrase = []
                    skip_iterations += 2
                else:
                    current_verb_phrase.append(token.text)
                    current_verb_phrase.append(doc[i + 1].text)
                    merged_verb_phrases.append(
                        {"text": "".join(current_verb_phrase), "type": token.pos_})
                    current_verb_phrase = []
                    skip_iterations += 1
            elif i < len(doc) - 1 and doc[i + 1].text in symbols:
                merged_verb_phrases.append(
                    {"text": token.text + doc[i + 1].text, "type": token.pos_})
                skip_iterations += 1
            else:
                merged_verb_phrases.append(
                    {"text": token.text, "type": token.pos_})
    return merged_verb_phrases