from subtitlecore import Subtitle
from subtitle_analyzer import VocabAnalyzer, PhraseAnalyzer
from subtitle_analyzer import VocabASSWriter, PhraseASSWriter

import click
import json

@click.command()
@click.option("--srtfile", help="Specify the subtitle filename", prompt="srtfile")
@click.option("--lang", help="Specify the language", default="en", prompt="language")
@click.option("--dstname", required=False, help="Specify the output csv name", default=None)
@click.option("--google", required=False, help="Whether extra help needed", type=bool, default=False)
def subtitle_vocab(srtfile, lang, dstname, google):

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

  if dstname:
    ass_writer = VocabASSWriter(srtfile, dstname)
    ass_writer.write(exs, {"animation": False})
    
    phase = {"step": 4, "msg": "Finish ass saving"} 
    print(json.dumps(phase), flush=True)


@click.command()
@click.option("--srtfile", help="Specify the subtitle filename", prompt="source")
@click.option("--lang", help="Specify the language", default="en", prompt="language")
@click.option("--dstname", required=False, help="Specify the output csv name", default=None)
def subtitle_phrase(srtfile, lang, dstname):

  phase = {"step": 1, "msg": "Start sentenizing"}
  print(json.dumps(phase), flush=True)

  sf = Subtitle(srtfile, lang)
  sens = sf.sentenize()
  for e in sens:
    print(e)

  phase = {"step": 2, "msg": "Finish sentenizing"}
  print(json.dumps(phase), flush=True)

  analyzer = PhraseAnalyzer(lang)
  exs = analyzer.get_line_phrases(sens)

  phase = {"step": 3, "msg": "Finish vocabs dictionary lookup", "vocabs": exs[:10]}
  print(json.dumps(phase), flush=True)

  if dstname:
    ass_writer = PhraseASSWriter(srtfile, dstname)
    ass_writer.write(exs, {"animation": False})
    
    phase = {"step": 4, "msg": "Finish ass saving"} 
    print(json.dumps(phase), flush=True)

