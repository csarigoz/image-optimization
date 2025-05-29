#!/usr/bin/env python3
"""
Cloudinary Integration Test Script

Simplified test script focusing on Cloudinary-specific integration testing.
Basic functionality tests are handled by the main CI pipeline.

Usage:
    python test_cloudinary.py
"""

import os
import sys

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_configuration_and_connection():
    """Test Cloudinary configuration and connection in one step"""
    print("🔧 Testing Cloudinary configuration and connection...")

    # Check environment variables
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
    api_key = os.getenv("CLOUDINARY_API_KEY")
    api_secret = os.getenv("CLOUDINARY_API_SECRET")

    if not all([cloud_name, api_key, api_secret]):
        print("❌ Missing Cloudinary credentials in environment")
        print(
            "   Required: CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET"
        )
        return False

    print(f"✅ Configuration found - Cloud: {cloud_name}, API Key: {api_key[:8]}...")

    # Test connection using existing function
    try:
        from cloudinary_provider import test_cloudinary_connection

        if test_cloudinary_connection():
            print("✅ Cloudinary connection successful")
            return True
        else:
            print("❌ Cloudinary connection failed")
            return False
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False


def test_unified_integration():
    """Test Cloudinary through the unified upload system"""
    print("\n🔄 Testing unified uploader integration...")

    try:
        from unified_upload import UnifiedUploader

        # Create uploader with explicit Cloudinary selection
        uploader = UnifiedUploader("cloudinary")
        print("✅ UnifiedUploader with Cloudinary created")

        # Test connection through uploader
        if uploader.test_connection():
            print("✅ Uploader connection test passed")

            # Test getting stats
            stats = uploader.get_stats()
            if stats and stats.get("provider") == "cloudinary":
                print(
                    f"✅ Stats retrieved - Total files: {stats.get('total_files', 0)}"
                )
                return True
            else:
                print("❌ Could not retrieve Cloudinary stats")
                return False
        else:
            print("❌ Uploader connection test failed")
            return False

    except Exception as e:
        print(f"❌ Error testing unified integration: {e}")
        return False


def main():
    """Run Cloudinary integration tests"""
    print("🧪 Cloudinary Integration Test Suite")
    print("=" * 50)

    tests = [
        ("Configuration & Connection", test_configuration_and_connection),
        ("Unified System Integration", test_unified_integration),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{'='*15} {test_name} {'='*15}")

        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"💥 {test_name} CRASHED: {e}")

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 Cloudinary integration is working correctly!")
        print("\n🚀 Ready to use:")
        print("   ./process_csv.sh (choose Cloudinary option)")
        print("   python unified_upload.py --provider cloudinary --mode csv")
        return True
    else:
        print("❌ Integration issues detected. Check configuration and credentials.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
