# 🚀 Quick Start Guide: Adding New Entries to S4A Dictionary

## TL;DR - Simplified Workflow

**Before:** Create 2-4 files manually (YAML + multiple MD files)  
**Now:** Create 1 YAML file, run script → Done! ✨

---

## Adding a New Business Object

### Step 1: Create YAML File

Create `data/objects/YOUR_OBJECT.yaml`:

```yaml
TermID: YOUR-001
Name: YOUR_OBJECT
Steward: "Department Name"
Status: "active"
BusinessDefinition: |
  Clear definition of what this object represents.

CoreAttributes:
  - Name: Attribute Name
    Type: String
    Source: Source System

CoreRelationships:
  - type: has-many
    object: RELATED_OBJECT
    dependency: required

SystemPerspectives:
  "Perspective Name":
    Status: "active"
    Context: "How this perspective is used"
    PermittedUserGroups: ["User Group"]
    RelevantAttributes:
      - Name: Attribute Name
        Type: String
    SystemSpecificCTAs: ["Action Name"]
    ViewsUsed:
      - ref: "ViewName"
```

### Step 2: Run Generator

```bash
python3 scripts/generate-content.py
```

### Step 3: Build & Preview

```bash
hugo server
```

**That's it!** The script automatically creates:
- `content/objects/your_object.md`
- `content/perspectives/your_object-perspective-name.md` (for each perspective)

---

## Adding a New View

### Step 1: Create YAML File

Create `data/views/YourView_Name.yaml`:

```yaml
Description: "What this view shows"
Platform: "Desktop Web"
Status: "draft"
IncludedAttributes:
  - Name: Attribute Name
    Condition: "When to show"
AvailableCTAs:
  - Name: Action Name
    Condition: "When available"
AccessRules:
  - Role: "User Role"
    Permission: "Read/Write"
```

### Step 2: Run Generator

```bash
python3 scripts/generate-content.py
```

**Done!** The script creates `content/views/YourView_Name.md`

---

## What Gets Generated?

The script creates minimal `.md` files with front matter:

**For Objects:**
```markdown
---
title: "OBJECT_NAME"
description: "Definition of the OBJECT_NAME business object."
---
```

**For Views:**
```markdown
---
title: "View Name"
description: "View description from YAML"
---
```

**For Perspectives:**
```markdown
---
title: "Perspective Name"
object_id: "PARENT_OBJECT"
perspective_id: "Perspective Name"
---
```

---

## Important Notes

⚠️ **Generated files are overwritten** - Don't edit `.md` files manually!  
✅ **All data lives in YAML** - Edit YAML files only  
🔄 **Re-run script after YAML changes** - Regenerates all `.md` files  

---

## Integration with Git Workflow

### Option 1: Track Generated Files (Current)
```bash
# Edit YAML
vim data/objects/CREW.yaml

# Generate content
python3 scripts/generate-content.py

# Commit both YAML and generated MD
git add data/objects/CREW.yaml content/objects/crew.md
git commit -m "Add CREW object"
```

### Option 2: Ignore Generated Files (Recommended)
Add to `.gitignore`:
```gitignore
# Generated content (regenerated from YAML)
content/objects/*.md
content/views/*.md
content/perspectives/*.md

# Keep index files
!content/*/_index.md
```

Then add to build process:
```bash
# In CI/CD or local build
python3 scripts/generate-content.py && hugo build
```

---

## Troubleshooting

**Script fails with "No module named 'yaml'"**
```bash
pip3 install pyyaml
```

**Generated perspective not showing up**
- Check `object_id` matches YAML filename (e.g., `AIRLINE.yaml` → `object_id: "AIRLINE"`)
- Check `perspective_id` matches key in `SystemPerspectives`
- Re-run generator after fixing

**Changes not visible in Hugo**
```bash
# Regenerate content
python3 scripts/generate-content.py

# Clear Hugo cache
hugo --gc

# Rebuild
hugo server
```
