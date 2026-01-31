import argparse
import csv
import json
import os
import tempfile
import time
import urllib.parse

import boto3
import requests
import werkzeug.utils
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from PIL import Image

# Optional: enable AVIF read/write support when pillow-avif-plugin is installed
try:
    import pillow_avif  # noqa: F401
except Exception:
    pass

# Load environment variables
load_dotenv()


# Try to import AltText.ai - it's optional
try:
    from alttext_ai import generate_alt_text, test_alttext_ai_connection

    ALTTEXT_AI_AVAILABLE = True
except ImportError:
    ALTTEXT_AI_AVAILABLE = False
    print(
        "📄 AltText.ai module not available. Install python-dotenv to enable alt text generation."
    )

# Configuration
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
S3_BUCKET = os.getenv("S3_BUCKET")
CLOUDFRONT_DOMAIN = os.getenv("CLOUDFRONT_DOMAIN")
# Remove the path prefix
# CLOUDFRONT_PATH_PREFIX = 'images/'  # This should match your CloudFront/S3 configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "data", "local_images")
JSON_FILE = os.path.join(
    os.path.dirname(__file__), "data", "output", "uploaded_files.json"
)
CSV_INPUT_FILE = os.path.join(
    os.path.dirname(__file__), "data", "input", "images_to_download_and_upload.csv"
)
CSV_OUTPUT_FILE = os.path.join(
    os.path.dirname(__file__), "data", "output", "images_mapping.csv"
)
LOCAL_ALT_TEXT_FILE = os.path.join(
    os.path.dirname(__file__), "data", "output", "local_files_alt_text.csv"
)

# Default optimization parameters
DEFAULT_QUALITY = 82
DEFAULT_MAX_WIDTH = None  # None means don't resize
SMART_FORMAT = True  # Enable smart format conversion by default

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize S3 client
s3_client = boto3.client(
    "s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY
)

# Initialize Flask app
app = Flask(__name__)


def load_uploaded_files():
    """Load the JSON file with already uploaded files"""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    return {}


def save_uploaded_files(uploaded_files):
    """Save the uploaded files data to JSON"""
    with open(JSON_FILE, "w") as f:
        json.dump(uploaded_files, f, indent=2)


def get_best_format(img, original_format, original_path, quality=DEFAULT_QUALITY):
    """Determine the best format (JPEG, PNG, WebP, AVIF) based on file size"""
    formats_to_try = ["JPEG", "PNG", "WEBP", "AVIF"]

    # Skip testing if the image has transparency and we're considering JPEG
    has_transparency = img.mode in ("RGBA", "LA") or (
        img.mode == "P" and "transparency" in img.info
    )

    # Store results for each format
    results = {}

    # Create a temporary directory for format testing
    with tempfile.TemporaryDirectory() as temp_dir:
        for fmt in formats_to_try:
            # Skip JPEG if image has transparency
            if fmt == "JPEG" and has_transparency:
                continue

            # Prepare image for this format
            test_img = img.copy()
            if fmt == "JPEG" and test_img.mode in ("RGBA", "P", "LA"):
                test_img = test_img.convert("RGB")

            # Create a temporary file for this format
            temp_file = os.path.join(temp_dir, f"test.{fmt.lower()}")

            try:
                # Save in this format
                if fmt == "JPEG":
                    test_img.save(temp_file, format=fmt, quality=quality, optimize=True)
                elif fmt == "PNG":
                    test_img.save(temp_file, format=fmt, optimize=True)
                elif fmt == "WEBP":
                    test_img.save(temp_file, format=fmt, quality=quality, method=6)
                elif fmt == "AVIF":
                    # AVIF uses a quality parameter similar to WebP.
                    # pillow-avif-plugin adds support for saving AVIF via Pillow.
                    test_img.save(temp_file, format=fmt, quality=quality)

                # Get file size
                file_size = os.path.getsize(temp_file)
                results[fmt] = {"size": file_size, "path": temp_file}

                print(f"Format {fmt}: {file_size/1024:.1f} KB")
            except Exception as e:
                print(f"Error testing format {fmt}: {e}")

    # If no formats worked, return the original format
    if not results:
        return original_format, original_path

    # Find the format with the smallest file size
    best_format = min(results.items(), key=lambda x: x[1]["size"])
    fmt_name, fmt_info = best_format

    print(f"Best format is {fmt_name} with size {fmt_info['size']/1024:.1f} KB")

    # Determine the appropriate file extension
    if fmt_name == "JPEG":
        extension = ".jpg"
    elif fmt_name == "PNG":
        extension = ".png"
    elif fmt_name == "WEBP":
        extension = ".webp"
    elif fmt_name == "AVIF":
        extension = ".avif"
    else:
        extension = os.path.splitext(original_path)[1]

    # Create a new path with the appropriate extension
    new_path = os.path.splitext(original_path)[0] + extension

    # If the best format is different from the original, save the image in the new format
    if fmt_name != original_format:
        # Prepare image for this format
        save_img = img.copy()
        if fmt_name == "JPEG" and save_img.mode in ("RGBA", "P", "LA"):
            save_img = save_img.convert("RGB")

        # Save in the best format
        if fmt_name == "JPEG":
            save_img.save(new_path, format=fmt_name, quality=quality, optimize=True)
        elif fmt_name == "PNG":
            save_img.save(new_path, format=fmt_name, optimize=True)
        elif fmt_name == "WEBP":
            save_img.save(new_path, format=fmt_name, quality=quality, method=6)
        elif fmt_name == "AVIF":
            save_img.save(new_path, format=fmt_name, quality=quality)

        print(f"Converted image from {original_format} to {fmt_name}")

        # If the new path is different from the original, remove the original
        if new_path != original_path and os.path.exists(original_path):
            os.remove(original_path)

    return fmt_name, new_path


