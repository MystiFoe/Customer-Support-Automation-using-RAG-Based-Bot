# Customer Support Automation using RAG-Based Bot

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.47+-red.svg)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A professional AI-powered customer support chatbot that uses Retrieval-Augmented Generation (RAG) technology to provide intelligent, context-aware responses. Built with Python, Streamlit, and OpenAI's GPT-4 for enterprise-grade customer support automation.

## 🚀 Features

- **RAG Technology**: Combines knowledge retrieval with AI generation for accurate responses
- **Professional UI**: Clean, business-ready interface optimized for professional environments
- **Real-time Analytics**: Performance metrics including accuracy, resolution rates, and response times
- **Knowledge Base Management**: Easy-to-update JSON-based document storage system
- **Conversation Export**: Download chat history and performance metrics in JSON format
- **Comprehensive Logging**: Multi-level logging system for monitoring and debugging
- **Modular Architecture**: Clean, maintainable codebase following SOLID principles

## 📋 Prerequisites

- Python 3.11 or higher
- Poetry (for dependency management)
- OpenAI API key

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MystiFoe/Customer-Support-Automation-using-RAG-Based-Bot.git
   cd Customer-Support-Automation-using-RAG-Based-Bot
   ```

2. **Install Poetry** (if not already installed)
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies**
   ```bash
   poetry install
   ```

4. **Set up environment variables**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```

## 🚀 Quick Start

1. **Run the application**
   ```bash
   poetry run streamlit run app.py --server.port 8501
   ```

2. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

3. **Start chatting**
   Type your customer support questions and get instant AI-powered responses!

## 📁 Project Structure

```
├── README.md                 # Project documentation
├── pyproject.toml           # Poetry dependency configuration
├── app.py                   # Main Streamlit application
├── config/
│   └── settings.py          # Centralized configuration management
├── src/
│   ├── knowledge_base.py    # Knowledge base document management
│   ├── rag_system.py        # RAG implementation with OpenAI
│   ├── metrics.py           # Performance tracking and analytics
│   └── logger.py            # Centralized logging utilities
├── data/
│   └── knowledge_base.json  # Knowledge base documents
└── logs/                    # Application logs (auto-created)
```

## 🔧 Configuration

Customize the application by editing `config/settings.py`:

```python
@dataclass
class OpenAIConfig:
    model: str = "gpt-4o"           # AI model to use
    temperature: float = 0.7         # Response creativity (0-1)
    max_tokens: int = 500           # Maximum response length

@dataclass
class UIConfig:
    page_title: str = "AI Customer Support"
    layout: str = "wide"            # Streamlit layout mode
```

## 📊 Performance Metrics

The system automatically tracks key performance indicators:

- **Accuracy Rate**: Response quality based on confidence scores and source relevance
- **Resolution Rate**: Percentage of queries successfully resolved without escalation
- **Response Time**: Average time to generate AI responses
- **Source Attribution**: Transparency showing which knowledge base articles informed responses

## 🎯 Use Cases

### Customer Support Teams
- Automate responses to frequently asked questions
- Provide consistent 24/7 support availability
- Reduce first response times and improve customer satisfaction
- Free up human agents for complex issues requiring personal attention

### Technical Documentation
- Create interactive help systems for software products
- Provide instant access to technical knowledge bases
- Support internal teams with quick procedure lookups

### Business Applications
- FAQ automation for company websites
- Internal knowledge management systems
- Employee training and onboarding support
- Product information and troubleshooting guides

## 🔍 How It Works

1. **Query Processing**: User submits a question through the professional web interface
2. **Document Retrieval**: RAG system searches the knowledge base using keyword matching and scoring
3. **Context Generation**: Most relevant documents are combined with the user query
4. **AI Response**: OpenAI's GPT-4 generates a contextual response using retrieved information
5. **Quality Tracking**: System logs performance metrics, confidence scores, and source attribution

## 📈 Monitoring & Analytics

