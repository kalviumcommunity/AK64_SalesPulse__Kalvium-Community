# Team GitHub Workflow

## Branching Strategy
- **Main branch:** Holds releasable code only
- **Feature branches:** Follow `feature/[description]` naming
- **Branch cleanup:** Branches are deleted after merge

## Commit Message Convention
- **Types used:** `feat`, `fix`, `docs`, `refactor`, `chore`
- **Format:** `[type]: [description]`
- **Why:** Enables automated changelog generation and clear history

## PR Review Process
- PRs require at least one approval before merge
- Code review focuses on: correctness, clarity, data integrity, and test coverage
- Commit messages are reviewed as part of code review

## GitHub Issue Tracking Approach
- Every feature or fix starts with an issue
- Issues have labels, assignees, and descriptions
- Issues are closed when the corresponding PR is merged

---

## Python Data Workflow Script

### How to Execute the Script

Ensure your virtual environment is activated, then from the **project root** run:

```bash
# macOS/Linux
source venv/bin/activate
python scripts/data_workflow.py

# Windows
venv\Scripts\activate
python scripts/data_workflow.py
```

To capture the output to a log file:

```bash
python scripts/data_workflow.py > output/sample_run.txt
```

### What Each Function Does

| Function | Description |
|---|---|
| `ingest_data(filepath)` | Reads a CSV file from `filepath` and returns a Pandas DataFrame. Raises `FileNotFoundError` if the path is invalid. |
| `process_data(df)` | Cleans the DataFrame: removes duplicate rows, fills missing numeric values with the column median, fills missing text values with `'Unknown'`, and adds a derived `deal_tier` column. |
| `output_results(df, output_path)` | Saves the cleaned DataFrame to a CSV at `output_path` and prints a summary of rows processed. |

### How to Modify the Script for New Datasets

1. **New data source:** Replace the CSV path in `ingest_data()` with your new file path or adapt the function to call `pd.read_json()` for JSON sources.
2. **Custom cleaning logic:** Add transformations inside `process_data()`. Follow the existing pattern: apply the change, then print a status message.
3. **Different output format:** In `output_results()`, replace `df.to_csv()` with `df.to_json()` or `df.to_excel()` for other output formats.
