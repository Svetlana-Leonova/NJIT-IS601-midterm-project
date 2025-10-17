# Order Processing System

A Python script that processes JSON order data and generates customer and item analytics files.

## Overview

This project processes restaurant order data from a JSON file and generates two output files:

- `customers.json`: Maps phone numbers to customer names
- `items.json`: Maps item names to pricing and order frequency data

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

- `process_orders()`: Safely loads and validates JSON input
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
python process_orders.py <orders_file.json>
```

MacOS(Unix):

```bash
python3 process_orders.py <orders_file.json>
```

### Example

```bash
python process_orders.py example_orders.json
```

This will generate:

- `customers.json`: Customer phone number to name mapping
- `items.json`: Item analytics with pricing and order counts

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

## Testing

The script has been tested with the provided `example_orders.json` file, which contains 10,000 orders from 30 unique customers and 19 unique menu items.
