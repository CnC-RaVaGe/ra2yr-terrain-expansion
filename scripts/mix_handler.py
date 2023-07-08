import json
import os
import shutil
from typing import Annotated, Optional

import ra2mix
import typer
from appdirs import user_data_dir
from pydantic import BaseModel

app = typer.Typer()


@app.command()
def extract(mix_filename: str, folder_name: str):
    cwd = os.getcwd()
    target_folder = os.path.join(cwd, folder_name)
    os.makedirs(target_folder)
    print(f"Writing {mix_filename} mix files to folder {target_folder}")

    filemap = ra2mix.read(mix_filename)
    print(f"filenames: {list(filemap.keys())[:5]}")

    for filename, file_data in filemap.items():
        mixdb_name = "local mix database.dat"
        if filename == mixdb_name:
            print(f"Skipping extract of {mixdb_name}")
            continue

        print(f"Creating {filename}")
        with open(os.path.join(target_folder, filename), "wb") as fp:
            fp.write(file_data)


@app.command()
def summarize(mix_filename: str):
    header, file_entries, _ = ra2mix.read_file_info(mix_filename)
    print(
        f"Header[flags={hex(header.flags)}, file_count={header.file_count}, size={header.data_size}"
    )
    print(file_entries[:20])

    filemap = ra2mix.read(mix_filename)
    filetypes = {}
    for filename in filemap.keys():
        filetype = filename.split(".")[-1]
        if filetype in filetypes:
            filetypes[filetype] = filetypes[filetype] + 1
        else:
            filetypes[filetype] = 1

    print(f"{mix_filename} contains the following file types:")
    for filetype, count in filetypes.items():
        print(f"\t*.{filetype}: {count}")


@app.command()
def create(folder_path: str, mix_filepath: str):
    ra2mix.write(mix_filepath=mix_filepath, folder_path=folder_path)


class Configuration(BaseModel):
    ra2_install_path: str = os.path.join(
        "C:\\", "Program Files (x86)", "Command and Conquer Red Alert II"
    )


config_location = os.path.join(user_data_dir("ra2yr-tx", "ra2yr-tx"), "config.json")


def get_current_config():
    if os.path.exists(config_location):
        with open(config_location, "r") as fp:
            config_data = json.load(fp)
            config_data = Configuration.model_validate(config_data)
            return config_data
    else:
        raise RuntimeError("No config exists yet, run config command first")


@app.command()
def config(option: str, value: Annotated[Optional[str], typer.Argument()] = None):
    if os.path.exists(config_location):
        with open(config_location, "r") as fp:
            config_data = json.load(fp)
            config_data = Configuration.model_validate(config_data)
    else:
        config_data = Configuration()
        os.makedirs(os.path.dirname(config_location), exist_ok=True)
        with open(config_location, "w") as fp:
            json.dump(config_data.model_dump(), fp)

    if value is not None:
        valid_fields = list(Configuration.model_fields.keys())
        if option in valid_fields:
            setattr(config_data, option, value)
        else:
            raise ValueError(
                f"`{option}` is not a valid configuration field: {valid_fields}"
            )

        print(f"Saving configuration: {config_data}")
        with open(config_location, "w") as fp:
            json.dump(config_data.model_dump(), fp)
    else:
        print(config_data.model_dump()[option])


mix_sources = {
    os.path.join("Development Files", "YR", "Urban"): "expandmd13.mix",
    os.path.join("Development Files", "YR", "Temperate"): "expandmd14.mix",
    os.path.join("Development Files", "YR", "Snow"): "expandmd15.mix",
    os.path.join("Development Files", "YR", "NewUrban"): "expandmd16.mix",
    os.path.join("Development Files", "YR", "Lunar"): "expandmd17.mix",
    os.path.join("Development Files", "YR", "Desert"): "expandmd18.mix",
}

ini_sources = [
    os.path.join("Development Files", "YR", "Urban", "urbanmd.ini"),
    os.path.join("Development Files", "YR", "Temperate", "temperatmd.ini"),
    os.path.join("Development Files", "YR", "Snow", "snowmd.ini"),
    os.path.join("Development Files", "YR", "NewUrban", "urbannmd.ini"),
    os.path.join("Development Files", "YR", "Lunar", "lunarmd.ini"),
    os.path.join("Development Files", "YR", "Desert", "desertmd.ini"),
]


@app.command()
def apply(theater: Annotated[Optional[str], typer.Argument()] = None):
    if not os.path.exists("Development Files") and not os.path.exists("scripts"):
        print(
            "Error! Make sure to run the script from the ra2yr-terrain-expansion "
            "directory!"
        )
        return

    config_data = get_current_config()
    for path, mix_filename in mix_sources.items():
        if theater is not None and not theater in path:
            continue
        write_path = os.path.join(config_data.ra2_install_path, mix_filename)
        ra2mix.write(mix_filepath=write_path, folder_path=path)

    for ini_path in ini_sources:
        if theater is not None and not theater in ini_path:
            continue
        write_path = os.path.join(
            config_data.ra2_install_path, os.path.basename(ini_path)
        )
        print(f"Copying {ini_path} to {write_path}")
        shutil.copyfile(ini_path, write_path)


@app.command()
def vanilla():
    config_data = get_current_config()
    for mix_filename in mix_sources.values():
        del_path = os.path.join(config_data.ra2_install_path, mix_filename)
        print(f"Deleting {del_path}")
        os.remove(del_path)

    for ini_path in ini_sources:
        del_path = os.path.join(
            config_data.ra2_install_path, os.path.basename(ini_path)
        )
        print(f"Deleting {del_path}")
        os.remove(del_path)


if __name__ == "__main__":
    app()
