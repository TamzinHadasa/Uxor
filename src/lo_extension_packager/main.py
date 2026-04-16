from pathlib import Path
import shutil


SRC_DIR = Path(__file__).parent.parent.absolute()
INGREDIENTS_DIR = SRC_DIR.joinpath("Scripts/_lo_extension_ingredients")
OUTPUT_DIR = SRC_DIR.joinpath("Scripts/_output")
PACKAGE_DIR = OUTPUT_DIR.joinpath(".package")
PYTHON_DEST_DIR = PACKAGE_DIR.joinpath("UxorLibrary/python")


def main(target_dir: str | Path = OUTPUT_DIR):
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copytree(INGREDIENTS_DIR, PACKAGE_DIR, dirs_exist_ok=True)
    for item in SRC_DIR.iterdir():
        if item.is_file():
            shutil.copy(item, PYTHON_DEST_DIR)
    shutil.make_archive(f"{PACKAGE_DIR}/uxor", 'zip', PACKAGE_DIR)
    shutil.move(f"{PACKAGE_DIR}/uxor.zip", f"{target_dir}/uxor.oxt")
    shutil.rmtree(PACKAGE_DIR)


if __name__ == "__main__":
    main()