def optimize_image(
    image_path, max_width=None, quality=DEFAULT_QUALITY, smart_format=SMART_FORMAT
):
    """Optimize an image by resizing, adjusting quality, and choosing the best format"""
    try:
        # Open the image
        img = Image.open(image_path)

        # Get original format
        original_format = img.format
        if not original_format:
            # Try to determine format from file extension
            ext = os.path.splitext(image_path)[1].lower()
            if ext in [".jpg", ".jpeg"]:
                original_format = "JPEG"
            elif ext == ".png":
                original_format = "PNG"
            elif ext == ".gif":
                original_format = "GIF"
            elif ext == ".webp":
                original_format = "WEBP"
            elif ext == ".avif":
                original_format = "AVIF"
            else:
                original_format = "JPEG"  # Default

        # Get original dimensions
        original_width, original_height = img.size

        # Resize if max_width is specified and the image is wider than max_width
        if max_width and original_width > max_width:
            # Calculate new height to maintain aspect ratio
            new_height = int(original_height * (max_width / original_width))
            img = img.resize((max_width, new_height), Image.LANCZOS)
            print(
                f"Resized image from {original_width}x{original_height} to {max_width}x{new_height}"
            )

        # Determine the format based on file extension
        file_ext = os.path.splitext(image_path)[1].lower()
        if file_ext in [".jpg", ".jpeg"]:
            format_name = "JPEG"
        elif file_ext == ".png":
            format_name = "PNG"
        elif file_ext == ".gif":
            format_name = "GIF"
        elif file_ext == ".webp":
            format_name = "WEBP"
        elif file_ext == ".avif":
            format_name = "AVIF"
        else:
            format_name = "JPEG"  # Default to JPEG

        # If smart format is enabled and the image is not a GIF, find the best format
        if smart_format and format_name != "GIF":
            format_name, image_path = get_best_format(
                img, format_name, image_path, quality
            )

            # If the format changed, we need to reopen the image
            if format_name != original_format:
                img = Image.open(image_path)
        else:
            # Save the optimized image in the original format
            if format_name == "JPEG":
                # Convert to RGB if necessary
                if img.mode in ("RGBA", "P", "LA"):
                    img = img.convert("RGB")
                img.save(image_path, format=format_name, quality=quality, optimize=True)
            elif format_name == "PNG":
                img.save(image_path, format=format_name, optimize=True)
            elif format_name == "WEBP":
                img.save(image_path, format=format_name, quality=quality, method=6)
            elif format_name == "AVIF":
                img.save(image_path, format=format_name, quality=quality)
            elif format_name == "GIF":
                # GIFs are saved as-is to preserve animation
                pass
            else:
                # Default to JPEG for unknown formats
                if img.mode in ("RGBA", "P", "LA"):
                    img = img.convert("RGB")
                img.save(image_path, format="JPEG", quality=quality, optimize=True)

        # Get file size after optimization
        file_size = os.path.getsize(image_path)
        print(
            f"Optimized image. Format: {format_name}, Quality: {quality}, Size: {file_size/1024:.1f} KB"
        )

        return True, image_path
    except Exception as e:
        print(f"Error optimizing image: {e}")
        return False, image_path


