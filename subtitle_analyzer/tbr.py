from subtitlecore import Subtitle
from subtitle_analyzer import PhraseAnalyzer
from subtitle_analyzer import PhraseASSWriter

import csv

import click
import json


def _write_to_csv(fields, content, csvfile="review.csv"):
  #print('Create {} file'.format(csvfile))
  with open(csvfile, encoding="utf8", mode='w') as output_file:
    dict_writer = csv.DictWriter(output_file, restval="-", fieldnames=fields, delimiter='\t')
    dict_writer.writeheader()
    dict_writer.writerows(content)


@click.command()
@click.option("--srtfile", help="Specify the subtitle filename", prompt="source")
@click.option("--lang", help="Specify the language", default="en", prompt="language")
@click.option("--dstname", help="Specify the review file name", prompt="destname")
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
  exs = analyzer._tbr_phrases(sens)

  phase = {"step": 3, "msg": "Finish phrases dictionary lookup", "vocabs": exs[:20]}
  print(json.dumps(phase), flush=True)

  np_content = []
  #pp_content = []
  v_content = []

  for e in exs:
    np_content.append({"start": e["start"], "end": e["end"], "sentence": e["sentence"], "phrases": json.dumps(e["noun_phrases"])})
    #pp_content.append({"start": e["start"], "end": e["end"], "sentence": e["sentence"], "phrases": json.dumps(e["prep_phrases"])})
    v_content.append({"start": e["start"], "end": e["end"], "sentence": e["sentence"], "vs": json.dumps(e["verbs"]), "pps": json.dumps(e["passive_phrases"]), "phrases": json.dumps(e["verb_phrases"])})

  _write_to_csv(["start", "end", "sentence", "phrases"], np_content, csvfile=dstname+".noun_phrase.csv")
  #_write_to_csv(["start", "end", "sentence", "phrases"], pp_content, csvfile=dstname+".prep_phrase.csv")
  _write_to_csv(["start", "end", "sentence", "vs", "pps", "phrases"], v_content, csvfile=dstname+".verb_phrase.csv")


def merge_content(npfile, vpfile):
  content = []
  nps, pps, vps = [], [], []
  
  with open(npfile, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    nps = [row for row in reader]   
  with open(vpfile, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    vps = [row for row in reader]   
  line_num = len(nps)
  assert(line_num == len(vps))
  for i in range(line_num):
    np, vp = nps[i], vps[i]
    sentence, start, end = np["sentence"], np["start"], np["end"]
    assert(start == vp["start"])
    assert(end == vp["end"])
    assert(sentence == vp["sentence"])
    content.append({"sentence": sentence, "start": start, "end": end, "noun_phrases": json.loads(np["phrases"]), "verbs": json.loads(vp["vs"])})
  return content

@click.command()
@click.option("--npfile", help="Specify the reviewed noun phrase filename", prompt="noun phrase source")
@click.option("--vpfile", help="Specify the reviewed verb phrase filename", prompt="verb phrase source")
@click.option("--lang", help="Specify the language", default="en", prompt="language")
@click.option("--cnsrtfile", required=False, help="Specify the Chinese subtitle filename", default=None)
@click.option("--assfile", required=False, help="Specify the output ass filename", default=None)
@click.option("--google", required=False, help="Whether extra help needed", type=bool, default=False)
def gen_phrase_ass(npfile, vpfile, lang, cnsrtfile, assfile, google):
  content = merge_content(npfile, vpfile)
  print(content)
  analyzer = PhraseAnalyzer(lang)
  exs = analyzer._tbr_line_phrases(content, google)
  print(exs)
  if assfile:
    ass_writer = PhraseASSWriter(cnsrtfile)
    ass_writer.write(exs, assfile, {"animation": False}) 


def test_read(npfile):
  with open(npfile, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    nps = [row for row in reader]   
    for r in nps:
      e = json.loads(r["phrases"])
      for item in e:
        print(item)

if __name__ == "__main__":
  test_read("./testsomething.csv")

