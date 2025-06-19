import os
import shutil
import yaml
import re
import secrets
from pathlib import Path
from typing import Dict, Any

def create_config(dist_folder: str = "dist") -> None:
    """
    Create configuration files by copying configs folder and replacing variables.
    
    Args:
        dist_folder: Destination folder for the configuration files
    """
    # Ensure dist folder exists
    dist_path = Path(dist_folder)
    dist_path.mkdir(exist_ok=True)
    
    # Copy configs folder to dist
    configs_source = Path("./configs")
    configs_dest = dist_path / "configs"
    
    if configs_source.exists():
        if configs_dest.exists():
            shutil.rmtree(configs_dest)
        shutil.copytree(configs_source, configs_dest)
    else:
        raise FileNotFoundError("./configs folder not found")
    
    # Read env.yml
    env_file = Path("./env.yml")
    if not env_file.exists():
        raise FileNotFoundError("./env.yml file not found")
    
    with open(env_file, 'r') as f:
        env_config = yaml.safe_load(f)
    
    # Extract variables and their values
    variables = _extract_variables(env_config)
    
    # Process each variable and update files
    for var_name, var_config in variables.items():
        value = var_config.get('value', var_config.get('default', ''))
        used_files = var_config.get('used_files', [])
        
        for file_path in used_files:
            _replace_variable_in_file(configs_dest, file_path, var_name, value)

def _generate_value(generator_type: str) -> str:
    """
    Generate a random value based on the generator type.
    
    Args:
        generator_type: Type of generator (RAND_HEX_64, RAND_HEX_32, etc.)
        
    Returns:
        Generated random string
    """
    if generator_type == "RAND_HEX_64":
        return secrets.token_hex(64)
    elif generator_type == "RAND_HEX_32":
        return secrets.token_hex(32)
    elif generator_type == "RAND_HEX_16":
        return secrets.token_hex(16)
    elif generator_type == "RAND_HEX_10":
        return secrets.token_hex(10)
    else:
        raise ValueError(f"Unknown generator type: {generator_type}")

def _extract_variables(env_config: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Extract variables from env.yml configuration.
    
    Args:
        env_config: Parsed env.yml configuration
        
    Returns:
        Dictionary of variable configurations
    """
    variables = {}
    
    if 'vars' in env_config:
        for var in env_config['vars']:
            var_name = var.get('name')
            if var_name:
                # Check for environment variable override
                env_value = os.environ.get(var_name)
                var_config = var.copy()
                
                if env_value is not None:
                    var_config['value'] = env_value
                elif 'value' not in var_config and 'generator' in var_config:
                    # Generate value if no value exists but generator is specified
                    generator_type = var_config['generator']
                    try:
                        var_config['value'] = _generate_value(generator_type)
                        print(f"Generated value for {var_name} using {generator_type}")
                    except ValueError as e:
                        print(f"Warning: {e} for variable {var_name}")
                        
                variables[var_name] = var_config
    
    return variables

def _replace_variable_in_file(configs_path: Path, file_path: str, var_name: str, value: str) -> None:
    """
    Replace variable in a specific file under dist/configs.
    """
    # resolve path inside dist/configs
    rel_path = file_path.lstrip('/')
    if rel_path.startswith('configs/'):
        rel_path = rel_path[len('configs/'):]
    full_file = configs_path / rel_path
    if not full_file.exists():
        print(f"Warning: cannot find {file_path} for variable {var_name}, skipping")
        return

    try:
        text = full_file.read_text()
        # replace occurrences of VAR, ${VAR} and $(VAR)
        patterns = [rf'\b{var_name}\b', rf'\${{{var_name}}}', rf'\$\({var_name}\)']
        for p in patterns:
            text = re.sub(p, str(value), text)
        full_file.write_text(text)
    except Exception as e:
        print(f"Error processing {full_file}: {e}")

if __name__ == "__main__":
    create_config()