def upload_file_to_s3(file_path, file_name, add_timestamp=True):
    """Upload a file to S3"""
    try:
        # Lowercase the file name and optionally add Unix timestamp
        file_name = file_name.lower()
        if add_timestamp:
            timestamp = int(time.time())
            file_name_to_upload = f"{os.path.splitext(file_name)[0]}_{timestamp}{os.path.splitext(file_name)[1]}"
        else:
            file_name_to_upload = file_name

        # Upload without ACL since the bucket blocks public ACLs
        # CloudFront will handle public access
        s3_client.upload_file(file_path, S3_BUCKET, file_name_to_upload)
        print(f"Successfully uploaded {file_name_to_upload}")
        return True, file_name_to_upload
    except ClientError as e:
        print(f"Error uploading {file_name}: {e}")
        return False, None


def upload_files(
    max_width=DEFAULT_MAX_WIDTH,
    quality=DEFAULT_QUALITY,
    smart_format=SMART_FORMAT,
    add_timestamp=True,
    generate_alt_text_flag=False,
    alt_text_keywords=None,
):
    """Main function to upload files and create JSON with optional alt text generation"""
    # Check if alt text generation is requested and available
    if generate_alt_text_flag and not ALTTEXT_AI_AVAILABLE:
        print("⚠️  Alt text generation requested but AltText.ai module not available.")
        print(
            "   Install python-dotenv and set ALTTEXT_AI_API_KEY to enable this feature."
        )
        generate_alt_text_flag = False

    # Test AltText.ai connection if alt text generation is enabled
    if generate_alt_text_flag:
        print("🔍 Testing AltText.ai connection...")
        if not test_alttext_ai_connection():
            print(
                "❌ AltText.ai connection failed. Alt text generation will be disabled."
            )
            generate_alt_text_flag = False
        else:
            print("✅ AltText.ai connection successful")

    uploaded_files = load_uploaded_files()

    # Get all files in the upload folder
    files_to_upload = [
        f
        for f in os.listdir(UPLOAD_FOLDER)
        if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))
    ]

    # Track files with alt text
    files_with_alt_text = []

    for file_name in files_to_upload:
        if file_name in uploaded_files:
            print(f"{file_name} already uploaded, skipping...")
            continue

        file_path = os.path.join(UPLOAD_FOLDER, file_name)

        # Check if it's an image file
        if file_name.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif")):
            # Optimize the image
            success, new_path = optimize_image(
                file_path, max_width, quality, smart_format
            )
            if success and new_path != file_path:
                # If the file path changed (due to format conversion), update the file name
                file_name = os.path.basename(new_path)
                file_path = new_path

        success, uploaded_file_name = upload_file_to_s3(
            file_path, file_name, add_timestamp
        )
        if success:
            cloudfront_url = f"https://{CLOUDFRONT_DOMAIN}/{uploaded_file_name}"

            # Add to uploaded files with CloudFront URL
            uploaded_files[file_name] = {
                "cloudfront_url": cloudfront_url,
                "s3_key": uploaded_file_name,
            }

            # Generate alt text if requested
            if generate_alt_text_flag:
                alt_text = generate_alt_text(cloudfront_url, alt_text_keywords)
                if alt_text:
                    uploaded_files[file_name]["alt_text"] = alt_text
                    files_with_alt_text.append(
                        {
                            "filename": file_name,
                            "cloudfront_url": cloudfront_url,
                            "alt_text": alt_text,
                        }
                    )
                    print(f"Generated alt text for {file_name}: {alt_text}")

    # Save the updated JSON
    save_uploaded_files(uploaded_files)
    print(f"Upload complete. {len(uploaded_files)} files tracked in {JSON_FILE}")

    # Save alt text information to a separate CSV if any were generated
    if files_with_alt_text:
        with open(LOCAL_ALT_TEXT_FILE, "w", newline="") as csv_file:
            csv_writer = csv.DictWriter(
                csv_file, fieldnames=["filename", "cloudfront_url", "alt_text"]
            )
            csv_writer.writeheader()
            for item in files_with_alt_text:
                csv_writer.writerow(item)
        print(f"📄 Alt text saved to {LOCAL_ALT_TEXT_FILE}")

    return uploaded_files


