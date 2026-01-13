#!/bin/bash

# Music Practice Tracker Build Script
# This script builds the application for different platforms

echo "==================================="
echo "Music Practice Tracker Build Script"
echo "==================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    exit 1
fi

print_status "Python 3 found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install requirements
print_status "Installing requirements..."
pip install -r requirements.txt

# Install PyInstaller
print_status "Installing PyInstaller..."
pip install pyinstaller

# Clean previous builds
print_status "Cleaning previous builds..."
rm -rf build dist

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     
        PLATFORM="Linux"
        OUTPUT_NAME="MusicPracticeTracker"
        ;;
    Darwin*)    
        PLATFORM="macOS"
        OUTPUT_NAME="MusicPracticeTracker"
        ;;
    MINGW*|CYGWIN*|MSYS*)     
        PLATFORM="Windows"
        OUTPUT_NAME="MusicPracticeTracker.exe"
        ;;
    *)          
        PLATFORM="Unknown"
        ;;
esac

print_status "Building for ${PLATFORM}..."

# Build with PyInstaller
if [ "$1" == "--onedir" ]; then
    print_status "Building as directory bundle..."
    pyinstaller \
        --name MusicPracticeTracker \
        --windowed \
        --add-data "config.json:." \
        --add-data "requirements.txt:." \
        --add-data "README.md:." \
        --add-data "license.md:." \
        --hidden-import pandas \
        --hidden-import reportlab \
        --hidden-import pypdfium2 \
        --hidden-import PIL \
        --hidden-import tkinter \
        --clean \
        app.py
else
    print_status "Building as single executable..."
    pyinstaller \
        --name MusicPracticeTracker \
        --onefile \
        --windowed \
        --add-data "config.json:." \
        --add-data "requirements.txt:." \
        --add-data "README.md:." \
        --add-data "license.md:." \
        --hidden-import pandas \
        --hidden-import reportlab \
        --hidden-import pypdfium2 \
        --hidden-import PIL \
        --hidden-import tkinter \
        --clean \
        app.py
fi

# Check if build was successful
if [ -f "dist/${OUTPUT_NAME}" ] || [ -d "dist/MusicPracticeTracker" ]; then
    print_status "Build completed successfully!"
    print_status "Output location: dist/"
    
    # Create a zip file for distribution
    print_status "Creating distribution archive..."
    cd dist
    if [ "$PLATFORM" == "Windows" ]; then
        # For Windows, use zip
        zip -r "MusicPracticeTracker-${PLATFORM}.zip" *
    else
        # For Unix-like systems, use tar
        tar -czf "MusicPracticeTracker-${PLATFORM}.tar.gz" *
    fi
    cd ..
    
    print_status "Distribution archive created in dist/"
else
    print_error "Build failed!"
    exit 1
fi

# Deactivate virtual environment
deactivate

echo ""
echo "==================================="
echo "Build Process Complete!"
echo "==================================="
echo ""
echo "To run the application:"
if [ "$1" == "--onedir" ]; then
    echo "  ./dist/MusicPracticeTracker/MusicPracticeTracker"
else
    echo "  ./dist/${OUTPUT_NAME}"
fi