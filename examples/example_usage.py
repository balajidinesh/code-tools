#!/usr/bin/env python3
"""
Example usage of the CodeInstance class with both Docker and Local deployments.
"""

import asyncio
from codetools import CodeInstance

async def example_docker_usage():
    """Example using Docker deployment"""
    print("=== Docker Deployment Example ===")
    
    config = {
        'docker': {
            'image': 'python:3.12',
            # Add any other docker parameters as needed
        },
        'tool_config': {
            # Tool-specific configuration
        }
    }
    
    try:
        # Using async context manager (recommended)
        async with CodeInstance('docker', config) as instance:
            print(f"Started CodeInstance with {instance.get_deployment_type()} deployment")
            print(f"Running: {instance.is_running()}")
            
            # Get available tools
            tools = instance.get_available_tools()
            print(f"Available tools: {len(tools)}")
            print(f"First 5 tools: {tools[:5]}")
            
            # Get wrapped tools
            wrapped_tools = instance.get_tools(include=['read_file', 'write_file', 'list_directory'])
            print(f"Wrapped tools: {len(wrapped_tools)}")
            
            # Get tool usage statistics
            stats = instance.get_usage_summary()
            print(f"Tool usage stats: {stats}")

            await instance.cleanup()
            
    except Exception as e:
        print(f"Error with Docker deployment: {e}")

async def example_local_usage():
    """Example using Local deployment"""
    print("\n=== Local Deployment Example ===")
    
    config = {
        'local': {
            # Local deployment configuration
        },
        'tool_config': {
            # Tool-specific configuration
        }
    }
    
    try:
        # Manual lifecycle management
        instance = CodeInstance('local', config)
        await instance.start()
        
        try:
            print(f"Started CodeInstance with {instance.get_deployment_type()} deployment")
            print(f"Running: {instance.is_running()}")
            
            # Get deployment info
            info = instance.get_deployment_info()
            print(f"Deployment info: {info}")
            
            # Get all available tools
            all_tools = instance.get_tools()
            print(f"All wrapped tools: {len(all_tools)}")
            
        finally:
            await instance.cleanup()
            print(f"Cleaned up. Running: {instance.is_running()}")
            
    except Exception as e:
        print(f"Error with Local deployment: {e}")

async def main():
    """Main function to run examples"""
    print("CodeInstance Examples")
    print("====================")
    
    # Try local deployment first (more likely to work without Docker)
    # await example_local_usage()
    
    # Try docker deployment (requires Docker to be installed and running)
    await example_docker_usage()

if __name__ == "__main__":
    asyncio.run(main())