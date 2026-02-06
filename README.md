# Image Upload Utility (CloudFront + Cloudinary)

> **Created by [Cagri Sarigoz](https://github.com/csarigoz)** | **Open Source** | **MIT License**

A comprehensive tool for downloading, optimizing, and uploading images to **AWS CloudFront/S3** or **Cloudinary**. Features automatic image optimization, format conversion, unique URL generation, and **AI-powered alt text generation** for accessibility and SEO.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

## 🌟 Multi-Provider Support

Choose between two powerful image delivery platforms:

| Provider | Best For | Key Benefits |
|----------|----------|-------------|
| **🌐 Cloudinary** | Most users, easy setup | Automatic optimization, global CDN, dynamic transformations |
| **☁️ CloudFront/S3** | AWS ecosystem integration | Full control, AWS pricing, existing infrastructure |

## 🚀 Features

- **🔄 Multi-Provider Support**: Choose between Cloudinary and AWS CloudFront/S3
- **📦 Batch Image Processing**: Download images from URLs and upload to your chosen provider
- **🎯 Smart Optimization**: Automatic resizing, quality adjustment, and format conversion
- **🎨 Format Intelligence**: Automatically chooses the best format (JPEG, PNG, WebP, AVIF) for optimal file size
- **⚡ Unique URLs**: Adds timestamps to prevent filename conflicts and ensure cache busting
- **🤖 AI Alt Text Generation**: Generate descriptive alt text using AltText.ai API
- **🔌 REST API**: HTTP endpoints for programmatic access
- **🎮 Interactive CLI**: User-friendly command-line interface with provider selection
- **📊 Comprehensive Logging**: Detailed progress tracking and error reporting
- **🌍 Global CDN**: Built-in CDN delivery with both providers

## 🛠 Installation

### Prerequisites

- **Python 3.9+** (Recommended: Python 3.13 for best performance)
- **Provider Account**: Choose one or both:
  - **Cloudinary account** (recommended for most users)
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
git clone https://github.com/csarigoz/image-optimization.git
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
   git clone https://github.com/csarigoz/image-optimization.git
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
- **AVIF support (optional)**: For CloudFront/S3 smart format conversion to AVIF, install `pillow-avif-plugin` (included in `requirements.txt`) and ensure your environment has AVIF codecs available (common on most modern Linux distributions).
- **Provider Account**: Choose one or both:
  - **Cloudinary account** (recommended for most users)
  - **AWS account** with S3 and CloudFront access
- **AltText.ai API key** (optional, for alt text generation)

## ⚡ Quick Usage

### 🌐 Cloudinary (Recommended)

**Setup:**
```bash
# 1. Sign up at cloudinary.com and get your credentials
# 2. Add to .env file:
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key  
CLOUDINARY_API_SECRET=your_api_secret
UPLOAD_PROVIDER=cloudinary

# 3. Run interactive setup
./process_csv.sh
# Choose option 2 (Cloudinary) when prompted
```

**Command Line:**
```bash
# Upload from CSV with Cloudinary
python unified_upload.py --provider cloudinary --mode csv --alt-text

# Upload local files with optimization
python unified_upload.py --provider cloudinary --mode local --max-width 800
```

### ☁️ CloudFront/S3 (AWS)

**Setup:**
```bash
# 1. Configure AWS credentials in .env:
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
S3_BUCKET=your_s3_bucket_name
CLOUDFRONT_DOMAIN=your_cloudfront_domain
UPLOAD_PROVIDER=cloudfront

# 2. Run interactive setup
./process_csv.sh
# Choose option 1 (CloudFront) when prompted
```

**Legacy Mode:**
```python
# Use the original upload_files.py for CloudFront
from upload_files import download_and_upload_from_csv

download_and_upload_from_csv(
    generate_alt_text=True,
    alt_text_keywords="product, ecommerce, lifestyle"
)
```

### 🎮 Interactive Mode (All Providers)

The interactive script automatically detects your provider configuration:

```bash
./process_csv.sh

# The script will:
# 1. Detect available providers from your .env file
# 2. Show provider selection menu if both are configured
# 3. Guide you through optimization settings
# 4. Process your images with the chosen provider
```

### 📋 Unified Command Line

The new `unified_upload.py` provides a consistent interface for both providers:

```bash
# Auto-detect provider from environment (.env file)
python unified_upload.py --mode csv --alt-text

# Force specific provider (overrides environment)
python unified_upload.py --provider cloudinary --mode csv --max-width 800 --quality 85
python unified_upload.py --provider cloudfront --mode csv --max-width 800 --quality 85

# Upload modes
python unified_upload.py --mode csv         # Process CSV file
python unified_upload.py --mode local       # Upload local files
python unified_upload.py --mode stats       # View upload statistics
python unified_upload.py --mode list        # List uploaded files

# Optimization options
python unified_upload.py --provider cloudinary --mode csv \
    --max-width 1200 \
    --quality 85 \
    --alt-text \
    --alt-text-keywords "product,modern,lifestyle"

# Advanced usage
python unified_upload.py --provider cloudinary --mode csv --no-smart-format --no-timestamp
```

### 🔄 Provider Comparison

| Feature | Cloudinary | CloudFront/S3 |
|---------|------------|---------------|
| **Setup Time** | 5 minutes | 30+ minutes |
| **Automatic Optimization** | ✅ Built-in | ⚠️ Manual (Pillow) |
| **Format Selection** | ✅ AI-powered | ⚠️ Rule-based |
| **Global CDN** | ✅ Included | ✅ CloudFront |
| **Real-time Transformations** | ✅ URL-based | ❌ Pre-upload only |
| **Direct URL Upload** | ✅ Native | ⚠️ Download first |
| **Cost Model** | Usage-based | Storage + bandwidth |
| **AWS Integration** | ❌ External service | ✅ Native AWS |
| **Learning Curve** | ⭐⭐ Easy | ⭐⭐⭐⭐ Advanced |

### 🔧 Provider Migration

You can easily switch between providers:

```bash
# Switch from CloudFront to Cloudinary
export UPLOAD_PROVIDER=cloudinary
python unified_upload.py --mode csv

# Switch from Cloudinary to CloudFront  
export UPLOAD_PROVIDER=cloudfront
python unified_upload.py --mode csv

# Use both providers (manual selection each time)
export UPLOAD_PROVIDER=auto
./process_csv.sh  # Will prompt for provider selection
```

### 🌐 **Cloudinary Deep Dive**

#### **Why Choose Cloudinary?**

- **⚡ Easy Setup**: 5 minutes vs 30+ minutes for CloudFront
- **🤖 Automatic Optimization**: Smart format selection (WebP, AVIF) and quality adjustment
- **🔄 Dynamic Transformations**: Real-time image resizing via URL parameters
- **📱 Responsive Images**: Automatic device-specific optimization
- **🌍 Global CDN**: Built-in worldwide delivery
- **💰 Usage-Based Pricing**: Pay only for what you use

#### **Dynamic URL Transformations**

One of Cloudinary's biggest advantages is URL-based transformations:

```bash
# Original image
https://res.cloudinary.com/your_cloud/image/upload/sample.jpg

# Resized to 300px width, auto height
https://res.cloudinary.com/your_cloud/image/upload/w_300/sample.jpg

# Optimized format and quality
https://res.cloudinary.com/your_cloud/image/upload/f_auto,q_auto/sample.jpg

# Combined transformations
https://res.cloudinary.com/your_cloud/image/upload/w_300,h_200,c_fill,f_auto,q_auto/sample.jpg
```

#### **Migration from CloudFront**

**Gradual Migration Approach:**
1. Configure both providers in your `.env`
2. Test Cloudinary with a few images first
3. Compare performance and costs
4. Gradually switch traffic

**Bulk Migration:**
```bash
# Re-upload existing URLs to Cloudinary
python unified_upload.py --provider cloudinary --mode csv
```

#### **Cloudinary Best Practices**

1. **Enable Smart Defaults**: Always use `smart_format=True` for automatic optimization
2. **Organize with Folders**: Use descriptive folder names for better organization
3. **Monitor Usage**: Regularly check your Cloudinary dashboard for usage patterns
4. **Use Responsive URLs**: Take advantage of automatic device optimization

#### **Troubleshooting Cloudinary**

```bash
# Test Cloudinary connection
python test_cloudinary.py

# View account usage
python unified_upload.py --provider cloudinary --mode stats

# Common issues:
# - Check API quotas in Cloudinary dashboard
# - Verify image format is supported  
# - Ensure stable internet connection
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with your configuration:

```bash
# Provider Selection
UPLOAD_PROVIDER=cloudinary  # or 'cloudfront'

# Cloudinary Configuration (if using Cloudinary)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# AWS Configuration (if using CloudFront)
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
S3_BUCKET=your_s3_bucket_name
CLOUDFRONT_DOMAIN=your_cloudfront_domain

# AltText.ai Configuration (Optional)
ALTTEXT_AI_API_KEY=your_alttext_ai_api_key
ALTTEXT_AI_KEYWORDS=default,keywords,for,seo
ALTTEXT_AI_WEBHOOK_URL=your_webhook_url
```

### Quick Setup Guide

| Provider | Setup Difficulty | Time to Setup | Best For |
|----------|-----------------|---------------|----------|
| **Cloudinary** | ⭐⭐ Easy | 5 minutes | Most users, quick setup |
| **CloudFront** | ⭐⭐⭐⭐ Advanced | 30+ minutes | AWS integration, advanced users |

**Cloudinary Setup:**
1. Sign up at [cloudinary.com](https://cloudinary.com)
2. Copy cloud name, API key, and secret from dashboard
3. Add to `.env` file
4. Run `python setup.py`

**CloudFront Setup:**
1. Configure S3 bucket with public read access
2. Create CloudFront distribution
3. Set up IAM user with S3 permissions
4. Add credentials to `.env` file
5. Run `python setup.py`

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
2. **Search existing issues**: Look for similar problems in [GitHub Issues](https://github.com/csarigoz/image-optimization/issues)
3. **Create a new issue**: Use our [bug report template](.github/ISSUE_TEMPLATE/bug_report.md)
4. **Join discussions**: Participate in [GitHub Discussions](https://github.com/csarigoz/image-optimization/discussions)

## 🤝 Contributing

We welcome contributions from the community! This project is open source and maintained by [Cagri Sarigoz](https://github.com/csarigoz).

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
- **[Cagri Sarigoz](https://github.com/csarigoz)** - Original creator and lead maintainer

### Technologies Used
- **[Python](https://python.org)** - Core programming language
- **[Pillow (PIL)](https://pillow.readthedocs.io/)** - Image processing library
- **[Flask](https://flask.palletsprojects.com/)** - Web framework for API
- **[Boto3](https://boto3.amazonaws.com/)** - AWS SDK for Python
- **[AltText.ai](https://alttext.ai/)** - AI-powered alt text generation

### Contributors

Contributors will be recognized here as the project grows. See [GitHub Contributors](https://github.com/csarigoz/image-optimization/graphs/contributors) for the current list.

## 🔗 Links

- **Repository**: [https://github.com/csarigoz/image-optimization](https://github.com/csarigoz/image-optimization)
- **Issues**: [Report bugs and request features](https://github.com/csarigoz/image-optimization/issues)
- **Discussions**: [Community discussions](https://github.com/csarigoz/image-optimization/discussions)
- **Releases**: [Download latest version](https://github.com/csarigoz/image-optimization/releases)

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/csarigoz/image-optimization?style=social)
![GitHub forks](https://img.shields.io/github/forks/csarigoz/image-optimization?style=social)
![GitHub issues](https://img.shields.io/github/issues/csarigoz/image-optimization)
![GitHub pull requests](https://img.shields.io/github/issues-pr/csarigoz/image-optimization)

---

**Made with ❤️ by [Cagri Sarigoz](https://github.com/csarigoz)**

*If this project helps you, please consider giving it a ⭐ on GitHub!* 