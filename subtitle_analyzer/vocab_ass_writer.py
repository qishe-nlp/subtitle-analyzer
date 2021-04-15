import pysubs2

class VocabASSWriter:
  """Write vocabulary information with time stamp into ass file
  """
  def __init__(self, srtfile):
    """Initialize subtitle object from srtfile

    Args:
      srtfile (str): subtitle filename
    """
    self._subs = pysubs2.load(srtfile) 

  def _create_bullets(self, content, animation):
    """Add vocabulary information into subtitle object

    Args:
      content (list): vocabulary information with time stamp
      animation (bool): whether using animation in ass
    """
    style = self._subs.styles["Default"].copy()
    style.alignment = 7
    style.fontsize = 13
    style.borderstyle = 1
    style.shadow = 0.5  # shadow: 0.5 px
    style.backcolor = pysubs2.Color(0, 0, 0, 100) # shadow color: black with (255-100)/255 transparent
    style.outline = 0.5 # font outline: 0.5 px
    style.outlinecolor = pysubs2.Color(0, 0, 0, 20) # outline color: black with (255-20)/255 transparent
    style.marginl = 70
    style.marginv = 30
    style.primarycolor = pysubs2.Color(255, 255, 255, 0) # font color: white, no transparent
    self._subs.styles["Bullet"] = style
    for s in self._subs:
      s.text = s.text.replace("\\N", " ")
    for bullet in content:
      ws = "\\N".join(["\\h\\h\\h\\h".join(["{\c&H58E08F&}"+w["word"], "{\\c&HFFFFFF&}"+w["meaning"], "{\\c&H2AD6C4&}"+"["+w["dict_pos"]+"]"]) for w in bullet["words"]])
      start = pysubs2.time.timestamp_to_ms(pysubs2.time.TIMESTAMP.match(bullet["start"]).groups())
      end = pysubs2.time.timestamp_to_ms(pysubs2.time.TIMESTAMP.match(bullet["end"]).groups())
      if animation:
        event = pysubs2.SSAEvent(start=start, end=end, text=ws, style="Bullet", effect="Scroll up;10;110;"+str(100000/(0.90*(end-start))))
      else:
        event = pysubs2.SSAEvent(start=start, end=end, text=ws, style="Bullet")
      self._subs.append(event)

  def write(self, content, assfile, options):
    """Write vocabulary information into ass file

    Args:
      content (list): vocabulary information with time stamp
      assfile (str): ass filename
      options (dict): argument for ass format
    """
    self._create_bullets(content, options["animation"])
    self._subs.save(assfile)
