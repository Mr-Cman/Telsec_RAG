#!/bin/bash

echo "🏢 Setting up Telsec RAG Assistant UI"
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if Ollama is running (for the LLM)
echo "🤖 Checking Ollama status..."
if ! pgrep -x "ollama" > /dev/null; then
    echo "⚠️  Warning: Ollama is not running. Please start it with: ollama serve"
    echo "💡 Also ensure you have the llama3.2 model: ollama pull llama3.2"
fi

echo ""
echo "✅ Setup complete!"
echo "🚀 Run the app with: python launch.py"
echo "🌐 Or directly with: streamlit run app.py"
echo ""
echo "🎨 Your UI will be available at: http://localhost:8501" 