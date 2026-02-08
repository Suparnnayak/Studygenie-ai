#!/bin/bash
# Quick script to run Flask backend locally

echo "🚀 Starting StudyGenie AI Backend locally..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.installed" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env from template..."
    cat > .env << EOF
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=dev-secret-key-change-me
CORS_ORIGINS=http://localhost:3000
GROQ_MODEL=llama-3.3-70b-versatile
EOF
    echo "✅ Created .env file. Please update it with your API keys!"
fi

# Run the server
echo "🌟 Starting Flask server on http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""
python -m app.main

