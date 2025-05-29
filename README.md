# CloudFront Image Upload Utility

> **Created by [Cagri Sarigoz](https://github.com/cagrisarigoz)** | **Open Source** | **MIT License**

A comprehensive tool for downloading, optimizing, and uploading images to AWS S3 with CloudFront distribution. Features automatic image optimization, format conversion, unique URL generation, and **AI-powered alt text generation** for accessibility and SEO.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

## 🚀 Features

- **Batch Image Processing**: Download images from URLs and upload to S3/CloudFront
- **Image Optimization**: Automatic resizing, quality adjustment, and format conversion
- **Smart Format Selection**: Automatically chooses the best format (JPEG, PNG, WebP) for optimal file size
- **Unique URLs**: Adds timestamps to prevent filename conflicts and ensure cache busting
- **AI Alt Text Generation**: Generate descriptive alt text using AltText.ai API
- **REST API**: HTTP endpoints for programmatic access
- **Interactive CLI**: User-friendly command-line interface
- **Comprehensive Logging**: Detailed progress tracking and error reporting

## 🛠 Installation

### Prerequisites

- **Python 3.9+** (Recommended: Python 3.13 for best performance)
- **AWS account** with S3 and CloudFront access
- **AltText.ai API key** (optional, for alt text generation)

### Recommended Setup with Python 3.13 Virtual Environment

For the best and most consistent experience, we recommend using Python 3.13 with a virtual environment:

#### 1. Install Python 3.13

**macOS (using Homebrew):**
```bash
brew install python@3.13
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-pip
```

**Windows:**
Download from [python.org](https://www.python.org/downloads/) or use Windows Store.

**Verify installation:**
```bash
python3.13 --version
# Should output: Python 3.13.x
```

#### 2. Create and Activate Virtual Environment

**Create virtual environment:**
```bash
# Clone the repository first
git clone https://github.com/cagrisarigoz/image-optimization.git
cd image-optimization

# Create virtual environment with Python 3.13
python3.13 -m venv venv

# Alternative if python3.13 is your default python
python -m venv venv
```

**Activate virtual environment:**

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Verify activation:**
```bash
which python  # Should point to venv/bin/python
python --version  # Should show Python 3.13.x
```

#### 3. Install Dependencies

```bash
# Upgrade pip to latest version
python -m pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

#### 4. Run Setup

```bash
python setup.py
```

#### 5. Configure Environment

```bash
# Copy environment template
cp env.example .env

# Edit .env with your credentials (use your preferred editor)
nano .env  # or vim .env, code .env, etc.
```

### Quick Start (Alternative Method)

If you prefer a simpler setup or already have Python 3.9+ installed:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/cagrisarigoz/image-optimization.git
   cd image-optimization
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run setup**:
   ```bash
   python setup.py
   ```

4. **Configure environment**:
   ```bash
   cp env.example .env
   # Edit .env with your credentials
   ```

### Virtual Environment Benefits

Using a virtual environment provides several advantages:

- **Isolation**: Dependencies don't conflict with system packages
- **Reproducibility**: Consistent environment across different machines
- **Version Control**: Lock specific package versions
- **Clean Uninstall**: Easy to remove by deleting the venv folder
- **Multiple Projects**: Different Python versions for different projects

### Deactivating Virtual Environment

When you're done working on the project:

```bash
deactivate
```

### Requirements

- **Python 3.9+** (Tested on 3.9, 3.10, 3.11, 3.12, 3.13)
- **AWS account** with S3 and CloudFront access
- **AltText.ai API key** (optional, for alt text generation)

## ⚡ Quick Usage

### Interactive CSV Processing
```bash
./process_csv.sh
```

### Direct Python Usage
```python
from upload_files import download_and_upload_from_csv

# Process images with alt text generation
download_and_upload_from_csv(
    generate_alt_text=True,
    alt_text_keywords="product, ecommerce, lifestyle"
)
```

### REST API
```bash
# Start the API server
export FLASK_RUN=1
python upload_files.py

# Upload a file
curl -X POST -F "file=@image.jpg" http://localhost:5000/upload
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with your configuration:

```bash
# AWS Configuration (Required)
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
S3_BUCKET=your_s3_bucket_name
CLOUDFRONT_DOMAIN=your_cloudfront_domain

# AltText.ai Configuration (Optional)
ALTTEXT_AI_API_KEY=your_alttext_ai_api_key
ALTTEXT_AI_KEYWORDS=default,keywords,for,seo
ALTTEXT_AI_WEBHOOK_URL=your_webhook_url
```

### CSV Input Format

Create `data/input/images_to_download_and_upload.csv`:

```csv
URL
https://example.com/image1.jpg
https://example.com/image2.png
https://example.com/image3.webp
```

## 🎯 Usage Examples

### 1. Basic CSV Processing

```bash
# Interactive mode with prompts
./process_csv.sh

# Follow the prompts to configure:
# - Alt text generation (Y/N)
# - Keywords for SEO
# - Image optimization settings
# - Quality and format options
```

### 2. Automated Processing

```bash
# Set environment variables for automation
export PROCESS_CSV=1
export GENERATE_ALT_TEXT=true
export ALT_TEXT_KEYWORDS="product, lifestyle, modern"
export MAX_WIDTH=1200
export QUALITY=85
export SMART_FORMAT=true

python upload_files.py
```

### 3. Local File Upload

```python
from upload_files import upload_files

# Upload local files with optimization
upload_files(
    max_width=800,
    quality=82,
    smart_format=True,
    generate_alt_text=True
)
```

### 4. REST API Usage

```bash
# Start the server
export FLASK_RUN=1
python upload_files.py &

# Upload single file
curl -X POST -F "file=@photo.jpg" http://localhost:5000/upload

# List uploaded files
curl http://localhost:5000/files

# Process CSV via API
curl http://localhost:5000/process-csv
```

## 🤖 AI Alt Text Generation

### Features
- **Automatic descriptions**: Generate descriptive alt text for accessibility
- **SEO optimization**: Include custom keywords for better search rankings
- **Batch processing**: Generate alt text for multiple images efficiently
- **Fallback handling**: Graceful degradation when API is unavailable

### Configuration
```bash
# Enable alt text generation
ALTTEXT_AI_API_KEY=your_api_key
ALTTEXT_AI_KEYWORDS=product,ecommerce,lifestyle,modern

# Optional webhook for async processing
ALTTEXT_AI_WEBHOOK_URL=https://your-domain.com/webhook
```

### Usage
```python
from alttext_ai import generate_alt_text

# Generate alt text for an image
alt_text = generate_alt_text(
    image_url="https://example.com/image.jpg",
    keywords="product, modern, lifestyle"
)
print(f"Generated alt text: {alt_text}")
```

## 📊 Output Files

The tool generates several output files in the `data/output/` directory:

### `data/output/images_mapping.csv`
Maps original URLs to optimized CloudFront URLs with alt text:
```csv
source_url,cloudfront_url,max_width,quality,smart_format,alt_text
https://example.com/image1.jpg,https://cdn.example.com/image_123.webp,800,85,True,"Modern lifestyle product photo"
```

### `data/output/uploaded_files.json`
Tracks upload status and metadata:
```json
{
  "image_123.webp": {
    "original_url": "https://example.com/image1.jpg",
    "cloudfront_url": "https://cdn.example.com/image_123.webp",
    "alt_text": "Modern lifestyle product photo",
    "upload_time": "2025-01-20T10:30:00Z"
  }
}
```

### `data/output/local_files_alt_text.csv`
Alt text for local files:
```csv
filename,alt_text
photo1.jpg,"Beautiful sunset over mountains"
product2.png,"Modern smartphone with sleek design"
```

## 🔧 Advanced Configuration

### Image Optimization Settings

```python
# Customize optimization parameters
optimize_image(
    image_path="photo.jpg",
    max_width=1200,        # Maximum width in pixels
    quality=85,            # JPEG/WebP quality (1-100)
    smart_format=True      # Auto-select best format
)
```

### Format Selection Logic

The tool automatically selects the best format:
- **JPEG**: For photos with many colors
- **PNG**: For images with transparency or few colors
- **WebP**: For modern browsers (best compression)

### Quality Guidelines

- **90-100**: Highest quality, larger files
- **80-89**: High quality, good for most use cases
- **70-79**: Good quality, smaller files
- **60-69**: Acceptable quality, much smaller files

## 🚀 API Reference

### Endpoints

#### `POST /upload`
Upload and optimize a single file.

**Request:**
```bash
curl -X POST -F "file=@image.jpg" \
     -F "max_width=800" \
     -F "quality=85" \
     http://localhost:5000/upload
```

**Response:**
```json
{
  "success": true,
  "cloudfront_url": "https://cdn.example.com/image_123.webp",
  "alt_text": "Generated alt text description",
  "original_size": "150KB",
  "optimized_size": "45KB",
  "format": "webp"
}
```

#### `GET /files`
List all uploaded files.

**Response:**
```json
{
  "files": [
    {
      "filename": "image_123.webp",
      "cloudfront_url": "https://cdn.example.com/image_123.webp",
      "upload_time": "2025-01-20T10:30:00Z"
    }
  ]
}
```

#### `GET /process-csv`
Process images from CSV file.

**Response:**
```json
{
  "success": true,
  "processed": 5,
  "failed": 0,
  "output_file": "data/output/images_mapping.csv"
}
```

## 🛠 Development

### Project Structure

```
image-optimization/
├── Core Application Files
│   ├── upload_files.py              # Main application & Flask API
│   ├── alttext_ai.py               # AltText.ai API integration
│   ├── setup.py                     # Setup & dependency checker
│   ├── process_csv.sh               # Interactive batch processor
│   └── requirements.txt             # Python dependencies
├── Configuration
│   ├── .env                        # Environment variables (gitignored)
│   ├── env.example                 # Environment template
│   └── .gitignore                  # Git exclusions
├── Data Files
│   ├── data/
│   │   ├── input/                  # Input CSV files
│   │   ├── output/                 # Generated output files
│   │   ├── examples/               # Example files for reference
│   │   └── local_images/           # Downloaded/local image files
├── Utilities
│   ├── check_s3_objects.py          # S3 debugging utility
│   └── regenerate_urls.py           # URL mapping regeneration
└── Documentation & CI/CD
    ├── README.md                    # Complete documentation
    ├── CONTRIBUTING.md              # Contribution guidelines
    ├── PROJECT_RULES.md             # Project rules and standards
    └── .github/                     # GitHub workflows & templates
```

### Running Tests

```bash
# Test core functionality
python upload_files.py

# Test AltText.ai integration
python alttext_ai.py

# Test CSV processing
./process_csv.sh

# Test API endpoints
export FLASK_RUN=1
python upload_files.py &
curl -X POST -F "file=@test.jpg" http://localhost:5000/upload
```

## 🐛 Troubleshooting

### Common Issues

#### Python Version Issues
```bash
# Error: Python version not supported
# Solution: Upgrade to Python 3.9+
python --version  # Check current version

# Install Python 3.13 (recommended)
# See installation instructions above
```

#### Virtual Environment Issues
```bash
# Error: Command not found after activation
# Solution: Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Verify activation
which python  # Should point to venv directory
```

#### AWS Credentials
```bash
# Error: AWS credentials not found
# Solution: Check your .env file
AWS_ACCESS_KEY=your_key_here
AWS_SECRET_KEY=your_secret_here
```

#### AltText.ai API
```bash
# Error: AltText.ai connection failed
# Solution: Verify your API key
python -c "from alttext_ai import test_alttext_ai_connection; test_alttext_ai_connection()"
```

#### Image Processing
```bash
# Error: PIL/Pillow issues
# Solution: Reinstall Pillow
pip uninstall Pillow
pip install Pillow
```

#### Permission Issues
```bash
# Error: process_csv.sh permission denied
# Solution: Make script executable
chmod +x process_csv.sh
```

### Debug Mode

Enable verbose logging:
```bash
export DEBUG=1
python upload_files.py
```

### Getting Help

1. **Check the documentation**: Review this README and [PROJECT_RULES.md](PROJECT_RULES.md)
2. **Search existing issues**: Look for similar problems in [GitHub Issues](https://github.com/cagrisarigoz/image-optimization/issues)
3. **Create a new issue**: Use our [bug report template](.github/ISSUE_TEMPLATE/bug_report.md)
4. **Join discussions**: Participate in [GitHub Discussions](https://github.com/cagrisarigoz/image-optimization/discussions)

## 🤝 Contributing

We welcome contributions from the community! This project is open source and maintained by [Cagri Sarigoz](https://github.com/cagrisarigoz).

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**: Follow our [coding standards](PROJECT_RULES.md)
4. **Test thoroughly**: Ensure your changes work as expected
5. **Submit a pull request**: Use our [PR template](.github/PULL_REQUEST_TEMPLATE.md)

### Contribution Areas

- 🐛 **Bug fixes**: Help improve stability and reliability
- ✨ **New features**: Add functionality that benefits users
- 📚 **Documentation**: Improve guides, examples, and API docs
- 🧪 **Testing**: Add tests and improve coverage
- 🎨 **UI/UX**: Enhance user experience and interface
- ⚡ **Performance**: Optimize speed and resource usage

### Development Guidelines

Please read our comprehensive contribution guidelines:
- [CONTRIBUTING.md](CONTRIBUTING.md) - Detailed contribution process
- [PROJECT_RULES.md](PROJECT_RULES.md) - Coding standards and conventions

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### License Summary

- ✅ **Commercial use**: Use in commercial projects
- ✅ **Modification**: Modify the source code
- ✅ **Distribution**: Distribute the software
- ✅ **Private use**: Use for private projects
- ❗ **License and copyright notice**: Include license in distributions

## 🙏 Acknowledgments

### Creator & Maintainer
- **[Cagri Sarigoz](https://github.com/cagrisarigoz)** - Original creator and lead maintainer

### Technologies Used
- **[Python](https://python.org)** - Core programming language
- **[Pillow (PIL)](https://pillow.readthedocs.io/)** - Image processing library
- **[Flask](https://flask.palletsprojects.com/)** - Web framework for API
- **[Boto3](https://boto3.amazonaws.com/)** - AWS SDK for Python
- **[AltText.ai](https://alttext.ai/)** - AI-powered alt text generation

### Contributors

Contributors will be recognized here as the project grows. See [GitHub Contributors](https://github.com/cagrisarigoz/image-optimization/graphs/contributors) for the current list.

## 🔗 Links

- **Repository**: [https://github.com/cagrisarigoz/image-optimization](https://github.com/cagrisarigoz/image-optimization)
- **Issues**: [Report bugs and request features](https://github.com/cagrisarigoz/image-optimization/issues)
- **Discussions**: [Community discussions](https://github.com/cagrisarigoz/image-optimization/discussions)
- **Releases**: [Download latest version](https://github.com/cagrisarigoz/image-optimization/releases)

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/cagrisarigoz/image-optimization?style=social)
![GitHub forks](https://img.shields.io/github/forks/cagrisarigoz/image-optimization?style=social)
![GitHub issues](https://img.shields.io/github/issues/cagrisarigoz/image-optimization)
![GitHub pull requests](https://img.shields.io/github/issues-pr/cagrisarigoz/image-optimization)

---

**Made with ❤️ by [Cagri Sarigoz](https://github.com/cagrisarigoz)**

*If this project helps you, please consider giving it a ⭐ on GitHub!* 