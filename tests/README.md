# slider-entity-row tests

This repository uses [ha-testcontainer](https://github.com/Lint-Free-Technology/ha-testcontainer)
for Home Assistant visual tests.

## Prerequisites

- Docker
- Python 3.11+
- Node dependencies installed and build generated (`npm ci && npm run build`)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[test]'
playwright install --with-deps chromium
```

## Run tests

```bash
pytest tests/visual/test_scenarios.py
pytest tests/visual/test_doc_images.py
```

## Update generated documentation images

```bash
DOC_IMAGE_UPDATE=1 pytest tests/visual/test_doc_images.py
```
