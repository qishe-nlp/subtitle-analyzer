from sencore import PhraseParser
from x2cdict import PhraseDict, VocabDict
from .lib import make_markers


class PhraseAnalyzer:
  """To get phrase information from sentences with timestamp
  """

  def __init__(self, lang):
    """Initialize the ``_phrase_parser``, ``_phrase_dictapi`` and ``_vocab_dictapi``
  
    Args:
      lang (str): language abbreviation
    """

    self._phrase_parser = PhraseParser(lang)
    self._phrase_dictapi = PhraseDict(lang)
    self._vocab_dictapi = VocabDict(lang)

  def _tbr_phrases(self, sentences):
    """Parse sentences with timestamp into phrases for being reviewed

    Args:
      sentences (list): sentences with timestamp information
    """

    _phrases = []

    for e in sentences:
      _line_phrases = self._phrase_parser.digest(e["text"])
      del _line_phrases["markers"]
      _line_phrases["sentence"] = e["text"]
      _line_phrases["start"] = e["start"]
      _line_phrases["end"] = e["end"]
      _phrases.append(_line_phrases)

    return _phrases
 
  def _tbr_line_phrases(self, reviewed, google=False):
    _phrases = []

    for e in reviewed:
      markers = make_markers(e)
      _phrases_with_meaning = self._look_up(e, google)
      _phrases_with_meaning["start"] = e["start"]
      _phrases_with_meaning["end"] = e["end"]
      _phrases_with_meaning["markers"] = markers
      _phrases.append(_phrases_with_meaning)

    return _phrases

  def get_line_phrases(self, sentences, google=False):
    """Parse sentences with timestamp into phrases and look up dictionary for explanation

    Args:
      sentences (list): sentences with timestamp information
      google (bool): whether using google translation
    """

    _phrases = []

    for e in sentences:
      _line_phrases = self._phrase_parser.digest(e["text"])
      _phrases_with_meaning = self._look_up(_line_phrases, google)
      _phrases_with_meaning["start"] = e["start"]
      _phrases_with_meaning["end"] = e["end"]
      _phrases_with_meaning["markers"] = _line_phrases["markers"] 
      _phrases.append(_phrases_with_meaning)

    return _phrases
  
  def _look_up(self, line_phrases, google=False):
    """Look up dictionary for vocabularies in one line of subtitle

    Args:
      line_words (list): vocabularies in one line of subtitle
      google (bool): whether using google translation
    """
    
    noun_phrases = []
    for p in line_phrases["noun_phrases"]:
      result = self._lookup_phrase(p)
      if result != None:
        noun_phrases.append(result)
    verbs = []
    for p in line_phrases["verbs"]:
      result = self._lookup_verb_dict(p, google)
      if result != None:
        verbs.append(result)

    return {
      "noun_phrases": noun_phrases,
      "verbs": verbs,
    }

  def _lookup_phrase(self, p):
    """Look up dictionary for phrase explanation
  
    Args:
      p (str): phrase
    """
    try:
      _r = self._phrase_dictapi.search(p)
      result = _r 
    except Exception as e:
      result = None
    return result 

  def _lookup_verb_dict(self, verb, google=False):
    """Look up dictionary for verb explanation
  
    Args:
      verb (str): verb
      google (bool): whether using google translation
    """

    result = None
    dict_searched = self._vocab_dictapi.search(verb['text'], 'VERB', google)
    if dict_searched != None:
      verb["meaning"] = dict_searched["meaning"]
      result = verb
    return result

