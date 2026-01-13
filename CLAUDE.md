# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 语言设置 (Language Settings)

**重要**: 在这个项目中工作时，Claude 应该默认使用中文回复，即使用户使用英文提问。技术术语和代码相关内容应同时提供中文和英文（英文在括号内）。

**IMPORTANT**: When working in this project, Claude should respond in Chinese by default, even when queried in English. Technical terms and code-related content should be provided in both Chinese and English (with English in parentheses).

## context7 MCP
for non trivial task, always get information from context7 mcp first unless especifically instructed not to.


## Project Overview

MusicPracticeSelector-n-Tracker is a Python desktop application for organizing and tracking music practice materials. It uses Tkinter for GUI, processes markdown files with YAML frontmatter, and generates PDF practice sheets.

## Commands

**Run the application:**
```bash
python app.py
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

## Architecture

### Core Components

- **app.py**: Main GUI application with tag filtering, PDF export, and configuration management
- **reading.py**: `Reading` class for parsing markdown files with frontmatter containing tags and practice dates
- **util.py**: PDF generation, file searching, and image embedding utilities

### Data Flow

1. Application reads vault path from `config.json`
2. Scans `VaultPath/Readings/` for markdown files with YAML frontmatter
3. Extracts tags from frontmatter and "Last Practice Date" from content
4. Creates pandas DataFrame with one-hot encoding for tag filtering
5. Exports selected pieces to PDF, updating practice dates in source files

### Expected Vault Structure

```
VaultPath/
├── Tags/       # Tag definition markdown files
└── Readings/   # Music piece markdown files with frontmatter
```

### Key Technical Details

- Uses `![[filename]]` syntax in markdown for embedding images/PDFs
- PDF generation via ReportLab with pypdfium2 for PDF-to-image conversion
- Tag filtering uses pandas DataFrame with one-hot encoding
- Practice dates format: "Last Practice Date: YYYY-MM-DD" in markdown body
- GUI built with tkinter, creating checkboxes dynamically for each tag

## Development Notes

- No test framework configured - manual testing only
- TypeScript config exists but no TypeScript code present
- Application saves vault path to `config.json` for persistence
- PDF exports go to `VaultPath/Exports/` directory