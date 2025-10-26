# Circuit Designer 1.0 Release Assets

This folder is reserved for packaged builds of the junior-physics circuit
composer. The intended distribution bundle is a Windows ``.exe`` built with
PyInstaller.

Because the execution environment that generated this commit has no outbound
network access, it cannot install PyInstaller and therefore cannot produce the
final executable artifact. To generate the Windows release locally:

1. Install Python 3.10+ and pip on a Windows machine.
2. ``pip install -r requirements.txt pyinstaller``
3. Run ``python packaging/win/build_release.py`` from the repository root.

The script consumes the pinned ``packaging/win/circuit_designer.spec`` file and
will place the resulting ``CircuitDesigner-1.0`` folder and ``.zip`` archive
inside this ``release`` directory. The portable ``CircuitDesigner-1.0.exe`` can
then be found in ``release/CircuitDesigner-1.0`` once the build finishes.
