from sencore import PhraseParser
from x2cdict import PhraseDict, VocabDict


class PhraseAnalyzer:

  def __init__(self, lang):
    self._phrase_parser = PhraseParser(lang)
    self._phrase_dictapi = PhraseDict(lang)
    self._vocab_dictapi = VocabDict(lang)

  def _get_phrases(self, sentences):
    _phrases = []

    for e in sentences:
      phrase_set = self._phrase_parser.digest(e["text"])
      _phrases.append({
        "noun_phrases": phrase_set["noun_phrases"],
        "prep_phrases": phrase_set["prep_phrases"],
        "verbs": phrase_set["verbs"],
        #"passive_phrases": phrase_set["passive_phrases"],
        #"verb_phrases": phrase_set["verb_phrases"],
        "start": e["start"],
        "end": e["end"],
        "markers": phrase_set["markers"]
      })
    return _phrases
  
  def _look_up(self, phrases):
    _phrases_with_meaning = []
    for ele in phrases:
      noun_phrases = []
      for p in ele["noun_phrases"]:
        result = self._lookup_phrase(p)
        if result != None:
          noun_phrases.append(result)
      prep_phrases = []
      for p in ele["prep_phrases"]:
        result = self._lookup_phrase(p)
        if result != None:
          prep_phrases.append(result)
      verbs = []
      for p in ele["verbs"]:
        result = self._lookup_verb_dict(p, False)
        if result != None:
          verbs.append(result)

      _phrases_with_meaning.append({
        "start": ele["start"],
        "end": ele["end"],
        "noun_phrases": noun_phrases,
        "prep_phrases": prep_phrases,
        "verbs": verbs,
        "markers": ele["markers"],
      })
    return _phrases_with_meaning

  def _lookup_phrase(self, p):
    try:
      _r = self._phrase_dictapi.search(p)
      result = _r 
    except Exception as e:
      result = None
    return result 

  def _lookup_verb_dict(self, verb, extra):
    result = None
    dict_searched = self._vocab_dictapi.search(verb['text'], 'VERB', extra)
    if dict_searched != None:
      verb["meaning"] = dict_searched["meaning"]
      result = verb
    return result

  def get_line_phrases(self, sentences):
    _phrases = self._get_phrases(sentences)
    result = self._look_up(_phrases)
    return result

