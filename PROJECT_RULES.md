# Project Rules & Guidelines

**Status**: Living Document  
**Version History**: See [CHANGELOG.md](CHANGELOG.md)  

This document serves as a comprehensive guide for AI models and developers working with the Multi-Provider Image Upload Utility repository. It outlines project structure, coding standards, conventions, and best practices for both Cloudinary and CloudFront integrations.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Core Components](#core-components)
- [Provider Architecture](#provider-architecture)
- [Coding Standards](#coding-standards)
- [File Naming Conventions](#file-naming-conventions)
- [Environment & Configuration](#environment--configuration)
- [API Integration Guidelines](#api-integration-guidelines)
- [Error Handling Standards](#error-handling-standards)
- [Documentation Standards](#documentation-standards)
- [Testing Guidelines](#testing-guidelines)
- [Security Guidelines](#security-guidelines)
- [Performance Guidelines](#performance-guidelines)
- [Deployment Guidelines](#deployment-guidelines)
- [Change Management](#change-management)

## 🎯 Project Overview

### Purpose
Multi-Provider Image Upload Utility is a comprehensive tool for downloading, optimizing, and uploading images to either **Cloudinary** or **AWS S3 with CloudFront distribution**. Features include AI-powered alt text generation for accessibility and SEO, multi-provider support with unified interface, and smart image optimization.

### Core Functionality
1. **Multi-Provider Support**: Choose between Cloudinary and AWS CloudFront/S3
2. **Image Processing**: Download, optimize, and upload images with smart format selection
3. **Format Optimization**: Automatic format selection (JPEG, PNG, WebP) based on content
4. **Alt Text Generation**: AI-powered descriptions using AltText.ai
5. **Batch Processing**: CSV-based bulk operations for both providers
6. **Unified Interface**: Single API for multiple cloud providers
7. **REST API**: HTTP endpoints for programmatic access

### Technology Stack
- **Language**: Python 3.9+ (Recommended: Python 3.13)
- **Cloud Providers**: 
  - **Cloudinary**: Recommended for most users (automatic optimization, global CDN)
  - **AWS S3 + CloudFront**: For AWS ecosystem integration
- **AI Service**: AltText.ai API for automated alt text generation
- **Image Processing**: Pillow (PIL) for local image optimization
- **Web Framework**: Flask for REST API endpoints
- **Environment**: python-dotenv for configuration management

### Provider Selection Strategy
- **Cloudinary**: Best for most users, easy setup, automatic optimization
- **CloudFront/S3**: Best for AWS ecosystem integration, full control over infrastructure
- **Multi-Provider**: Support both providers in the same codebase with unified interface

### Supported Python Versions
- **Python 3.9**: Minimum supported version
- **Python 3.10**: Fully supported
- **Python 3.11**: Fully supported
- **Python 3.12**: Fully supported
- **Python 3.13**: Recommended (latest stable)

## 📁 Repository Structure

```
image-optimization/
├── Core Application Files
│   ├── upload_files.py              # Legacy CloudFront application & Flask API
│   ├── unified_upload.py            # New unified upload system (both providers)
│   ├── alttext_ai.py               # AltText.ai API integration
│   ├── setup.py                     # Setup & dependency checker
│   └── requirements.txt             # Python dependencies
├── Provider System
│   ├── upload_provider.py           # Provider factory and base classes
│   ├── cloudfront_provider.py       # AWS CloudFront/S3 provider implementation
│   ├── cloudinary_provider.py       # Cloudinary provider implementation
│   └── test_cloudinary.py          # Cloudinary integration tests
├── Processing Scripts
│   ├── process_csv.sh               # Interactive batch processor (multi-provider)
│   ├── check_s3_objects.py          # S3 debugging utility
│   └── regenerate_urls.py           # URL mapping regeneration
├── Configuration
│   ├── .env                        # Environment variables (gitignored)
│   ├── .env.example                # Environment template
│   └── .gitignore                  # Git exclusions
├── Data Files
│   ├── data/
│   │   ├── input/                  # Input CSV files
│   │   │   └── images_to_download_and_upload.csv
│   │   ├── output/                 # Generated output files
│   │   │   ├── images_mapping.csv
│   │   │   ├── uploaded_files.json
│   │   │   └── local_files_alt_text.csv
│   │   ├── examples/               # Example files for reference
│   │   └── local_images/           # Downloaded/local image files
└── Documentation & CI/CD
    ├── README.md                    # Complete documentation
    ├── CHANGELOG.md                 # Version history and releases
    ├── PROJECT_RULES.md             # This document
    ├── CONTRIBUTING.md              # Contribution guidelines
    └── .github/                     # GitHub workflows & templates
```

### File Categories

#### **Core Application Files**
- `upload_files.py`: Legacy CloudFront-only application with Flask API
- `unified_upload.py`: New multi-provider upload system with command-line interface
- `alttext_ai.py`: Dedicated AltText.ai API client
- `setup.py`: Environment setup and dependency management

#### **Provider System**
- `upload_provider.py`: Abstract base class and provider factory
- `cloudfront_provider.py`: AWS CloudFront/S3 implementation
- `cloudinary_provider.py`: Cloudinary implementation with optimization
- `test_cloudinary.py`: Integration tests for Cloudinary provider

#### **Processing Scripts**
- `process_csv.sh`: User-friendly batch processing interface with provider selection
- Utility scripts for debugging and maintenance

#### **Configuration Files**
- `.env`: Sensitive configuration (API keys, credentials for both providers)
- `.env.example`: Template for environment setup with all provider options

#### **Data Files**
- Input files (CSV with URLs)
- Output files (mappings, alt text, provider-specific tracking)
- State files (tracking uploads across providers)

## 🔧 Core Components

### 1. Unified Upload System (`unified_upload.py`)

**Primary Functions:**
- `UnifiedUploader()`: Main class supporting both providers
- `upload_from_csv()`: Batch processing with provider selection
- `upload_from_local()`: Local file upload with optimization
- `test_connection()`: Provider connectivity testing

**Command Line Interface:**
- `--provider {cloudfront,cloudinary}`: Provider selection
- `--mode {local,csv,stats,list}`: Operation modes
- `--alt-text`: Enable AI alt text generation
- `--max-width`, `--quality`: Optimization parameters

**Key Features:**
- Provider-agnostic interface
- Automatic provider detection from environment
- Comprehensive error handling with provider-specific messages
- Progress tracking and detailed logging

### 2. Legacy CloudFront Application (`upload_files.py`)

**Primary Functions:**
- `upload_files()`: Local file upload with optimization
- `download_and_upload_from_csv()`: Batch processing from CSV
- `optimize_image()`: Image optimization and format conversion
- `upload_file_to_s3()`: S3 upload functionality

**Flask API Endpoints:**
- `POST /upload`: Single file upload
- `GET /files`: List uploaded files
- `GET /process-csv`: Batch CSV processing

**Key Features:**
- Legacy CloudFront-only functionality
- Complete Flask web interface
- Original optimization algorithms
- Backward compatibility maintained

### 3. AltText.ai Integration (`alttext_ai.py`)

**Classes:**
- `AltTextAI`: Main API client class

**Key Methods:**
- `generate_alt_text()`: Generate alt text for images
- `test_connection()`: Verify API connectivity
- `_poll_for_result()`: Handle asynchronous processing

**Features:**
- Provider-agnostic alt text generation
- Synchronous and asynchronous processing
- Keyword integration for SEO optimization
- Webhook support for large batches
- Robust error handling and retries

### 4. Setup & Utilities (`setup.py`)

**Functions:**
- Multi-provider dependency checking and installation
- Environment file creation with provider templates
- Connection testing for both Cloudinary and AWS
- Directory structure validation
- Provider configuration validation

## 🏗️ Provider Architecture

### Design Principles

#### **Provider Abstraction**
```python
# Base provider interface
class UploadProvider(ABC):
    @abstractmethod
    def upload_image(self, file_path: str, **kwargs) -> Tuple[bool, Optional[str], Optional[Dict]]
    
    @abstractmethod
    def upload_from_url(self, url: str, **kwargs) -> Tuple[bool, Optional[str], Optional[Dict]]
    
    @abstractmethod
    def test_connection(self) -> bool
```

#### **Factory Pattern**
```python
# Provider creation
class ProviderFactory:
    @staticmethod
    def create_provider(provider_name: str) -> UploadProvider:
        if provider_name == 'cloudinary':
            return CloudinaryProvider()
        elif provider_name == 'cloudfront':
            return CloudFrontProvider()
        else:
            raise ValueError(f"Unknown provider: {provider_name}")
```

### Provider Implementations

#### **Cloudinary Provider (`cloudinary_provider.py`)**

**Key Features:**
- Automatic format optimization (`format=auto`, `quality=auto`)
- Smart transformation parameters using SDK format
- Direct URL upload capabilities
- Built-in CDN delivery
- Real-time image transformations

**Configuration:**
```python
cloudinary.config(
    cloud_name=self.cloud_name,
    api_key=self.api_key,
    api_secret=self.api_secret,
    secure=True
)
```

**Transformation Parameters:**
```python
transformation_params = {
    "format": "auto",           # Automatic format selection
    "quality": "auto",          # Automatic quality optimization
    "gravity": "auto",          # Smart cropping
    "width": max_width,         # Width constraint
    "crop": "scale"            # Scaling method
}
```

#### **CloudFront Provider (`cloudfront_provider.py`)**

**Key Features:**
- S3 upload with CloudFront distribution
- Manual image optimization using Pillow
- Custom format selection logic
- ACL management for public access
- Traditional file-based upload workflow

**S3 Configuration:**
```python
s3_client = boto3.client(
    's3',
    aws_access_key_id=self.aws_access_key,
    aws_secret_access_key=self.aws_secret_key
)
```

**Upload Process:**
1. Download image to local storage
2. Optimize using Pillow (format, quality, resizing)
3. Upload to S3 bucket
4. Generate CloudFront URL
5. Clean up local files

### Provider Selection Logic

#### **Environment-Based Selection**
```python
# Auto-detection from environment
provider = os.getenv('UPLOAD_PROVIDER', 'auto')

if provider == 'auto':
    if all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY]):
        provider = 'cloudinary'
    elif all([AWS_ACCESS_KEY, S3_BUCKET]):
        provider = 'cloudfront'
```

#### **Command Line Override**
```python
# Explicit provider selection
python unified_upload.py --provider cloudinary --mode csv
python unified_upload.py --provider cloudfront --mode csv
```

#### **Configuration Validation**
```python
def validate_provider_config(provider_name: str) -> bool:
    if provider_name == 'cloudinary':
        return all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET])
    elif provider_name == 'cloudfront':
        return all([AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET, CLOUDFRONT_DOMAIN])
    return False
```

## 📝 Coding Standards

### Python Version Compatibility

#### **Target Versions**
- **Primary**: Python 3.13 (recommended for development)
- **Supported**: Python 3.9, 3.10, 3.11, 3.12, 3.13
- **Testing**: All supported versions in CI/CD

#### **Version-Specific Guidelines**
```python
# Use features available in Python 3.9+
from typing import Optional, Union, List, Dict, Tuple
from pathlib import Path

# Avoid features from Python 3.14+ (not yet stable)
# Use type hints compatible with Python 3.9+
def process_image(path: str | Path) -> bool:  # ❌ Union syntax (3.10+)
def process_image(path: Union[str, Path]) -> bool:  # ✅ Compatible with 3.9+
```

### Development Environment Setup

#### **Virtual Environment (Recommended)**
```python
# Create virtual environment with Python 3.13
python3.13 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Verify Python version
python --version  # Should show Python 3.13.x
```

#### **Development Dependencies**
```bash
# Core dependencies
pip install -r requirements.txt

# Development tools
pip install flake8 black isort mypy bandit safety
```

### Python Code Style

#### **Import Organization**
```python
# Standard library imports
import os
import json
import time
from pathlib import Path
from typing import Optional, Union, List, Dict, Tuple

# Third-party imports
import boto3
import requests
from PIL import Image

# Local imports
from alttext_ai import generate_alt_text
```

#### **Function Documentation**
```python
def optimize_image(image_path: str, max_width: Optional[int] = None, 
                  quality: int = 82, smart_format: bool = True) -> Tuple[bool, str]:
    """
    Optimize an image by resizing, adjusting quality, and choosing the best format
    
    Args:
        image_path (str): Path to the image file
        max_width (int, optional): Maximum width for resizing
        quality (int): JPEG/WebP quality (1-100)
        smart_format (bool): Enable smart format selection
        
    Returns:
        tuple: (success: bool, optimized_path: str)
        
    Raises:
        FileNotFoundError: If image file doesn't exist
        ValueError: If quality is not in valid range
    """
```

#### **Error Handling Pattern**
```python
try:
    # Main operation
    result = perform_operation()
    print(f"✅ Operation successful: {result}")
    return True, result
except SpecificException as e:
    print(f"❌ Specific error: {e}")
    return False, None
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    return False, None
```

#### **Logging Standards**
- Use emoji prefixes for visual clarity: ✅ ❌ 🔍 ⏳ 📄
- Include context in error messages
- Provide actionable feedback to users
- Use consistent formatting

### Configuration Management

#### **Environment Variables**
```python
# Required AWS Configuration
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
S3_BUCKET = os.getenv('S3_BUCKET')
CLOUDFRONT_DOMAIN = os.getenv('CLOUDFRONT_DOMAIN')

# Optional AltText.ai Configuration
ALTTEXT_AI_API_KEY = os.getenv('ALTTEXT_AI_API_KEY')
ALTTEXT_AI_KEYWORDS = os.getenv('ALTTEXT_AI_KEYWORDS', '')
```

#### **Default Values**
```python
# Use constants for default values
DEFAULT_QUALITY = 82
DEFAULT_MAX_WIDTH = None
SMART_FORMAT = True
```

## 📋 File Naming Conventions

### **Python Files**
- Use snake_case: `upload_files.py`, `alttext_ai.py`
- Descriptive names indicating purpose
- Avoid abbreviations unless widely understood

### **Data Files**
- CSV files: descriptive_purpose.csv
- JSON files: state_tracking.json
- Use underscores for multi-word names

### **Generated Files**
- Include timestamps: `image_1748441097.webp`
- Lowercase filenames for web compatibility
- Preserve original extensions when possible

### **Directory Structure**
- Use lowercase with underscores: `images_to_upload/`
- Descriptive directory names
- Separate input/output/state directories

## 🔐 Environment & Configuration

### **Required Environment Variables**

#### **Provider Selection**
```bash
# Provider Selection (Required)
UPLOAD_PROVIDER=cloudinary  # or 'cloudfront' or 'auto'
```

#### **Cloudinary Configuration (if using Cloudinary)**
```bash
# Cloudinary Credentials
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

#### **AWS Configuration (if using CloudFront/S3)**
```bash
# AWS Credentials
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
S3_BUCKET=your_s3_bucket_name
CLOUDFRONT_DOMAIN=your_cloudfront_domain
```

#### **AltText.ai Configuration (Optional for both providers)**
```bash
# AltText.ai Integration
ALTTEXT_AI_API_KEY=your_alttext_ai_api_key
ALTTEXT_AI_KEYWORDS=default,keywords,for,seo
ALTTEXT_AI_WEBHOOK_URL=your_webhook_url
```

### **Configuration Hierarchy**
1. Command line arguments (highest priority)
   - `--provider cloudinary` overrides environment
2. Environment variables
   - `UPLOAD_PROVIDER` for default provider
3. Auto-detection from available credentials
   - Cloudinary credentials → Use Cloudinary
   - AWS credentials → Use CloudFront
4. Default values in code (lowest priority)

### **Provider Auto-Detection Logic**
```python
def detect_provider() -> str:
    """Auto-detect available provider from environment"""
    explicit_provider = os.getenv('UPLOAD_PROVIDER')
    if explicit_provider and explicit_provider != 'auto':
        return explicit_provider
    
    # Auto-detect based on available credentials
    cloudinary_available = all([
        os.getenv('CLOUDINARY_CLOUD_NAME'),
        os.getenv('CLOUDINARY_API_KEY'),
        os.getenv('CLOUDINARY_API_SECRET')
    ])
    
    aws_available = all([
        os.getenv('AWS_ACCESS_KEY'),
        os.getenv('AWS_SECRET_KEY'),
        os.getenv('S3_BUCKET')
    ])
    
    if cloudinary_available and aws_available:
        return 'cloudinary'  # Prefer Cloudinary if both available
    elif cloudinary_available:
        return 'cloudinary'
    elif aws_available:
        return 'cloudfront'
    else:
        raise ValueError("No valid provider configuration found")
```

### **Security Requirements**
- Never commit `.env` files to version control
- Use `.env.example` as template for both providers
- Validate all environment variables on startup
- Provide clear error messages for missing configuration
- Support both providers in same environment file
- Rotate API keys regularly for both providers

### **Configuration Examples**

#### **Cloudinary-Only Setup**
```bash
# .env file for Cloudinary-only setup
UPLOAD_PROVIDER=cloudinary
CLOUDINARY_CLOUD_NAME=my_cloud_name
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=your_secret_key

# Optional AltText.ai
ALTTEXT_AI_API_KEY=your_alttext_api_key
```

#### **CloudFront-Only Setup**
```bash
# .env file for CloudFront-only setup
UPLOAD_PROVIDER=cloudfront
AWS_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
S3_BUCKET=my-images-bucket
CLOUDFRONT_DOMAIN=d123456789.cloudfront.net

# Optional AltText.ai
ALTTEXT_AI_API_KEY=your_alttext_api_key
```

#### **Multi-Provider Setup**
```bash
# .env file supporting both providers
UPLOAD_PROVIDER=auto  # or specify preferred provider

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=my_cloud_name
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=your_cloudinary_secret

# AWS Configuration
AWS_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
S3_BUCKET=my-images-bucket
CLOUDFRONT_DOMAIN=d123456789.cloudfront.net

# AltText.ai (shared by both providers)
ALTTEXT_AI_API_KEY=your_alttext_api_key
ALTTEXT_AI_KEYWORDS=product,lifestyle,modern
```

## 🔌 API Integration Guidelines

### **Multi-Provider Integration Strategy**

#### **Provider-Agnostic Interface**
```python
# Unified interface for all providers
class UploadProvider(ABC):
    @abstractmethod
    def upload_image(self, file_path: str, file_name: str, **kwargs) -> Tuple[bool, Optional[str], Optional[Dict]]:
        """Upload image file with optimization"""
        pass
    
    @abstractmethod
    def upload_from_url(self, source_url: str, **kwargs) -> Tuple[bool, Optional[str], Optional[Dict]]:
        """Upload image directly from URL"""
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """Test provider API connectivity"""
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Return provider identifier"""
        pass
```

### **Cloudinary Integration**

#### **Connection Testing**
```python
def test_connection(self) -> bool:
    """Test Cloudinary API connectivity using ping endpoint"""
    try:
        result = cloudinary.api.ping()
        print(f"✅ Cloudinary connection successful: {result}")
        return True
    except Exception as e:
        print(f"❌ Cloudinary connection failed: {e}")
        return False
```

#### **Transformation Parameters**
```python
# Use SDK-style parameters, not URL-style
transformation_params = {
    "format": "auto",        # Not "f_auto"
    "quality": "auto",       # Not "q_auto"
    "gravity": "auto",       # Not "g_auto"
    "width": max_width,      # Not "w_800"
    "crop": "scale"
}

# Apply to upload
upload_options = {
    "public_id": public_id,
    "folder": folder,
    "transformation": transformation_params  # Dict, not string
}
```

#### **Error Handling**
- Graceful degradation when API unavailable
- Clear user feedback about API status
- Retry mechanisms for transient failures
- Timeout handling for upload operations
- Provider-specific error message formatting

#### **Rate Limiting & Optimization**
- Respect Cloudinary's transformation limits
- Use direct URL uploads when possible
- Batch operations for efficiency
- Monitor account usage and quotas

### **AWS S3/CloudFront Integration**

#### **Connection Testing**
```python
def test_connection(self) -> bool:
    """Test AWS S3 connectivity"""
    try:
        s3_client.head_bucket(Bucket=self.s3_bucket)
        print(f"✅ S3 bucket '{self.s3_bucket}' accessible")
        return True
    except ClientError as e:
        print(f"❌ S3 connection failed: {e}")
        return False
```

#### **Upload Strategy**
- Use unique filenames with timestamps
- Handle ACL restrictions gracefully
- Implement retry logic for failed uploads
- Validate file uploads after completion
- Generate CloudFront URLs consistently

#### **Error Handling**
```python
try:
    s3_client.upload_file(file_path, S3_BUCKET, file_name)
    cloudfront_url = f"https://{CLOUDFRONT_DOMAIN}/{file_name}"
    return True, cloudfront_url
except ClientError as e:
    error_code = e.response['Error']['Code']
    if error_code == 'NoSuchBucket':
        print(f"❌ S3 bucket '{S3_BUCKET}' does not exist")
    elif error_code == 'AccessDenied':
        print(f"❌ Access denied to S3 bucket '{S3_BUCKET}'")
    else:
        print(f"❌ S3 upload failed: {e}")
    return False, None
```

### **AltText.ai Integration**

#### **Provider-Agnostic Integration**
```python
# Works with both Cloudinary and CloudFront URLs
def generate_alt_text_for_upload(image_url: str, provider: str) -> Optional[str]:
    """Generate alt text regardless of provider"""
    try:
        alt_text = generate_alt_text(
            image_url=image_url,
            keywords=os.getenv('ALTTEXT_AI_KEYWORDS', '')
        )
        print(f"✅ Alt text generated for {provider}: {alt_text}")
        return alt_text
    except Exception as e:
        print(f"❌ Alt text generation failed for {provider}: {e}")
        return None
```

#### **Connection Testing**
```python
def test_alttext_ai_connection() -> bool:
    """Test AltText.ai API connectivity without using external resources"""
    try:
        response = requests.get(
            f"{base_url}/jobs/test-connection-check",
            headers=headers,
            timeout=10
        )
        return response.status_code in [200, 202, 404]  # 404 is acceptable for test endpoint
    except Exception:
        return False
```

#### **Error Handling & Fallbacks**
- Continue upload process if alt text generation fails
- Provide meaningful error messages
- Support webhook-based processing for large batches
- Implement retry logic for temporary failures
- Graceful degradation when API is unavailable

## ⚠️ Error Handling Standards

### **Error Categories**

#### **User Errors**
- Missing configuration
- Invalid file formats
- Network connectivity issues
- Provide clear, actionable messages

#### **System Errors**
- API failures
- File system issues
- Memory/resource constraints
- Log detailed information for debugging

#### **Graceful Degradation**
- Continue processing when possible
- Disable optional features if unavailable
- Provide fallback mechanisms
- Maintain data integrity

### **Error Message Format**
```python
# Good error messages
print("❌ AltText.ai API connection failed. Alt text generation will be disabled.")
print("✅ Solution: Check your API key in .env file")
print("🔍 Test: Run `python setup.py` to verify connection")

# Include context and solutions
print(f"❌ Failed to upload {filename}: {error_details}")
print("🔄 Retrying with alternative method...")
```

## 📚 Documentation Standards

### **Code Documentation**

#### **Function Docstrings**
- Use Google-style docstrings
- Include parameter types and descriptions
- Document return values
- Provide usage examples for complex functions

#### **Inline Comments**
- Explain complex logic
- Document business rules
- Clarify non-obvious code
- Keep comments up-to-date

### **README Structure**
- Quick start section first
- Comprehensive usage examples
- Troubleshooting section
- Configuration reference
- API documentation

### **Change Documentation**
- Update version numbers
- Document breaking changes
- Provide migration guides
- Update examples and screenshots

## 🧪 Testing Guidelines

### **Multi-Provider Testing Strategy**

#### **Provider-Specific Test Suites**
```bash
# Test Cloudinary integration
python test_cloudinary.py

# Test unified system with Cloudinary
python unified_upload.py --provider cloudinary --mode csv

# Test unified system with CloudFront
python unified_upload.py --provider cloudfront --mode csv

# Test auto-detection
python unified_upload.py --mode csv  # Uses UPLOAD_PROVIDER or auto-detects
```

#### **Provider Isolation Testing**
```bash
# Test with only Cloudinary credentials
export CLOUDINARY_CLOUD_NAME=test_cloud
export CLOUDINARY_API_KEY=test_key
export CLOUDINARY_API_SECRET=test_secret
unset AWS_ACCESS_KEY AWS_SECRET_KEY

# Test with only AWS credentials
export AWS_ACCESS_KEY=test_access
export AWS_SECRET_KEY=test_secret
export S3_BUCKET=test_bucket
unset CLOUDINARY_CLOUD_NAME CLOUDINARY_API_KEY
```

### **Python Version Testing**

#### **Local Testing**
```bash
# Test with different Python versions (if available)
python3.9 unified_upload.py --provider cloudinary --mode stats
python3.10 unified_upload.py --provider cloudfront --mode stats
python3.11 unified_upload.py --provider cloudinary --mode stats
python3.12 unified_upload.py --provider cloudfront --mode stats
python3.13 unified_upload.py --provider cloudinary --mode stats
```

#### **CI/CD Testing**
- Automated testing on Python 3.9-3.13
- Matrix builds for all supported versions
- Provider-specific test environments
- Cross-provider compatibility validation

### **Manual Testing**

#### **Core Functionality Tests**
```bash
# Test provider connections
python -c "from cloudinary_provider import test_cloudinary_connection; test_cloudinary_connection()"
python -c "from cloudfront_provider import test_cloudfront_connection; test_cloudfront_connection()"

# Test AltText.ai integration
python -c "from alttext_ai import test_alttext_ai_connection; test_alttext_ai_connection()"

# Test unified upload system
python unified_upload.py --provider cloudinary --mode stats
python unified_upload.py --provider cloudfront --mode stats
```

#### **Provider-Specific Testing**

**Cloudinary Tests:**
```bash
# Test Cloudinary provider directly
python cloudinary_provider.py

# Test with various optimization settings
python unified_upload.py --provider cloudinary --mode csv --max-width 800 --quality 85

# Test alt text integration
python unified_upload.py --provider cloudinary --mode csv --alt-text
```

**CloudFront Tests:**
```bash
# Test legacy CloudFront system
python upload_files.py

# Test CloudFront via unified system
python unified_upload.py --provider cloudfront --mode csv

# Test Flask API (CloudFront only)
export FLASK_RUN=1
python upload_files.py &
curl -X POST -F "file=@test.jpg" http://localhost:5000/upload
```

#### **Cross-Provider Validation**
```bash
# Upload same image to both providers
export TEST_IMAGE="https://example.com/test-image.jpg"

# Upload to Cloudinary
python unified_upload.py --provider cloudinary --mode url --url "$TEST_IMAGE"

# Upload to CloudFront
python unified_upload.py --provider cloudfront --mode url --url "$TEST_IMAGE"

# Compare results and optimization
```

### **Integration Testing**

#### **Provider Factory Testing**
```python
from upload_provider import ProviderFactory

# Test factory with all providers
cloudinary_provider = ProviderFactory.create_provider('cloudinary')
cloudfront_provider = ProviderFactory.create_provider('cloudfront')

# Test provider identification
assert cloudinary_provider.get_provider_name() == 'cloudinary'
assert cloudfront_provider.get_provider_name() == 'cloudfront'
```

#### **Configuration Testing**
```bash
# Test with minimal configuration
cp .env.example .env.test
echo "UPLOAD_PROVIDER=cloudinary" >> .env.test
echo "CLOUDINARY_CLOUD_NAME=test" >> .env.test

# Test configuration validation
python setup.py
```

### **Error Scenario Testing**

#### **Provider Unavailability**
```bash
# Test with invalid Cloudinary credentials
export CLOUDINARY_API_KEY=invalid_key
python unified_upload.py --provider cloudinary --mode stats

# Test with invalid AWS credentials
export AWS_ACCESS_KEY=invalid_key
python unified_upload.py --provider cloudfront --mode stats
```

#### **Network Failure Simulation**
```bash
# Test with unreachable endpoints (modify hosts file or use firewall rules)
# Verify graceful degradation and error messages
```

#### **Missing Dependencies**
```bash
# Test without cloudinary package
pip uninstall cloudinary
python unified_upload.py --provider cloudinary --mode stats

# Test without boto3
pip uninstall boto3
python unified_upload.py --provider cloudfront --mode stats
```

### **Performance Testing**

#### **Provider Performance Comparison**
```bash
# Time uploads with different providers
time python unified_upload.py --provider cloudinary --mode csv
time python unified_upload.py --provider cloudfront --mode csv

# Compare optimization results
python unified_upload.py --provider cloudinary --mode stats
python unified_upload.py --provider cloudfront --mode stats
```

#### **Batch Upload Testing**
```bash
# Test with large CSV files
# Create test CSV with 100+ image URLs
python unified_upload.py --provider cloudinary --mode csv --verbose
```

## 🔒 Security Guidelines

### **Credential Management**
- Store sensitive data in `.env` files
- Never commit credentials to version control
- Use environment variables in production
- Rotate API keys regularly

### **Input Validation**
- Validate all user inputs
- Sanitize file names
- Check file types and sizes
- Prevent path traversal attacks

### **API Security**
- Use HTTPS for all API calls
- Implement request timeouts
- Validate API responses
- Handle authentication errors gracefully

## ⚡ Performance Guidelines

### **Image Processing**
- Use efficient image libraries (Pillow)
- Implement smart format selection
- Optimize compression settings
- Process images in parallel when possible

### **API Usage**
- Batch API requests when possible
- Implement caching for repeated requests
- Use connection pooling
- Monitor API rate limits

### **File Operations**
- Use streaming for large files
- Implement progress tracking
- Clean up temporary files
- Optimize disk I/O operations

## 🚀 Deployment Guidelines

### **Environment Setup**
1. Install Python 3.9+ (recommended: 3.13): `python3.13 --version`
2. Create virtual environment: `python3.13 -m venv venv`
3. Activate virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run setup script: `python setup.py`
6. Configure environment variables
7. Test all integrations

### **Production Considerations**
- Use production-grade WSGI server for Flask API
- Implement proper logging
- Set up monitoring and alerting
- Configure backup strategies

### **Scaling Considerations**
- Implement queue-based processing for large batches
- Use distributed storage for temporary files
- Consider containerization for deployment
- Implement health checks

## 📝 Change Management

### **Git Workflow & Branch Protection**

#### **Branching Strategy**

**🚫 NEVER COMMIT DIRECTLY TO MAIN BRANCH**

All development must follow a feature branch workflow:

```bash
# 1. ALWAYS START FROM LATEST MAIN
git checkout main
git pull origin main

# 2. CREATE FEATURE BRANCH WITH DESCRIPTIVE NAME
git checkout -b feature/cloudinary-optimization-improvements
git checkout -b fix/provider-auto-detection-bug
git checkout -b docs/update-installation-guide
git checkout -b refactor/provider-factory-pattern

# 3. MAKE YOUR CHANGES AND COMMIT
git add .
git commit -m "feat: improve Cloudinary transformation parameters"

# 4. PUSH FEATURE BRANCH
git push origin feature/cloudinary-optimization-improvements

# 5. CREATE PULL REQUEST (NEVER MERGE DIRECTLY)
```

#### **Branch Naming Conventions**

Use descriptive prefixes for all branches:

- **`feature/`** - New functionality or enhancements
  - `feature/multi-provider-support`
  - `feature/alt-text-generation`
  - `feature/batch-upload-optimization`

- **`fix/`** - Bug fixes and patches
  - `fix/cloudinary-transformation-bug`
  - `fix/env-variable-detection`
  - `fix/memory-leak-in-batch-processing`

- **`docs/`** - Documentation updates
  - `docs/update-readme-multi-provider`
  - `docs/add-troubleshooting-guide`
  - `docs/provider-comparison-table`

- **`refactor/`** - Code refactoring without new features
  - `refactor/provider-architecture`
  - `refactor/error-handling-system`
  - `refactor/configuration-management`

- **`chore/`** - Maintenance tasks
  - `chore/update-dependencies`
  - `chore/improve-ci-pipeline`
  - `chore/cleanup-unused-files`

#### **Pull Request Requirements**

**ALL CHANGES MUST GO THROUGH PULL REQUEST REVIEW:**

1. **PR Title Format**:
   ```
   feat: add Cloudinary auto-optimization support
   fix: resolve provider detection in unified uploader
   docs: update installation guide for multi-provider setup
   refactor: implement factory pattern for providers
   ```

2. **PR Description Template**:
   ```markdown
   ## Summary
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Refactoring
   - [ ] Performance improvement

   ## Testing
   - [ ] Unit tests pass
   - [ ] Integration tests pass
   - [ ] Manual testing completed
   - [ ] Provider tests pass (Cloudinary/CloudFront)

   ## Documentation
   - [ ] README.md updated
   - [ ] PROJECT_RULES.md updated
   - [ ] CHANGELOG.md updated
   - [ ] Code comments added

   ## Breaking Changes
   - [ ] No breaking changes
   - [ ] Breaking changes documented in CHANGELOG.md

   ## Checklist
   - [ ] Pre-commit checks pass (`./pre_commit_check.sh`)
   - [ ] Code follows project standards
   - [ ] Tests added for new functionality
   - [ ] Documentation updated
   ```

3. **Required Reviews**:
   - **1 approving review** minimum for standard changes
   - **2 approving reviews** for breaking changes or major features
   - **Author cannot approve their own PR**

4. **Automated Checks**:
   - All CI/CD tests must pass
   - Pre-commit validation required
   - No merge conflicts with main
   - Branch must be up-to-date with main

#### **Branch Protection Rules**

Configure the following protection rules on the main branch:

```yaml
# GitHub Branch Protection Settings
main:
  protection_rules:
    required_status_checks:
      strict: true
      checks:
        - "ci/github-actions"
        - "pre-commit-validation"
        - "provider-tests"
    enforce_admins: false
    required_pull_request_reviews:
      required_approving_review_count: 1
      dismiss_stale_reviews: true
      require_code_owner_reviews: false
      require_last_push_approval: true
    restrictions: null
    allow_force_pushes: false
    allow_deletions: false
```

#### **Commit Message Standards**

Follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

```bash
# Format: <type>(<scope>): <description>

# Examples:
feat(cloudinary): add automatic format optimization
fix(provider): resolve auto-detection logic bug
docs(readme): update multi-provider setup guide
refactor(upload): implement factory pattern for providers
test(cloudinary): add integration tests for SDK
chore(deps): update boto3 to latest version
perf(optimization): improve image processing speed
style(format): fix code formatting issues
```

**Commit Types:**
- **feat**: New feature or functionality
- **fix**: Bug fix
- **docs**: Documentation changes
- **refactor**: Code refactoring without feature changes
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependency updates
- **perf**: Performance improvements
- **style**: Code style/formatting changes
- **ci**: CI/CD pipeline changes

#### **Code Review Guidelines**

**For Reviewers:**
- Review within 24 hours of PR creation
- Check for adherence to project standards
- Verify tests cover new functionality
- Ensure documentation is updated
- Test provider-specific changes locally
- Verify backward compatibility

**For Authors:**
- Address all review feedback
- Update PR description with changes
- Re-request review after changes
- Ensure CI/CD passes before requesting review
- Provide clear explanations for complex changes

#### **Hotfix Process**

For critical production issues:

```bash
# 1. Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-provider-connection-fix

# 2. Make minimal fix
# Keep changes as small as possible

# 3. Test thoroughly
./pre_commit_check.sh
python test_cloudinary.py
python unified_upload.py --mode stats

# 4. Create urgent PR
# Mark as "urgent" and request immediate review

# 5. After merge, ensure fix is included in next feature releases
```

#### **Release Workflow**

```bash
# 1. Create release branch from main
git checkout -b release/v2.1.0

# 2. Update version numbers
# - CHANGELOG.md
# - setup.py (if applicable)
# - README.md version badges

# 3. Final testing
./pre_commit_check.sh
python test_cloudinary.py
python unified_upload.py --provider cloudinary --mode csv
python unified_upload.py --provider cloudfront --mode csv

# 4. Create release PR
# 5. After merge, create and push git tag
git tag -a v2.1.0 -m "Release v2.1.0 - Enhanced multi-provider support"
git push origin v2.1.0
```

### **Pre-Commit Checks**

**MANDATORY: All commits must pass pre-commit validation**

```bash
# Before every commit
./pre_commit_check.sh

# The script will:
# 1. Run code formatting (black, isort)
# 2. Check linting (flake8)
# 3. Run security checks (bandit, safety)
# 4. Validate imports and functionality
# 5. Check documentation completeness
```

### **Emergency Procedures**

**If main branch is accidentally compromised:**

1. **Immediate Actions**:
   ```bash
   # Revert problematic commit
   git revert <commit-hash>
   git push origin main
   ```

2. **Communication**:
   - Notify all team members immediately
   - Create incident report
   - Document root cause and prevention

3. **Prevention**:
   - Review and strengthen branch protection
   - Audit repository access permissions
   - Additional training on Git workflow

### **Repository Access Management**

**Permission Levels:**
- **Admin**: Repository owners only
- **Maintainer**: Core contributors with merge rights
- **Developer**: Contributors with PR creation rights
- **Read**: Documentation contributors

**Access Review:**
- Quarterly review of repository access
- Remove access for inactive contributors
- Document access rationale
- Use principle of least privilege

## 🏷️ GitHub Releases & Git Tagging

### **Key Concepts**

#### **CHANGELOG.md vs GitHub Releases**
- `CHANGELOG.md` file does **NOT** automatically create GitHub releases
- GitHub releases are separate entities tied to git tags
- Both should be maintained for comprehensive version history

#### **Git Tags as Release Triggers**
- Git tags serve as the foundation for GitHub releases
- Pushing tags triggers automated release workflows
- Tags should follow semantic versioning: `v1.0.0`, `v1.1.2`, etc.

### **Automated Release Workflow**

#### **Workflow Location**
`.github/workflows/release.yml` - Automated GitHub release creation

#### **Trigger Mechanism**
```yaml
on:
  push:
    tags:
      - 'v*.*.*'  # Matches v1.0.0, v1.1.2, etc.
```

#### **Workflow Features**
- Extracts release notes from `CHANGELOG.md`
- Creates downloadable archives (.tar.gz and .zip)
- Validates release contents before publishing
- Supports Python 3.9-3.13 compatibility testing

### **Release Creation Process**

#### **Manual Release Steps**
```bash
# 1. Update CHANGELOG.md with new version
# 2. Commit and push changes
git add CHANGELOG.md
git commit -m "Update CHANGELOG for v1.2.0"
git push origin main

# 3. Create and push git tag
git tag -a v1.2.0 -m "Release v1.2.0 - New features and improvements"
git push origin v1.2.0

# 4. GitHub Action automatically creates the release
```

#### **Tag Naming Convention**
- Format: `v{MAJOR}.{MINOR}.{PATCH}`
- Examples: `v1.0.0`, `v1.1.2`, `v2.0.0`
- Use semantic versioning principles
- Include descriptive tag messages

### **CHANGELOG.md Integration**

#### **Format for Automated Extraction**
```markdown
## [1.2.0] - 2025-01-15

### Added
- New feature descriptions
- API endpoint additions

### Changed
- Modified functionality
- Updated dependencies

### Fixed
- Bug fixes and improvements
```

#### **Release Notes Extraction**
The workflow automatically extracts content between version headers:
- Looks for `## [version]` headers
- Extracts content until next version header
- Uses extracted content as GitHub release notes

### **Release Archive Contents**

#### **Included Files**
- All Python source files (`*.py`)
- Shell scripts (`*.sh`)
- Documentation files (`*.md`)
- Configuration templates (`.env.example`)
- Requirements file (`requirements.txt`)
- License file (`LICENSE`)
- Data directory structure (`data/`)

#### **Excluded Files**
- Environment files (`.env`)
- Git metadata (`.git/`)
- Virtual environments (`venv/`)
- IDE configurations
- Temporary files

### **Release Validation**

#### **Automated Checks**
- Core files existence validation
- Python import testing
- Archive integrity verification
- Cross-platform compatibility (tar.gz + zip)

#### **Manual Verification**
After automated release creation:
1. Check GitHub Releases page
2. Verify release notes content
3. Test downloadable archives
4. Confirm release assets are present

### **Troubleshooting Releases**

#### **Common Issues**

**No Release Created**
- Check GitHub Actions for workflow errors
- Verify tag format matches `v*.*.*` pattern
- Ensure workflow file is in correct location

**Empty Release Notes**
- Verify CHANGELOG.md format matches expected structure
- Check version header format: `## [version] - date`
- Ensure content exists between version headers

**Missing Files in Archive**
- Check workflow file patterns for included files
- Verify file paths and naming conventions
- Review archive creation step logs

#### **Debugging Commands**
```bash
# Check existing tags
git tag --list

# View tag details
git show v1.1.2

# Check GitHub Actions status
# Visit: https://github.com/username/repo/actions

# Test CHANGELOG extraction locally
awk "/^## \[.*v1.1.2.*\]/{flag=1; next} /^## \[/{if(flag) exit} flag && /^### |^- |^[A-Z]/ {print}" CHANGELOG.md
```

### **Best Practices**

#### **Pre-Release Checklist**
- [ ] Update `CHANGELOG.md` with comprehensive notes
- [ ] Test all functionality in target Python versions
- [ ] Verify configuration examples are current
- [ ] Update version numbers in relevant files
- [ ] Test release workflow in development environment

#### **Release Communication**
- Use clear, descriptive release titles
- Include migration notes for breaking changes
- Highlight major new features
- Provide links to detailed documentation
- Acknowledge contributors when applicable

#### **Version Strategy**
- **MAJOR**: Breaking changes, major new features
- **MINOR**: New features, backwards-compatible
- **PATCH**: Bug fixes, minor improvements
- **Pre-release**: Alpha/beta versions (v1.0.0-alpha.1)

### **Integration with Project Workflow**

#### **Development Cycle**
1. Feature development and testing
2. Update documentation and CHANGELOG.md
3. Code review and merge to main
4. Create git tag for release
5. Automated release creation via GitHub Actions
6. Manual verification and communication

#### **Hotfix Process**
```bash
# For urgent fixes
git checkout main
# Make fixes
git commit -m "hotfix: critical bug fix"
git push origin main
git tag -a v1.1.3 -m "Hotfix v1.1.3 - Critical bug fix"
git push origin v1.1.3
```

## 🔄 Living Document Updates

### **When to Update This Document**
- Adding new features or components
- Changing coding standards or conventions
- Updating dependencies or integrations
- Modifying project structure
- Learning from production issues

### **Update Process**
1. Identify changes needed
2. Update relevant sections
3. Review with team if applicable
4. Document significant changes in [CHANGELOG.md](CHANGELOG.md)

### **Version History**
All version history and significant changes are tracked in [CHANGELOG.md](CHANGELOG.md). This document focuses on current standards and guidelines rather than historical changes.

---

**Note**: This document should be consulted before making any significant changes to the codebase. When in doubt, follow the patterns established in existing code and update this document to reflect any new conventions.

### **Example: Proper Workflow for Future Changes**

**How the multi-provider refactoring should have been done:**

```bash
# 1. Start from main
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b refactor/multi-provider-architecture

# 3. Make incremental changes with focused commits
git add upload_provider.py
git commit -m "feat(provider): add abstract provider interface and factory"

git add cloudinary_provider.py
git commit -m "feat(cloudinary): implement Cloudinary provider with SDK integration"

git add cloudfront_provider.py
git commit -m "refactor(cloudfront): extract CloudFront logic into provider class"

git add unified_upload.py
git commit -m "feat(unified): add unified upload interface for multi-provider support"

git add test_cloudinary.py
git commit -m "test(cloudinary): add comprehensive integration tests"

# 4. Update documentation
git add README.md PROJECT_RULES.md CHANGELOG.md
git commit -m "docs: update documentation for multi-provider architecture"

git add .github/PULL_REQUEST_TEMPLATE.md .github/workflows/ci.yml
git commit -m "ci: update templates and workflows for multi-provider testing"

# 5. Run pre-commit checks
./pre_commit_check.sh

# 6. Push feature branch
git push origin refactor/multi-provider-architecture

# 7. Create Pull Request
# - Use descriptive title: "refactor: implement multi-provider architecture with Cloudinary support"
# - Fill out PR template completely
# - Request reviews from maintainers
# - Ensure all CI checks pass

# 8. Address review feedback
# Make changes based on feedback, commit with descriptive messages

# 9. After approval, maintainer merges with "Squash and merge" or "Create merge commit"
```

**Benefits of This Approach:**
- ✅ **Clear history**: Each commit has a focused purpose
- ✅ **Reviewable**: Changes can be reviewed incrementally
- ✅ **Rollback-friendly**: Individual features can be reverted if needed
- ✅ **Documentation**: Commit messages tell the story of the changes
- ✅ **Testing**: CI validates each push to the branch
- ✅ **Collaboration**: Multiple developers can contribute to the branch

**For Future Major Features:**
Always use this workflow instead of direct commits to main. Even for solo projects, this approach maintains code quality and provides a safety net. 