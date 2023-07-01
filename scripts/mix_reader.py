import struct
from collections import namedtuple

from scripts.checksum import ra2_crc

Header = namedtuple("Header", "flags file_count data_size")
HEADER_SIZE = 10

FileEntry = namedtuple("FileEntry", "id offset size")
FILE_ENTRY_SIZE = 12

MIX_DB_FILENAME = "local mix database.dat"


def get_file_entries(header: Header, mix_data: bytes) -> list[FileEntry]:
    file_entries = []
    for i in range(header.file_count):
        start = 10 + (i * FILE_ENTRY_SIZE)
        end = start + FILE_ENTRY_SIZE
        # print(binascii.b2a_hex(mix_data[start:end], ":"))
        file_entries.append(FileEntry._make(struct.unpack("=3I", mix_data[start:end])))

    return file_entries


def get_filenames_from_mix_db(mix_db_file_data: bytes) -> list[str]:
    filenames = []
    end = 52
    start = 52
    while start < len(mix_db_file_data):
        while mix_db_file_data[end] != 0:
            end += 1
        filename = mix_db_file_data[start:end].decode("utf-8")
        filenames.append(filename)
        # print(f"{start=}, {end=}, {filename=}")
        end += 1
        start = end

    return filenames


def get_file_data_from_mix_body(file_entry: FileEntry, mix_body_data: bytes) -> bytes:
    return mix_body_data[file_entry.offset : file_entry.offset + file_entry.size]


def get_file_map(file_entries: list[FileEntry], mix_data: bytes):
    if len(file_entries) == 1:
        return {}

    MIX_DB_ID = ra2_crc(MIX_DB_FILENAME)

    BODY_START = HEADER_SIZE + (FILE_ENTRY_SIZE * len(file_entries))
    for file_entry in file_entries:
        if file_entry.id != MIX_DB_ID:
            continue
        mix_db_file_entry = file_entry
        break

    mix_body_data = mix_data[BODY_START:]
    mix_db_file_data = get_file_data_from_mix_body(mix_db_file_entry, mix_body_data)

    filenames = get_filenames_from_mix_db(mix_db_file_data)
    filename_id_map = {ra2_crc(filename): filename for filename in filenames}
    # print(f"{filename_id_map=}")

    filemap = {}
    for file_entry in file_entries:
        file_data = get_file_data_from_mix_body(file_entry, mix_body_data)
        filemap[filename_id_map[file_entry.id]] = file_data

    return filemap


def read(mix_filename: str) -> dict[str, bytes]:
    with open(mix_filename, "rb") as fp:
        mix_data = fp.read()

    header = Header._make(struct.unpack("=I H I", mix_data[:HEADER_SIZE]))
    if (header.flags & 2) != 0:
        raise NotImplementedError("Cannot parse encrypted mix header")

    file_entries = get_file_entries(header, mix_data)

    return get_file_map(file_entries, mix_data)
