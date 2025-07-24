# Script to update EFG Code dropdowns

This script adds new EFG codes to the existing EFG code dropdown menus.  
See issue: https://github.com/allenai/Earth-System-Feedback/issues/47

## Installation & Setup

1. Clone this repository and navigate into the project directory.

2. Create and activate a virtual environment (on Windows):

    ```bash
    py -m venv .venv
    .venv\Scripts\activate
    ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `api_key.txt` file and paste your ESS API key inside. 

5. Set the variables `new_efgs`, `project_id` and `metadata_names` at the beginning of the script

6. Run the script. 
    ```bash
    py main.py
    ```