- **Real-time Dashboard**: Live performance metrics displayed in the sidebar
- **Conversation Export**: Download complete chat history and metrics in JSON format
- **Comprehensive Logging**: Detailed application logs for system monitoring and debugging
- **Performance Tracking**: Historical data analysis for continuous system optimization

## 🚀 Deployment Options

### Local Development
```bash
poetry run streamlit run app.py
```

### Docker Deployment
Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install poetry && poetry install --no-dev
EXPOSE 8501
CMD ["poetry", "run", "streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

Build and run:
```bash
docker build -t ai-support-bot .
docker run -p 8501:8501 -e OPENAI_API_KEY="your-key" ai-support-bot
```

### Cloud Deployment
The application is compatible with major cloud platforms:
- **AWS**: EC2, ECS, or Lambda deployments
- **Google Cloud Platform**: Compute Engine or Cloud Run
- **Microsoft Azure**: Container Instances or App Service
- **Heroku**: Direct deployment with buildpacks

## 🤝 Contributing

We welcome contributions to improve the AI Customer Support Bot!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and ensure tests pass
4. Commit your changes: `git commit -m 'Add new feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request with a clear description

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comprehensive docstrings to new functions
- Include appropriate logging statements
- Update documentation for new features

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for complete details.

## 🐛 Troubleshooting

### Common Issues

**OpenAI API Key Error**
```bash
# Ensure your API key is properly set
export OPENAI_API_KEY="your-actual-api-key"
# Or add to your shell profile for persistence
echo 'export OPENAI_API_KEY="your-key"' >> ~/.bashrc
```

**Port Already in Use**
```bash
# Use a different port
poetry run streamlit run app.py --server.port 8502
# Or kill existing processes
pkill -f streamlit
```

**Knowledge Base Not Loading**
- Ensure `data/knowledge_base.json` exists and is readable
- Verify JSON format is valid using online JSON validators
- Check file permissions and directory structure

**Dependencies Issues**
```bash
# Clear Poetry cache and reinstall
poetry cache clear pypi --all
poetry install --no-cache
```

### Logging and Debugging
Check application logs for detailed error information:
```bash
# View recent logs
tail -f logs/app.log

# Search for specific errors
grep "ERROR" logs/app.log

# Monitor logs in real-time
tail -f logs/app.log | grep -E "(ERROR|WARNING)"
```

## 📚 Documentation

### API Reference
- **RAGSystem.get_response(query)**: Main method for generating AI responses
- **MetricsTracker.add_interaction()**: Log user interactions for analytics
- **KnowledgeBase.search_documents()**: Search knowledge base documents

### Configuration Options
- **OpenAI Model Settings**: Customize AI behavior and response characteristics
- **UI Customization**: Modify interface appearance and layout
- **Logging Configuration**: Adjust log levels and output destinations

## 🌟 Support

If you find this project helpful, please consider:
- Giving it a ⭐ star on GitHub
- Sharing it with others who might benefit
- Contributing improvements or bug fixes

For support and questions:
- 📋 Open an issue on GitHub for bug reports or feature requests
- 📖 Check the troubleshooting section above
- 📊 Review application logs for detailed error information

## 🏆 Acknowledgments

- **OpenAI** for providing the GPT-4 API that powers the intelligent responses
- **Streamlit** for the excellent web application framework
- **Python Community** for the robust ecosystem of libraries and tools

## 📞 Contact

- **Repository**: [Customer-Support-Automation-using-RAG-Based-Bot](https://github.com/MystiFoe/Customer-Support-Automation-using-RAG-Based-Bot)
- **Issues**: [GitHub Issues](https://github.com/MystiFoe/Customer-Support-Automation-using-RAG-Based-Bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/MystiFoe/Customer-Support-Automation-using-RAG-Based-Bot/discussions)

---

**Built with dedication for professional customer support automation**

*Transform your customer support with AI-powered intelligence*