from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # Azure AD Configuration
    TENANT_ID: str = "common"
    CLIENT_ID: str
    CLIENT_SECRET: str
    REDIRECT_URI: str = "http://localhost:8000/auth/callback"
    
    # MCP Server Configuration
    MCP_SERVER_NAME: str = "OneDrive MCP Server"
    MCP_PORT: int = 8000
    
    # Allowed Paths Configuration
    ALLOWED_PATHS_FILE: str = "allowed_paths.txt"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Load allowed paths
def load_allowed_paths():
    paths = []
    if os.path.exists(settings.ALLOWED_PATHS_FILE):
        with open(settings.ALLOWED_PATHS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Normalize paths to start with /
                    if not line.startswith('/'):
                        line = '/' + line
                    paths.append(line)
    return paths

ALLOWED_PATHS = load_allowed_paths()