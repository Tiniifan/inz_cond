import json

from pathlib import Path
from PyQt6.QtWidgets import QMessageBox

class FileController:
    """Controller for managing files and templates"""
    
    def __init__(self):
        self.current_file = None
        self.file_memory = {}
        self.templates = {}
        self.playground_data = {}
        self.playground_json = Path.cwd() / "playground.json"
    
    def load_templates(self):
        """Load all .inzcond files from the templates folder"""
        self.templates = {}
        templates_dir = Path.cwd() / "templates"
        
        if templates_dir.exists() and templates_dir.is_dir():
            for file_path in templates_dir.glob("*.inzcond"):
                try:
                    with open(file_path, 'r') as f:
                        base64_content = f.read().strip()
                    self.templates[file_path.name] = {
                        'path': str(file_path),
                        'base64': base64_content
                    }
                except Exception as e:
                    print(f"Error loading template {file_path}: {e}")
        
        return self.templates
    
    def load_or_create_playground_data(self):
        """Load or create the playground.json file"""
        default_data = {
            "LANGUAGE": "C",
            "SUB_PHASE_VALUE": 0,
            "PHASE_VALUE": 0,
            "CHAPTER_VALUE": 0,
            "FRAME_CHAPTER_VALUE": 0,
            "SHOP_OPEN_VALUE": False,
            "TEMP_BIT_FLAG": {},
            "TEMP_MAP_BIT_FLAG": {},
            "GLOBAL_BIT_FLAG": {},
            "GLOBAL_T_BOX_FLAG": {},
            "HAVE_ITEM": []
        }
        
        if not self.playground_json.exists():
            with open(self.playground_json, 'w') as f:
                json.dump(default_data, f, indent=4)
            self.playground_data = default_data
        else:
            try:
                with open(self.playground_json, 'r') as f:
                    self.playground_data = json.load(f)
                
                # Check and add any missing keys
                updated = False
                for key, default_value in default_data.items():
                    if key not in self.playground_data:
                        self.playground_data[key] = default_value
                        updated = True
                
                # Save only if changes have been made
                if updated:
                    with open(self.playground_json, 'w') as f:
                        json.dump(self.playground_data, f, indent=4)
                        
            except Exception:
                self.playground_data = default_data
        
        return self.playground_data
    
    def save_playground_data(self, data):
        """Save the playground.json file"""
        try:
            self.playground_data = data
            with open(self.playground_json, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            return False, str(e)

    def save_language(self, language):
        """Save the current language to playground.json"""
        try:
            self.playground_data["LANGUAGE"] = language
            with open(self.playground_json, 'w') as f:
                json.dump(self.playground_data, f, indent=4)
            return True
        except Exception as e:
            return False, str(e)

    def get_saved_language(self):
        """Get the saved language from playground.json"""
        return self.playground_data.get("LANGUAGE", "C")
    
    def is_playground(self, file_path):
        """Check if it's the playground file"""
        return Path(file_path).name == "playground.inzcond"
    
    def save_to_memory(self, file_path, code):
        """Saves the code in memory"""
        self.file_memory[file_path] = code
    
    def load_from_memory(self, file_path):
        """Load the code from memory"""
        return self.file_memory.get(file_path)
    
    def load_file_content(self, file_path):
        """Loads the contents of a file from disk"""
        try:
            file_path_obj = Path(file_path)
            if file_path_obj.exists():
                with open(file_path, 'r') as f:
                    return f.read().strip()
            return ""
        except Exception as e:
            return None, str(e)
    
    def save_file_content(self, file_path, content):
        """Saves the content to a file"""
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            return False, str(e)