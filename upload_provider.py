#!/usr/bin/env python3
"""
Upload Provider Interface

This module defines the abstract base class for upload providers,
allowing the application to support multiple cloud services
(CloudFront/S3, Cloudinary, etc.) through a unified interface.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple, Union


class UploadProvider(ABC):
    """Abstract base class for upload providers"""

    @abstractmethod
    def test_connection(self) -> bool:
        """Test the provider's API connection"""
        pass

    @abstractmethod
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
        """
        Upload an image file with optimization

        Args:
            file_path: Path to the local image file
            file_name: Original filename
            max_width: Maximum width for resizing
            quality: Image quality (1-100)
            smart_format: Enable automatic format selection
            add_timestamp: Add timestamp to filename
            **kwargs: Provider-specific options

        Returns:
            Tuple of (success, public_url, metadata)
        """
        pass

    @abstractmethod
    def upload_from_url(
        self,
        source_url: str,
        max_width: Optional[int] = None,
        quality: int = 82,
        smart_format: bool = True,
        add_timestamp: bool = True,
        **kwargs,
    ) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Upload an image directly from URL

        Args:
            source_url: URL of the image to upload
            max_width: Maximum width for resizing
            quality: Image quality (1-100)
            smart_format: Enable automatic format selection
            add_timestamp: Add timestamp to filename
            **kwargs: Provider-specific options

        Returns:
            Tuple of (success, public_url, metadata)
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the name of this provider"""
        pass

    def get_upload_stats(self) -> Dict[str, Any]:
        """Get provider usage statistics (optional)"""
        return {}

    def delete_image(self, identifier: str, **kwargs) -> bool:
        """Delete an image (optional)"""
        return False

    def generate_responsive_url(
        self, identifier: str, transformations: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate a responsive URL with transformations (optional)"""
        return ""


class ProviderFactory:
    """Factory class for creating upload providers"""

    @staticmethod
    def create_provider(provider_type: str) -> UploadProvider:
        """
        Create an upload provider based on type

        Args:
            provider_type: Type of provider ('cloudfront' or 'cloudinary')

        Returns:
            UploadProvider instance
        """
        provider_type = provider_type.lower().strip()

        if provider_type == "cloudfront":
            from cloudfront_provider import CloudFrontProvider

            return CloudFrontProvider()
        elif provider_type == "cloudinary":
            from cloudinary_provider import CloudinaryProvider

            # Wrap CloudinaryProvider to match the interface
            return CloudinaryProviderAdapter()
        else:
            raise ValueError(f"Unknown provider type: {provider_type}")


class CloudinaryProviderAdapter(UploadProvider):
    """Adapter to make CloudinaryProvider conform to UploadProvider interface"""

    def __init__(self):
        from cloudinary_provider import CloudinaryProvider

        self.provider = CloudinaryProvider()

    def test_connection(self) -> bool:
        return self.provider.test_connection()

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
        folder = kwargs.get("folder", "images")
        return self.provider.upload_image(
            file_path,
            file_name,
            max_width,
            quality,
            smart_format,
            add_timestamp,
            folder,
        )

    def upload_from_url(
        self,
        source_url: str,
        max_width: Optional[int] = None,
        quality: int = 82,
        smart_format: bool = True,
        add_timestamp: bool = True,
        **kwargs,
    ) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        folder = kwargs.get("folder", "images")
        return self.provider.upload_from_url(
            source_url, max_width, quality, smart_format, add_timestamp, folder
        )

    def get_provider_name(self) -> str:
        return "cloudinary"

    def get_upload_stats(self) -> Dict[str, Any]:
        return self.provider.get_upload_stats()

    def delete_image(self, identifier: str, **kwargs) -> bool:
        folder = kwargs.get("folder", "images")
        return self.provider.delete_image(identifier, folder)

    def generate_responsive_url(
        self, identifier: str, transformations: Optional[Dict[str, Any]] = None
    ) -> str:
        folder = "images"  # Default folder
        return self.provider.generate_responsive_url(
            identifier, folder, transformations
        )
