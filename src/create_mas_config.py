import subprocess
import tempfile
import yaml
import os
from pathlib import Path


def create_mas_config(merge_file_input: str) -> None:
    """
    Generate a new MAS config using Docker and merge the secrets section
    with the existing config file.
    
    Args:
        merge_file_input: Path to the existing config file (e.g., chat_server/mas/config.yaml)
    """
    # Convert to Path object for easier handling
    merge_file_path = Path(merge_file_input)
    
    # Verify the merge file exists
    if not merge_file_path.exists():
        raise FileNotFoundError(f"Merge file not found: {merge_file_input}")
    
    # Create a temporary file for the generated config
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.yaml', delete=False) as temp_file:
        temp_config_path = temp_file.name
    
    try:
        # Run the Docker command to generate config
        docker_command = [
            "docker", "run", 
            "ghcr.io/element-hq/matrix-authentication-service", 
            "config", "generate"
        ]
        
        with open(temp_config_path, 'w') as temp_file:
            result = subprocess.run(
                docker_command, 
                stdout=temp_file, 
                stderr=subprocess.PIPE, 
                text=True, 
                check=True
            )
        
        # Read the generated config
        with open(temp_config_path, 'r') as temp_file:
            generated_config = yaml.safe_load(temp_file)
        
        # Read the existing config
        with open(merge_file_path, 'r') as existing_file:
            existing_config = yaml.safe_load(existing_file)
        
        # Extract secrets from generated config and merge
        if 'secrets' in generated_config:
            existing_config['secrets'] = generated_config['secrets']
        else:
            raise ValueError("Generated config does not contain 'secrets' section")
        
        # Write the updated config back to the original file with proper formatting
        with open(merge_file_path, 'w') as output_file:
            yaml.dump(existing_config, output_file, 
                     default_flow_style=False, 
                     indent=2,
                     allow_unicode=True,
                     default_style='|' if '\n' in str(existing_config.get('secrets', {}).get('keys', [])) else None)
        
        print(f"Successfully updated secrets in {merge_file_input}")
        
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Docker command failed: {e.stderr}")
    except yaml.YAMLError as e:
        raise RuntimeError(f"YAML parsing error: {e}")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_config_path):
            os.unlink(temp_config_path)


if __name__ == "__main__":
    # Example usage
    create_mas_config("chat_server/mas/config.yaml")
