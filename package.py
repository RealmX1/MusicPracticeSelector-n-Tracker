#!/usr/bin/env python3
"""
Cross-platform packaging script for Music Practice Tracker
Provides both installer creation and portable packaging options
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

class AppPackager:
    def __init__(self):
        self.app_name = "MusicPracticeTracker"
        self.version = "1.0.0"
        self.root_dir = Path.cwd()
        self.dist_dir = self.root_dir / "dist"
        self.build_dir = self.root_dir / "build"
        self.system = platform.system()
        
    def clean_directories(self):
        """Clean build and dist directories"""
        print("🧹 Cleaning previous builds...")
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        print("✅ Cleaned build directories")
        
    def install_dependencies(self):
        """Install required dependencies"""
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ Dependencies installed")
        
    def build_executable(self, single_file=True):
        """Build executable using PyInstaller"""
        print(f"🔨 Building {'single file' if single_file else 'directory'} executable...")
        
        cmd = [
            "pyinstaller",
            "--name", self.app_name,
            "--windowed",
            "--add-data", f"config.json{os.pathsep}.",
            "--add-data", f"requirements.txt{os.pathsep}.",
            "--add-data", f"README.md{os.pathsep}.",
            "--add-data", f"license.md{os.pathsep}.",
            "--hidden-import", "pandas",
            "--hidden-import", "reportlab", 
            "--hidden-import", "pypdfium2",
            "--hidden-import", "PIL",
            "--hidden-import", "tkinter",
            "--clean",
        ]
        
        if single_file:
            cmd.append("--onefile")
            
        cmd.append("app.py")
        
        subprocess.run(cmd, check=True)
        print("✅ Executable built successfully")
        
    def create_portable_package(self):
        """Create a portable package with all necessary files"""
        print("📁 Creating portable package...")
        
        portable_dir = self.dist_dir / f"{self.app_name}-Portable-{self.system}"
        portable_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy executable
        if self.system == "Windows":
            exe_name = f"{self.app_name}.exe"
        else:
            exe_name = self.app_name
            
        exe_path = self.dist_dir / exe_name
        if exe_path.exists():
            shutil.copy2(exe_path, portable_dir / exe_name)
        
        # Copy documentation
        for doc_file in ["README.md", "license.md", "requirements.txt"]:
            if Path(doc_file).exists():
                shutil.copy2(doc_file, portable_dir / doc_file)
        
        # Create sample config
        sample_config = portable_dir / "config.sample.json"
        sample_config.write_text('{"VaultPath": ""}')
        
        # Create run script
        if self.system == "Windows":
            run_script = portable_dir / "run.bat"
            run_script.write_text(f"@echo off\nstart {exe_name}\n")
        else:
            run_script = portable_dir / "run.sh"
            run_script.write_text(f"#!/bin/bash\n./{exe_name}\n")
            run_script.chmod(0o755)
        
        print(f"✅ Portable package created at: {portable_dir}")
        return portable_dir
        
    def create_archive(self, source_dir):
        """Create compressed archive for distribution"""
        print("🗜️ Creating distribution archive...")
        
        archive_name = f"{self.app_name}-{self.version}-{self.system}"
        
        if self.system == "Windows":
            archive_path = self.dist_dir / f"{archive_name}.zip"
            shutil.make_archive(
                archive_path.with_suffix(""),
                'zip',
                self.dist_dir,
                source_dir.name
            )
        else:
            archive_path = self.dist_dir / f"{archive_name}.tar.gz"
            shutil.make_archive(
                archive_path.with_suffix("").with_suffix(""),
                'gztar',
                self.dist_dir,
                source_dir.name
            )
            
        print(f"✅ Archive created: {archive_path}")
        return archive_path
        
    def create_installer_script(self):
        """Create platform-specific installer scripts"""
        print("📝 Creating installer scripts...")
        
        if self.system == "Windows":
            # Create NSIS installer script
            nsis_script = self.dist_dir / "installer.nsi"
            nsis_content = f"""
