# use this file to create a agent to give tools and create 
# read write run command and test scirpt simple test scrip ask it to create something 

from dotenv import load_dotenv
from swarms import Agent
from swarms.structs import Conversation
from codetools import CodeInstance

load_dotenv() 

conv = Conversation(
    name="coding_agent_chat",
    time_enabled=True,
    save_enabled=True,
    save_filepath="coding_agent_chat.json",
    save_as_json_bool=True,
    conversations_dir='agent_workspace',
)

def create_coding_agent_with_tools():
    """Create a coding agent with read, write, and run_command tools using Docker"""
    print("=== Setting up Coding Agent with Docker Tools ===")
    
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
        # Create CodeInstance with auto_start=True to immediately get tools
        instance = CodeInstance('docker', config, auto_start=True)
        print(f"Started CodeInstance with {instance.get_deployment_type()} deployment")
        print(f"Running: {instance.is_running()}")
        
        # Get the three main tools: read, write, run_command
        tools = instance.get_tools(include=['read_file', 'write_file', 'run_command'])
        print(f"Retrieved {len(tools)} tools for the agent")
        
        # Create the coding agent with tools
        coding_agent = Agent(
            agent_name="CodingAgent",
            system_prompt="""You are a helpful coding agent with access to file operations and command execution in a Docker container.
            You can:
            1. Read files to understand code structure
            2. Write/modify files to implement features
            3. Run commands to test and execute code
            
            You are running in a Python 3.12 Docker container environment.
            Always be careful with file operations and command execution. 
            Explain what you're doing before taking actions.""",
            model_name="gemini/gemini-2.0-flash",
            max_loops=3,
            max_tokens=4096,
            temperature=0.3,
            output_type="str",
            tools=tools
        )
        
        coding_agent.short_memory = conv
        
        # Example tasks for the agent
        tasks = [
            "Create a simple Python script called 'hello_world.py' that prints 'Hello, World!' and then run it",
            # "Read the contents of the file you just created",
            # "Modify the script to also print the current date and time, then run it again"
        ]
        
        print("\n=== Running Coding Agent Tasks ===")
        for i, task in enumerate(tasks, 1):
            print(f"\nTask {i}: {task}")
            print("-" * 50)
            response = coding_agent.run(task)
            print(f"Agent Response: {response}")
            print("-" * 50)
        
        # Save conversation
        conv.save_as_json(filename="agent_workspace/coding_agent_chat.json")
        print("\nConversation saved!")
        
        # Clean up when done (optional - will also be cleaned up automatically on exit)
        print("\n=== Cleaning up CodeInstance ===")
        instance.stop_sync()
        print("CodeInstance stopped successfully")
        
        return coding_agent, instance
        
    except Exception as e:
        print(f"Error setting up coding agent: {e}")
        return None, None

def main():
    """Main function to demonstrate agent with coding tools in Docker"""
    print("Coding Agent with Docker Environment Example")
    print("===========================================")
    
    agent, instance = create_coding_agent_with_tools()
    
    if agent:
        print("\n=== Final Conversation History ===")
        print(conv.return_history_as_string())
        
        # Demonstrate that the instance can be reused or shared
        print(f"\n=== Instance Info ===")
        print(f"Deployment type: {instance.get_deployment_type()}")
        print(f"Instance running: {instance.is_running()}")
        print(f"Available tools: {instance.get_available_tools()}")

if __name__ == "__main__":
    main()