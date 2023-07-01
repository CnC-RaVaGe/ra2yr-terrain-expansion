import os

import typer

from scripts import mix_reader

app = typer.Typer()


@app.command()
def extract(mix_filename: str, folder_name: str):
    cwd = os.getcwd()
    target_folder = os.path.join(cwd, folder_name)
    os.makedirs(target_folder)
    print(f"Writing {mix_filename} mix files to folder {target_folder}")

    filemap = mix_reader.read(mix_filename)
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
    filemap = mix_reader.read(mix_filename)
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


if __name__ == "__main__":
    app()
