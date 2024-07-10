from pydantic import BaseModel
from pathlib import Path
import json

# Set the path for the log file
root = Path(__file__).parent
LOG_FILE_PATH = root / "conversations.json"

class Conversation(BaseModel):
    messages: list[dict] = []

    def add_message(self, message: str, role: str):
        """Add a message to the conversation."""
        entry = {"role": role, "content": message}
        self.messages.append(entry)

class Settings(BaseModel):
    conversations: dict[str, Conversation] = {}

def get_conversations() -> Settings:
    """Retrieve all conversations, returns a new settings instance if the file does not exist."""
    if not LOG_FILE_PATH.exists():
        return Settings()
    try:
        setting = Settings.model_validate_json(LOG_FILE_PATH.read_text())
        return setting
    except json.JSONDecodeError:
        print("Error decoding JSON")
        return Settings()

def save_conversations(setting: Settings):
    """Save the current settings to a file."""
    try:
        dump = setting.model_dump()
        read_dump = json.dumps(dump, indent=4)
        LOG_FILE_PATH.write_text(read_dump)
    except IOError as e:
        print(f"Error writing to file: {e}")