!define APP_NAME "{self.app_name}"
!define APP_VERSION "{self.version}"
!define EXE_NAME "${{APP_NAME}}.exe"

Name "${{APP_NAME}} ${{APP_VERSION}}"
OutFile "${{APP_NAME}}-${{APP_VERSION}}-Setup.exe"
InstallDir "$PROGRAMFILES\\${{APP_NAME}}"

Section "Main"
    SetOutPath $INSTDIR
    File "dist\\${{EXE_NAME}}"
    File "README.md"
    File "license.md"
    
    CreateDirectory "$SMPROGRAMS\\${{APP_NAME}}"
    CreateShortcut "$SMPROGRAMS\\${{APP_NAME}}\\${{APP_NAME}}.lnk" "$INSTDIR\\${{EXE_NAME}}"
    CreateShortcut "$DESKTOP\\${{APP_NAME}}.lnk" "$INSTDIR\\${{EXE_NAME}}"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\\*.*"
    RMDir "$INSTDIR"
    Delete "$SMPROGRAMS\\${{APP_NAME}}\\*.*"
    RMDir "$SMPROGRAMS\\${{APP_NAME}}"
    Delete "$DESKTOP\\${{APP_NAME}}.lnk"
SectionEnd
"""
            nsis_script.write_text(nsis_content)
            print(f"✅ NSIS installer script created: {nsis_script}")
            
        elif self.system == "Linux":
            # Create .desktop file
            desktop_file = self.dist_dir / f"{self.app_name}.desktop"
            desktop_content = f"""[Desktop Entry]
Name={self.app_name}
Comment=Music Practice Material Organizer
Exec=/opt/{self.app_name}/{self.app_name}
Icon=/opt/{self.app_name}/icon.png
Terminal=false
Type=Application
Categories=Audio;Education;
"""
            desktop_file.write_text(desktop_content)
            
            # Create install script
            install_script = self.dist_dir / "install.sh"
            install_content = f"""#!/bin/bash
echo "Installing {self.app_name}..."
sudo mkdir -p /opt/{self.app_name}
sudo cp -r ./* /opt/{self.app_name}/
sudo chmod +x /opt/{self.app_name}/{self.app_name}
sudo cp {self.app_name}.desktop /usr/share/applications/
echo "Installation complete!"
"""
            install_script.write_text(install_content)
            install_script.chmod(0o755)
            print(f"✅ Linux installer script created: {install_script}")
            
    def package(self, single_file=True, create_installer=False):
        """Main packaging workflow"""
        print(f"\n🎵 Music Practice Tracker Packager v{self.version}")
        print(f"📍 Platform: {self.system}\n")
        
        try:
            self.clean_directories()
            self.install_dependencies()
            self.build_executable(single_file)
            
            portable_dir = self.create_portable_package()
            archive_path = self.create_archive(portable_dir)
            
            if create_installer:
                self.create_installer_script()
                
            print("\n✨ Packaging complete!")
            print(f"📦 Distribution files in: {self.dist_dir}")
            print("\nAvailable packages:")
            print(f"  • Portable: {portable_dir}")
            print(f"  • Archive: {archive_path}")
            
            if create_installer:
                if self.system == "Windows":
                    print("  • Run NSIS on installer.nsi to create installer")
                elif self.system == "Linux":
                    print("  • Run install.sh to install on Linux")
                    
        except Exception as e:
            print(f"\n❌ Error during packaging: {e}")
            sys.exit(1)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Package Music Practice Tracker")
    parser.add_argument(
        "--onedir",
        action="store_true",
        help="Build as directory instead of single file"
    )
    parser.add_argument(
        "--installer",
        action="store_true",
        help="Create installer scripts"
    )
    
    args = parser.parse_args()
    
    packager = AppPackager()
    packager.package(
        single_file=not args.onedir,
        create_installer=args.installer
    )

if __name__ == "__main__":
    main()