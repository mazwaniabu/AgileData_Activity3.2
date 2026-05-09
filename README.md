# Agile Data Science CI/CD Duplicate Removal Pipeline

![Python](https://img.shields.io/badge/Python-3.10%20|%203.11%20|%203.12-blue)
![pytest](https://img.shields.io/badge/tests-pytest-brightgreen)

## Project Overview
This project implements a production-quality, beginner-friendly data engineering pipeline that removes duplicate rows from a CSV dataset. It includes automated tests, a Jupyter Notebook, and a GitHub Actions CI/CD workflow to validate every change.

## Agile Data Science Concept
Agile Data Science emphasizes iterative delivery, short feedback loops, and automated validation. In this project, each commit triggers CI to run tests and execute the pipeline, supporting rapid and reliable improvements.

## Setup Instructions
1. Ensure Python 3.10+ is installed.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running Locally
To run the duplicate removal pipeline:

```bash
python -m src.duplicate_removal
```

Input: data/raw/*.csv
Output: data/process/*.csv

You can override paths (single-file mode):

```bash
python -m src.duplicate_removal --input data/raw/dataset.csv --output data/process/dataset.csv
```

Directory mode:

```bash
python -m src.duplicate_removal --raw-dir data/raw --processed-dir data/process
```

## Running Tests
```bash
pytest -q
```

## GitHub Actions CI/CD
The workflow runs on push and pull request to:
- main
- dev
- phase/**
- phase*
- phase-*

Pipeline steps include dependency caching, validation, tests, pipeline execution, artifact upload, and success messaging.

## Repository Structure
```
project-root/
├── .github/workflows/ci.yml
├── data/
│   ├── raw/
│   │   └── dataset.csv
│   └── process/
│       └── dataset.csv
├── notebooks/ci_cd_duplicate.ipynb
├── src/__init__.py
├── src/duplicate_removal.py
├── tests/__init__.py
├── tests/test_duplicate_removal.py
├── requirements.txt
├── README.md
├── .gitignore
└── reflection.md
```

## Screenshots (Placeholders)
- Notebook execution screenshot
- GitHub Actions successful run screenshot

## CI/CD Explanation
The CI/CD pipeline uses a Python version matrix (3.10-3.12), caches pip dependencies, runs unit tests, executes the script, verifies output generation, and uploads the processed dataset as an artifact.

## Deliverables Checklist
- [x] Python duplicate removal pipeline
- [x] Jupyter Notebook
- [x] GitHub Actions workflow
- [x] Automated tests
- [x] Dataset processing
- [x] Documentation and reflection

## Reflection Summary
The pipeline automates duplicate removal and uses CI to validate each change. The Agile approach encourages small, testable updates with rapid feedback.
