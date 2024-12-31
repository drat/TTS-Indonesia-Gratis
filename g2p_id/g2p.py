import json
import os
import re

import numpy as np
import onnxruntime
from nltk.tokenize import TweetTokenizer
from sacremoses import MosesDetokenizer

from .syllable_splitter import SyllableSplitter

ABJAD_MAPPING = {
    "a": "a",
    "b": "bé",
    "c": "cé",
    "d": "dé",
    "e": "é",
    "f": "èf",
    "g": "gé",
    "h": "ha",
    "i": "i",
    "j": "jé",
    "k": "ka",
    "l": "èl",
    "m": "èm",
    "n": "èn",
    "o": "o",
    "p": "pé",
    "q": "ki",
    "r": "èr",
    "s": "ès",
    "t": "té",
    "u": "u",
    "v": "vé",
    "w": "wé",
    "x": "èks",
    "y": "yé",
    "z": "zèt",
}

PHONETIC_MAPPING = {
    "sy": "ʃ",
    "ny": "ɲ",
    "ng": "ŋ",
    "dj": "dʒ",
    "'": "ʔ",
    "c": "tʃ",
    "é": "e",
    "è": "ɛ",
    "ê": "ə",
    "g": "ɡ",
    "I": "ɪ",
    "j": "dʒ",
    "ô": "ɔ",
    "q": "k",
    "U": "ʊ",
    "v": "f",
    "x": "ks",
    "y": "j",
}


dirname = os.path.dirname(__file__)


# Predict pronounciation with BERT Masking
# Read more:
# https://w11wo.github.io/posts/2022/04/predicting-phonemes-with-bert/
class Predictor:
    def __init__(self, model_path):
        # fmt: off
        self.vocab = ['', '[UNK]', 'a', 'n', 'ê', 'e', 'i', 'r', 'k', 's', 't',
                      'g', 'm', 'u', 'l', 'p', 'o', 'd', 'b', 'h', 'c', 'j',
                      'y', 'f', 'w', 'v', 'z', 'x', 'q', '[mask]']
        self.mask_token_id = self.vocab.index("[mask]")
        # fmt: on
        self.session = onnxruntime.InferenceSession(model_path)

    def predict(self, word: str) -> str:
        """
        Predict the phonetic representation of a word.

        Args:
            word (str): The word to predict.

        Returns:
            str: The predicted phonetic representation of the word.
        """
        text = [self.vocab.index(c) if c != "e" else self.mask_token_id
                for c in word]
        text.extend([0] * (32 - len(text)))  # Pad to 32 tokens
        inputs = np.array([text], dtype=np.int64)
        (predictions,) = self.session.run(None, {"input_4": inputs})

        # find masked idx token
        _, masked_index = np.where(inputs == self.mask_token_id)

        # get prediction at those masked index only
        mask_prediction = predictions[0][masked_index]
        predicted_ids = np.argmax(mask_prediction, axis=1)

        # replace mask with predicted token
        for i, idx in enumerate(masked_index):
            text[idx] = predicted_ids[i]

        return "".join([self.vocab[i] for i in text if i != 0])


class G2P:
    def __init__(self):
        self.tokenizer = TweetTokenizer()
        self.detokenizer = MosesDetokenizer(lang="id")

        dict_path = os.path.join(dirname, "data/dict.json")
        with open(dict_path) as f:
            self.dict = json.load(f)

        model_path = os.path.join(dirname, "model/bert_pron.onnx")
        self.predictor = Predictor(model_path)

        self.syllable_splitter = SyllableSplitter()

    def __call__(self, text: str) -> str:
        """
        Convert text to phonetic representation.

        Args:
            text (str): The text to convert.

        Returns:
            str: The phonetic representation of the text.
        """
        text = text.lower()
        text = re.sub(r"[^ a-z0-9'\.,?!-]", "", text)
        text = text.replace("-", " ")

        prons = []
        words = self.tokenizer.tokenize(text)
        for word in words:
            # PUEBI pronunciation
            if word in self.dict:
                pron = self.dict[word]
            elif len(word) == 1 and word in ABJAD_MAPPING:
                pron = ABJAD_MAPPING[word]
            elif "e" not in word or not word.isalpha():
                pron = word
            elif "e" in word:
                pron = self.predictor.predict(word)

            # Replace alofon /e/ with e (temporary)
            pron = pron.replace("é", "e")
            pron = pron.replace("è", "e")

            # Replace /x/ with /s/
            if pron.startswith("x"):
                pron = "s" + pron[1:]

            sylls = self.syllable_splitter.split_syllables(pron)
            # Decide where to put the stress
            stress_loc = len(sylls) - 1
            if len(sylls) > 1 and "ê" in sylls[-2]:
                if "ê" in sylls[-1]:
                    stress_loc = len(sylls) - 2
                else:
                    stress_loc = len(sylls)

            # Apply rules on syllable basis
            # All alophone are set to tense by default
            # and will be changed to lax if needed
            alophone = {"e": "é", "o": "o"}
            alophone_map = {"i": "I", "u": "U", "e": "è", "o": "ô"}
            for i, syll in enumerate(sylls, start=1):
                # Put Syllable stress
                if i == stress_loc:
                    syll = "ˈ" + syll

                # Alophone syllable rules
                for v in ["e", "o"]:
                    # Replace with lax allphone [ɛ, ɔ] if
                    # in closed final syllables
                    if v in syll and not syll.endswith(v) and i == len(sylls):
                        alophone[v] = alophone_map[v]

                # Alophone syllable stress rules
                for v in ["i", "u"]:
                    # Replace with lax allphone [ɪ, ʊ] if
                    # in the middle of syllable without stress
                    # and not ends with coda nasal [m, n, ng] (except for final
                    # syllable)
                    if (
                        v in syll
                        and not syll.startswith("ˈ")
                        and not syll.endswith(v)
                        and (
                            not any(syll.endswith(x) for x in ["m", "n", "ng"])
                            or i == len(sylls)
                        )
                    ):
                        syll = syll.replace(v, alophone_map[v])

                if syll.endswith("nk"):
                    syll = syll[:-2] + "ng"
                elif syll.endswith("d"):
                    syll = syll[:-1] + "t"
                elif syll.endswith("b"):
                    syll = syll[:-1] + "p"
                elif syll.endswith("k") or (
                    syll.endswith("g") and not syll.endswith("ng")
                ):
                    syll = syll[:-1] + "'"
                sylls[i - 1] = syll

            pron = "".join(sylls)
            # Apply phonetic and alophone mapping
            for v in alophone:
                if v == "o" and pron.count("o") == 1:
                    continue
                pron = pron.replace(v, alophone[v])
            for g, p in PHONETIC_MAPPING.items():
                pron = pron.replace(g, p)
            pron = pron.replace("kh", "x")

            prons.append(pron)
            prons.append(" ")

        return self.detokenizer.detokenize(prons)