def download_and_upload_from_csv(
    max_width=DEFAULT_MAX_WIDTH,
    quality=DEFAULT_QUALITY,
    smart_format=SMART_FORMAT,
    add_timestamp=True,
    generate_alt_text_flag=False,
    alt_text_keywords=None,
):
    """Download images from URLs in CSV file and upload them to S3/CloudFront with optional alt text generation"""
    if not os.path.exists(CSV_INPUT_FILE):
        print(f"Error: CSV file {CSV_INPUT_FILE} not found")
        return False

    # Check if alt text generation is requested and available
    if generate_alt_text_flag and not ALTTEXT_AI_AVAILABLE:
        print("⚠️  Alt text generation requested but AltText.ai module not available.")
        print(
            "   Install python-dotenv and set ALTTEXT_AI_API_KEY to enable this feature."
        )
        generate_alt_text_flag = False

    # Test AltText.ai connection if alt text generation is enabled
    if generate_alt_text_flag:
        print("🔍 Testing AltText.ai connection...")
        if not test_alttext_ai_connection():
            print(
                "❌ AltText.ai connection failed. Alt text generation will be disabled."
            )
            generate_alt_text_flag = False
        else:
            print("✅ AltText.ai connection successful")

    # Load existing uploaded files
    uploaded_files = load_uploaded_files()

    # Load existing URL mappings from the output CSV
    existing_mappings = {}
    if os.path.exists(CSV_OUTPUT_FILE):
        with open(CSV_OUTPUT_FILE, "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                existing_mappings[row["source_url"]] = row

    # Create a list to store mapping of original URL to CloudFront URL
    url_mapping = []

    # Set up headers to mimic a browser request - using the user's specific headers
    headers = {
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/134.0.0.0 Safari/537.36"
        ),
        "sec-ch-ua": '"Not:A-Brand";v="24", "Chromium";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://citizenshipper.com/",
    }

    # Read URLs from CSV file (skip header row)
    with open(CSV_INPUT_FILE, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader, None)  # Skip header row

        for row in csv_reader:
            if not row or not row[0].strip():
                continue  # Skip empty rows

            source_url = row[0].strip()
            print(f"Processing URL: {source_url}")

            # Check if this URL has already been processed
            if source_url in existing_mappings:
                print(f"URL {source_url} already processed, skipping...")
                url_mapping.append(existing_mappings[source_url])
                continue

            try:
                # Extract filename from URL
                parsed_url = urllib.parse.urlparse(source_url)
                file_name = os.path.basename(parsed_url.path)

                # Check if file already exists in our records by filename
                if file_name in uploaded_files:
                    print(
                        f"File {file_name} already uploaded, using existing CloudFront URL"
                    )
                    cloudfront_url = uploaded_files[file_name]["cloudfront_url"]

                    # Generate alt text for existing image if requested
                    alt_text = None
                    if generate_alt_text_flag:
                        alt_text = generate_alt_text(cloudfront_url, alt_text_keywords)

                    mapping_data = {
                        "source_url": source_url,
                        "cloudfront_url": cloudfront_url,
                        "max_width": max_width,
                        "quality": quality,
                        "smart_format": smart_format,
                    }

                    if alt_text:
                        mapping_data["alt_text"] = alt_text

                    url_mapping.append(mapping_data)
                    continue

                # Download the image with headers
                print(f"Downloading {source_url}...")

                # Create a session to maintain cookies
                session = requests.Session()

                # First visit the main site to get cookies
                session.get("https://citizenshipper.com/", headers=headers)

                # Then try to get the image
                response = session.get(
                    source_url, stream=True, timeout=30, headers=headers
                )
                response.raise_for_status()  # Raise exception for HTTP errors

                # Save the image to the upload folder
                file_path = os.path.join(UPLOAD_FOLDER, file_name)
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                # Optimize the image if it's an image file
                if file_name.lower().endswith(
                    (".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif")
                ):
                    print(
                        f"Optimizing image with max_width={max_width}, quality={quality}, smart_format={smart_format}..."
                    )
                    success, new_path = optimize_image(
                        file_path, max_width, quality, smart_format
                    )
                    if success and new_path != file_path:
                        # If the file path changed (due to format conversion), update the file name
                        file_name = os.path.basename(new_path)
                        file_path = new_path

                # Upload to S3
                success, uploaded_file_name = upload_file_to_s3(
                    file_path, file_name, add_timestamp
                )
                if success:
                    cloudfront_url = f"https://{CLOUDFRONT_DOMAIN}/{uploaded_file_name}"
                    uploaded_files[file_name] = {
                        "cloudfront_url": cloudfront_url,
                        "s3_key": uploaded_file_name,
                    }

                    # Generate alt text if requested
                    alt_text = None
                    if generate_alt_text_flag:
                        # Use the original source URL for better context
                        alt_text = generate_alt_text(source_url, alt_text_keywords)

                    mapping_data = {
                        "source_url": source_url,
                        "cloudfront_url": cloudfront_url,
                        "max_width": max_width,
                        "quality": quality,
                        "smart_format": smart_format,
                    }

                    if alt_text:
                        mapping_data["alt_text"] = alt_text

                    url_mapping.append(mapping_data)

                    print(f"Successfully processed {source_url} -> {cloudfront_url}")
                    if alt_text:
                        print(f"  Alt text: {alt_text}")
                else:
                    print(f"Failed to upload {file_name} to S3 after curl retry")

            except Exception as e:
                print(f"Error processing URL {source_url}: {e}")
                # Add retry mechanism with curl as a last resort
                try:
                    print("Retrying with curl as a last resort...")

                    # Create a temporary file for curl output
                    temp_file = os.path.join(UPLOAD_FOLDER, f"temp_{file_name}")

                    # Construct curl command with all the headers
                    curl_cmd = [
                        "curl",
                        source_url,
                        "-H",
                        "DNT: 1",
                        "-H",
                        "Upgrade-Insecure-Requests: 1",
                        "-H",
                        (
                            "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/134.0.0.0 Safari/537.36"
                        ),
                        "-H",
                        'sec-ch-ua: "Not:A-Brand";v="24", "Chromium";v="134"',
                        "-H",
                        "sec-ch-ua-mobile: ?0",
                        "-H",
                        'sec-ch-ua-platform: "macOS"',
                        "-o",
                        temp_file,
                    ]

                    # Execute curl command
                    import subprocess

                    result = subprocess.run(curl_cmd, capture_output=True, text=True)

                    if result.returncode != 0:
                        raise Exception(f"Curl command failed: {result.stderr}")

                    # Check if file was downloaded
                    if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0:
                        raise Exception("Curl downloaded an empty file")

                    # Move temp file to final location
                    os.rename(temp_file, file_path)

                    # Continue with optimization and upload
                    if file_name.lower().endswith(
                        (".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif")
                    ):
                        print(
                            f"Optimizing image with max_width={max_width}, quality={quality}, smart_format={smart_format}..."
                        )
                        success, new_path = optimize_image(
                            file_path, max_width, quality, smart_format
                        )
                        if success and new_path != file_path:
                            file_name = os.path.basename(new_path)
                            file_path = new_path

                    success, uploaded_file_name = upload_file_to_s3(
                        file_path, file_name, add_timestamp
                    )
                    if success:
                        cloudfront_url = (
                            f"https://{CLOUDFRONT_DOMAIN}/{uploaded_file_name}"
                        )
                        uploaded_files[file_name] = {
                            "cloudfront_url": cloudfront_url,
                            "s3_key": uploaded_file_name,
                        }

                        # Generate alt text if requested
                        alt_text = None
                        if generate_alt_text_flag:
                            alt_text = generate_alt_text(source_url, alt_text_keywords)

                        mapping_data = {
                            "source_url": source_url,
                            "cloudfront_url": cloudfront_url,
                            "max_width": max_width,
                            "quality": quality,
                            "smart_format": smart_format,
                        }

                        if alt_text:
                            mapping_data["alt_text"] = alt_text

                        url_mapping.append(mapping_data)

                        print(
                            f"Successfully processed {source_url} -> {cloudfront_url} (after curl retry)"
                        )
                        if alt_text:
                            print(f"  Alt text: {alt_text}")
                    else:
                        print(f"Failed to upload {file_name} to S3 after curl retry")
                except Exception as retry_error:
                    print(f"Curl retry also failed: {retry_error}")

    # Save the updated JSON
    save_uploaded_files(uploaded_files)

    # Write URL mapping to CSV with alt text if available
    fieldnames = [
        "source_url",
        "cloudfront_url",
        "max_width",
        "quality",
        "smart_format",
    ]
    if generate_alt_text_flag:
        fieldnames.append("alt_text")

    with open(CSV_OUTPUT_FILE, "w", newline="") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for item in url_mapping:
            # Only include fields that are in fieldnames
            filtered_item = {k: v for k, v in item.items() if k in fieldnames}
            csv_writer.writerow(filtered_item)

    print(f"Download and upload complete. Processed {len(url_mapping)} URLs.")
    print(f"URL mapping saved to {CSV_OUTPUT_FILE}")
    return True


