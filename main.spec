# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run_with_console.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)


pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='PcStatsRichPresence',
          debug=False,
          strip=False,
          upx=False,
          console=False)