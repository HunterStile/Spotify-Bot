# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['spotify_bot_gui.py'],
    pathex=['.'],
    binaries=[],    datas=[
        ('config.py', '.'),
        ('Main.py', '.'),
        ('funzioni/', 'funzioni/'),
        ('chromedriver.exe', '.'),
        ('user_agents.txt', '.'),
        ('gui_config.json', '.'),
        ('account_spotify.csv', '.'),
        ('account_spotify_creati.csv', '.'),
    ],
    hiddenimports=[
        'selenium',
        'selenium.webdriver',
        'selenium.webdriver.chrome',
        'selenium.webdriver.common.by',
        'selenium.webdriver.support.ui',
        'selenium.webdriver.support.expected_conditions',
        'selenium.webdriver.common.action_chains',
        'selenium.common.exceptions',
        'webdriver_manager',
        'webdriver_manager.chrome',
        'faker',
        'pyautogui',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.font',
        'threading',
        'concurrent.futures',
        'queue',
        'json',
        'csv',
        'random',
        'time',
        'os',
        'sys',
        'importlib.util',
        'ctypes'
    ],
    hookspath=[],
    hooksconfig={},
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
    name='SpotifyBot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True if you want to see console output
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # You can add an .ico file path here if you have an icon
)
