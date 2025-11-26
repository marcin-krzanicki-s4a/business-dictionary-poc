# S4A Business Dictionary

A comprehensive business dictionary built with Hugo, featuring interactive data lineage visualization and role-based access simulation.

## 🚀 Features

- **Business Objects**: Canonical data models with attributes and relationships
- **Perspectives**: System-specific views of business objects
- **UI Views**: Interface definitions with permissions and actions
- **Attributes**: Detailed data element specifications
- **Data Lineage Maps**: Interactive Mermaid.js diagrams showing data flow
- **Role Simulator**: Filter views and actions by user role
- **Search**: Fast client-side search across all entities

## 📋 Prerequisites

- [Hugo Extended](https://gohugo.io/installation/) v0.152.2 or later
- Python 3.x (for content generation scripts)

## 🛠️ Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/marcin-krzanicki-s4a/business-dictionary-poc.git
   cd business-dictionary-poc
   ```

2. **Run the development server**
   ```bash
   hugo server -D
   ```

3. **View the site**
   Open your browser to `http://localhost:1313`

## 📦 Building for Production

```bash
hugo --minify
```

The built site will be in the `public/` directory.

## 🔄 Content Generation

To generate attribute pages from YAML data:

```bash
python scripts/generate-content.py
```

## 📁 Project Structure

```
.
├── content/           # Markdown content files
│   ├── attributes/    # Attribute definitions
│   ├── objects/       # Business object pages
│   ├── perspectives/  # Perspective pages
│   └── views/         # UI view pages
├── data/              # YAML data files
│   ├── attributes/    # Attribute metadata
│   ├── objects/       # Object definitions
│   └── views/         # View configurations
├── layouts/           # Hugo templates
│   ├── _default/      # Default layouts
│   ├── attributes/    # Attribute templates
│   ├── perspectives/  # Perspective templates
│   └── views/         # View templates
├── static/            # Static assets
│   ├── css/          # Stylesheets
│   ├── js/           # JavaScript files
│   └── images/       # Images and icons
└── scripts/          # Utility scripts
```

## 🚢 Deployment

This site is automatically deployed to GitHub Pages using GitHub Actions.

### Setup GitHub Pages

1. Go to your repository **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. Push to the `main` branch to trigger deployment

The site will be available at: `https://marcin-krzanicki-s4a.github.io/business-dictionary-poc/`

## 🎨 Customization

### Colors

Edit CSS variables in `static/css/style.css`:

```css
:root {
    --s4a-red: #d32f2f;
    --s4a-light-violet: #7b1fa2;
    --s4a-dark-violet: #4a148c;
}
```

### Data Model

- Add new objects in `data/objects/`
- Add new views in `data/views/`
- Run `python scripts/generate-content.py` to update content

## 📄 License

Copyright © 2025 S4A. All Rights Reserved.

## 🤝 Contributing

This is an internal POC. For questions or suggestions, contact the Data Governance team.
