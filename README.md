# Order Processing System

A Python script that processes JSON order data and generates customer and item analytics files.

## Overview

This project processes restaurant order data from a JSON file and generates two output files:

- `customers.json`: Maps phone numbers to customer names
- `items.json`: Maps item names to pricing and order frequency data

## Script Overview

This project includes a single, flexible order processing script that combines the following features:

- **Input file from command line** - User specifies the input file as an argument
- **Configuration file support** - All other settings are configurable via JSON config files
- **Flexible usage** - Can use default config or specify custom configuration

## Design

The system is designed with the following principles:

- **Modularity**: Each processing function has a single responsibility
- **Error Handling**: Comprehensive error handling for file operations and data validation
- **Type Safety**: Uses Python type hints for better code documentation and IDE support
- **Data Validation**: Validates phone number format and handles missing data gracefully

### Architecture

The script follows a simple pipeline architecture:

1. **Input**: Load orders from JSON file
2. **Processing**: Extract and aggregate customer and item data
3. **Output**: Generate formatted JSON files

### Key Functions

- `load_orders()`: Safely loads and validates JSON input
- `process_customers()`: Creates phone-to-name mapping with duplicate handling
- `process_items()`: Aggregates item pricing and order counts
- `save_json()`: Writes formatted JSON output with proper encoding

## Usage

### Prerequisites

- Python 3.6 or higher
- Valid JSON file containing order data (see example_orders.json)

### Command Line Usage

Windows/Linux:

```bash
python process_orders.py <input_file.json> [config_file.json]
```

MacOS(Unix):

```bash
python3 process_orders.py <input_file.json> [config_file.json]
```

### Examples

```bash
# Use default config
python3 process_orders.py example_orders.json

# Use custom config
python3 process_orders.py example_orders.json my_config.json

# Process different input files
python3 process_orders.py january_orders.json
python3 process_orders.py february_orders.json
```

This will generate:

- `customers.json`: Customer phone number to name mapping
- `items.json`: Item analytics with pricing and order counts

## Configuration Files

The configuration-based scripts use JSON configuration files to customize behavior:

### Default Configuration (config.json)

```json
{
	"output_customers": "customers.json",
	"output_items": "items.json",
	"phone_pattern": "^\\d{3}-\\d{3}-\\d{4}$",
	"sort_output": true,
	"encoding": "utf-8",
	"indent": 4
}
```

### Configuration Options

| Option             | Description                        | Default                  | Example                  |
| ------------------ | ---------------------------------- | ------------------------ | ------------------------ |
| `output_customers` | Output filename for customer data  | `customers.json`         | `"my_customers.json"`    |
| `output_items`     | Output filename for item data      | `items.json`             | `"my_items.json"`        |
| `phone_pattern`    | Regex pattern for phone validation | `^\\d{3}-\\d{3}-\\d{4}$` | `^\\d{3}-\\d{3}-\\d{4}$` |
| `sort_output`      | Sort JSON output keys              | `true`                   | `false`                  |
| `encoding`         | File encoding                      | `utf-8`                  | `"utf-8"`                |
| `indent`           | JSON indentation spaces            | `4`                      | `2`                      |

### Creating Custom Configurations

Create different config files for different scenarios:

**compact_config.json** (for API integration):

```json
{
	"output_customers": "customers_compact.json",
	"output_items": "items_compact.json",
	"sort_output": false,
	"indent": 0
}
```

**report_config.json** (for human-readable reports):

```json
{
	"output_customers": "customer_report.json",
	"output_items": "item_report.json",
	"sort_output": true,
	"indent": 4
}
```

## Input Data Format

The script expects a JSON file containing an array of order objects with the following structure:

```json
[
	{
		"timestamp": 1702219784,
		"name": "Customer Name",
		"phone": "732-555-5509",
		"items": [
			{
				"name": "Item Name",
				"price": 12.95
			}
		],
		"notes": "Optional notes"
	}
]
```

## Output Format

### customers.json

```json
{
	"732-555-5509": "Damodhar",
	"609-555-2301": "Tom"
}
```

### items.json

```json
{
	"Butter Masala Dosa": {
		"price": 12.95,
		"orders": 52
	}
}
```

## Error Handling

The script handles various error conditions:

- Missing or invalid input files
- Malformed JSON data
- Invalid phone number formats
- File write permissions

## Development

This project follows Python best practices:

- PEP 8 style guidelines
- Comprehensive docstrings
- Type hints for better code documentation
- Modular function design
- Proper error handling and user feedback
- Configuration file support for flexibility

### Script Features

The single script (`process_orders.py`) provides:

- **Command-line input file** - Specify input file as first argument
- **Optional configuration file** - Use default `config.json` or specify custom config
- **Flexible output settings** - Output file names and formatting are configurable
- **Robust error handling** - Comprehensive validation and error messages

### Key Features

- **Input Validation**: Robust phone number validation using regex
- **Error Handling**: Comprehensive error handling for file operations
- **Type Safety**: Full type hints for better IDE support
- **Modularity**: Clean separation of concerns
- **Configurability**: Flexible configuration system
- **Performance**: Optimized regex compilation and data processing

## File Structure

```
project/
├── process_orders.py                   # Main processing script
├── config.json                         # Default configuration
├── example_orders.json                 # Sample input data
├── customers.json                      # Generated customer data
├── items.json                          # Generated item data
└── README.md                           # This documentation
```

## Testing

The script has been tested with the provided `example_orders.json` file, which contains:

- **10,000 orders** from 30 unique customers
- **19 unique menu items**
- Various phone number formats and data structures

### Test Commands

```bash
# Test with default config
python3 process_orders.py example_orders.json

# Test with custom config (create your own config file)
python3 process_orders.py example_orders.json my_config.json
```

The script successfully generates the required output files with correct data processing and formatting.
