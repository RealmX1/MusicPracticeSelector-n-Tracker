# Music Practice Selector & Tracker

A Python desktop application for organizing, filtering, and tracking music practice materials. Designed to work seamlessly with digital music readers and page-turning pedals.

## Overview

This application helps musicians systematically manage their sheet music library by providing tag-based filtering, practice tracking, and PDF export capabilities. The exported PDFs are optimized for use with tablet-based music reading apps that support Bluetooth page-turning pedals, enabling hands-free practice sessions.

## Features

- **Smart Music Library Management**: Organize sheet music using markdown files with metadata tags
- **Tag-Based Filtering**: Filter pieces by difficulty level, genre, composer, or custom tags
- **Practice Tracking**: Automatically track and update last practice date for each piece
- **PDF Export**: Generate consolidated PDF practice books from selected pieces
- **Pedal-Friendly Output**: Exported PDFs work perfectly with digital music stands and page-turning pedals
- **Persistent Configuration**: Remembers your music library location between sessions

## Installation

### Prerequisites
- Python 3.x
- pip (Python package manager)

### Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/MusicPracticeSelector-n-Tracker.git
   cd MusicPracticeSelector-n-Tracker
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Dependencies
- `pandas` - Data manipulation and filtering
- `reportlab` - PDF generation
- `pypdfium2` - PDF to image conversion

## Usage

### Running the Application
```bash
python app.py
```

### Initial Setup
1. Launch the application
2. Click "Select Vault Path" to choose your music library folder
3. The application will scan for compatible markdown files with tags

### Workflow with Digital Music Readers

1. **Select Practice Material**: Use tag filters to choose pieces for your practice session
2. **Export to PDF**: Click "Export to PDF" to generate a consolidated practice book
3. **Transfer to Tablet**: Copy the PDF to your tablet or music reading device
4. **Connect Pedal**: Pair your Bluetooth page-turning pedal with your device
5. **Practice Hands-Free**: Use the pedal to navigate through pieces while playing

### Recommended Music Reader Apps
Works great with:
- forScore (iOS)
- MobileSheets (Android/Windows)
- Piascore (iOS)
- Any PDF reader app that supports external page-turning devices

## Music Library Structure

Your music library should follow this structure:

```
YourMusicVault/
├── Tags/           # Tag definition files (optional)
├── Readings/       # Your sheet music files
│   ├── piece1.md
│   ├── piece2.md
│   └── ...
└── Exports/        # Generated PDFs (created automatically)
```

### Music File Format

Each music piece should be a markdown file with YAML frontmatter:

```markdown
---
tags:
  - intermediate
  - classical
  - bach
---

# Invention No. 1 in C Major

Last Practice Date: 2024-01-15

![[invention1_page1.pdf]]
![[invention1_page2.pdf]]
```

### Supported Tags
Common tags include:
- Difficulty: `beginner`, `intermediate`, `advanced`
- Genre: `classical`, `jazz`, `contemporary`, `etude`
- Composer: `bach`, `chopin`, `beethoven`
- Custom tags for your organization needs

## Features in Detail

### Tag Filtering
- Multiple tag selection with AND logic
- Dynamic checkbox generation based on available tags
- Real-time piece count updates

### Practice Tracking
- Automatically updates "Last Practice Date" in source files
- Helps identify pieces that need review
- Maintains practice history in markdown format

### PDF Generation
- Embeds images and existing PDFs into consolidated output
- Maintains proper page formatting for music notation
- Optimized file size for tablet storage

## System Requirements

- **Operating Systems**: Windows, macOS, Linux (Ubuntu tested)
- **Python Version**: 3.6 or higher
- **Display**: Minimum 800x600 resolution
- **Storage**: Varies based on music library size

## Tips for Best Results

1. **Consistent Naming**: Use clear, descriptive filenames for your music pieces
2. **Regular Backups**: Keep backups of your music vault
3. **Tag Strategy**: Develop a consistent tagging system that matches your practice goals
4. **PDF Optimization**: For large libraries, export practice sessions in smaller batches
5. **Pedal Settings**: Configure your pedal app for optimal page-turn sensitivity

## Troubleshooting

### Application Won't Start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.6+)

### PDFs Not Generating
- Verify source markdown files have proper frontmatter
- Check that referenced images/PDFs exist in the vault
- Ensure write permissions in the Exports directory

### Tags Not Showing
- Confirm markdown files have valid YAML frontmatter
- Check that tags are properly formatted as a list

## License

See [license.md](license.md) for details.

## Contributing

This project has reached feature completion and is no longer under active development. However, feel free to fork and adapt it for your needs.

## Acknowledgments

Designed for musicians who value organized practice sessions and seamless integration with modern digital music tools.