@app.route("/upload", methods=["POST"])
def upload_file_api():
    """API endpoint to upload a file via HTTP request"""
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Get optimization parameters
    max_width = request.form.get("max_width", DEFAULT_MAX_WIDTH)
    if max_width and max_width.isdigit():
        max_width = int(max_width)
    else:
        max_width = DEFAULT_MAX_WIDTH

    quality = request.form.get("quality", DEFAULT_QUALITY)
    if quality and quality.isdigit():
        quality = int(quality)
    else:
        quality = DEFAULT_QUALITY

    smart_format = request.form.get("smart_format", SMART_FORMAT)
    if isinstance(smart_format, str):
        smart_format = smart_format.lower() in ("true", "1", "yes")

    # Secure the filename
    filename = werkzeug.utils.secure_filename(file.filename)

    # Save the file temporarily
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Optimize the image if it's an image file
    new_filename = filename
    if filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif")):
        success, new_path = optimize_image(file_path, max_width, quality, smart_format)
        if success and new_path != file_path:
            # If the file path changed (due to format conversion), update the file name
            new_filename = os.path.basename(new_path)
            file_path = new_path

    # Load existing uploaded files
    uploaded_files = load_uploaded_files()

    # Check if file already exists in our records
    if new_filename in uploaded_files:
        return (
            jsonify(
                {
                    "message": f"File {new_filename} already uploaded",
                    "file_info": uploaded_files[new_filename],
                }
            ),
            200,
        )

    # Upload to S3
    success, uploaded_file_name = upload_file_to_s3(file_path, new_filename)
    if success:
        # Add to uploaded files with CloudFront URL
        uploaded_files[new_filename] = {
            "cloudfront_url": f"https://{CLOUDFRONT_DOMAIN}/{uploaded_file_name}",
            "s3_key": uploaded_file_name,
        }

        # Save the updated JSON
        save_uploaded_files(uploaded_files)

        return (
            jsonify(
                {
                    "message": f"Successfully uploaded {new_filename}",
                    "file_info": uploaded_files[new_filename],
                    "original_filename": filename,
                    "optimization": {
                        "max_width": max_width,
                        "quality": quality,
                        "smart_format": smart_format,
                        "format_changed": new_filename != filename,
                    },
                }
            ),
            201,
        )
    else:
        return jsonify({"error": f"Failed to upload {new_filename} to S3"}), 500


