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

### Key Functions

- `load_orders()`: Safely loads and validates JSON input
- `process_customers()`: Creates phone-to-name mapping with duplicate handling
- `process_items()`: Aggregates item pricing and order counts
- `save_json()`: Writes formatted JSON output with proper encoding

## Usage

### Prerequisites

- Python 3.6 or higher
- Valid JSON input file containing order data (see example_orders.json)

### Command Line Usage

Windows/Linux:

```bash
python process_orders.py <input_file.json> [config_file.json]
```

MacOS(Unix):

```bash
python3 process_orders.py <input_file.json> [config_file.json]
```

#### Options

- `-c, --config FILE`: Configuration file to use. Default: `config.json`.
- `-o, --output-dir DIR`: Output directory for generated files. Default: current directory.
- `-v, --verbose`: Enable verbose output with extra details.

### Examples

```bash
# Use default config
python process_orders.py example_orders.json

# Use custom config
python process_orders.py example_orders.json my_config.json

# Verbose mode
python process_orders.py example_orders.json --verbose

# Custom output directory
python process_orders.py example_orders.json --output-dir results

# Combine options
python process_orders.py example_orders.json -c my_config.json -o results -v

# Process different input files
python process_orders.py january_orders.json
python process_orders.py february_orders.json
```

## Configuration Files

Use JSON configuration files to customize behavior:

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

## Development

This project follows Python best practices:

- PEP 8 style guidelines
- Comprehensive docstrings
- Type hints for better code documentation
- Modular function design
- Proper error handling and user feedback
- Configuration file support for flexibility

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
