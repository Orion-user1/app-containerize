# CI/CD Application Containerization

Harness pipeline for containerizing OpenShift applications with security validation.

---

## Pipeline: App Containerize

**Repository:** `cicd-app-containerize`  
**Runs when:** Merges to main and hotfix pushes, OpenShift applications only  
**Type:** Build  
**Environment:** Non-Production (Initial Phase)

---

## Pipeline Steps

| Step | Description |
|------|-------------|
| 1. Container file lint | Check formatting, syntax and the stack's linter rules |
| 2. Create Image | Build the container image |
| 3. SCA Scan on Image | Scan newly built image for known vulnerabilities and disallowed licenses |
| 4. Vulnerability Check | Perform appropriate Cyber Security Vulnerability policy making sure all appropriate vulnerabilities do not exist |
| 5. Create SBOM | Create a Software Bill of Materials for the containerized application |
| 6. Publish Image | Publish all artifacts with the containerized application. Update all metadata properties |
| 7. Record Image Digest | Create the list of detailed metadata for the newly created Image Digest |
| 8. Image and Digest attestation | Sign and verify the containerized image and digest with an attestation |

---

## Tools Used

| Functionality | Tool |
|--------------|------|
| Code Repo | GitHub |
| CI/CD Orchestrator | Harness |
| SAST | Coverity |
| SCA | BlackDuck |
| Security reporting | SRM |
| Artifact Repository | JFrog Artifactory |
| Artifact security scan | JFrog Xray |
| GitOps deployment | ArgoCD |
| Secret Scan | Coverity |
| Container scan | BlackDuck |
| SBOM | BlackDuck |
| Sign container image | Cosign |

---

## Deployment Environment

**Current Phase:** Initial/Testing  
**Target Environment:** Non-Production  
**JFrog Repository:** `docker-nonprod-local`

All deployments go to Non-Production repository for testing and validation.

---

## Trigger Configuration

### When Pipeline Runs

**Automatic Triggers:**
- ✅ Merge to `main` branch
- ✅ Hotfix pushes to `main`

**Application Type:**
- ✅ OpenShift applications only

**Deployment Target:**
- ✅ Non-Production environment (docker-nonprod-local)

**Configuration in Harness:**
```yaml
Trigger Type: Webhook
Event: Push, Pull Request Merge
Branch: main
Application Filter: OpenShift
Deployment: Non-Production
```

---

## Project Structure

```
cicd-app-containerize/
├── README.md
├── cicd-app-containerize/
│   └── pipelines/
│       └── cicd-app-containerize.yaml
└── devops-automation/
    └── scripts/
        ├── container_file_lint.py
        ├── create_image.py
        ├── blackduck_image_scan.py
        ├── vulnerability_check.py
        ├── create_sbom.py
        ├── publish_image.py
        ├── create_image_digest.py
        └── cosign_attestation.py
```

---

## Deployment Strategy

### Trunk-Based Development (Initial Phase)

```
main branch → Non-Production (Testing)
  ↑
  └── feature/* branches → Local development
```

**Current Deployment Flow:**
1. Developers work on feature branches
2. Create Pull Request to `main`
3. After code review → Merge to `main`
4. **Pipeline triggers automatically**
5. Image built and published to **Non-Production** for testing

**Hotfix Flow:**
1. Create hotfix branch
2. Fix the issue
3. Push to `main`
4. **Pipeline triggers automatically**
5. Hotfix tested in **Non-Production**

---

## Environment Detection

Pipeline automatically deploys to Non-Production:

```
Branch: main → Environment: Non-Production → Repository: docker-nonprod-local
```

**Note:** Currently in **initial/testing phase** - all deployments go to Non-Production for validation and testing before production rollout.

---

## Configuration

### Required Variables (Set in Harness)

```
IMAGE_NAME                    # Application image name (e.g., "myapp")
IMAGE_TAG                     # Image version (e.g., build number)
ARTIFACTORY_URL               # JFrog URL (e.g., "artifactory.company.com")
ARTIFACTORY_NONPROD_REPO      # Non-Prod repo (e.g., "docker-nonprod-local")
BLACKDUCK_URL                 # BlackDuck URL (e.g., "https://blackduck.company.com")
BLACKDUCK_PROJECT             # BlackDuck project name
```

### Required Secrets (Set in Harness)

```
ARTIFACTORY_USER              # JFrog username
ARTIFACTORY_PASSWORD          # JFrog password/token
BLACKDUCK_API_TOKEN           # BlackDuck API token
COSIGN_KEY                    # Cosign private key
COSIGN_PASSWORD               # Cosign key password
```

---

## Script Execution Flow