@app.route("/files", methods=["GET"])
def list_files():
    """API endpoint to list all uploaded files"""
    uploaded_files = load_uploaded_files()
    return jsonify(uploaded_files)


@app.route("/process-csv", methods=["GET"])
def process_csv_api():
    """API endpoint to process the CSV file"""
    # Get optimization parameters
    max_width = request.args.get("max_width", DEFAULT_MAX_WIDTH)
    if max_width and max_width.isdigit():
        max_width = int(max_width)
    else:
        max_width = DEFAULT_MAX_WIDTH

    quality = request.args.get("quality", DEFAULT_QUALITY)
    if quality and quality.isdigit():
        quality = int(quality)
    else:
        quality = DEFAULT_QUALITY

    smart_format = request.args.get("smart_format", SMART_FORMAT)
    if isinstance(smart_format, str):
        smart_format = smart_format.lower() in ("true", "1", "yes")

    generate_alt_text_flag = (
        request.args.get("generate_alt_text", "false").lower() == "true"
    )
    alt_text_keywords = request.args.get("alt_text_keywords", None)

    if download_and_upload_from_csv(
        max_width,
        quality,
        smart_format,
        generate_alt_text_flag=generate_alt_text_flag,
        alt_text_keywords=alt_text_keywords,
    ):
        return (
            jsonify(
                {
                    "message": "CSV processing complete",
                    "output_file": CSV_OUTPUT_FILE,
                    "optimization": {
                        "max_width": max_width,
                        "quality": quality,
                        "smart_format": smart_format,
                    },
                }
            ),
            200,
        )
    else:
        return jsonify({"error": "Failed to process CSV file"}), 500


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Upload files to S3/CloudFront with optional optimization"
    )
    parser.add_argument(
        "--max-width",
        type=str,
        default=None,
        help="Max width for image resizing (None or blank = no resizing)",
    )
    parser.add_argument(
        "--quality", type=int, default=DEFAULT_QUALITY, help="JPEG/WebP quality (0-100)"
    )
    parser.add_argument(
        "--smart-format",
        type=str,
        choices=["true", "false"],
        default=str(SMART_FORMAT).lower(),
        help="Enable smart format conversion",
    )
    parser.add_argument(
        "--no-timestamp", action="store_true", help="Do not add timestamps to filenames"
    )

    # Parse arguments
    args = parser.parse_args()

    # Convert arguments to appropriate types
    if args.max_width and args.max_width.lower() != "none":
        max_width = int(args.max_width)
    else:
        max_width = None
    quality = args.quality
    smart_format = args.smart_format.lower() == "true"
    add_timestamp = not args.no_timestamp

    # If run directly, you can still use the original function
    if os.environ.get("FLASK_RUN", "0") == "1":
        # Use environment variables for security
        host = os.environ.get("FLASK_HOST", "127.0.0.1")  # Default to localhost only
        debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
        app.run(host=host, port=5000, debug=debug)
    elif os.environ.get("PROCESS_CSV", "0") == "1":
        # Get optimization parameters from environment variables
        max_width_env = os.environ.get("MAX_WIDTH", "")
        if max_width_env and max_width_env.isdigit():
            max_width = int(max_width_env)

        quality_env = os.environ.get("QUALITY", "")
        if quality_env and quality_env.isdigit():
            quality = int(quality_env)

        smart_format_env = os.environ.get("SMART_FORMAT", "")
        if smart_format_env:
            smart_format = smart_format_env.lower() in ("true", "1", "yes")

        # Get alt text parameters from environment variables
        generate_alt_text_flag = os.environ.get("GENERATE_ALT_TEXT", "0").lower() in (
            "true",
            "1",
            "yes",
        )
        alt_text_keywords = os.environ.get("ALT_TEXT_KEYWORDS", None)
        if alt_text_keywords and not alt_text_keywords.strip():
            alt_text_keywords = None

        print(
            f"Using optimization parameters: max_width={max_width}, quality={quality}, smart_format={smart_format}"
        )
        if generate_alt_text_flag:
            print(
                f"Alt text generation enabled with keywords: {alt_text_keywords or 'none'}"
            )

        download_and_upload_from_csv(
            max_width,
            quality,
            smart_format,
            generate_alt_text_flag=generate_alt_text_flag,
            alt_text_keywords=alt_text_keywords,
        )
    else:
        # Check for alt text environment variables for local file uploads too
        generate_alt_text_flag = os.environ.get("GENERATE_ALT_TEXT", "0").lower() in (
            "true",
            "1",
            "yes",
        )
        alt_text_keywords = os.environ.get("ALT_TEXT_KEYWORDS", None)
        if alt_text_keywords and not alt_text_keywords.strip():
            alt_text_keywords = None

        print(
            f"Uploading files with: max_width={max_width}, quality={quality}, smart_format={smart_format}"
        )
        if generate_alt_text_flag:
            print(
                f"Alt text generation enabled with keywords: {alt_text_keywords or 'none'}"
            )

        upload_files(
            max_width=max_width,
            quality=quality,
            smart_format=smart_format,
            generate_alt_text_flag=generate_alt_text_flag,
            alt_text_keywords=alt_text_keywords,
        )
