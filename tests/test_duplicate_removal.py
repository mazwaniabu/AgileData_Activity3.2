from pathlib import Path

import pandas as pd
import pytest

from src.duplicate_removal import (
    load_dataset,
    process_dataset,
    process_new_files,
    remove_duplicates,
    save_dataset,
)


def make_sample_csv(path: Path) -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "col_a": [1, 1, 2, 3, 3],
            "col_b": ["x", "x", "y", "z", "z"],
        }
    )
    df.to_csv(path, index=False)
    return df


def test_remove_duplicates_function():
    df = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]})
    cleaned, duplicate_count = remove_duplicates(df)

    assert duplicate_count == 1
    assert len(cleaned) == 2
    assert cleaned.duplicated().sum() == 0


def test_process_dataset_creates_file(tmp_path: Path):
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"

    make_sample_csv(input_path)
    processed = process_dataset(input_path, output_path)

    assert output_path.exists()
    assert len(processed) < 5


def test_no_duplicates_remain(tmp_path: Path):
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"

    make_sample_csv(input_path)
    processed = process_dataset(input_path, output_path)

    assert processed.duplicated().sum() == 0


def test_invalid_input_file_raises(tmp_path: Path):
    missing_path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_dataset(missing_path)


def test_save_dataset_writes_csv(tmp_path: Path):
    output_path = tmp_path / "output.csv"
    df = pd.DataFrame({"a": [1, 2]})

    save_dataset(df, output_path)

    saved = pd.read_csv(output_path)
    assert len(saved) == 2


def test_process_new_files_creates_output(tmp_path: Path):
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "process"
    raw_dir.mkdir()

    input_path = raw_dir / "sample.csv"
    make_sample_csv(input_path)

    outputs = process_new_files(raw_dir, processed_dir)

    assert len(outputs) == 1
    assert outputs[0].exists()


def test_process_new_files_skips_existing_output(tmp_path: Path):
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "process"
    raw_dir.mkdir()
    processed_dir.mkdir()

    input_path = raw_dir / "sample.csv"
    make_sample_csv(input_path)

    existing_output = processed_dir / "sample.csv"
    make_sample_csv(existing_output)

    outputs = process_new_files(raw_dir, processed_dir)

    assert outputs == []


def test_process_new_files_missing_raw_dir(tmp_path: Path):
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "process"

    with pytest.raises(FileNotFoundError):
        process_new_files(raw_dir, processed_dir)
