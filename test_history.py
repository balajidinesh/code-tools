#!/usr/bin/env python3
"""
Test script to demonstrate the new history tracking functionality in CodeInstance
"""

from codetools import CodeInstance

def test_history_functionality():
    """Test the new get_history() and print_history() functions"""
    print("=== Testing CodeInstance History Functionality ===")
    
    config = {
        'docker': {
            'image': 'python:3.12',
        },
        'tool_config': {}
    }
    
    try:
        # Create CodeInstance with auto_start=True
        instance = CodeInstance('docker', config, auto_start=True)
        print(f"Started CodeInstance with {instance.get_deployment_type()} deployment")
        print(f"Running: {instance.is_running()}")
        
        # Get some tools to test with
        tools = instance.get_tools(include=['write_file', 'read_file', 'list_directory'])
        print(f"Retrieved {len(tools)} tools for testing")
        
        # Execute some tool calls to generate history
        print("\n=== Executing Tool Calls ===")
        
        # Test 1: Write a file
        print("1. Writing a test file...")
        write_tool = tools[0]  # write_file
        result1 = write_tool(path="/tmp/test.txt", content="Hello, World!\nThis is a test file.")
        print(f"Write result: {result1}")
        
        # Test 2: Read the file back
        print("\n2. Reading the test file...")
        read_tool = tools[1]  # read_file  
        result2 = read_tool(path="/tmp/test.txt")
        print(f"Read result: {result2}")
        
        # Test 3: List directory
        print("\n3. Listing directory...")
        list_tool = tools[2]  # list_directory
        result3 = list_tool(path="/tmp")
        print(f"List result: {result3}")
        
        # Test 4: Try to read a non-existent file (should fail)
        print("\n4. Trying to read non-existent file...")
        try:
            result4 = read_tool(path="/tmp/nonexistent.txt")
            print(f"Unexpected success: {result4}")
        except Exception as e:
            print(f"Expected error: {e}")
        
        # Test the new history functionality
        print("\n=== Testing History Functions ===")
        
        # Get history
        history = instance.get_history()
        print(f"\nHistory contains {len(history)} tool calls")
        
        # Print history using the new print_history function
        instance.print_history()
        
        # Also demonstrate accessing history data programmatically
        print("\n=== Programmatic History Access ===")
        for i, call in enumerate(history, 1):
            print(f"{i}. {call['tool_name']} - Success: {call['success']} - Duration: {call['duration']:.3f}s")
        
        # Clean up
        print("\n=== Cleaning up ===")
        instance.stop_sync()
        print("CodeInstance stopped successfully")
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_history_functionality()