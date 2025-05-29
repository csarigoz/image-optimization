#!/usr/bin/env python3
"""
Unified Upload Utility

This module provides a unified interface for uploading images using different
providers (CloudFront/S3 or Cloudinary) based on configuration.

Usage:
    from unified_upload import UnifiedUploader

    uploader = UnifiedUploader()
    result = uploader.upload_image(file_path, options)
"""

import argparse
import csv
import json
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from upload_provider import ProviderFactory, UploadProvider

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

# Configuration paths
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
DEFAULT_MAX_WIDTH = None
SMART_FORMAT = True


class UnifiedUploader:
    """Unified uploader that works with multiple providers"""

    def __init__(self, provider_type: Optional[str] = None):
        """
        Initialize the unified uploader

        Args:
            provider_type: Provider to use ('cloudfront', 'cloudinary', or 'auto')
                          If None, will use UPLOAD_PROVIDER from environment or auto-detect
        """
        # Determine provider type
        if provider_type is None:
            provider_type = os.getenv("UPLOAD_PROVIDER", "auto")

        self.provider_type = provider_type.lower().strip()

        # Auto-detect provider if needed
        if self.provider_type == "auto":
            self.provider_type = self._auto_detect_provider()

        # Create the provider
        try:
            self.provider: UploadProvider = ProviderFactory.create_provider(
                self.provider_type
            )
            print(f"🚀 Using {self.provider.get_provider_name()} provider")
        except Exception as e:
            print(f"❌ Failed to initialize {self.provider_type} provider: {e}")
            raise

        # Create directories
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(os.path.dirname(JSON_FILE), exist_ok=True)

    def _auto_detect_provider(self) -> str:
        """Auto-detect available provider from environment variables"""
        # Check Cloudinary credentials
        cloudinary_available = all(
            [
                os.getenv("CLOUDINARY_CLOUD_NAME"),
                os.getenv("CLOUDINARY_API_KEY"),
                os.getenv("CLOUDINARY_API_SECRET"),
            ]
        )

        # Check AWS credentials
        aws_available = all(
            [
                os.getenv("AWS_ACCESS_KEY"),
                os.getenv("AWS_SECRET_KEY"),
                os.getenv("S3_BUCKET"),
            ]
        )

        if cloudinary_available and aws_available:
            print(
                "🔍 Both Cloudinary and AWS credentials found - preferring Cloudinary"
            )
            return "cloudinary"
        elif cloudinary_available:
            print("🔍 Cloudinary credentials found - using Cloudinary")
            return "cloudinary"
        elif aws_available:
            print("🔍 AWS credentials found - using CloudFront")
            return "cloudfront"
        else:
            raise ValueError(
                "❌ No valid provider configuration found. Please configure either:\n"
                "   Cloudinary: CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET\n"
                "   AWS: AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET"
            )

    def test_connection(self) -> bool:
        """Test the provider connection"""
        return self.provider.test_connection()

    def load_uploaded_files(self) -> Dict[str, Any]:
        """Load the list of uploaded files from JSON"""
        if os.path.exists(JSON_FILE):
            try:
                with open(JSON_FILE, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return {}

    def save_uploaded_files(self, uploaded_files: Dict[str, Any]) -> None:
        """Save the list of uploaded files to JSON"""
        with open(JSON_FILE, "w") as f:
            json.dump(uploaded_files, f, indent=2)

    def upload_local_files(
        self,
        max_width: Optional[int] = DEFAULT_MAX_WIDTH,
        quality: int = DEFAULT_QUALITY,
        smart_format: bool = SMART_FORMAT,
        add_timestamp: bool = True,
        generate_alt_text_flag: bool = False,
        alt_text_keywords: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Upload files from the local folder"""
        uploaded_files = self.load_uploaded_files()
        files_with_alt_text = []

        # Get list of files to upload
        files_to_upload = []
        for file_name in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, file_name)
            if os.path.isfile(file_path):
                files_to_upload.append(file_name)

        print(f"📁 Found {len(files_to_upload)} files to upload")

        for file_name in files_to_upload:
            if file_name in uploaded_files:
                print(f"{file_name} already uploaded, skipping...")
                continue

            file_path = os.path.join(UPLOAD_FOLDER, file_name)

            print(f"📤 Uploading {file_name}...")
            success, public_url, metadata = self.provider.upload_image(
                file_path, file_name, max_width, quality, smart_format, add_timestamp
            )

            if success and public_url:
                # Add to uploaded files
                uploaded_files[file_name] = {
                    "public_url": public_url,
                    "provider": self.provider.get_provider_name(),
                    "metadata": metadata or {},
                }

                # Generate alt text if requested
                if generate_alt_text_flag and ALTTEXT_AI_AVAILABLE:
                    alt_text = generate_alt_text(public_url, alt_text_keywords)
                    if alt_text:
                        uploaded_files[file_name]["alt_text"] = alt_text
                        files_with_alt_text.append(
                            {
                                "filename": file_name,
                                "public_url": public_url,
                                "alt_text": alt_text,
                            }
                        )
                        print(f"📄 Generated alt text for {file_name}: {alt_text}")

                print(f"✅ Successfully uploaded: {public_url}")
            else:
                print(f"❌ Failed to upload {file_name}")

        # Save the updated JSON
        self.save_uploaded_files(uploaded_files)
        print(f"✅ Upload complete. {len(uploaded_files)} files tracked")

        # Save alt text information if any were generated
        if files_with_alt_text:
            with open(LOCAL_ALT_TEXT_FILE, "w", newline="") as csv_file:
                csv_writer = csv.DictWriter(
                    csv_file, fieldnames=["filename", "public_url", "alt_text"]
                )
                csv_writer.writeheader()
                for item in files_with_alt_text:
                    csv_writer.writerow(item)
            print(f"📄 Alt text saved to {LOCAL_ALT_TEXT_FILE}")

        return uploaded_files

    def upload_from_csv(
        self,
        max_width: Optional[int] = DEFAULT_MAX_WIDTH,
        quality: int = DEFAULT_QUALITY,
        smart_format: bool = SMART_FORMAT,
        add_timestamp: bool = True,
        generate_alt_text_flag: bool = False,
        alt_text_keywords: Optional[str] = None,
    ) -> bool:
        """Upload images from URLs in CSV file"""
        if not os.path.exists(CSV_INPUT_FILE):
            print(f"❌ CSV file {CSV_INPUT_FILE} not found")
            return False

        # Check if alt text generation is requested and available
        if generate_alt_text_flag and not ALTTEXT_AI_AVAILABLE:
            print(
                "⚠️  Alt text generation requested but AltText.ai module not available."
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
        uploaded_files = self.load_uploaded_files()

        # Load existing URL mappings from the output CSV
        existing_mappings = {}
        if os.path.exists(CSV_OUTPUT_FILE):
            with open(CSV_OUTPUT_FILE, "r") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    existing_mappings[row["source_url"]] = row

        # Create a list to store mapping of original URL to public URL
        url_mapping = []

        # Process URLs from CSV
        with open(CSV_INPUT_FILE, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader, None)  # Skip header row

            for row in csv_reader:
                if not row or not row[0].strip():
                    continue

                source_url = row[0].strip()
                print(f"📥 Processing URL: {source_url}")

                # Check if this URL has already been processed
                if source_url in existing_mappings:
                    print(f"URL {source_url} already processed, skipping...")
                    url_mapping.append(existing_mappings[source_url])
                    continue

                try:
                    # Upload directly from URL using the provider
                    success, public_url, metadata = self.provider.upload_from_url(
                        source_url, max_width, quality, smart_format, add_timestamp
                    )

                    if success and public_url:
                        # Generate a filename for tracking
                        import urllib.parse

                        parsed_url = urllib.parse.urlparse(source_url)
                        file_name = os.path.basename(parsed_url.path)

                        # Add to uploaded files
                        uploaded_files[file_name] = {
                            "public_url": public_url,
                            "provider": self.provider.get_provider_name(),
                            "metadata": metadata or {},
                            "source_url": source_url,
                        }

                        # Generate alt text if requested
                        alt_text = None
                        if generate_alt_text_flag:
                            alt_text = generate_alt_text(source_url, alt_text_keywords)

                        # Create mapping data
                        mapping_data = {
                            "source_url": source_url,
                            "public_url": public_url,
                            "provider": self.provider.get_provider_name(),
                            "max_width": max_width,
                            "quality": quality,
                            "smart_format": smart_format,
                        }

                        if alt_text:
                            mapping_data["alt_text"] = alt_text
                            uploaded_files[file_name]["alt_text"] = alt_text

                        url_mapping.append(mapping_data)

                        print(
                            f"✅ Successfully processed: {source_url} -> {public_url}"
                        )
                        if alt_text:
                            print(f"   Alt text: {alt_text}")
                    else:
                        print(f"❌ Failed to upload from URL: {source_url}")

                except Exception as e:
                    print(f"❌ Error processing {source_url}: {e}")

        # Save the updated JSON
        self.save_uploaded_files(uploaded_files)

        # Write URL mapping to CSV
        fieldnames = [
            "source_url",
            "public_url",
            "provider",
            "max_width",
            "quality",
            "smart_format",
        ]
        if generate_alt_text_flag:
            fieldnames.append("alt_text")

        with open(CSV_OUTPUT_FILE, "w", newline="") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            for mapping in url_mapping:
                csv_writer.writerow(mapping)

        print(f"✅ URL mapping saved to {CSV_OUTPUT_FILE}")
        print(f"📊 Processed {len(url_mapping)} URLs")
        return True

    def get_stats(self) -> Dict[str, Any]:
        """Get upload statistics"""
        uploaded_files = self.load_uploaded_files()
        provider_stats = self.provider.get_upload_stats()

        stats = {
            "provider": self.provider.get_provider_name(),
            "total_files": len(uploaded_files),
            "provider_stats": provider_stats,
        }

        return stats

    def list_files(self) -> List[Dict[str, Any]]:
        """List all uploaded files"""
        uploaded_files = self.load_uploaded_files()
        return [
            {
                "filename": filename,
                "public_url": info.get("public_url"),
                "provider": info.get("provider"),
                "has_alt_text": "alt_text" in info,
            }
            for filename, info in uploaded_files.items()
        ]


def main():
    """Command line interface for the unified uploader"""
    parser = argparse.ArgumentParser(description="Unified Image Upload Utility")
    parser.add_argument(
        "--provider",
        choices=["cloudfront", "cloudinary"],
        help="Upload provider to use (default: from UPLOAD_PROVIDER env var)",
    )
    parser.add_argument(
        "--mode",
        choices=["local", "csv", "stats", "list"],
        default="local",
        help="Operation mode",
    )
    parser.add_argument(
        "--max-width", type=int, help="Maximum width for image resizing"
    )
    parser.add_argument(
        "--quality", type=int, default=DEFAULT_QUALITY, help="Image quality (1-100)"
    )
    parser.add_argument(
        "--no-smart-format", action="store_true", help="Disable smart format conversion"
    )
    parser.add_argument(
        "--no-timestamp", action="store_true", help="Don't add timestamps to filenames"
    )
    parser.add_argument(
        "--alt-text", action="store_true", help="Generate alt text using AltText.ai"
    )
    parser.add_argument("--alt-text-keywords", help="Keywords for alt text generation")

    args = parser.parse_args()

    try:
        # Create uploader
        uploader = UnifiedUploader(args.provider)

        # Test connection
        if not uploader.test_connection():
            print("❌ Provider connection test failed")
            return

        if args.mode == "local":
            # Upload local files
            uploader.upload_local_files(
                max_width=args.max_width,
                quality=args.quality,
                smart_format=not args.no_smart_format,
                add_timestamp=not args.no_timestamp,
                generate_alt_text_flag=args.alt_text,
                alt_text_keywords=args.alt_text_keywords,
            )
        elif args.mode == "csv":
            # Upload from CSV
            uploader.upload_from_csv(
                max_width=args.max_width,
                quality=args.quality,
                smart_format=not args.no_smart_format,
                add_timestamp=not args.no_timestamp,
                generate_alt_text_flag=args.alt_text,
                alt_text_keywords=args.alt_text_keywords,
            )
        elif args.mode == "stats":
            # Show stats
            stats = uploader.get_stats()
            print(f"\n📊 Upload Statistics")
            print(f"Provider: {stats['provider']}")
            print(f"Total Files: {stats['total_files']}")
            if stats["provider_stats"]:
                print("Provider Stats:")
                for key, value in stats["provider_stats"].items():
                    print(f"  {key}: {value}")
        elif args.mode == "list":
            # List files
            files = uploader.list_files()
            print(f"\n📁 Uploaded Files ({len(files)} total)")
            for file_info in files:
                alt_text_indicator = "📄" if file_info["has_alt_text"] else ""
                print(
                    f"  {file_info['filename']} -> {file_info['public_url']} ({file_info['provider']}) {alt_text_indicator}"
                )

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
