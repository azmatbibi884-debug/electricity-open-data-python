# Quick Setup Guide - Fingrid Open Data Viewer

## Step 1: Install Dependencies

Open PowerShell and run:
```powershell
cd d:\electricity_data_app
pip install -r requirements.txt
```

## Step 2: Set Your Fingrid API Key

Set the environment variable in PowerShell:
```powershell
$env:FINGRID_API_KEY = "your_api_key_here"
```

To get an API key:
1. Visit https://www.fingrid.fi/en/electricity-market/data-sources/open-data/
2. Register and subscribe to the Open Data API
3. Copy your API key

## Step 3: Run the Application

From the same PowerShell window (same session):
```powershell
python app.py
```

## Step 4: Use the Application

When you run the app, you'll see a menu:

**Option 1: View electricity data**
- Enter a variable ID (e.g., 124 for hydro production)
  - Or type "list" to see all available variables
- Enter start date/time (format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)
- Enter end date/time in the same format
- View results as a table with statistics
- Optionally generate a chart

**Option 2: Show available variables**
- Lists common electricity variables you can query

**Option 3: Exit**
- Closes the application

## Common Variable IDs

| ID  | Description |
|-----|-------------|
| 74  | Total electricity generation |
| 100 | Wind power production |
| 101 | Thermal power production |
| 102 | Solar power production |
| 124 | Hydro power production |
| 172 | Load forecast |
| 191 | Reserve capacity |
| 200 | Cross-border electricity flow |

## Example Usage

```
Enter variable ID: 124
Start time (YYYY-MM-DD...): 2024-01-10
End time (YYYY-MM-DD...): 2024-01-15
```

This will fetch 5 days of hydro power production data and display it.

## Project Structure

The application is organized as microservices:

- **app.py** - Main user interface
- **config.py** - API configuration
- **services/api_client.py** - Handles API communication
- **services/data_processor.py** - Processes and formats data
- **utils/error_handler.py** - Error handling and validation

## Troubleshooting

**Error: "FINGRID_API_KEY is missing"**
- Make sure you set the environment variable in the same PowerShell session before running the app
- Use: `$env:FINGRID_API_KEY = "your_key"`

**Error: "Module not found"**
- Install dependencies: `pip install -r requirements.txt`

**No data returned**
- Check that the variable ID exists
- Verify your date range is in the correct format
- Make sure there's data available for that time period in Fingrid's API

For detailed documentation, see README.md
