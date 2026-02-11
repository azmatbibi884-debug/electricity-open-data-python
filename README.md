# 🔌 Fingrid Open Data Viewer

A Python application for retrieving and analyzing electricity data from **Fingrid Open Data API**. This application demonstrates modern software architecture with modular design, comprehensive error handling, and user-friendly data visualization.

## 📋 Overview

This application retrieves selected electricity-related data from Fingrid's public API and presents it to the user in multiple formats:
- **Table format** in the command line with formatted statistics
- **Visualization** using matplotlib charts
- **Statistical analysis** including average, maximum, minimum, median, and standard deviation

## 🎯 Features

✅ **Data Retrieval**: Fetch real-time electricity data from Fingrid Open Data API  
✅ **Multiple Variables**: Support for various electricity metrics (hydro, wind, thermal, solar, load, etc.)  
✅ **Time Range Query**: Get data for any specified date/time range  
✅ **Table Display**: Formatted table output in the console  
✅ **Statistical Analysis**: Calculate comprehensive statistics  
✅ **Data Visualization**: Generate charts using matplotlib  
✅ **Error Handling**: Robust error handling for API and network issues  
✅ **Modular Architecture**: Clean separation of concerns with service and utility modules  

## 🏗️ Project Structure

```
electricity_data_app/
├── app.py                    # Main application entry point
├── config.py                 # Configuration and environment variables
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── services/
│   ├── __init__.py
│   ├── api_client.py        # Fingrid API client
│   └── data_processor.py     # Data processing and statistics
└── utils/
    ├── __init__.py
    └── error_handler.py      # Error handling utilities
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.7+**
- **Fingrid API Key** (free, register at [Fingrid Open Data](https://www.fingrid.fi/en/electricity-market/data-sources/open-data/))

### Installation

1. **Clone or extract the project** to your desired location

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set API Key as environment variable**:
   
   **Windows (PowerShell)**:
   ```powershell
   $env:FINGRID_API_KEY = "your_api_key_here"
   ```
   
   **Windows (Command Prompt)**:
   ```cmd
   set FINGRID_API_KEY=your_api_key_here
   ```
   
   **macOS/Linux**:
   ```bash
   export FINGRID_API_KEY="your_api_key_here"
   ```

### Running the Application

```bash
python app.py
```

This will start an interactive menu where you can:
1. View electricity data
2. See available variables
3. Exit the application

## 📖 Usage Guide

### Main Menu

When you run the application, you'll see:
```
==================================================
  Fingrid Open Data Viewer
==================================================
1. View electricity data
2. Show available variables
3. Exit
==================================================
```

### Viewing Data

1. Select option **1** to view electricity data
2. Enter a **Variable ID** (or type "list" to see available variables)
3. Specify the **time range** in format: `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SSZ`
4. View results as a **formatted table** with statistics
5. Optionally **generate a chart** to visualize the data

### Available Variables

Common electricity variables you can query:

| ID  | Description |
|-----|-------------|
| 100 | Production (Wind) |
| 101 | Production (Thermal) |
| 102 | Production (Solar) |
| 124 | Production (Hydro) |
| 172 | Load forecast |
| 191 | Reserved capacity |
| 200 | Cross-border flow |
| 74  | Electricity generation |

For a complete list of variables, visit [Fingrid Open Data Documentation](https://www.fingrid.fi/en/electricity-market/data-sources/open-data/).

## 🏗️ Architecture

### Modular Design

The application follows a **service-oriented architecture**:

**Services Layer** (`services/`):
- `api_client.py`: Handles all API communication with Fingrid
- `data_processor.py`: Processes raw data, calculates statistics, formats output

**Utilities Layer** (`utils/`):
- `error_handler.py`: Centralized error handling with specific exception types

**Configuration**:
- `config.py`: Manages environment variables and API configuration

**Main Application**:
- `app.py`: User interface and application orchestration

### Error Handling

The application includes comprehensive error handling for:
- **Missing API Key**: Checks for FINGRID_API_KEY environment variable
- **Invalid Input**: Validates time formats and variable IDs
- **Network Errors**: Handles connection timeouts and failures
- **API Errors**: Distinguishes between authentication and data errors
- **Data Processing Errors**: Catches issues during statistics calculation

Custom exception classes:
- `AuthenticationError`: API authentication failures
- `NetworkError`: Network connectivity issues
- `ValidationError`: Invalid input parameters
- `DataProcessingError`: Data processing failures

## 📊 Example Output

### Table Display
```
Variable 124: Hydro Production
+---------------------+--------+
| start_time          |  value |
+=====================+========+
| 2024-01-15 12:00:00 | 1234.5 |
| 2024-01-15 13:00:00 | 1245.3 |
| 2024-01-15 14:00:00 | 1256.8 |
+---------------------+--------+

📈 Statistics:
--------------------------------------------------
Count:     72
Average:   1234.56
Maximum:   1289.45
Minimum:   1198.23
Median:    1232.10
Std Dev:   28.34
--------------------------------------------------
```

### Chart Display
Generates an interactive matplotlib chart showing electricity data over time.

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Python 3.7+** | Core language |
| **requests** | HTTP API requests |
| **pandas** | Data processing and analysis |
| **matplotlib** | Data visualization |
| **tabulate** | Table formatting |

## 🔐 Security Notes

- **API Key Management**: Store your API key safely as an environment variable, never commit it to version control
- **Rate Limiting**: Be mindful of API rate limits when making multiple requests
- **Data Privacy**: Fingrid data is public, but respect their terms of service

## 📚 Fingrid API Documentation

For detailed API documentation, visit:
- [Fingrid Open Data Portal](https://www.fingrid.fi/en/electricity-market/data-sources/open-data/)
- [API Documentation](https://www.fingrid.fi/en/electricity-market/data-sources/open-data/api-documentation/)
- [Available Variables](https://www.fingrid.fi/en/electricity-market/data-sources/open-data/available-data/)

## 🐛 Troubleshooting

### Issue: "FINGRID_API_KEY is missing"
**Solution**: Set your API key as an environment variable. See Installation section above.

### Issue: "Invalid API key"
**Solution**: Verify you've set the correct API key from Fingrid's website.

### Issue: "Variable ID not found"
**Solution**: Check the variable ID using option 2 in the menu, or view Fingrid's API documentation.

### Issue: "Request timed out"
**Solution**: The API may be temporarily unavailable. Try again in a few moments.

### Issue: Chart not displaying
**Solution**: Ensure matplotlib is installed: `pip install --upgrade matplotlib`

## 📈 Future Enhancements

Possible improvements for future versions:
- Export data to CSV/Excel format
- Compare multiple variables side-by-side
- Save charts to files
- Web interface using Flask/Django
- Real-time data streaming
- Advanced filtering and aggregation options

## 📝 License

This project is for educational purposes. Please respect Fingrid's terms of service when using their API.

## 👤 Author

Created as part of a programming assignment to demonstrate modern Python application development with open data APIs.

## 📞 Support

For issues with:
- **Application**: Review the error message and check the Troubleshooting section
- **API**: Consult [Fingrid documentation](https://www.fingrid.fi/en/electricity-market/data-sources/open-data/)
- **Dependencies**: Check [PyPI](https://pypi.org/) for package documentation
