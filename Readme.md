# Analytics Workspace Setup

A standardized, reproducible analytics development environment for cross-functional data product development teams. This repository provides a scalable structure, isolated virtual environment management, secret protection, locked dependencies, and clear handoff documentation.

## Setup

Follow these steps to replicate the project environment on your local machine:

1. **Clone the repository**
   ```bash
   git clone https://github.com/kalviumcommunity/AK64_SalesPulse__Kalvium-Community.git
   cd SalesPulse
   ```

2. **Create a virtual environment**
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     ```
   - **Windows:**
     ```bash
     python -m venv venv
     ```

3. **Activate the virtual environment**
   - **macOS / Linux:**
     ```bash
     source venv/bin/activate
     ```
   - **Windows (Command Prompt):**
     ```cmd
     venv\Scripts\activate
     ```
   - **Windows (PowerShell):**
     ```powershell
     venv\Scripts\Activate.ps1
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
analytics-workspace-setup/
├── data/
│   ├── raw/          # Source data as received - never modified directly
│   └── processed/    # Cleaned and transformed data ready for downstream analysis
├── notebooks/        # Jupyter notebooks for interactive exploration and reporting
├── scripts/          # Repeatable, automatable Python pipeline scripts
├── output/           # Generated reports, figures, export datasets, and models
├── .env.example      # Template for environment variables and secret configurations
├── .gitignore        # Specifies untracked files (venv, secrets, cache, checkpoints)
├── requirements.txt  # Pinned dependency manifest for environment reproducibility
└── README.md         # Workspace setup guidelines and documentation
```

## Notes

- **Secrets Management:** Environment-specific settings and sensitive credentials are store in `.env`. Copy `.env.example` to `.env` using `cp .env.example .env` (or `copy .env.example .env` on Windows) and fill in your local credentials.
- **Version Control Safety:** The `.env` file and `venv/` directory are excluded via `.gitignore` to protect sensitive information and prevent repository bloat.
