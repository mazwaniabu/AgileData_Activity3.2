"""Duplicate removal pipeline."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import List, Tuple

import pandas as pd


logger = logging.getLogger(__name__)


def load_dataset(path: Path) -> pd.DataFrame:
    """Load a CSV dataset from disk."""
    if not path.exists():
        logger.error("Input file not found: %s", path)
        raise FileNotFoundError(f"Input file not found: {path}")

    try:
        df = pd.read_csv(path)
    except Exception as exc:  # pragma: no cover - pandas errors vary by version
        logger.exception("Failed to read CSV: %s", path)
        raise RuntimeError(f"Failed to read CSV: {path}") from exc

    return df


def remove_duplicates(df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
    """Remove duplicate rows from a DataFrame."""
    duplicate_count = int(df.duplicated().sum())
    cleaned = df.drop_duplicates().reset_index(drop=True)
    return cleaned, duplicate_count


def save_dataset(df: pd.DataFrame, path: Path) -> None:
    """Save a DataFrame to disk as CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        df.to_csv(path, index=False)
    except Exception as exc:  # pragma: no cover - pandas errors vary by version
        logger.exception("Failed to write CSV: %s", path)
        raise RuntimeError(f"Failed to write CSV: {path}") from exc


def process_dataset(input_path: Path, output_path: Path) -> pd.DataFrame:
    """Load, de-duplicate, and save a dataset."""
    df = load_dataset(input_path)
    cleaned, duplicate_count = remove_duplicates(df)

    logger.info("Rows before: %s", len(df))
    logger.info("Duplicate rows removed: %s", duplicate_count)
    logger.info("Rows after: %s", len(cleaned))

    save_dataset(cleaned, output_path)
    return cleaned


def list_raw_files(raw_dir: Path) -> List[Path]:
    """Return CSV files from the raw directory."""
    if not raw_dir.exists():
        logger.error("Raw directory not found: %s", raw_dir)
        raise FileNotFoundError(f"Raw directory not found: {raw_dir}")

    return sorted(
        path
        for path in raw_dir.iterdir()
        if path.is_file() and path.suffix.lower() == ".csv"
    )


def process_new_files(raw_dir: Path, processed_dir: Path) -> List[Path]:
    """Process CSV files that have not been cleaned yet."""
    processed_dir.mkdir(parents=True, exist_ok=True)
    output_paths: List[Path] = []

    for input_path in list_raw_files(raw_dir):
        output_path = processed_dir / input_path.name
        if output_path.exists():
            logger.info("Skipping already processed file: %s", output_path)
            continue

        process_dataset(input_path, output_path)
        output_paths.append(output_path)

    if not output_paths:
        logger.info("No new files found in %s", raw_dir)

    return output_paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Remove duplicate rows from CSV.")
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Path to input dataset CSV (single-file mode).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Path to save cleaned dataset CSV (single-file mode).",
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=Path("data/raw"),
        help="Directory containing raw CSV files.",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=Path("data/process"),
        help="Directory to write cleaned CSV files.",
    )
    return parser.parse_args()


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    args = parse_args()

    try:
        if args.input or args.output:
            if not (args.input and args.output):
                logger.error("Both --input and --output are required in single-file mode.")
                return 2

            process_dataset(args.input, args.output)
            logger.info("Cleaned dataset saved to %s", args.output)
        else:
            output_paths = process_new_files(args.raw_dir, args.processed_dir)
            if output_paths:
                logger.info("Processed %s file(s) into %s", len(output_paths), args.processed_dir)
                for output_path in output_paths:
                    logger.info("Processed file: %s", output_path)
    except FileNotFoundError:
        return 2
    except Exception:
        logger.exception("Processing failed")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
