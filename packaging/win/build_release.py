"""Helper script to build the Windows executable with PyInstaller."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RELEASE_DIR = REPO_ROOT / "release"
DIST_DIR = REPO_ROOT / "dist"
BUILD_DIR = REPO_ROOT / "build"
SPEC_PATH = Path(__file__).resolve().parent / "circuit_designer.spec"


def clean_build_artifacts() -> None:
    """Remove intermediate build folders from previous runs."""
    for path in (DIST_DIR, BUILD_DIR):
        if path.exists():
            shutil.rmtree(path)
    spec_build = REPO_ROOT / "CircuitDesigner-1.0.spec"
    if spec_build.exists():
        spec_build.unlink()


def run_pyinstaller() -> None:
    """Invoke PyInstaller with the pinned spec file."""
    subprocess.run(
        [
            "pyinstaller",
            "--noconfirm",
            "--clean",
            str(SPEC_PATH),
        ],
        check=True,
        cwd=REPO_ROOT,
    )


def move_release() -> Path:
    """Move the generated dist folder into ``release`` and return its path."""
    RELEASE_DIR.mkdir(exist_ok=True)
    target = RELEASE_DIR / "CircuitDesigner-1.0"
    if target.exists():
        shutil.rmtree(target)
    shutil.move(str(DIST_DIR / "CircuitDesigner-1.0"), target)
    return target


def zip_release(target: Path) -> Path:
    zip_path = RELEASE_DIR / f"{target.name}.zip"
    if zip_path.exists():
        zip_path.unlink()
    shutil.make_archive(str(zip_path.with_suffix("")), "zip", target)
    return zip_path


if __name__ == "__main__":
    clean_build_artifacts()
    run_pyinstaller()
    release_dir = move_release()
    zip_release(release_dir)
    clean_build_artifacts()
