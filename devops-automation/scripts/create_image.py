#!/usr/bin/env python3
"""
Create Image Script - Dummy Implementation
This builds the Docker image.
TODO: Implement actual Docker build
"""
import sys
import os

def main():
    print("=" * 60)
    print("Create Image - Dummy Implementation")
    print("=" * 60)

    image_name = os.getenv('IMAGE_NAME', 'myapp')
    image_tag = os.getenv('IMAGE_TAG', '1.0.0')

    print(f"→ Building image: {image_name}:{image_tag}")
    print("  (Dummy build - not actually building Docker image)")

    # Create dummy image ID for next stage
    image_id = "sha256:dummy123456789abcdef"
    with open('image_id.txt', 'w') as f:
        f.write(image_id)

    print(f"\n✅ Image created (dummy)")
    print(f"   Image ID: {image_id}")
    print(f"   Saved to: image_id.txt")
    return 0

if __name__ == "__main__":
    sys.exit(main())
