import os
import uuid
from dotenv import load_dotenv
from memos import MOS, MOSConfig

# --- Setup ---
# This script requires your Deepseek API key in a .env file in this directory.
# DEEPSEEK_API_KEY="your_api_key_here"
load_dotenv()

# This makes the script's path handling more robust.
# It builds an absolute path to the config files from the script's own location,
# so it works whether you run it from the 'app/' folder or the project root.
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))
config_path = os.path.join(project_root, "examples/data/config/simple_memos_config.json")


# This example also requires configuration files from the MemOS examples.
# As per the README, run `memos download_examples` in your project root first.
# This will create an 'examples/' directory at the root of the project.
if not os.path.exists(config_path):
    print(f"Error: Config file not found at '{config_path}'")
    print("\nPlease run 'memos download_examples' from your project root directory first.")
    exit()

# --- Lesson 1: Using the MOS object ---

# Let's walk through the core components from the Quick Start guide.
# 1. The MOSConfig object loads the agent's configuration.
print("1. Loading configuration...")
mos_config = MOSConfig.from_json_file(config_path)

# 2. The MOS (Memory Operating System) object is the main entry point.
mos = MOS(mos_config)

# 3. In MemOS, every piece of information belongs to a user.
user_id = str(uuid.uuid4())
print(f"2. Creating a new user with ID: {user_id}")
mos.create_user(user_id=user_id)

# 4. A MemCube is a user's dedicated memory space. We need to register one.
mem_cube_path = os.path.join(project_root, "examples/data/mem_cube_2")
print(f"3. Registering a memory cube for the user from '{mem_cube_path}'...")
mos.register_mem_cube(mem_cube_path, user_id=user_id)

# 5. Now, let's add a memory. The .add() method takes a list of messages.
print("4. Adding a memory: 'User loves playing football.'")
mos.add(
    messages=[
        {"role": "user", "content": "I love playing football."},
        {"role": "assistant", "content": "That's awesome! I'll remember that."}
    ],
    user_id=user_id
)

# 6. Finally, let's retrieve the memory with a search query.
print("5. Searching memory with the query: 'What does the user love?'")
result = mos.search(
  query="What does the user love?",
  user_id=user_id
)

print("\n--- Search Result ---")
print("Memories found:", result["text_mem"])
print("\nLesson complete! We successfully stored and retrieved a memory.") 