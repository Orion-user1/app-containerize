#!/usr/bin/env python3
"""
Create Image Digest Script - Dummy Implementation
This creates the cryptographic digest of the published image.
TODO: Implement actual digest retrieval from registry
"""
import sys
import json

def main():
    print("=" * 60)
    print("Create Image Digest - Dummy Implementation")
    print("=" * 60)

    # Read image URL from previous stage
    try:
        with open('image_url.txt', 'r') as f:
            image_url = f.read().strip()
        print(f"→ Getting digest for: {image_url}")
    except FileNotFoundError:
        print("✗ Error: image_url.txt not found")
        return 1

    print("  (Dummy digest - not actually querying registry)")

    # Create dummy digest
    digest = "sha256:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"

    with open('image_digest.txt', 'w') as f:
        f.write(digest)

    # Create dummy manifest
    manifest = {
        "schemaVersion": 2,
        "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
        "config": {
            "digest": digest,
            "size": 1234
        },
        "layers": [
            {"digest": "sha256:layer1", "size": 1000},
            {"digest": "sha256:layer2", "size": 2000}
        ]
    }

    with open('manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"\n✅ Digest created (dummy)")
    print(f"   Digest: {digest[:20]}...")
    print(f"   Saved to: image_digest.txt")
    print(f"   Manifest saved to: manifest.json")
    return 0

if __name__ == "__main__":
    sys.exit(main())
