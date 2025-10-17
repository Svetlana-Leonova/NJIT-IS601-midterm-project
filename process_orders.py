#!/usr/bin/env python3
"""
Order Processing Script

This script reads JSON orders from a file and generates two output files:
1. customers.json - Maps phone numbers to customer names
2. items.json - Maps menu item names to their price and calculates the number of times each item has been ordered

Usage:
    python3 process_orders.py <input_file.json> [config_file.json]

The input file is required as a command-line argument.
If no config file is provided, it will look for 'config.json' in the current directory.
"""

import json
import sys
import re
from collections import defaultdict
from typing import Dict, Any, List, Optional


def load_config(config_file: str = "config.json") -> Dict[str, Any]:
    """
    Load configuration from a JSON file.

    Args:
        config_file: Path to the configuration file

    Returns:
        Dictionary containing configuration settings

    Raises:
        FileNotFoundError: If the config file doesn't exist
        json.JSONDecodeError: If the config file contains invalid JSON
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            config = json.load(file)

        # Validate required configuration keys (excluding input_file since it comes from command line)
        required_keys = ['output_customers', 'output_items']
        missing_keys = [key for key in required_keys if key not in config]

        if missing_keys:
            print(f"Error: Missing required configuration keys: {missing_keys}")
            sys.exit(1)

        return config

    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        print("Please create a config.json file or specify a different config file.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config file '{config_file}': {e}")
        sys.exit(1)


def load_orders(filename: str) -> List[Dict[str, Any]]:
    """
    Load orders from a JSON file.

    Args:
        filename: Path to the JSON file containing orders

    Returns:
        List of order dictionaries

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{filename}': {e}")
        sys.exit(1)


def validate_phone_number(phone: str, pattern: re.Pattern) -> bool:
    """
    Validate phone number format.

    Args:
        phone: Phone number string to validate
        pattern: Compiled regex pattern for validation

    Returns:
        True if phone number is in correct format, False otherwise
    """
    return bool(pattern.match(phone.strip()))


def process_customers(orders: List[Dict[str, Any]], phone_pattern: re.Pattern) -> Dict[str, str]:
    """
    Process orders to create a mapping of phone numbers to customer names.

    Args:
        orders: List of order dictionaries
        phone_pattern: Compiled regex pattern for phone validation

    Returns:
        Dictionary mapping phone numbers to customer names
    """
    customers = {}

    for order in orders:
        phone = order.get('phone', '').strip()
        name = order.get('name', '').strip()

        # Validate phone number format using configurable pattern
        if phone and name and validate_phone_number(phone, phone_pattern):
            # Only add the phone number if it is not already in the dictionary
            if phone not in customers:
                customers[phone] = name

    return customers


def process_items(orders: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Process orders to create a mapping of menu item names to price and order count.

    Args:
        orders: List of order dictionaries

    Returns:
        Dictionary mapping item names to price and order count
    """
    items = defaultdict(lambda: {'price': 0.0, 'orders': 0})

    for order in orders:
        order_items = order.get('items', [])

        for item in order_items:
            item_name = item.get('name', '').strip()
            item_price = item.get('price', 0.0)

            if item_name:
                # Set price (assuming all items of the same name have the same price)
                if items[item_name]['price'] == 0.0:
                    items[item_name]['price'] = item_price

                # Increment order count
                items[item_name]['orders'] += 1

    return dict(items)


def save_json(data: Dict[str, Any], filename: str, config: Dict[str, Any]) -> None:
    """
    Save data to a JSON file with configurable formatting.

    Args:
        data: Dictionary to save
        filename: Output filename
        config: Configuration dictionary
    """
    try:
        encoding = config.get('encoding', 'utf-8')
        indent = config.get('indent', 4)
        sort_keys = config.get('sort_output', True)

        with open(filename, 'w', encoding=encoding) as file:
            json.dump(data, file, indent=indent, ensure_ascii=False, sort_keys=sort_keys)
        print(f"Successfully created {filename}")
    except (IOError, OSError) as e:
        print(f"Error writing to {filename}: {e}")
        sys.exit(1)


def main():
    """
    Main function to process orders and generate output files.
    """
    # Check command line arguments
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Error: Invalid number of arguments")
        print("Usage: python3 process_orders.py <input_file.json> [config_file.json]")
        print("")
        print("Examples:")
        print("  python3 process_orders.py example_orders.json")
        print("  python3 process_orders.py example_orders.json my_config.json")
        sys.exit(1)

    # Get input file from command line (required)
    input_file = sys.argv[1]

    # Get config file from command line (optional)
    config_file = sys.argv[2] if len(sys.argv) == 3 else "config.json"

    # Load configuration
    config = load_config(config_file)

    print(f"Using configuration from: {config_file}")
    print(f"Processing orders from: {input_file}")

    # Compile phone pattern from config
    phone_pattern_str = config.get('phone_pattern', r'^\d{3}-\d{3}-\d{4}$')
    phone_pattern = re.compile(phone_pattern_str)

    # Load orders
    orders = load_orders(input_file)
    print(f"Loaded {len(orders)} orders")

    # Process customers
    customers = process_customers(orders, phone_pattern)
    print(f"Found {len(customers)} unique customers")

    # Process items
    items = process_items(orders)
    print(f"Found {len(items)} unique items")

    # Save output files using config
    save_json(customers, config['output_customers'], config)
    save_json(items, config['output_items'], config)

    print("Processing complete!")


if __name__ == "__main__":
    main()
