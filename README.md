# Xiaohongshu Post Generator
This project deploys DeepSeek's R1 model to generate posts on the Chinese social media platform REDnote, known in Chinese as Xiaohongshu, which has recently gained popularity around the world.

## Setup Instructions

### Requirements
```
python >= 3.8
deepseek-api >= 1.0.0
requests >= 2.26.0
python-dotenv >= 0.19.0
```

### Installation
1. Clone the repository
```bash
git clone https://github.com/yourusername/xiaohongshu-generator.git
cd xiaohongshu-generator
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

### Configuration
1. Get your DeepSeek API key from their [developer portal](https://deepseek.com/developers)

2. Create a `.env` file in project root:
```
DEEPSEEK_API_KEY=your_api_key_here
```

### Running the App
```bash
python main.py
```

For testing:
```bash
python -m pytest tests/
```
