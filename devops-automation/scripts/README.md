# Pipeline Scripts

## Status

All 8 scripts are **ready with dummy implementation** for testing.

---

## Scripts

| # | Script | Purpose |
|---|--------|---------|
| 1 | `container_file_lint.py` | Validate Dockerfile |
| 2 | `create_image.py` | Build Docker image |
| 3 | `blackduck_image_scan.py` | Security scan (BlackDuck) |
| 4 | `vulnerability_check.py` | Enforce security policies |
| 5 | `create_sbom.py` | Generate SBOM |
| 6 | `publish_image.py` | Publish to JFrog (Non-Prod/Prod) |
| 7 | `create_image_digest.py` | Create image digest |
| 8 | `cosign_attestation.py` | Sign with Cosign |

---

## Data Flow

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
publish_image.py → image_url.txt
   ↓
create_image_digest.py → image_digest.txt
   ↓
cosign_attestation.py → signature.txt
```

---

## Current Implementation

**Dummy scripts:**
- ✅ Return exit code 0 (success)
- ✅ Create output files for next steps
- ✅ Print informative messages
- ✅ Pipeline runs successfully end-to-end
- ❌ Don't do actual work (Docker, BlackDuck, Cosign)

**Purpose:** Test pipeline structure before real implementation.

---

## Next Steps

Replace dummy implementation with real logic:

1. `container_file_lint.py` - Add real Dockerfile validation
2. `create_image.py` - Add `docker build` command
3. `blackduck_image_scan.py` - Integrate BlackDuck API
4. `vulnerability_check.py` - Add policy enforcement
5. `create_sbom.py` - Generate real SBOM
6. `publish_image.py` - Add `docker push` to JFrog
7. `create_image_digest.py` - Get real digest from registry
8. `cosign_attestation.py` - Implement Cosign signing

---

## Script Template

```python
#!/usr/bin/env python3
import sys
import os

def main():
    try:
        # 1. Read inputs (from previous step)
        # 2. Do the work
        # 3. Save outputs (for next step)
        # 4. Print status
        return 0  # Success
    except Exception as e:
        print(f"Error: {e}")
        return 1  # Failure

if __name__ == "__main__":
    sys.exit(main())
```

---

**Version:** 1.0 (Dummy Implementation)
