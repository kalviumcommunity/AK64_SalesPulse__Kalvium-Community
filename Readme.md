# Analytics Workspace Setup

This project provides a standard data analytics workspace setup for a B2B sales organization. It establishes a consistent directory structure, a Python virtual environment, and installs a typical data analytics stack to analyze CRM updates, email response history, and deal-stage transitions.

## Setup

Follow these steps to set up your local development environment:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/analytics-workspace-setup.git
   cd analytics-workspace-setup
   ```

2. **Create the virtual environment:**
   - **macOS/Linux:**
     ```bash
     python3 -m venv venv
     ```
   - **Windows:**
     ```bash
     python -m venv venv
     ```

3. **Activate the virtual environment:**
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

- `data/raw/`: Contains raw, unaltered data files.
- `data/processed/`: Contains cleaned and processed data files ready for analysis.
- `notebooks/`: Contains Jupyter notebooks for exploratory data analysis and experimentation.
- `scripts/`: Contains Python scripts for data processing and pipeline tasks.
- `output/`: Contains output files like generated reports, figures, and exported models.

## Notes

- This project requires environment variables for configuration (e.g., database credentials, API keys).
- Please copy the `.env.example` file to a new file named `.env` and fill in your own specific values.
- **Do not commit your `.env` file to version control.** It is already ignored by `.gitignore`.
