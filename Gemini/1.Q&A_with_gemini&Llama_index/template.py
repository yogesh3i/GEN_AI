from pathlib import Path

list_of_files = [
    "QAWithPDF/__init__.py",
    "QAWithPDF/data_ingestion.py",
    "QAWithPDF/embedding.py",
    "QAWithPDF/model_api.py",
    "Experiments/experiment.ipynb",
    "StreamlitApp.py",
    "logger.py",
    "exception.py",
    "setup.py"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    
    # Create parent directories if they do not exist
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    # Create an empty file if it does not exist
    filepath.touch(exist_ok=True)
    
print("Project structure created successfully! ✅")
