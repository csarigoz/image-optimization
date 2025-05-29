#!/usr/bin/env python3
"""
Cloudinary Provider for Image Upload Utility

This module provides Cloudinary integration as an alternative to AWS CloudFront
for image uploading, optimization, and delivery.

Features:
- Automatic image optimization (format, quality, dimensions)
- Built-in CDN delivery
- Dynamic URL-based transformations
- Responsive image support
- Direct upload from URLs or local files

Usage:
    from cloudinary_provider import CloudinaryProvider

    provider = CloudinaryProvider()
    result = provider.upload_image(file_path, optimization_options)
"""

import os
import time
import urllib.parse
from typing import Any, Dict, Optional, Tuple

try:
    import cloudinary
    import cloudinary.api
    import cloudinary.uploader
    import cloudinary.utils
    from cloudinary.exceptions import Error as CloudinaryError

    CLOUDINARY_AVAILABLE = True
except ImportError:
    CLOUDINARY_AVAILABLE = False


class CloudinaryProvider:
    """Cloudinary image upload and optimization provider"""

    def __init__(self):
        """Initialize Cloudinary provider with configuration from environment variables"""
        if not CLOUDINARY_AVAILABLE:
            raise ImportError(
                "Cloudinary package not available. Install with: pip install cloudinary"
            )

        # Get configuration from environment variables
        self.cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
        self.api_key = os.getenv("CLOUDINARY_API_KEY")
        self.api_secret = os.getenv("CLOUDINARY_API_SECRET")

        if not all([self.cloud_name, self.api_key, self.api_secret]):
            raise ValueError(
                "Cloudinary configuration incomplete. Please set CLOUDINARY_CLOUD_NAME, "
                "CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET environment variables."
            )

        # Configure Cloudinary
        cloudinary.config(
            cloud_name=self.cloud_name,
            api_key=self.api_key,
            api_secret=self.api_secret,
            secure=True,
        )

        print(f"✅ Cloudinary configured for cloud: {self.cloud_name}")

    def test_connection(self) -> bool:
        """Test Cloudinary API connection"""
        try:
            # Test by getting account details
            result = cloudinary.api.ping()
            print(f"✅ Cloudinary connection successful: {result}")
            return True
        except Exception as e:
            print(f"❌ Cloudinary connection failed: {e}")
            return False

    def upload_image(
        self,
        file_path: str,
        file_name: str,
        max_width: Optional[int] = None,
        quality: int = 82,
        smart_format: bool = True,
        add_timestamp: bool = True,
        folder: str = "images",
    ) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Upload an image to Cloudinary with optimization

        Args:
            file_path: Path to the local image file
            file_name: Original filename
            max_width: Maximum width for resizing (None = no resizing)
            quality: Image quality (1-100, 'auto' for automatic)
            smart_format: Enable automatic format selection
            add_timestamp: Add timestamp to filename for uniqueness
            folder: Cloudinary folder for organization

        Returns:
            Tuple of (success, cloudinary_url, upload_result)
        """
        try:
            # Prepare filename
            base_name, ext = os.path.splitext(file_name.lower())
            if add_timestamp:
                timestamp = int(time.time())
                public_id = f"{base_name}_{timestamp}"
            else:
                public_id = base_name

            # Build transformation parameters
            transformation_params = {}

            # Add width constraint if specified
            if max_width:
                transformation_params["width"] = max_width
                transformation_params["crop"] = "scale"

            # Add quality and format settings
            if smart_format:
                transformation_params["format"] = "auto"
                transformation_params["quality"] = "auto"
            else:
                transformation_params["quality"] = quality

            # Add automatic optimization
            transformation_params["gravity"] = "auto"  # Smart cropping if needed

            # Upload options
            upload_options = {
                "public_id": public_id,
                "folder": folder,
                "resource_type": "image",
                "invalidate": True,  # Invalidate CDN cache
                "overwrite": False,  # Don't overwrite existing files
            }

            # Add transformation if any parameters were set
            if transformation_params:
                upload_options["transformation"] = transformation_params

            print(f"📤 Uploading {file_name} to Cloudinary...")
            print(f"   Public ID: {folder}/{public_id}")
            print(
                f"   Transformations: {transformation_params if transformation_params else 'None'}"
            )

            # Upload the file
            result = cloudinary.uploader.upload(file_path, **upload_options)

            # Generate optimized URL
            cloudinary_url = result.get("secure_url")

            if cloudinary_url:
                print(f"✅ Successfully uploaded to Cloudinary: {cloudinary_url}")
                return True, cloudinary_url, result
            else:
                print("❌ Upload succeeded but no URL returned")
                return False, None, result

        except CloudinaryError as e:
            print(f"❌ Cloudinary upload error: {e}")
            return False, None, None
        except Exception as e:
            print(f"❌ Unexpected error during upload: {e}")
            return False, None, None

    def upload_from_url(
        self,
        source_url: str,
        max_width: Optional[int] = None,
        quality: int = 82,
        smart_format: bool = True,
        add_timestamp: bool = True,
        folder: str = "images",
    ) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Upload an image directly from URL to Cloudinary

        Args:
            source_url: URL of the image to upload
            max_width: Maximum width for resizing
            quality: Image quality (1-100)
            smart_format: Enable automatic format selection
            add_timestamp: Add timestamp to filename
            folder: Cloudinary folder for organization

        Returns:
            Tuple of (success, cloudinary_url, upload_result)
        """
        try:
            # Extract filename from URL
            parsed_url = urllib.parse.urlparse(source_url)
            file_name = os.path.basename(parsed_url.path)
            base_name, ext = os.path.splitext(file_name.lower())

            if add_timestamp:
                timestamp = int(time.time())
                public_id = f"{base_name}_{timestamp}"
            else:
                public_id = base_name

            # Build transformation parameters
            transformation_params = {}

            if max_width:
                transformation_params["width"] = max_width
                transformation_params["crop"] = "scale"

            if smart_format:
                transformation_params["format"] = "auto"
                transformation_params["quality"] = "auto"
            else:
                transformation_params["quality"] = quality

            transformation_params["gravity"] = "auto"

            # Upload options
            upload_options = {
                "public_id": public_id,
                "folder": folder,
                "resource_type": "image",
                "invalidate": True,
                "overwrite": False,
            }

            if transformation_params:
                upload_options["transformation"] = transformation_params

            print(f"📤 Uploading from URL to Cloudinary: {source_url}")
            print(f"   Public ID: {folder}/{public_id}")
            print(
                f"   Transformations: {transformation_params if transformation_params else 'None'}"
            )

            # Upload directly from URL
            result = cloudinary.uploader.upload(source_url, **upload_options)

            cloudinary_url = result.get("secure_url")

            if cloudinary_url:
                print(f"✅ Successfully uploaded from URL: {cloudinary_url}")
                return True, cloudinary_url, result
            else:
                print("❌ Upload succeeded but no URL returned")
                return False, None, result

        except CloudinaryError as e:
            print(f"❌ Cloudinary upload error: {e}")
            return False, None, None
        except Exception as e:
            print(f"❌ Unexpected error during URL upload: {e}")
            return False, None, None

    def generate_responsive_url(
        self,
        public_id: str,
        folder: str = "images",
        transformations: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate a responsive Cloudinary URL with dynamic transformations

        Args:
            public_id: The Cloudinary public ID
            folder: Cloudinary folder
            transformations: Additional transformation parameters

        Returns:
            Responsive Cloudinary URL
        """
        try:
            # Base transformations for responsive images
            base_transformations = {
                "format": "auto",
                "quality": "auto",
                "gravity": "auto",
                "crop": "scale",
            }

            # Merge with provided transformations
            if transformations:
                base_transformations.update(transformations)

            # Generate URL
            url = cloudinary.utils.cloudinary_url(
                f"{folder}/{public_id}", **base_transformations
            )[0]

            return url

        except Exception as e:
            print(f"❌ Error generating responsive URL: {e}")
            return ""

    def get_upload_stats(self) -> Dict[str, Any]:
        """Get account usage statistics"""
        try:
            usage = cloudinary.api.usage()
            return {
                "credits_used": usage.get("credits", {}).get("used", 0),
                "credits_limit": usage.get("credits", {}).get("limit", 0),
                "transformations": usage.get("transformations", {}).get("used", 0),
                "storage": usage.get("storage", {}).get("used", 0),
                "bandwidth": usage.get("bandwidth", {}).get("used", 0),
            }
        except Exception as e:
            print(f"❌ Error getting upload stats: {e}")
            return {}

    def delete_image(self, public_id: str, folder: str = "images") -> bool:
        """Delete an image from Cloudinary"""
        try:
            result = cloudinary.uploader.destroy(f"{folder}/{public_id}")
            return result.get("result") == "ok"
        except Exception as e:
            print(f"❌ Error deleting image: {e}")
            return False


def test_cloudinary_connection() -> bool:
    """Test function for Cloudinary connection"""
    try:
        provider = CloudinaryProvider()
        return provider.test_connection()
    except Exception as e:
        print(f"❌ Cloudinary test failed: {e}")
        return False


if __name__ == "__main__":
    # Test the Cloudinary provider
    print("🧪 Testing Cloudinary Provider")
    print("=" * 40)

    if test_cloudinary_connection():
        provider = CloudinaryProvider()
        stats = provider.get_upload_stats()
        if stats:
            print("📊 Account Stats:")
            print(f"   Credits Used: {stats.get('credits_used', 'N/A')}")
            print(f"   Storage Used: {stats.get('storage', 'N/A')} bytes")
            print(f"   Transformations: {stats.get('transformations', 'N/A')}")
        else:
            print("✅ Cloudinary integration is working correctly!")
            print("\n🚀 Ready to use:")
            print("   ./process_csv.sh (choose Cloudinary option)")
            print("   python unified_upload.py --provider cloudinary --mode csv")
    else:
        print("❌ Cloudinary connection test failed")
