import pysubs2
import os

def _underline(w):
  """Add underline for phrases with ass style

  Args:
    w (tuple): phrase information, first element is phrase, second is its marker, e.g, ``noun_phrases``, ``verbs`` or ``plain``
  """
  if w[1] == "noun_phrases":
    return "{\\u1}" + w[0] + "{\\u0}"
  else:
    return w[0]

class PhraseASSWriter:
  """Write phrase information with time stamp into ass file
  """

  _local_dir = os.path.dirname(__file__)
  _srtfile = os.path.join(_local_dir, 'empty.srt')

  def __init__(self, cn_srtfile=None):
    """Initialize subtitle object from empty srtfile

    Args:
      cn_srtfile (str): Chineses subtitle filename
    """

    self._subs = pysubs2.load(self.__class__._srtfile)
    self._subs.info['PlayResX'] = 640
    self._subs.info['PlayResY'] = 360
    self._cn_subs = None
    if cn_srtfile:
      self._cn_subs = pysubs2.load(cn_srtfile)

  def _create_bullets(self, content, animation):
    """Add phrase information into subtitle object

    Args:
      content (list): phrase information with time stamp
      animation (bool): whether using animation in ass
    """

    default_style = self._subs.styles["Default"]
    default_style.fontsize = 20
    default_style.shadow = 0.3  # shadow: 0.3 px
    default_style.outline = 0.3 # font outline: 0.3 px
    default_style.italic = -1 
    default_style.bold = -1 
    default_style.marginl = 10
    default_style.marginr = 10
    default_style.marginv = 30 if self._cn_subs else 10

    phrase_style = self._subs.styles["Default"].copy()
    phrase_style.italic = 0 
    phrase_style.bold = 0
    phrase_style.alignment = 4
    phrase_style.fontsize = 24
    phrase_style.borderphrase_style = 1
    phrase_style.shadow = 0.3  # shadow: 0.3 px
    phrase_style.backcolor = pysubs2.Color(0, 0, 0, 100) # shadow color: black with (255-100)/255 transparent
    phrase_style.outline = 0.3 # font outline: 0.3 px
    phrase_style.outlinecolor = pysubs2.Color(0, 0, 0, 20) # outline color: black with (255-20)/255 transparent
    phrase_style.marginl = 24
    phrase_style.marginr = 10
    phrase_style.marginv = 10
    phrase_style.primarycolor = pysubs2.Color(255, 255, 255, 0) # font color: white, no transparent
    self._subs.styles["Phrase"] = phrase_style



    verb_style = self._subs.styles["Default"].copy()
    verb_style.italic = 0 
    verb_style.bold = 0
    verb_style.alignment = 7
    verb_style.fontsize = 24
    verb_style.borderverb_style = 1
    verb_style.shadow = 0.3  # shadow: 0.3 px
    verb_style.backcolor = pysubs2.Color(0, 0, 0, 100) # shadow color: black with (255-100)/255 transparent
    verb_style.outline = 0.3 # font outline: 0.3 px
    verb_style.outlinecolor = pysubs2.Color(0, 0, 0, 20) # outline color: black with (255-20)/255 transparent
    verb_style.marginl = 24
    verb_style.marginr = 10
    verb_style.marginv = 24
    verb_style.primarycolor = pysubs2.Color(255, 255, 255, 0) # font color: white, no transparent
    self._subs.styles["Verb"] = verb_style

    cn_default_style = self._subs.styles["Default"].copy()
    cn_default_style.fontsize = 20
    cn_default_style.shadow = 0.1  # shadow: 0.1 px
    cn_default_style.outline = 0.1 # font outline: 0.1 px
    cn_default_style.italic = -1 
    cn_default_style.bold = -1 
    cn_default_style.marginl = 10
    cn_default_style.marginr = 10
    cn_default_style.marginv = 3
    self._subs.styles["CN"] = cn_default_style


    marker_colors = {
      "plain": "{\\c&HFFFFFF&}",
      "verbs": "{\\c&H7C94FF&}",
      "noun_phrases": "{\\c&H93F8E9&}",
    }

    self._subs.events = []
    for bullet in content:
      phrases = bullet["noun_phrases"]
      _phrases = "\\N".join(["\\h\\h\\h\\h".join([marker_colors["noun_phrases"]+w["original"], marker_colors["plain"]+w["translated"]]) for w in phrases])
      _verbs = "\\N".join(["\\h\\h\\h\\h".join([marker_colors["verbs"]+w["text"], marker_colors["plain"]+"("+w["lemma"]+")", marker_colors["plain"]+w["meaning"]]) for w in bullet["verbs"]])

      
      start = pysubs2.time.timestamp_to_ms(pysubs2.time.TIMESTAMP.match(bullet["start"]).groups())
      end = pysubs2.time.timestamp_to_ms(pysubs2.time.TIMESTAMP.match(bullet["end"]).groups())
      if animation:
        phrase_event = pysubs2.SSAEvent(start=start, end=end, text=_phrases, style="Phrase", effect="Scroll up;10;110;"+str(100000/(0.90*(end-start))))
        verb_event = pysubs2.SSAEvent(start=start, end=end, text=_verbs, style="Verb", effect="Scroll up;10;110;"+str(100000/(0.90*(end-start))))
      else:
        phrase_event = pysubs2.SSAEvent(start=start, end=end, text=_phrases, style="Phrase")
        verb_event = pysubs2.SSAEvent(start=start, end=end, text=_verbs, style="Verb")


      _markers = " ".join([marker_colors[w[1]]+_underline(w) for w in bullet["markers"]])
      event = pysubs2.SSAEvent(start=start, end=end, text=_markers, style="Default")
      self._subs.append(event)
      self._subs.append(phrase_event)
      self._subs.append(verb_event)
    
    if self._cn_subs:
      for e in self._cn_subs:
        e.style = "CN"
        self._subs.append(e)


  def write(self, content, assfile, options):
    """Write phrase information into ass file

    Args:
      content (list): phrase information with time stamp
      assfile (str): ass filename
      options (dict): argument for ass format
    """

    self._create_bullets(content, options["animation"])
    self._subs.save(assfile)
