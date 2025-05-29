# Pull Request

## 📋 Description

Brief description of the changes in this PR.

## 🔗 Related Issues

- Fixes #(issue number)
- Relates to #(issue number)
- Part of #(issue number)

## 🎯 Type of Change

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📚 Documentation update
- [ ] 🎨 Code style/formatting changes
- [ ] ♻️ Code refactoring (no functional changes)
- [ ] ⚡ Performance improvements
- [ ] 🧪 Adding or updating tests
- [ ] 🔧 Build/CI changes
- [ ] 🌐 Provider-specific changes (Cloudinary/CloudFront)

## 🚀 Changes Made

### Core Changes
- [ ] Modified `upload_files.py` (legacy CloudFront application)
- [ ] Modified `unified_upload.py` (new multi-provider system)
- [ ] Modified `cloudinary_provider.py` (Cloudinary integration)
- [ ] Modified `cloudfront_provider.py` (CloudFront provider)
- [ ] Modified `upload_provider.py` (provider factory/interface)
- [ ] Modified `alttext_ai.py` (AltText.ai integration)
- [ ] Modified `setup.py` (environment setup)
- [ ] Modified `process_csv.sh` (interactive processor)
- [ ] Added new files
- [ ] Updated dependencies

### Provider-Specific Changes
- [ ] Cloudinary transformations/optimizations
- [ ] CloudFront/S3 upload logic
- [ ] Provider auto-detection logic
- [ ] Provider factory pattern
- [ ] Multi-provider configuration

### Specific Changes
- List specific changes made
- Include any new functions/classes added
- Mention any removed functionality
- Note any configuration changes

## 🧪 Testing

### Multi-Provider Testing
- [ ] Tested with Cloudinary provider
- [ ] Tested with CloudFront provider
- [ ] Tested provider auto-detection
- [ ] Tested provider switching
- [ ] Tested with both providers configured

### Manual Testing Performed
- [ ] Tested image upload functionality
- [ ] Tested CSV processing
- [ ] Tested local file uploads
- [ ] Tested AltText.ai integration
- [ ] Tested Flask API endpoints (legacy)
- [ ] Tested unified command line interface
- [ ] Tested error handling scenarios
- [ ] Tested provider connection validation

### Test Cases Covered
```bash
# Multi-provider testing commands
python test_cloudinary.py
python unified_upload.py --provider cloudinary --mode csv
python unified_upload.py --provider cloudfront --mode csv
python unified_upload.py --mode stats  # Auto-detection
./process_csv.sh

# Legacy testing commands  
python upload_files.py

# Provider-specific testing
python cloudinary_provider.py
python cloudfront_provider.py
```

### Test Results
- [ ] All existing functionality works as expected
- [ ] New functionality works as described
- [ ] Error cases are handled gracefully
- [ ] Performance is acceptable
- [ ] Both providers work correctly
- [ ] Provider switching works seamlessly

## 📸 Screenshots (if applicable)

Before:
<!-- Add screenshots showing the current behavior -->

After:
<!-- Add screenshots showing the new behavior -->

## 🔧 Configuration Changes

### Environment Variables
```bash
# Multi-provider configuration
UPLOAD_PROVIDER=cloudinary  # or 'cloudfront' or 'auto'

# Cloudinary configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# CloudFront configuration (existing)
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
S3_BUCKET=your_s3_bucket_name
CLOUDFRONT_DOMAIN=your_cloudfront_domain
```

### Dependencies
- [ ] Added new dependencies to `requirements.txt`
- [ ] Updated existing dependencies
- [ ] Removed dependencies

### Breaking Changes
- [ ] This PR introduces breaking changes
- [ ] Migration guide needed
- [ ] Backward compatibility maintained

## 📚 Documentation

- [ ] Updated README.md
- [ ] Updated CONTRIBUTING.md
- [ ] Updated PROJECT_RULES.md
- [ ] Updated CHANGELOG.md
- [ ] Added inline code comments
- [ ] Updated function docstrings
- [ ] Added usage examples
- [ ] Updated provider comparison documentation

## ✅ Pre-Commit Validation

**MANDATORY: All PRs must pass pre-commit checks**

- [ ] Ran `./pre_commit_check.sh` and all checks pass
- [ ] Code formatting (black, isort) applied
- [ ] Linting (flake8) passes
- [ ] Security checks (bandit, safety) pass
- [ ] All imports and functionality validated
- [ ] No uncommitted changes remain

```bash
# Verification command
./pre_commit_check.sh
```

## ✅ Checklist

### Code Quality
- [ ] My code follows the project's coding standards
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] I have followed the Git workflow (feature branch, no direct commits to main)

### Documentation
- [ ] I have made corresponding changes to the documentation
- [ ] I have updated the PROJECT_RULES.md if needed
- [ ] I have added examples for new features
- [ ] Provider-specific documentation is updated

### Testing
- [ ] I have tested my changes locally
- [ ] I have tested with different Python versions (3.9-3.13)
- [ ] I have tested with different image formats
- [ ] I have tested error scenarios
- [ ] I have tested provider-specific functionality

### Compatibility
- [ ] My changes are compatible with Python 3.9+
- [ ] My changes work on different operating systems
- [ ] My changes don't break existing functionality
- [ ] Backward compatibility is maintained for CloudFront users

## 🔍 Review Focus Areas

Please pay special attention to:
- [ ] Security implications
- [ ] Performance impact
- [ ] Error handling
- [ ] Code maintainability
- [ ] Documentation clarity
- [ ] Provider abstraction correctness
- [ ] Backward compatibility
- [ ] Multi-provider configuration handling

## 🤝 Contribution Guidelines

- [ ] I have read and followed the [CONTRIBUTING.md](../CONTRIBUTING.md) guidelines
- [ ] I have followed the [PROJECT_RULES.md](../PROJECT_RULES.md) conventions
- [ ] I understand this contribution will be licensed under the MIT License
- [ ] I have not committed directly to the main branch
- [ ] I am using a descriptive branch name with appropriate prefix

## 📝 Additional Notes

### Implementation Details
<!-- Explain any complex implementation decisions -->

### Future Improvements
<!-- Mention any follow-up work or improvements that could be made -->

### Known Limitations
<!-- List any known limitations or edge cases -->

### Provider-Specific Notes
<!-- Any provider-specific considerations or limitations -->

---

**For Maintainers:**

### Review Checklist
- [ ] Code quality meets project standards
- [ ] Tests are comprehensive and pass
- [ ] Documentation is updated and clear
- [ ] No security vulnerabilities introduced
- [ ] Performance impact is acceptable
- [ ] Breaking changes are properly documented
- [ ] Pre-commit checks have been run
- [ ] Provider abstraction is correct
- [ ] Multi-provider testing completed

### Merge Checklist
- [ ] All CI checks pass
- [ ] At least one maintainer approval
- [ ] No conflicts with main branch
- [ ] Release notes updated (if needed)
- [ ] Branch follows naming conventions
- [ ] PR title follows conventional commit format

---

**Thank you for contributing to the Multi-Provider Image Upload Utility!** 🎉

Your contribution helps make this tool better for everyone. If you have any questions about this PR, please don't hesitate to ask. 