```
container_file_lint.py
   ↓
create_image.py → image_id.txt
   ↓
blackduck_image_scan.py → blackduck_report.json
   ↓
vulnerability_check.py
   ↓
create_sbom.py → sbom.json
   ↓
publish_image.py → image_url.txt (to docker-nonprod-local)
   ↓
create_image_digest.py → image_digest.txt
   ↓
cosign_attestation.py → signature.txt
```

**Communication:** Scripts share data via files in the Harness workspace.

---

## How It Works

### 1. Script Execution

```
Pipeline Step → Harness runs: python3 devops-automation/scripts/<script>.py
                    ↓
              Script executes task
                    ↓
              Returns exit code (0 = success, 1 = failure)
                    ↓
              Success → Next step | Failure → Stop pipeline
```

### 2. JFrog Connection (Non-Prod)

```
Script reads environment variables from Harness:
  - ARTIFACTORY_URL
  - ARTIFACTORY_USER
  - ARTIFACTORY_PASSWORD
  - ARTIFACTORY_NONPROD_REPO (docker-nonprod-local)
     ↓
Script executes:
  1. docker login artifactory.company.com -u user -p password
  2. docker tag myapp:1 artifactory.company.com/docker-nonprod-local/myapp:1
  3. docker push artifactory.company.com/docker-nonprod-local/myapp:1
     ↓
Image published to JFrog Non-Production repository for testing
```

---

## Getting Started

### Prerequisites

- OpenShift application with Dockerfile
- Harness account with project configured
- JFrog Artifactory access (Non-Prod)
- BlackDuck project created
- Cosign keys generated

### Setup Steps

1. **Import Pipeline**
   - Copy `cicd-app-containerize.yaml` to Harness
   - Create new pipeline or import YAML

2. **Configure Variables**
   - Set `ARTIFACTORY_NONPROD_REPO` = `docker-nonprod-local`
   - Set all other required variables in Harness
   - Set all required secrets

3. **Setup Trigger**
   - Configure webhook for main branch
   - Test with a merge to main

4. **Connect Repository**
   - Link GitHub repository to Harness
   - Ensure webhook is active

5. **Test**
   - Create feature branch
   - Make changes
   - Create Pull Request to main
   - Merge PR
   - **Pipeline triggers automatically**
   - **Image published to Non-Prod for testing**

---

## Usage

### Non-Production Deployment

```bash
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Make changes and commit
git add .
git commit -m "Add new feature"
git push origin feature/new-feature

# 3. Create Pull Request on GitHub
# Merge to main after code review

# 4. Pipeline automatically triggers on merge
# 5. Image built and deployed to Non-Production for testing
```

### Testing in Non-Prod

```bash
# After pipeline completes:
# 1. Image available in: artifactory.company.com/docker-nonprod-local/myapp:1
# 2. Test the image in Non-Prod environment
# 3. Validate functionality
# 4. Check security scan results
# 5. Verify SBOM and attestation
```

---

## Security Features

- ✅ **Dockerfile Validation** - Linting and syntax check
- ✅ **Vulnerability Scanning** - BlackDuck SCA scan
- ✅ **Policy Enforcement** - No critical/high CVEs allowed
- ✅ **SBOM Generation** - Complete component inventory
- ✅ **Image Signing** - Cosign cryptographic signature
- ✅ **Attestation** - SBOM attached to image
- ✅ **Non-Prod Testing** - Validate in testing environment before production

---

## Troubleshooting

### Pipeline Not Triggering

**Check:**
- Webhook configured in Harness and GitHub
- Branch is `main`
- Event is push or merged PR
- Application is OpenShift type

### Script Fails

**Check:**
- Scripts exist in `devops-automation/scripts/` in Git
- All variables configured in Harness
- All secrets configured in Harness

### JFrog Push Fails

**Check:**
- `ARTIFACTORY_USER` and `ARTIFACTORY_PASSWORD` are correct
- Network connectivity to JFrog
- Repository `docker-nonprod-local` exists and is accessible
- User has write permissions to Non-Prod repository

### Vulnerability Check Fails

**Check:**
- BlackDuck scan results
- Critical or High CVEs found
- Update dependencies or request security exception

---

## Next Steps

After successful testing in Non-Production:

1. ✅ Validate all pipeline steps work correctly
2. ✅ Test image functionality in Non-Prod environment
3. ✅ Review security scan results
4. ✅ Verify SBOM and attestation
5. ✅ Update pipeline for Production deployment (when ready)

---

## Support

For pipeline issues or questions:
- **Pipeline Issues:** Check Harness execution logs
- **Script Issues:** Review script output in logs
- **Security Issues:** Contact Security team
- **Access Issues:** Contact DevOps team

---

**Status:** Testing/Non-Production  
**Version:** 1.0  
**Application Type:** OpenShift Only  
**Current Phase:** Initial - Non-Prod Testing  
**Deployment Target:** docker-nonprod-local
