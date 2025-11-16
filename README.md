# FP Template

Template for **Cem & Javi**: LaTeX documents for academic papers in German academic contexts.

---

## Table of Contents

- [FP Template](#fp-template)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Installation](#installation)
    - [LaTeX Installation](#latex-installation)
      - [Fedora Linux](#fedora-linux)
      - [macOS](#macos)
      - [Windows](#windows)
  - [Repository Structure](#repository-structure)
  - [Troubleshooting](#troubleshooting)
    - [Common Issues](#common-issues)
      - [Python Environment](#python-environment)
      - [LaTeX Build](#latex-build)
      - [Windows Specific](#windows-specific)
    - [Getting Help](#getting-help)

---

## Project Overview

This template provides **LaTeX document generation** specifically designed for German academic papers. It provides:

- **Structured LaTeX documents** following German academic conventions
- **Modern development workflow** with uv package management
- **VS Code integration** for LaTeX development

---

## Installation

**Linux/macOS:**
```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create environment and install dependencies
uv sync
```

**Windows**
```powershell
# Install uv
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Create environment
uv sync
```

### LaTeX Installation

#### Fedora Linux
```bash
sudo dnf install -y texlive-scheme-medium latexmk biber texlive-cleveref
```

#### macOS
```bash
brew install --cask basictex
sudo tlmgr update --self
sudo tlmgr install latexmk biber
```

#### Windows
1. Download and install **MiKTeX** from [miktex.org/download](https://miktex.org/download)
2. Enable "Install missing packages on-the-fly" during installation
3. Verify installation:
   ```powershell
   latexmk -v
   pdflatex --version
   ```

---

## Repository Structure

```
├── tex/                      # LaTeX document structure
│   ├── main.tex              # Main document (German academic format)
│   ├── references.bib        # Bibliography database
│   └── sections/             # Modular document sections
│       ├── 00_zusammenfassung.tex    # Abstract/Summary
│       ├── 01_einführung.tex         # Introduction
│       ├── 02_theorie.tex            # Theory
│       ├── 03_durchführung.tex       # Methodology
│       ├── 04_ergebnisse.tex         # Results
│       ├── 05_diskussion.tex         # Discussion
│       ├── 06_schlussfolgerung.tex   # Conclusion
│       └── 07_anhang.tex             # Appendix
├── python-scripts/           # Python scripts directory (currently empty)
├── data/                     # Data directory (currently empty)
├── .vscode/                  # VS Code configuration
├── pyproject.toml            # Python project configuration
├── uv.lock                   # uv dependency lock file
└── README.md
```

---

## Troubleshooting

### Common Issues

#### Python Environment
- **"Command not found"**: Ensure virtual environment is activated (prompt shows `(.venv)`)
- **"uv not found"**: Install uv using the instructions in [Environment Setup](#environment-setup)
- **Import errors**: Run `uv sync` or `pip install -e .` to install dependencies

#### LaTeX Build
- **"latexmk not found"**: Install LaTeX using [LaTeX Installation](#latex-installation) instructions
- **Missing packages**: MiKTeX should install missing packages automatically on Windows
- **Build failures**: Check LaTeX compilation logs for detailed error messages

#### Windows Specific
- **PowerShell execution policy**: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- **Python not in PATH**: Reinstall Python and check "Add to PATH" option
- **LaTeX issues**: Try Git Bash terminal if PowerShell/Command Prompt fail

### Getting Help

1. Check LaTeX compilation logs for detailed error messages
2. Ensure all prerequisites are installed
3. If it doesn't work, contact Javi

