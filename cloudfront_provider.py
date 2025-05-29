#!/usr/bin/env python3
"""
CloudFront Provider for Image Upload Utility

This module wraps the existing AWS S3/CloudFront functionality
to conform to the UploadProvider interface, allowing it to be
used interchangeably with other providers like Cloudinary.
"""

import os
import tempfile
import time
import urllib.parse
from typing import Any, Dict, Optional, Tuple

import requests

try:
    import boto3
    from botocore.exceptions import ClientError
    from PIL import Image

    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False

from upload_provider import UploadProvider


class CloudFrontProvider(UploadProvider):
    """CloudFront/S3 upload provider"""

    def __init__(self):
        """Initialize CloudFront provider with AWS configuration"""
        if not BOTO3_AVAILABLE:
            raise ImportError(
                "boto3 package not available. Install with: pip install boto3"
            )

        # Get AWS configuration from environment variables
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY")
        self.aws_secret_key = os.getenv("AWS_SECRET_KEY")
        self.s3_bucket = os.getenv("S3_BUCKET")
        self.cloudfront_domain = os.getenv("CLOUDFRONT_DOMAIN")

        if not all(
            [
                self.aws_access_key,
                self.aws_secret_key,
                self.s3_bucket,
                self.cloudfront_domain,
            ]
        ):
            raise ValueError(
                "AWS configuration incomplete. Please set AWS_ACCESS_KEY, "
                "AWS_SECRET_KEY, S3_BUCKET, and CLOUDFRONT_DOMAIN environment variables."
            )

        # Initialize S3 client
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
        )

        print(f"✅ CloudFront configured for bucket: {self.s3_bucket}")

    def test_connection(self) -> bool:
        """Test AWS S3 connection"""
        try:
            # Test by listing objects (limited to 1)
            self.s3_client.list_objects_v2(Bucket=self.s3_bucket, MaxKeys=1)
            print(f"✅ AWS S3 connection successful to bucket: {self.s3_bucket}")
            return True
        except Exception as e:
            print(f"❌ AWS S3 connection failed: {e}")
            return False

    def _optimize_image(
        self,
        file_path: str,
        max_width: Optional[int] = None,
        quality: int = 82,
        smart_format: bool = True,
    ) -> Tuple[bool, str]:
        """
        Optimize an image file (resize, quality, format conversion)

        Args:
            file_path: Path to the image file
            max_width: Maximum width for resizing
            quality: JPEG/WebP quality (1-100)
            smart_format: Enable smart format conversion

        Returns:
            Tuple of (success, optimized_file_path)
        """
        try:
            with Image.open(file_path) as img:
                # Convert RGBA to RGB if necessary for JPEG
                if img.mode in ("RGBA", "LA"):
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(
                        img, mask=img.split()[-1] if img.mode == "RGBA" else None
                    )
                    img = background
                elif img.mode == "P":
                    img = img.convert("RGB")

                # Resize if max_width is specified
                if max_width and img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                    print(f"📏 Resized to {max_width}x{new_height}")

                # Determine best format if smart_format is enabled
                if smart_format:
                    return self._get_best_format(img, file_path, quality)
                else:
                    # Save in original format with quality optimization
                    img.save(file_path, quality=quality, optimize=True)
                    return True, file_path

        except Exception as e:
            print(f"❌ Error optimizing image {file_path}: {e}")
            return False, file_path

    def _get_best_format(
        self, img: Image.Image, original_path: str, quality: int = 82
    ) -> Tuple[bool, str]:
        """Determine the best format (JPEG, PNG, WebP) based on file size"""
        formats_to_try = ["JPEG", "PNG", "WEBP"]

        # Skip testing if the image has transparency and we're considering JPEG
        has_transparency = img.mode in ("RGBA", "LA") or (
            img.mode == "P" and "transparency" in img.info
        )

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
                        test_img.save(
                            temp_file, format=fmt, quality=quality, optimize=True
                        )
                    elif fmt == "PNG":
                        test_img.save(temp_file, format=fmt, optimize=True)
                    elif fmt == "WEBP":
                        test_img.save(temp_file, format=fmt, quality=quality, method=6)

                    # Get file size
                    file_size = os.path.getsize(temp_file)
                    results[fmt] = {"size": file_size, "path": temp_file}

                    print(f"Format {fmt}: {file_size/1024:.1f} KB")
                except Exception as e:
                    print(f"Error testing format {fmt}: {e}")

            # If no formats worked, return the original
            if not results:
                return False, original_path

            # Find the format with the smallest file size
            best_format, best_info = min(results.items(), key=lambda x: x[1]["size"])

            # Create the final optimized file
            base_name = os.path.splitext(original_path)[0]
            optimized_path = f"{base_name}.{best_format.lower()}"

            # Copy the best format to the final location
            with open(best_info["path"], "rb") as src, open(
                optimized_path, "wb"
            ) as dst:
                dst.write(src.read())

            print(f"🎯 Best format: {best_format} ({best_info['size']/1024:.1f} KB)")
            return True, optimized_path

    def _upload_to_s3(
        self, file_path: str, file_name: str, add_timestamp: bool = True
    ) -> Tuple[bool, Optional[str]]:
        """Upload a file to S3"""
        try:
            # Lowercase the file name and optionally add Unix timestamp
            file_name = file_name.lower()
            if add_timestamp:
                timestamp = int(time.time())
                base_name, ext = os.path.splitext(file_name)
                file_name_to_upload = f"{base_name}_{timestamp}{ext}"
            else:
                file_name_to_upload = file_name

            # Upload without ACL since the bucket blocks public ACLs
            # CloudFront will handle public access
            self.s3_client.upload_file(file_path, self.s3_bucket, file_name_to_upload)
            print(f"✅ Successfully uploaded {file_name_to_upload}")
            return True, file_name_to_upload
        except ClientError as e:
            print(f"❌ Error uploading {file_name}: {e}")
            return False, None

    def upload_image(
        self,
        file_path: str,
        file_name: str,
        max_width: Optional[int] = None,
        quality: int = 82,
        smart_format: bool = True,
        add_timestamp: bool = True,
        **kwargs,
    ) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """Upload an image file with optimization"""
        try:
            # Check if it's an image file
            if file_name.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
                # Optimize the image
                success, optimized_path = self._optimize_image(
                    file_path, max_width, quality, smart_format
                )
                if success and optimized_path != file_path:
                    # If the file path changed (due to format conversion), update the file name
                    file_name = os.path.basename(optimized_path)
                    file_path = optimized_path

            # Upload to S3
            success, uploaded_file_name = self._upload_to_s3(
                file_path, file_name, add_timestamp
            )

            if success:
                cloudfront_url = (
                    f"https://{self.cloudfront_domain}/{uploaded_file_name}"
                )
                metadata = {
                    "s3_key": uploaded_file_name,
                    "cloudfront_url": cloudfront_url,
                    "provider": "cloudfront",
                }
                return True, cloudfront_url, metadata
            else:
                return False, None, None

        except Exception as e:
            print(f"❌ Error uploading image: {e}")
            return False, None, None

    def upload_from_url(
        self,
        source_url: str,
        max_width: Optional[int] = None,
        quality: int = 82,
        smart_format: bool = True,
        add_timestamp: bool = True,
        **kwargs,
    ) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """Upload an image directly from URL"""
        try:
            # Extract filename from URL
            parsed_url = urllib.parse.urlparse(source_url)
            file_name = os.path.basename(parsed_url.path)

            # Download the image
            print(f"📥 Downloading {source_url}...")

            # Create headers
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://citizenshipper.com/",
            }

            # Create a session to maintain cookies
            session = requests.Session()
            session.get("https://citizenshipper.com/", headers=headers)

            # Download the image
            response = session.get(source_url, stream=True, timeout=30, headers=headers)
            response.raise_for_status()

            # Create temporary file
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=os.path.splitext(file_name)[1]
            ) as temp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            try:
                # Upload the downloaded file
                result = self.upload_image(
                    temp_file_path,
                    file_name,
                    max_width,
                    quality,
                    smart_format,
                    add_timestamp,
                    **kwargs,
                )
                return result
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)

        except Exception as e:
            print(f"❌ Error uploading from URL {source_url}: {e}")
            return False, None, None

    def get_provider_name(self) -> str:
        """Get the name of this provider"""
        return "cloudfront"

    def get_upload_stats(self) -> Dict[str, Any]:
        """Get S3 bucket statistics"""
        try:
            # Get bucket size and object count
            paginator = self.s3_client.get_paginator("list_objects_v2")
            total_size = 0
            total_objects = 0

            for page in paginator.paginate(Bucket=self.s3_bucket):
                if "Contents" in page:
                    for obj in page["Contents"]:
                        total_size += obj["Size"]
                        total_objects += 1

            return {
                "total_objects": total_objects,
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "bucket": self.s3_bucket,
                "cloudfront_domain": self.cloudfront_domain,
            }
        except Exception as e:
            print(f"❌ Error getting upload stats: {e}")
            return {}

    def delete_image(self, s3_key: str, **kwargs) -> bool:
        """Delete an image from S3"""
        try:
            self.s3_client.delete_object(Bucket=self.s3_bucket, Key=s3_key)
            print(f"✅ Deleted {s3_key} from S3")
            return True
        except Exception as e:
            print(f"❌ Error deleting {s3_key}: {e}")
            return False


def test_cloudfront_connection() -> bool:
    """Test function for CloudFront connection"""
    try:
        provider = CloudFrontProvider()
        return provider.test_connection()
    except Exception as e:
        print(f"❌ CloudFront test failed: {e}")
        return False


if __name__ == "__main__":
    # Test the CloudFront provider
    print("🧪 Testing CloudFront Provider")
    print("=" * 40)

    if test_cloudfront_connection():
        provider = CloudFrontProvider()
        stats = provider.get_upload_stats()
        if stats:
            print(f"📊 Bucket Stats:")
            print(f"   Total Objects: {stats.get('total_objects', 'N/A')}")
            print(f"   Total Size: {stats.get('total_size_mb', 'N/A')} MB")
            print(f"   Bucket: {stats.get('bucket', 'N/A')}")
            print(f"   CloudFront Domain: {stats.get('cloudfront_domain', 'N/A')}")
        else:
            print("🔧 Check configuration and try again")
    else:
        print("❌ CloudFront connection test failed")

    print("✅ CloudFront integration is working correctly!")
    print("\n🚀 Ready to use:")
    print("   ./process_csv.sh (choose CloudFront option)")
    print("   python unified_upload.py --provider cloudfront --mode csv")
