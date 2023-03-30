from sencore import VocabParser
from x2cdict import VocabDict

class VocabAnalyzer:
  """To get vocabulary information from sentences with timestamp
  """

  def __init__(self, lang):
    """Initialize the ``_vocab_parser``, ``_dictapi``
  
    Args:
      lang (str): language abbreviation
    """
    self._vocab_parser = VocabParser(lang)
    self._dictapi = VocabDict(lang)
    self._pos_free = ['ADJ', 'ADV', 'AUX', 'NOUN', 'VERB', 'ADP', 'CONJ', 'CCONJ', 'SCONJ', 'PRON']

  def get_line_vocabs(self, sentences, external=False):
    """Parse sentences with timestamp into vocabularies and look up dictionary for explanation 

    Args:
      sentences (list): sentences with timestamp information
      external (bool): whether using external translation
    """
    _words = []
    for e in sentences:
      ws = [e for e in self._vocab_parser.digest(e["text"]) if e['pos'] in self._pos_free]
      ws_with_meaning = self._lookup_dict(ws, external)
      _words.append({"words": ws_with_meaning, "start": e["start"], "end": e["end"]})
    return _words

  def _lookup_dict(self, line_words, external=False):
    """Look up dictionary for vocabularies in one line of subtitle

    Args:
      line_words (list): vocabularies in one line of subtitle
      external (bool): whether using external translation
    """
    print(line_words)
    _words = []
    for e in line_words:
      dict_searched = self._dictapi.search(e['word'], e['pos'], external)
      if dict_searched != None:
        _words.append(dict_searched)
    return _words

