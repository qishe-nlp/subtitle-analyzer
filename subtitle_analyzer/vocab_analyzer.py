from sencore import VocabParser
from x2cdict import VocabDict

class VocabAnalyzer:

  def __init__(self, lang):
    self._vocab_parser = VocabParser(lang)
    self._dictapi = VocabDict(lang)
    self._pos_free = ['ADJ', 'ADV', 'AUX', 'NOUN', 'VERB', 'ADP', 'CONJ', 'CCONJ', 'SCONJ', 'PRON']

  def _get_words(self, sentences):
    _words = []
    for e in sentences:
      ws = [e for e in self._vocab_parser.digest(e["text"]) if e['pos'] in self._pos_free]
      ws_with_meaning = self._lookup_dict(ws)
      _words.append({"words": ws_with_meaning, "start": e["start"], "end": e["end"]})
    return _words

  def _lookup_dict(self, line_words, extra=False):
    _words = []
    for e in line_words:
      dict_searched = self._dictapi.search(e['word'], e['pos'], extra)
      if dict_searched != None:
        _words.append(dict_searched)
    return _words

  def get_line_vocabs(self, sentences, extra=False):
    words = self._get_words(sentences)
    return words 

