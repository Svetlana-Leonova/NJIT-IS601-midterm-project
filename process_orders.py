#!/usr/bin/env python3
"""
Order Processing Script

This script reads JSON orders from a file and generates two output files:
1. customers.json - Maps phone numbers to customer names
2. items.json - Maps menu item names to their price and calculates the number of times each item has been ordered

Usage:
    linux/windows:
        python process_orders.py <example_orders.json>
    macOS:
        python3 process_orders.py <example_orders.json>

"""

import json
import sys
import re
from collections import defaultdict
from typing import Dict, Any, List

# Compile regex pattern once for better performance
PHONE_PATTERN = re.compile(r'^\d{3}-\d{3}-\d{4}$')


def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format.

    Args:
        phone: Phone number string to validate

    Returns:
        True if phone number is in correct format (xxx-xxx-xxxx), False otherwise
    """
    return bool(PHONE_PATTERN.match(phone.strip()))


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


def process_customers(orders: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Process orders to create a mapping of phone numbers to customer names.

    Args:
        orders: List of order dictionaries

    Returns:
        Dictionary mapping phone numbers to customer names
    """
    customers = {}

    for order in orders:
        phone = order.get('phone', '').strip()
        name = order.get('name', '').strip()

        # Validate phone number format (xxx-xxx-xxxx) using regex
        if phone and name and validate_phone_number(phone):
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


def save_json(data: Dict[str, Any], filename: str) -> None:
    """
    Save data to a JSON file with proper formatting.

    Args:
        data: Dictionary to save
        filename: Output filename
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False, sort_keys=True)
        print(f"Successfully created {filename}")
    except (IOError, OSError) as e:
        print(f"Error writing to {filename}: {e}")
        sys.exit(1)


def main():
    """
    Main function to process orders and generate output files.
    """
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Error: process_orders.py requires exactly one argument")
        print("Usage (linux/windows): python process_orders.py <example_orders.json>")
        print("Usage (macOS): python3 process_orders.py <example_orders.json>")
        sys.exit(1)

    # store the orders file name from the command line argument
    orders_file = sys.argv[1]

    print(f"Processing orders from: {orders_file}")

    # Load orders
    orders = load_orders(orders_file)
    print(f"Loaded {len(orders)} orders")

    # Process customers
    customers = process_customers(orders)
    print(f"Found {len(customers)} unique customers")

    # Process items
    items = process_items(orders)
    print(f"Found {len(items)} unique items")

    # Save output files
    save_json(customers, 'customers.json')
    save_json(items, 'items.json')

    print("Processing complete!")

# When a Python file is run directly, __name__ is set to "__main__"
if __name__ == "__main__":
    main()
