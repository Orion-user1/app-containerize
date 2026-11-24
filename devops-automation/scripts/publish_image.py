#!/usr/bin/env python3
"""
Publish Image Script - Environment-Aware Dummy Implementation
This publishes the image to JFrog Artifactory (Non-Prod or Prod).
TODO: Implement actual Docker push to Artifactory
"""
import sys
import os

def determine_environment():
    """
    Determine deployment environment.
    Priority:
    1. ENVIRONMENT variable (set by Harness)
    2. DEPLOY_ENV variable (pipeline parameter)
    3. GIT_BRANCH (infer from branch name)
    4. Default to 'nonprod' (safe default)
    """
    # Option 1: Explicit environment variable
    env = os.getenv('ENVIRONMENT')
    if env:
        return env.lower()

    # Option 2: Deploy environment parameter
    deploy_env = os.getenv('DEPLOY_ENV')
    if deploy_env:
        return deploy_env.lower()

    # Option 3: Infer from Git branch
    git_branch = os.getenv('GIT_BRANCH', os.getenv('BRANCH_NAME', ''))
    if git_branch:
        if git_branch in ['main', 'master']:
            return 'prod'
        elif git_branch.startswith('release/'):
            return 'prod'
        else:
            return 'nonprod'

    # Default: Non-prod (safe default)
    return 'nonprod'

def get_repository_config(environment):
    """
    Get JFrog repository configuration based on environment.
    """
    # Base URL (same for both environments)
    artifactory_url = os.getenv('ARTIFACTORY_URL', 'artifactory.company.com')

    # Allow explicit repo override
    override_repo = os.getenv('ARTIFACTORY_REPO')

    if environment == 'prod':
        repo = override_repo or os.getenv('ARTIFACTORY_PROD_REPO', 'docker-prod-local')
    else:
        repo = override_repo or os.getenv('ARTIFACTORY_NONPROD_REPO', 'docker-nonprod-local')

    return {
        'url': artifactory_url,
        'repo': repo
    }

def main():
    print("=" * 60)
    print("Publish Image - Environment-Aware (Dummy)")
    print("=" * 60)

    # Read image ID from earlier stage
    try:
        with open('image_id.txt', 'r') as f:
            image_id = f.read().strip()
    except FileNotFoundError:
        print("✗ Error: image_id.txt not found")
        return 1

    # Determine environment
    environment = determine_environment()
    print(f"\n→ Environment Detection:")
    print(f"   ENVIRONMENT var: {os.getenv('ENVIRONMENT', '(not set)')}")
    print(f"   GIT_BRANCH var: {os.getenv('GIT_BRANCH', os.getenv('BRANCH_NAME', '(not set)'))}")
    print(f"   Determined: {environment.upper()}")

    # Get repository configuration
    config = get_repository_config(environment)

    # Get image details
    image_name = os.getenv('IMAGE_NAME', 'myapp')
    image_tag = os.getenv('IMAGE_TAG', '1.0.0')

    # Build full image URL
    image_url = f"{config['url']}/{config['repo']}/{image_name}:{image_tag}"

    print(f"\n→ Publishing Details:")
    print(f"   Target Environment: {environment.upper()}")
    print(f"   Artifactory URL: {config['url']}")
    print(f"   Repository: {config['repo']}")
    print(f"   Image: {image_name}:{image_tag}")
    print(f"   Full URL: {image_url}")

    print(f"\n→ Publishing to JFrog {environment.upper()} (dummy)...")
    print("   (Dummy - not actually pushing to Artifactory)")
    print("   Would execute:")
    print(f"   1. docker login {config['url']}")
    print(f"   2. docker tag {image_id} {image_url}")
    print(f"   3. docker push {image_url}")
    print("   4. Update metadata in Artifactory")

    # Save image URL for next stage
    with open('image_url.txt', 'w') as f:
        f.write(image_url)

    print(f"\n✅ Image published to {environment.upper()} (dummy)")
    print(f"   URL: {image_url}")
    print(f"   Saved to: image_url.txt")
    return 0

if __name__ == "__main__":
    sys.exit(main())
