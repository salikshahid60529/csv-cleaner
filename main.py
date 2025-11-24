import csv
from pathlib import Path

INPUT_FILE = "input.csv"
OUTPUT_FILE = "clean.csv"

def is_row_empty(row: dict) -> bool:
    return all((value is None or str(value).strip() == "") for value in row.values())

def normalize_row(row: dict) -> tuple:
    return tuple((str(v).strip() if v is not None else "") for v in row.values())

def clean_csv(input_path: Path, output_path: Path):
    if not input_path.exists():
        print(f"❌ Datei nicht gefunden: {input_path}")
        return

    with input_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        if not fieldnames:
            print("❌ CSV hat keine Header.")
            return

        seen = set()
        cleaned_rows = []

        for row in reader:
            if is_row_empty(row):
                continue

            key = normalize_row(row)
            if key in seen:
                continue

            seen.add(key)
            cleaned_rows.append(row)

    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    print("✅ Fertig!")
    print(f"Input:  {input_path.resolve()}")
    print(f"Output: {output_path.resolve()}")
    print(f"Zeilen vorher: {len(list(csv.DictReader(input_path.open('r', encoding='utf-8'))))}")
    print(f"Zeilen nachher: {len(cleaned_rows)}")

if __name__ == "__main__":
    clean_csv(Path(INPUT_FILE), Path(OUTPUT_FILE))
