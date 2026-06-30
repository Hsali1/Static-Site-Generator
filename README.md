# Static Site Generator

A static site generator written in Python that converts Markdown documents into a complete static website.

The generator recursively traverses a content directory, parses Markdown into an HTML node tree, applies an HTML template, copies static assets, and produces a deployable website.

---

## Live Demo

https://hsali1.github.io/Static-Site-Generator/

---

## Features

- Converts Markdown to HTML
- Recursive directory traversal
- Generates entire websites from Markdown content
- Supports:
  - Headings
  - Paragraphs
  - Blockquotes
  - Ordered lists
  - Unordered lists
  - Code blocks
  - Bold text
  - Italic text
  - Inline code
  - Images
  - Links
- HTML template system
- Automatic static asset copying
- GitHub Pages compatible (configurable base path)
- Recursive page generation while preserving directory structure

---

## Example Project Structure

```text
content/
├── index.md
├── contact/
│   └── index.md
└── blog/
    ├── glorfindel/
    │   └── index.md
    ├── majesty/
    │   └── index.md
    └── tom/
        └── index.md
```

Generated output:

```text
docs/
├── index.html
├── contact/
│   └── index.html
└── blog/
    ├── glorfindel/
    │   └── index.html
    ├── majesty/
    │   └── index.html
    └── tom/
        └── index.html
```

---

## How It Works

The generation pipeline consists of several stages:

```
Markdown
      │
      ▼
TextNode objects
      │
      ▼
HTML Node Tree
      │
      ▼
Rendered HTML
      │
      ▼
Template Rendering
      │
      ▼
Static Website
```

The site generator recursively walks the `content` directory, converts every Markdown page into HTML, applies a common HTML template, copies static assets, and writes the finished pages to the output directory.

---

## Technologies

- Python 3
- HTML
- Recursive algorithms
- File system traversal
- Object-oriented programming

---

## Running Locally

Build the site:

```bash
./build.sh
```

Run the local development server:

```bash
./main.sh
```

Then open:

```
http://localhost:8888
```

---

## Deployment

The project supports deployment to GitHub Pages.

The build script generates the site with the appropriate base path so links and static assets work correctly when hosted from a repository.

---

## Testing

Run the complete test suite:

```bash
./test.sh
```

---

## What I Learned

This project helped me practice:

- Recursive filesystem traversal
- Recursive HTML generation
- Parsing Markdown
- Designing an HTML node tree
- Object-oriented design
- File I/O
- Template rendering
- Static website generation
- Building command-line applications

---

## Acknowledgements

This project was built as part of the **Boot.dev Backend Developer** curriculum. The implementation, architecture, and code are my own.