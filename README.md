# Telsec RAG Assistant

A Retrieval-Augmented Generation (RAG) system designed for querying property management documents including leases, agreements, and procedural documents.

## Table of Contents
- [System Requirements](#system-requirements)
- [Installation Guide](#installation-guide)
  - [macOS Setup](#macos-setup)
  - [Windows Setup](#windows-setup)
- [Adding Documents](#adding-documents)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Core Requirements (Both Platforms)
- **Python 3.9 - 3.11** (Python 3.11 recommended)
- **Ollama** (for local LLM and embeddings)
- **LibreOffice** (for .doc file processing)
- **8GB+ RAM** (recommended for embedding generation)
- **2GB+ free disk space**

### Supported Document Types
- PDF files (`.pdf`)
- Word documents (`.docx`, `.doc`)

## Installation Guide

### macOS Setup

#### 1. Install Prerequisites

**Install Python 3.11:**
```bash
# Using Homebrew (recommended)
brew install python@3.11

# Or download from https://www.python.org/downloads/
```

**Install Ollama:**
```bash
# Using Homebrew
brew install ollama

# Or download from https://ollama.ai
```

**Install LibreOffice:**
```bash
# Using Homebrew
brew install libreoffice

# Or download from https://www.libreoffice.org/
```

#### 2. Clone and Setup Project

```bash
# Clone the repository
git clone https://github.com/[your-username]/Telsec_RAG.git
cd Telsec_RAG

# Run automated setup
chmod +x setup.sh
./setup.sh
```

#### 3. Install Required Models

```bash
# Start Ollama service
ollama serve

# In a new terminal, pull required models
ollama pull nomic-embed-text
ollama pull mistral  # or llama3.2
```

### Windows Setup

#### 1. Install Prerequisites

**Install Python 3.11:**
1. Download from [python.org](https://www.python.org/downloads/)
2. **IMPORTANT:** Check "Add Python to PATH" during installation
3. Verify: Open Command Prompt and run `python --version`

**Install Ollama:**
1. Download from [ollama.ai](https://ollama.ai)
2. Run the installer
3. Verify: Open Command Prompt and run `ollama list`

**Install LibreOffice:**
1. Download from [libreoffice.org](https://www.libreoffice.org/)
2. Run the installer
3. Required for processing .doc files

#### 2. Setup Project

**Open Windows Terminal or Command Prompt as Administrator:**

```cmd
# Navigate to your desired location
cd C:\

# Clone the repository
git clone https://github.com/[your-username]/Telsec_RAG.git
cd Telsec_RAG

# Create virtual environment
py -3.11 -m venv venv

# Activate virtual environment
venv\Scripts\activate.bat

# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

#### 3. Configure PowerShell (if using)

If using PowerShell and encountering execution policy errors:

```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate virtual environment
venv\Scripts\Activate.ps1
```

#### 4. Install Required Models

```cmd
# Start Ollama service (keep this terminal open)
ollama serve

# Open new Command Prompt, navigate to project, activate venv
cd C:\path\to\Telsec_RAG
venv\Scripts\activate.bat

# Pull required models
ollama pull nomic-embed-text
ollama pull mistral
```

## Adding Documents

### 1. Prepare Your Documents

Place your documents in the `data/` folder:

```
data/
├── lease-agreement.pdf
├── property-handbook.docx
└── procedures.doc
```

### 2. Process and Embed Documents

**macOS:**
```bash
source venv/bin/activate
python populate_database.py --reset
```

**Windows:**
```cmd
venv\Scripts\activate.bat
python populate_database.py --reset
```

### 3. Verify Database Population

```bash
# Check database contents
python -c "
from langchain_chroma import Chroma
from get_embedding_function import get_embedding_function
db = Chroma(persist_directory='chroma', embedding_function=get_embedding_function())
items = db.get(include=[])
print(f'Documents in database: {len(items[\"ids\"])}')
"
```

## Usage

### Starting the System

**macOS:**
```bash
source venv/bin/activate
streamlit run app.py
```

**Windows:**
```cmd
venv\Scripts\activate.bat
streamlit run app.py
```

### Accessing the Interface

1. Open your browser to `http://localhost:8501`
2. Ask questions about your documents in natural language
3. The system will provide answers with source citations

### Example Questions

- "How is annual rent calculated in our lease agreements?"
- "What are the insurance requirements for tenants?"
- "What are the tenant's maintenance obligations?"
- "Is there a personal guarantee clause in the lease?"
- "What documents do I need before sending a lease for signing?"

## Troubleshooting

### Common Issues

#### "No module named 'xyz'" Error
```bash
# Ensure virtual environment is activated
# macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate.bat

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

#### Ollama Connection Error
```bash
# Check if Ollama is running
ollama list

# If not running, start it
ollama serve

# Verify models are installed
ollama pull nomic-embed-text
ollama pull mistral
```

#### "0 documents in database" Issue
```bash
# Test embedding function
python -c "
from get_embedding_function import get_embedding_function
emb = get_embedding_function()
result = emb.embed_query('test')
print(f'Embedding works: {len(result)} dimensions')
"

# If this fails, try alternative embedding (see Advanced Troubleshooting)
```

#### Windows PowerShell Script Execution Error
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or use Command Prompt instead
```

#### LibreOffice .doc File Error
- Ensure LibreOffice is installed and accessible
- Convert .doc files to .docx if issues persist
- Check file permissions

### Advanced Troubleshooting

#### Alternative Embedding Options

If Ollama embeddings fail, modify `get_embedding_function.py`:

**Option 1: Hugging Face (offline)**
```python
from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_function():
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    return embeddings
```

**Option 2: OpenAI (requires API key)**
```python
from langchain_openai import OpenAIEmbeddings

def get_embedding_function():
    # Set environment variable: OPENAI_API_KEY=your_key
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return embeddings
```

#### Debug Mode

Create `debug_populate.py` for detailed error tracking:
```python
# See the debug script in the troubleshooting guide
# Provides step-by-step progress monitoring
```

### Performance Optimization

- **Reduce chunk size** for large documents: Edit `chunk_size=400` in `populate_database.py`
- **Process fewer documents** initially to test system
- **Monitor RAM usage** during embedding generation
- **Close other applications** during initial setup

### System Requirements Check

**Minimum specs:**
- 4GB RAM (8GB+ recommended)
- 2GB free disk space
- Stable internet for model downloads

## Support

For technical issues:
1. Check this troubleshooting guide first
2. Verify all prerequisites are installed
3. Test individual components (Python, Ollama, LibreOffice)
4. Document exact error messages for debugging

## Security Notes

- This system is designed for internal use only
- Documents are processed locally (no data sent to external services when using Ollama)
- Ensure sensitive documents are handled according to your organization's data policies

