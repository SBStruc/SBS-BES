import xlwings as xw
import pathlib
import re


def make_new_staad_file(staad_file: str, output_filename: str, dst_folder: str) -> None:
    SUMMARY_SHEET_NAME: str = "SUMMARY"
    excel_file: pathlib.Path = pathlib.Path(dst_folder) / f"{output_filename}.xlsm"
    wb: xw.Book = xw.Book(excel_file)
    print("Extracting new beam dimensions from", excel_file)
    if SUMMARY_SHEET_NAME not in wb.sheet_names:
        raise Exception(
            f"{SUMMARY_SHEET_NAME} not found in {output_filename}. Exiting..."
        )

    new_beam_dims: list[list] = get_new_beam_dims(wb.sheets[SUMMARY_SHEET_NAME])
    print("Extracting new beam dimensions done! Writing new staad file...")
    with open(staad_file, "r") as f:
        staad_lines: list[str] = f.readlines()
        new_staad_content: list[str] = replace_beam_dims_in_file(
            staad_lines, new_beam_dims
        )

    with open(f"{dst_folder}/{output_filename}.txt", "w") as f:
        f.writelines(new_staad_content)

    print(f"Writing new staad file done!\n{dst_folder}/{output_filename}.txt")


def get_new_beam_dims(summary_sheet: xw.Sheet) -> list[list]:
    new_beam_dims: list[list] = []
    start_range: int = 12

    while summary_sheet.range(f"B{start_range}").value:
        # this reverses our logic in extract_from_staad_syntax.load_dim_to_df
        # [beam name, b (z), h (y)]
        values: list | None = summary_sheet.range(
            f"B{start_range}:D{start_range}"
        ).value
        if values is None:
            raise ValueError

        if not (
            isinstance(values[0], str)
            and isinstance(values[1], float)
            and isinstance(values[2], float)
        ):
            raise ValueError
        if re.match(r"0\d", values[0]):
            raise ValueError("Beam names cannot contain 0 followed by a number")
        values[0] = f"_{values[0]}"
        values[1] = values[1] / 1000
        values[2] = values[2] / 1000
        new_beam_dims.append(values)

        start_range += 2

    return new_beam_dims


def replace_beam_dims_in_file(lines: list[str], new_beam_dims: list[list]) -> list[str]:
    # the logic is similar to extract_from_staad_syntax.extract_beam_dimensions

    start_idx: int = lines.index("MEMBER PROPERTY AMERICAN\n") + 1
    end_idx: int = -1
    changed_beams: list[str] = []

    # REFACTOR NESTED LOOP
    for idx, bd_line in enumerate(lines[start_idx:], start_idx):
        if re.match(r"^_[A-Z\-\.]+0\d", bd_line):
            raise ValueError("Beam names cannot contain 0 followed by a number")
        for dim in new_beam_dims:
            if re.match(f"{dim[0]}" + r"\s+", bd_line):
                if dim_to_doc_line(dim) == bd_line:
                    break
                print(
                    f"Updating {dim[0]}; CURRENT: ",
                    bd_line.strip(),
                    "NEW: ",
                    dim_to_doc_line(dim).strip(),
                )
                lines[idx] = dim_to_doc_line(dim)

                changed_beams.append(dim[0])

        if re.match(r"^[A-Z\s]+\n$", bd_line):
            end_idx = idx
            break

    if len(changed_beams) == 0:
        print("No beams changed. Exiting...")
        quit()

    print("Beam group changed: ", changed_beams)

    if end_idx == -1:
        raise Exception

    return lines


def dim_to_doc_line(dim_values: list[str]) -> str:
    return f"{dim_values[0]} PRIS YD {dim_values[2]} ZD {dim_values[1]}\n"
