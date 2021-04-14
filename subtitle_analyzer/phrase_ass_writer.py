import pysubs2


def underline(w):
  if w[1] == "noun_phrases" or w[1] == "prep_phrases":
    return "{\\u1}" + w[0] + "{\\u0}"
  else:
    return w[0]

class PhraseASSWriter:
  def __init__(self, srtfile, name):
    self.dstfile = name + '.ass'
    self.subs = pysubs2.load(srtfile) 
    self.subs.info['PlayResX'] = 640
    self.subs.info['PlayResY'] = 360

  def create_bullets(self, content, animation):
    default_style = self.subs.styles["Default"]
    default_style.fontsize = 16
    default_style.shadow = 0.5  # shadow: 0.5 px
    default_style.outline = 0.5 # font outline: 0.5 px
    default_style.italic = -1 
    default_style.bold = -1 
    default_style.marginl = 10
    default_style.marginr = 10
    default_style.marginv = 10

    phrase_style = self.subs.styles["Default"].copy()
    phrase_style.italic = 0 
    phrase_style.bold = 0
    phrase_style.alignment = 4
    phrase_style.fontsize = 16
    phrase_style.borderphrase_style = 1
    phrase_style.shadow = 0.5  # shadow: 0.5 px
    phrase_style.backcolor = pysubs2.Color(0, 0, 0, 100) # shadow color: black with (255-100)/255 transparent
    phrase_style.outline = 0.5 # font outline: 0.5 px
    phrase_style.outlinecolor = pysubs2.Color(0, 0, 0, 20) # outline color: black with (255-20)/255 transparent
    phrase_style.marginl = 24
    phrase_style.marginr = 10
    phrase_style.marginv = 10
    phrase_style.primarycolor = pysubs2.Color(255, 255, 255, 0) # font color: white, no transparent
    self.subs.styles["Phrase"] = phrase_style



    verb_style = self.subs.styles["Default"].copy()
    verb_style.italic = 0 
    verb_style.bold = 0
    verb_style.alignment = 7
    verb_style.fontsize = 16
    verb_style.borderverb_style = 1
    verb_style.shadow = 0.5  # shadow: 0.5 px
    verb_style.backcolor = pysubs2.Color(0, 0, 0, 100) # shadow color: black with (255-100)/255 transparent
    verb_style.outline = 0.5 # font outline: 0.5 px
    verb_style.outlinecolor = pysubs2.Color(0, 0, 0, 20) # outline color: black with (255-20)/255 transparent
    verb_style.marginl = 24
    verb_style.marginr = 10
    verb_style.marginv = 24
    verb_style.primarycolor = pysubs2.Color(255, 255, 255, 0) # font color: white, no transparent
    self.subs.styles["Verb"] = verb_style


    marker_colors = {
      "plain": "{\\c&HFFFFFF&}",
      "verbs": "{\\c&H7C94FF&}",
      "noun_phrases": "{\\c&H93F8E9&}",
      "prep_phrases": "{\\c&H93F8E9&}",
    }

    self.subs.events = []
    for bullet in content:
      phrases = bullet["prep_phrases"] + bullet["noun_phrases"]
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


      _markers = " ".join([marker_colors[w[1]]+underline(w) for w in bullet["markers"]])
      event = pysubs2.SSAEvent(start=start, end=end, text=_markers, style="Default")
      self.subs.append(event)
      self.subs.append(phrase_event)
      self.subs.append(verb_event)


  def write(self, content, options):
    self.create_bullets(content, options["animation"])
    self.subs.save(self.dstfile)
