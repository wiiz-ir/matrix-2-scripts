import subprocess
import shutil
import os
import tempfile
from pathlib import Path


def get_element(input_path: str) -> None:
    """
    Download/setup Element web client and copy configuration file.
    
    Args:
        input_path: Target directory path (e.g., 'chat_server/element/www')
    """
    target_path = Path(input_path)
    config_source = Path("src/statics/config.json")
    
    # Verify the source config file exists
    if not config_source.exists():
        raise FileNotFoundError(f"Config file not found: {config_source}")
    
    # Create target directory if it doesn't exist
    target_path.mkdir(parents=True, exist_ok=True)
    
    # Create temporary file for download
    with tempfile.NamedTemporaryFile(suffix='.tar.gz', delete=False) as temp_file:
        temp_archive_path = temp_file.name
    
    try:
        # Download Element web client (using specific version)
        # Using Element v1.11.104
        element_url = "https://github.com/element-hq/element-web/releases/download/v1.11.104/element-v1.11.104.tar.gz"
        
        # Download Element
        print(f"Downloading Element web client v1.11.104 to {target_path}")
        download_result = subprocess.run(
            ["wget", "-O", temp_archive_path, element_url],
            check=True,
            capture_output=True,
            text=True
        )
        
        # Extract the archive
        print("Extracting Element...")
        extract_result = subprocess.run(
            ["tar", "-xzf", temp_archive_path, "-C", str(target_path), "--strip-components=1"],
            check=True,
            capture_output=True,
            text=True
        )
        
        # Copy config.json to the target directory
        config_target = target_path / "config.json"
        shutil.copy2(config_source, config_target)
        
        print(f"Successfully setup Element in {input_path}")
        print(f"Copied config.json to {config_target}")
        
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to download/extract Element: {e.stderr if e.stderr else str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error setting up Element: {e}")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_archive_path):
            os.unlink(temp_archive_path)


if __name__ == "__main__":
    # Example usage
    get_element("chat_server/element/www")
