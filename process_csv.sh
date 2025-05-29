#!/bin/bash

# Image Upload Utility - Interactive CSV Processor
# This script provides an interactive interface for processing images from CSV files
# Supports both CloudFront/S3 and Cloudinary providers

echo "🚀 Image Upload Utility - CSV Processor"
echo "======================================================"

# Check if input file exists
INPUT_FILE="data/input/images_to_download_and_upload.csv"
if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ Input file not found: $INPUT_FILE"
    echo ""
    echo "📋 Please create the input file with your image URLs:"
    echo "   mkdir -p data/input"
    echo "   echo 'URL' > $INPUT_FILE"
    echo "   echo 'https://example.com/your-image.jpg' >> $INPUT_FILE"
    echo ""
    echo "📄 Example files are available in data/examples/"
    exit 1
fi

echo "📄 Input file: $INPUT_FILE"
echo "📊 Output files:"
echo "   - data/output/images_mapping.csv"
echo "   - data/output/uploaded_files.json"
echo "   - data/output/local_files_alt_text.csv (if alt text is generated)"
echo ""

# Count URLs in input file
URL_COUNT=$(tail -n +2 "$INPUT_FILE" | grep -v '^#' | grep -v '^$' | wc -l | tr -d ' ')
echo "🔍 Found $URL_COUNT image URLs to process"
echo ""

# Prompt for provider selection
echo "🌐 Select upload provider:"
echo "   1) CloudFront/S3 (AWS)"
echo "   2) Cloudinary"
echo "   3) Auto-detect from environment (UPLOAD_PROVIDER)"
echo -n "Enter choice (1-3, default: 3): "
read provider_choice

case $provider_choice in
    1)
        PROVIDER="cloudfront"
        echo "☁️  Using CloudFront/S3 provider"
        ;;
    2)
        PROVIDER="cloudinary"
        echo "🌐 Using Cloudinary provider"
        ;;
    *)
        PROVIDER=""
        echo "🔧 Using provider from environment configuration"
        ;;
esac

echo ""

# Prompt for max width
echo -n "Enter max width (leave empty for no resizing): "
read max_width

# Prompt for quality
echo -n "Enter quality (1-100, leave empty for default 82): "
read quality

# Prompt for smart format
echo -n "Use smart format conversion to optimize file size? (y/n, leave empty for yes): "
read smart_format

# Prompt for alt text generation
echo -n "Generate alt text for images using AltText.ai? (y/n, leave empty for no): "
read generate_alt_text

# Prompt for alt text keywords if alt text generation is enabled
alt_text_keywords=""
if [[ "$generate_alt_text" =~ ^[Yy] ]]; then
    echo -n "Enter keywords for SEO optimization (optional, leave empty for none): "
    read alt_text_keywords
fi

# Prompt for verbose mode
echo -n "Enable verbose output for debugging? (y/n, leave empty for no): "
read verbose_mode

echo ""
echo "🔄 Processing configuration:"
echo "   Provider: ${PROVIDER:-'Auto-detect'}"
echo "   Max width: ${max_width:-'No resizing'}"
echo "   Quality: ${quality:-'82 (default)'}"
echo "   Smart format: ${smart_format:-'Yes (default)'}"
echo "   Alt text: ${generate_alt_text:-'No (default)'}"
if [[ "$generate_alt_text" =~ ^[Yy] ]] && [[ -n "$alt_text_keywords" ]]; then
    echo "   Keywords: $alt_text_keywords"
fi
echo "   Verbose: ${verbose_mode:-'No (default)'}"
echo ""

# Build command line arguments
CMD_ARGS=()

# Add provider if specified
if [[ -n "$PROVIDER" ]]; then
    CMD_ARGS+=(--provider "$PROVIDER")
fi

# Add mode for CSV processing
CMD_ARGS+=(--mode csv)

# Add max width if specified
if [[ -n "$max_width" ]]; then
    CMD_ARGS+=(--max-width "$max_width")
fi

# Add quality if specified
if [[ -n "$quality" ]]; then
    CMD_ARGS+=(--quality "$quality")
fi

# Add smart format option
if [[ "$smart_format" =~ ^[Nn] ]]; then
    CMD_ARGS+=(--no-smart-format)
fi

# Add alt text options
if [[ "$generate_alt_text" =~ ^[Yy] ]]; then
    CMD_ARGS+=(--alt-text)
    if [[ -n "$alt_text_keywords" ]]; then
        CMD_ARGS+=(--alt-text-keywords "$alt_text_keywords")
    fi
fi

# Confirmation prompt
echo "⚡ Ready to process $URL_COUNT URLs"
echo -n "Proceed with upload? (y/n): "
read confirm

if [[ ! "$confirm" =~ ^[Yy] ]]; then
    echo "❌ Upload cancelled by user"
    exit 0
fi

echo ""
echo "🚀 Starting upload process..."
echo "=============================================="

# Set verbose output if requested
if [[ "$verbose_mode" =~ ^[Yy] ]]; then
    set -x
fi

# Execute the unified upload script
if command -v python3 &> /dev/null; then
    python3 unified_upload.py "${CMD_ARGS[@]}"
    EXIT_CODE=$?
else
    python unified_upload.py "${CMD_ARGS[@]}"
    EXIT_CODE=$?
fi

# Disable verbose mode
set +x

echo ""
echo "=============================================="

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Upload process completed successfully!"
    echo ""
    echo "📊 Results:"
    echo "   - URL mappings: data/output/images_mapping.csv"
    echo "   - Upload tracking: data/output/uploaded_files.json"
    
    # Check if alt text file was generated
    if [ -f "data/output/local_files_alt_text.csv" ]; then
        echo "   - Alt text: data/output/local_files_alt_text.csv"
    fi
    
    echo ""
    echo "📈 View statistics:"
    echo "   python unified_upload.py --mode stats"
    echo ""
    echo "📁 List uploaded files:"
    echo "   python unified_upload.py --mode list"
else
    echo "❌ Upload process failed with exit code $EXIT_CODE"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "   1. Check your provider credentials in .env file"
    echo "   2. Verify internet connection"
    echo "   3. Run setup: python setup.py"
    echo "   4. Check logs above for specific error messages"
fi

echo "" 