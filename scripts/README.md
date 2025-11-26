# Scripts Directory

## generate-content.sh

Automatically generates Hugo content files (`.md`) from YAML data files.

### Purpose

This script eliminates the need to manually create `.md` files in `content/` directories. You only need to create/edit YAML files in `data/`, and the script will automatically generate the required Hugo content files.

### Prerequisites

- **yq** - YAML processor
  ```bash
  brew install yq
  ```

### Usage

```bash
# From project root
./scripts/generate-content.sh

# Or from scripts directory
cd scripts
./generate-content.sh
```

### What it does

1. **Objects** (`data/objects/*.yaml` → `content/objects/*.md`)
   - Reads each YAML file in `data/objects/`
   - Generates a minimal `.md` file with title and description
   - Example: `AIRLINE.yaml` → `airline.md`

2. **Views** (`data/views/*.yaml` → `content/views/*.md`)
   - Reads each YAML file in `data/views/`
   - Generates a minimal `.md` file with title and description
   - Example: `PassengerCheckIn_KioskView.yaml` → `PassengerCheckIn_KioskView.md`

3. **Perspectives** (from `data/objects/*.yaml` → `content/perspectives/*.md`)
   - Reads SystemPerspectives from each object YAML
   - Generates one `.md` file per perspective
   - Example: AIRLINE's "Route Management" → `airline-route-management.md`

### Workflow

**Before (Manual):**
1. Create `data/objects/CREW.yaml` with all data
2. Manually create `content/objects/crew.md` with front matter
3. Manually create `content/perspectives/crew-roster.md` for each perspective

**After (Automated):**
1. Create `data/objects/CREW.yaml` with all data
2. Run `./scripts/generate-content.sh`
3. ✨ All `.md` files generated automatically!

### Integration with Hugo

Add to your build process:

```bash
# Before building
./scripts/generate-content.sh

# Then build
hugo build
```

Or add to `package.json`:

```json
{
  "scripts": {
    "prebuild": "./scripts/generate-content.sh",
    "build": "hugo build",
    "dev": "./scripts/generate-content.sh && hugo server"
  }
}
```

### Safety

- ⚠️ The script **overwrites** existing `.md` files in `content/`
- 💡 This is intentional - `.md` files are now considered "generated artifacts"
- ✅ All real data lives in YAML files (which are version controlled)
- ✅ `.md` files can be regenerated anytime

### Adding to .gitignore (Optional)

If you want to treat `.md` files as build artifacts:

```gitignore
# Generated content files (can be regenerated from YAML)
content/objects/*.md
content/views/*.md
content/perspectives/*.md

# Keep index files
!content/objects/_index.md
!content/views/_index.md
!content/perspectives/_index.md
```

This ensures only YAML files are tracked in Git, and `.md` files are generated during build.
