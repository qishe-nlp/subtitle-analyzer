# -*- coding: utf-8 -*-
"""``subtitle_analyzer`` pacakage

This module demostrates the usage of package `subtitle_analyzer`.

.. topic:: Install package
  
  .. code:: shell
    
    $ pip3 install --verbose subtitle_analyzer
    $ python -m spacy download en_core_web_trf
    $ python -m spacy download es_dep_news_trf


.. topic:: Use as executable

  .. code:: shell

    $ sta_vocab --srtfile movie.srt --lang en --assfile en_vocab.ass --google False

  .. code:: shell

    $ sta_phrase --srtfile movie.srt --lang en --assfile en_phrase.ass --google False


.. topic:: Write assfile with vocabulary information 

  .. code:: python

    from subtitlecore import Subtitle
    from subtitle_analyzer import VocabAnalyzer
    from subtitle_analyzer import VocabASSWriter
    import json

    def subtitle_vocab(srtfile, lang, assfile, google):

      phase = {"step": 1, "msg": "Start sentenizing"}
      print(json.dumps(phase), flush=True)

      sf = Subtitle(srtfile, lang)
      sens = sf.sentenize()
      for e in sens:
        print(e)

      phase = {"step": 2, "msg": "Finish sentenizing"}
      print(json.dumps(phase), flush=True)

      analyzer = VocabAnalyzer(lang)
      exs = analyzer.get_line_vocabs(sens, google)
      shown = exs[:20]

      phase = {"step": 3, "msg": "Finish vocabs dictionary lookup", "vocabs": shown}
      print(json.dumps(phase), flush=True)

      if assfile:
        ass_writer = VocabASSWriter(srtfile)
        ass_writer.write(exs, assfile, {"animation": False})
        
        phase = {"step": 4, "msg": "Finish ass saving"} 
        print(json.dumps(phase), flush=True)


.. topic:: Write assfile with phrase information 

  .. code:: python

    from subtitlecore import Subtitle
    from subtitle_analyzer import PhraseAnalyzer
    from subtitle_analyzer import PhraseASSWriter
    import json

    def subtitle_phrase(srtfile, lang, assfile, google):

      phase = {"step": 1, "msg": "Start sentenizing"}
      print(json.dumps(phase), flush=True)

      sf = Subtitle(srtfile, lang)
      sens = sf.sentenize()
      for e in sens:
        print(e)

      phase = {"step": 2, "msg": "Finish sentenizing"}
      print(json.dumps(phase), flush=True)

      analyzer = PhraseAnalyzer(lang)
      exs = analyzer.get_line_phrases(sens, google)

      phase = {"step": 3, "msg": "Finish phrases dictionary lookup", "vocabs": exs[:10]}
      print(json.dumps(phase), flush=True)

      if assfile:
        ass_writer = PhraseASSWriter(srtfile)
        ass_writer.write(exs, assfile, {"animation": False})
        
        phase = {"step": 4, "msg": "Finish ass saving"} 
        print(json.dumps(phase), flush=True)

"""

__version__ = '0.1.14'

from .vocab_analyzer import VocabAnalyzer
from .vocab_ass_writer import VocabASSWriter
from .phrase_analyzer import PhraseAnalyzer
from .phrase_ass_writer import PhraseASSWriter
