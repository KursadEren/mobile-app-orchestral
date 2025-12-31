#!/bin/bash

# Klasörleri oluştur
mkdir -p agents tools config tests

# requirements.txt
cat > requirements.txt << 'REQ'
langchain>=0.2.0
langgraph>=0.2.0
langchain-anthropic>=0.1.0
anthropic>=0.18.0
pydantic>=2.0.0
rich>=13.0.0
python-dotenv>=1.0.0
REQ

# .env.example
cat > .env.example << 'ENV'
ANTHROPIC_API_KEY=your_api_key_here
ENV

# agents/__init__.py
cat > agents/__init__.py << 'INIT'
from .planner import PlannerAgent
from .coder import CoderAgent
from .tester import TesterAgent
INIT

echo "✅ Proje yapısı oluşturuldu!"
