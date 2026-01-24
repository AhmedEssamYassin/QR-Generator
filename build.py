import PyInstaller.__main__
import os
import shutil
import sys
from pathlib import Path
import qrcode

# Project configuration
APP_NAME = "QRCodeGeneratorPro"
VERSION = "1.0.0"
AUTHOR = "Ahmed Yassin"
DESCRIPTION = "Professional QR Code Generator"

# Paths
PROJECT_ROOT = Path(__file__).parent
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"
ASSETS_DIR = PROJECT_ROOT / "assets"

# Ensure this points to the exact location of your icon
ICON_PATH = ASSETS_DIR / "images" / "icon.ico"

QRCODE_PATH = os.path.dirname(qrcode.__file__)
print(f"Found qrcode library at: {QRCODE_PATH}")

def cleanBuildDirs():
    """Clean previous build directories"""
    print("Cleaning previous builds...")
    for directory in [DIST_DIR, BUILD_DIR]:
        if directory.exists():
            shutil.rmtree(directory)
            
    # Clean spec file
    specFile = PROJECT_ROOT / f"{APP_NAME}.spec"
    if specFile.exists():
        specFile.unlink()
        print(f"Deleted spec file: {specFile}")

    print("Build directories cleaned")


def createSpecFile():
    """Create PyInstaller spec file"""
    # Define source path
    SRC_PATH = PROJECT_ROOT / "src"
    
    # Handle icon path for spec file (escape backslashes for Windows)
    iconStr = str(ICON_PATH).replace('\\', '\\\\') if ICON_PATH.exists() else 'None'
    
    specContent = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[r'{str(SRC_PATH)}'],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        (r'{QRCODE_PATH}', 'qrcode'),
    ],
    hiddenimports=[
        'PIL._tkinter_finder',
        'customtkinter',
        'qrcode',
        'qrcode.image.styles.moduledrawers',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=r'{iconStr}',
)
'''
    
    specFile = PROJECT_ROOT / f"{APP_NAME}.spec"
    with open(specFile, 'w') as f:
        f.write(specContent)
    
    print(f"Created spec file: {specFile}")
    return specFile


def buildExecutable(specFile):
    """Build executable using PyInstaller"""
    print(f"\nBuilding {APP_NAME} v{VERSION}...")
    
    PyInstaller.__main__.run([
        str(specFile),
        '--clean',
        '--noconfirm',
    ])
    
    print(f"\nBuild complete!")
    print(f"Executable location: {DIST_DIR / APP_NAME}")


def buildOnefile():
    """Build as single file executable"""
    print(f"\nBuilding {APP_NAME} (One File) v{VERSION}...")
    
    args = [
        'main.py',
        '--name', APP_NAME,
        '--onefile',
        '--windowed',
        '--clean',
        '--noconfirm',
        f'--paths={PROJECT_ROOT / "src"}',
        f'--distpath={DIST_DIR}',
        f'--workpath={BUILD_DIR}',
        '--add-data', f'assets{os.pathsep}assets',
        '--add-data', f'{QRCODE_PATH}{os.pathsep}qrcode',
        '--collect-all', 'qrcode', 
        '--hidden-import', 'PIL._tkinter_finder',
        '--hidden-import', 'customtkinter',
        '--hidden-import', 'qrcode',
        '--hidden-import', 'qrcode.image.styles.moduledrawers',
    ]

    # Add icon if exists
    if ICON_PATH.exists():
        print(f"Using icon: {ICON_PATH}")
        args.extend(['--icon', str(ICON_PATH)])
    else:
        print(f"WARNING: Icon not found at {ICON_PATH}")
    
    PyInstaller.__main__.run(args)
    
    print(f"\nBuild complete!")
    print(f"Executable location: {DIST_DIR / f'{APP_NAME}.exe'}")


def buildOnedir():
    """Build as directory with executable and dependencies"""
    print(f"\nBuilding {APP_NAME} (One Directory) v{VERSION}...")
    
    args = [
        'main.py',
        '--name', APP_NAME,
        '--onedir',
        '--windowed',
        '--clean',
        '--noconfirm',
        f'--paths={PROJECT_ROOT / "src"}',
        f'--distpath={DIST_DIR}',
        f'--workpath={BUILD_DIR}',
        '--add-data', f'assets{os.pathsep}assets',
        '--add-data', f'{QRCODE_PATH}{os.pathsep}qrcode',
        '--collect-all', 'qrcode', 
        '--hidden-import', 'PIL._tkinter_finder',
        '--hidden-import', 'customtkinter',
        '--hidden-import', 'qrcode',
        '--hidden-import', 'qrcode.image.styles.moduledrawers',
    ]
    
    # Add icon if exists
    if ICON_PATH.exists():
        print(f"Using icon: {ICON_PATH}")
        args.extend(['--icon', str(ICON_PATH)])
    else:
        print(f"WARNING: Icon not found at {ICON_PATH}")
    
    PyInstaller.__main__.run(args)
    
    print(f"\nBuild complete!")
    print(f"Executable location: {DIST_DIR / APP_NAME}")


def showMenu():
    """Show build options menu"""
    print("=" * 60)
    print(f"  {APP_NAME} v{VERSION} - Build Script")
    print("=" * 60)
    print("\nBuild Options:")
    print("  1. One File (single .exe, slower startup)")
    print("  2. One Directory (folder with .exe, faster startup)")
    print("  3. Custom spec file")
    print("  4. Clean build directories only")
    print("  0. Exit")
    print()
    
    choice = input("Select option [1-4, 0]: ").strip()
    return choice


def main():
    """Main build process"""
    try:
        choice = showMenu()
        
        if choice == "0":
            print("Exiting...")
            return
        
        if choice == "4":
            cleanBuildDirs()
            return
        
        # Create assets directory if it doesn't exist
        # We also check if the images subdirectory exists
        ASSETS_DIR.mkdir(exist_ok=True)
        (ASSETS_DIR / "images").mkdir(exist_ok=True)
        
        if choice == "1":
            cleanBuildDirs()
            buildOnefile()
        
        elif choice == "2":
            cleanBuildDirs()
            buildOnedir()
        
        elif choice == "3":
            cleanBuildDirs()
            specFile = createSpecFile()
            buildExecutable(specFile)
        
        else:
            print("Invalid option")
            return
        
        print("\n" + "=" * 60)
        print("Build process completed successfully!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\nBuild cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nBuild failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()