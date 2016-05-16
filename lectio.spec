# -*- mode: python -*-
a = Analysis(['lectio.py'],
             pathex=['C:\\Users\\mich087q\\Desktop\\lectio-app2'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='lectio.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas + [('cacert.pem', 'C:\\Users\\mich087q\\Desktop\\lectio-app2\\cacert.pem', 'DATA')],
               strip=None,
               upx=True,
               name='lectio')
