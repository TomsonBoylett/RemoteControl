# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None


a = Analysis(['main.py'],
             pathex=['E:\\RemoteControl'],
             binaries=[],
             datas=[('static', 'static'), ('templates', 'templates'), ('icon/icon-128.ico', 'icon')],
             hiddenimports=collect_submodules('uvicorn') + collect_submodules('websockets'),
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
		  a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='remote-control',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='icon/icon-128.ico')
coll = COLLECT(exe,
               [('config.toml', 'config.toml', 'DATA')],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='remote-control')