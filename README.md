# code-tools

A powerful framework for providing tools to AI agents with Docker/local deployment support.

CodeInstance is a class that wraps deployment environments (Docker/local) and provides various code tools to AI agents including file operations, bash sessions, search capabilities, and more.


## Installation

You can install the package using pip:

```bash
pip install code-tools-agent
```

Or for development:

```bash
pip install -e .
```

## Quick Start

```python
from codetools import CodeInstance

# Create instance with Docker environment
config = {
    'docker': {
        'image': 'python:3.12',
    },
    'tool_config': {}
}

# Create and start the instance
instance = CodeInstance('docker', config, auto_start=True)

# Get specific tools for your agent
tools = instance.get_tools(include=['read_file', 'write_file', 'run_command'])

# Use with your AI agent framework (e.g., Swarms)
from swarms import Agent

agent = Agent(
    agent_name="CodingAgent",
    system_prompt="You are a helpful coding assistant with file and command tools.",
    tools=tools
)

# Clean up when done
instance.stop_sync()
```

## Available Tools

The CodeInstance provides access to these tools:

- **File Operations**: `read_file`, `write_file`, `edit_file`
- **Directory Operations**: `list_directory`
- **Command Execution**: `run_command`, `run_bash_session`, `create_bash_session`
- **Code Analysis**: `format_code`, `analyze_project_structure`, `get_file_dependencies`
- **Search Operations**: `glob_files`, `grep_files`, `find_references`

## Usage Examples

### Basic Usage (Async)

```python
import asyncio
from codetools import CodeInstance

async def example_usage():
    config = {
        'docker': {'image': 'python:3.12'},
        'tool_config': {}
    }
    
    # Using async context manager (recommended)
    async with CodeInstance('docker', config) as instance:
        print(f"Started CodeInstance with {instance.get_deployment_type()} deployment")
        
        # Get available tools
        tools = instance.get_available_tools()
        print(f"Available tools: {len(tools)}")
        
        # Get wrapped tools for your agent
        wrapped_tools = instance.get_tools(include=['read_file', 'write_file', 'list_directory'])
        print(f"Wrapped tools: {len(wrapped_tools)}")

asyncio.run(example_usage())
```

### Agent Integration Example

```python
from dotenv import load_dotenv
from swarms import Agent
from swarms.structs import Conversation
from codetools import CodeInstance

load_dotenv()

def create_coding_agent_with_tools():
    """Create a coding agent with read, write, and run_command tools using Docker"""
    
    config = {
        'docker': {
            'image': 'python:3.12',
        },
        'tool_config': {}
    }
    
    # Create CodeInstance with auto_start=True to immediately get tools
    instance = CodeInstance('docker', config, auto_start=True)
    
    # Get the three main tools: read, write, run_command
    tools = instance.get_tools(include=['read_file', 'write_file', 'run_command'])
    
    # Create the coding agent with tools
    coding_agent = Agent(
        agent_name="CodingAgent",
        system_prompt="""You are a helpful coding agent with access to file operations and command execution in a Docker container.
        You can:
        1. Read files to understand code structure
        2. Write/modify files to implement features
        3. Run commands to test and execute code
        
        You are running in a Python 3.12 Docker container environment.
        Always be careful with file operations and command execution.""",
        model_name="gemini/gemini-2.0-flash",
        max_loops=3,
        max_tokens=4096,
        temperature=0.3,
        output_type="str",
        tools=tools
    )
    
    return coding_agent, instance

# Create and use the agent
agent, instance = create_coding_agent_with_tools()

# Run a task
response = agent.run("Create a simple Python script called 'hello_world.py' that prints 'Hello, World!' and then run it")
print(response)

# Clean up
instance.stop_sync()
```

## Features

- **Docker & Local Deployment**: Run tools in isolated Docker containers or local environment
- **Tool Statistics**: Track tool usage and performance metrics
- **Async Support**: Full async/await support with context managers
- **Safety Features**: Read-before-write protection for file operations
- **Agent Integration**: Works seamlessly with AI agent frameworks like Swarms
- **Comprehensive Tools**: 14+ built-in tools for file operations, command execution, and code analysis

## Requirements

- Python 3.10+
- Docker (for Docker deployment)
- Dependencies: swarms, swerex

## Development

### Code Quality 🧹

- `make style` to format the code
- `make check_code_quality` to check code quality (PEP8 basically)
- `black .`
- `ruff . --fix`

### Tests 🧪

[`pytests`](https://docs.pytest.org/en/7.1.x/) is used to run our tests.

### Publishing 🚀

```bash
poetry build
poetry publish
```

## License

MIT
