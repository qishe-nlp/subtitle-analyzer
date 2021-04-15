# Installation from pip3

```shell
pip3 install --verbose subtitle_analyzer
python -m spacy download en_core_web_trf
python -m spacy download es_dep_news_trf
```

# Usage

Please refer to [api docs](https://qishe-nlp.github.io/subtitle-analyzer/).

### Excutable usage

* Write ass file with vocabulary information

```shell
sta_vocab --srtfile movie.srt --lang en --assfile en_vocab.ass --google False
``` 

* Write ass file with phrase information 

```shell
sta_phrase --srtfile movie.srt --lang en --assfile en_phrase.ass --google False
```

### Package usage
```
from subtitlecore import Subtitle
from subtitle_analyzer import VocabAnalyzer, PhraseAnalyzer
from subtitle_analyzer import VocabASSWriter, PhraseASSWriter
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
```

# Development

### Clone project
```
git clone https://github.com/qishe-nlp/subtitle-analyzer.git
```

### Install [poetry](https://python-poetry.org/docs/)

### Install dependencies
```
poetry update
```

### Test
```
poetry run pytest -rP
```
which run tests under `tests/*`

### Execute
```
poetry run sta_vocab --help
poetry run sta_phrase --help
```

### Create sphinx docs
```
poetry shell
cd apidocs
sphinx-apidoc -f -o source ../subtitle_analyzer
make html
python -m http.server -d build/html
```

### Hose docs on github pages
```
cp -rf apidocs/build/html/* docs/
```

### Build
* Change `version` in `pyproject.toml` and `subtitle_analyzer/__init__.py`
* Build python package by `poetry build`

### Git commit and push

### Publish from local dev env
* Set pypi test environment variables in poetry, refer to [poetry doc](https://python-poetry.org/docs/repositories/)
* Publish to pypi test by `poetry publish -r test`

### Publish through CI 

* Github action build and publish package to [test pypi repo](https://test.pypi.org/)

```
git tag [x.x.x]
git push origin master
```

* Manually publish to [pypi repo](https://pypi.org/) through [github action](https://github.com/qishe-nlp/subtitle-analyzer/actions/workflows/pypi.yml)

