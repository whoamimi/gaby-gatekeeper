# core/config.py
"""
Configuration management for agent workflows.
Minimal, clean, Pydantic-based.
"""

from pathlib import Path
from typing import Optional, Literal
import os

from pydantic import BaseSettings, validator
import yaml

load_dotenv = lambda: __import__('dotenv').load_dotenv('.env.local')
load_dotenv()

class Settings(BaseSettings):
    """All environment-based settings."""
    
    # Local endpoints
    lightning_ollama_url: str = ""
    local_ollama_url: str = ""
    agent_sandbox_url: str = ""
    
    # BigQuery
    bq_model_connection: Optional[str] = None
    bq_model_endpoint: Optional[str] = None
    bq_model_id: Optional[str] = None
    bq_project_id: Optional[str] = None
    bq_dataset_id: str = "cleaning_service"
    bq_table_id: str = "sample_dataset"
    bq_model_type: str = "gemini-2.5-flash"
    
    # Debug
    debug: bool = False
    
    class Config:
        env_file = '.env.local'
        case_sensitive = False
    
    @validator('bq_model_*', pre=True, always=True)
    def validate_bq_config(cls, v, values):
        """Ensure BQ config is complete if any field is set."""
        bq_fields = ['bq_model_connection', 'bq_model_endpoint', 'bq_model_id']
        if any(values.get(f) for f in bq_fields if f in values):
            if not all(values.get(f) for f in bq_fields):
                raise ValueError("BigQuery config incomplete. Set all: connection, endpoint, model_id")
        return v


# Global settings instance
settings = Settings()

class LocalConfig(BaseSettings):
    """Local server connections."""
    
    lightning_ollama: str = settings.lightning_ollama_url
    local_ollama: str = settings.local_ollama_url
    agent_sandbox: str = settings.agent_sandbox_url
    
    @property
    def model_stack(self) -> dict:
        """Load model config from YAML."""
        try:
            with open("config_models.yaml") as f:
                return {m['model_name']: m for m in yaml.safe_load(f)}
        except FileNotFoundError:
            return {}
    
    def get_model(self, name: str) -> Optional[dict]:
        """Get model config by name."""
        return self.model_stack.get(name)


class EpisodeConfig(BaseSettings):
    """Runtime episode configuration."""
    
    input_id: str
    bq_connection: str = settings.bq_model_connection or ""
    bq_endpoint: str = settings.bq_model_endpoint or ""
    bq_model_id: str = settings.bq_model_id or ""
    project_id: str = settings.bq_project_id or ""
    dataset_id: str = settings.bq_dataset_id
    table_id: str = settings.bq_table_id
    
    @property
    def action_table(self) -> str:
        """Fully qualified action table name."""
        return f"{self.project_id}.{self.dataset_id}.{self.input_id}_cognitive"
    
    @property
    def observation_table(self) -> str:
        """Fully qualified observation table name."""
        return f"{self.project_id}.{self.dataset_id}.{self.input_id}_observations"

def setup_workspace(root: str = 'gaby') -> None:
    """Change working directory to project root."""
    current = Path.cwd()
    
    if current.stem == root:
        print(f'✓ Already at {root}')
        return
    
    for parent in [current, *current.parents]:
        if parent.name == root:
            os.chdir(parent)
            print(f'📂 Working directory: {parent}')
            return
    
    raise FileNotFoundError(f"Root '{root}' not found")

__all__ = ['settings', 'LocalConfig', 'EpisodeConfig', 'setup_workspace']


if __name__ == "__main__":
    local = LocalConfig()
    print(local.get_model('base'))
    episode = EpisodeConfig(input_id="test_run")
    print(episode.action_table)
