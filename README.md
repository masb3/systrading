# Systematic trading strategy

This is a Python project built using [`uv`](https://docs.astral.sh/uv/), a fast Python package installer and resolver. Below are the instructions to set up and run the project.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- `uv` (installation instructions below)

## Installation

1. **Install `uv`:**

   If you haven't installed `uv` yet, you can do so by running the following command:  
   macOS / Linux:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   macOS:
   ```bash
   brew install uv
   ```
   Using `pip`:
   ```bash
   pip install uv
   ```
   Detailed instructions https://docs.astral.sh/uv/getting-started/installation/

## Execution

1. **Locate data files:**  

   Put `futuresA.csv` and `futuresB.csv` into the project root (where `pyptoject.toml`).  
   Alternatively update `FUTURES_A_SOURCE` and `FUTURES_B_SOURCE` in [conf.py](https://github.com/masb3/systrading/blob/main/src/conf.py)
   with absolute paths.  

2. **Check the possible configuration parameters in [conf.py](https://github.com/masb3/systrading/blob/main/src/conf.py)**  

3. **Run the program:**  

   From the project root:
   ```bash
   uv run -m src.main
   ```