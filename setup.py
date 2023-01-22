import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["pygame", "time", "sys"],
    "excludes": ["tkinter", "OpenGL", "OpenGL_accelerate", "numpy"],
    "zip_include_packages": ["encodings", "PySide6"],
}

base = "Win32GUI" if sys.platform == "win32" else None

setup(
      name="PacMan",
      version="0.1",
      description="Jeu pacman en pygame",
      options={"build_exe": build_exe_options},
      executables=[Executable("main.py", base=base)],
)
