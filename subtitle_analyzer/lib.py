import re

def find_phrases_pos(sentence, phrases, label):
  phrases_ranges = []
  for p in phrases:
    start = sentence.find(p)
    if start != -1:
      end = start + len(p)
      phrases_ranges.append((start, end, label))
    else: # strange cases, should NOT happened
      print("{} {} {}".format("="*10, "ERROR BEGIN", "="*10))
      print(sentence)
      print(p)
      print("{} {} {}".format("="*10, "ERROR END", "="*10))
  return phrases_ranges

def find_vocabs_pos(sentence, vocabs, label):
  vocabs_ranges = []
  segs = re.split('(\W+)', sentence)
  for v in vocabs:
    try:
      index_in_segs = segs.index(v)
      start = sum([len(s) for s in segs[:index_in_segs]])
      end = start + len(v)
      vocabs_ranges.append((start, end, label))
    except Exception as e:
      print(e)
      print("{} {} {}".format("="*10, "ERROR BEGIN", "="*10))
      print(sentence)
      print(v)
      print("{} {} {}".format("="*10, "ERROR END", "="*10))
  return vocabs_ranges


def merge_ranges(ranges):
  ordered = sorted(ranges, key=lambda x: x[0])
  purified = []
  index = 0
  while index < len(ordered)-1:
    first, second = ordered[index], ordered[index+1]
    if first[1] > second[0]:
      purified.append((first[0], max(first[1], second[1]), first[2]))
      index = index + 2
    else:
      purified.append(first)
      index = index + 1
  if index == len(ordered)-1:
    purified.append(ordered[index])
  return purified

def extend_ranges(ranges, maxlen):
  ordered = merge_ranges(ranges)
  start = 0
  result = []
  for e in ordered:
    if start < e[0]:
      result.append((start, e[0], "plain"))
    result.append(e)
    start = e[1]
  if start < maxlen:
    result.append((start, maxlen, "plain"))
  return result

def make_markers(line_phrases):
  vs = [v["text"] for v in line_phrases["verbs"]]
  nps = line_phrases["noun_phrases"]
  sentence = line_phrases["sentence"]
  filtered_sentence = " ".join(sentence.split()) # remove /xa0

  verbs_ranges = find_vocabs_pos(filtered_sentence, vs, "verbs")
  noun_phrases_ranges = find_phrases_pos(filtered_sentence, nps, "noun_phrases")

  all_ranges = noun_phrases_ranges+verbs_ranges
  print(all_ranges)
  doc_mark = extend_ranges(all_ranges, len(filtered_sentence))
  markers = [(filtered_sentence[d[0]: d[1]], d[2]) for d in doc_mark]
  return markers
