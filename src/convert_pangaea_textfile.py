from pathlib import Path
from typing import Optional, Union, Dict


import pandas as pd


def find_table_header_line(
    file_path: Union[str, Path],
    header_prefix: str = "Event\tLatitude\tLongitude\tDate/Time",
    encoding: str = "utf-8",
    verbose: bool = False,
) -> int:
    """
    Find the line index of the actual tabular header in a PANGAEA text file.

    Parameters
    ----------
    file_path : Union[str, Path]
        Path to the raw PANGAEA text file.
    header_prefix : str, default="Event\\tLatitude\\tLongitude\\tDate/Time"
        Prefix that identifies the real table header line.
    encoding : str, default="utf-8"
        Encoding used to read the text file.
    verbose : bool, default=False
        If True, print detailed information about the detected header line.

    Returns
    -------
    int
        Zero-based line index of the table header.

    Raises
    ------
    FileNotFoundError
        If the input file does not exist.
    ValueError
        If the table header cannot be found.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Input file does not exist: {file_path}")

    with file_path.open("r", encoding=encoding) as file:
        for line_index, line in enumerate(file):
            if line.startswith(header_prefix):
                if verbose:
                    print(f"Detected table header at line index: {line_index}")
                return line_index

    raise ValueError(
        f"Could not find a table header starting with: {header_prefix}"
    )


def convert_pangaea_textfile_to_csv(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    header_prefix: str = "Event\tLatitude\tLongitude\tDate/Time",
    encoding: str = "utf-8",
    verbose: bool = False,
) -> Path:
    """
    Convert a PANGAEA tab-delimited text file with metadata block into a clean CSV file.

    Parameters
    ----------
    input_path : Union[str, Path]
        Path to the raw PANGAEA text file.
    output_path : Union[str, Path]
        Path where the cleaned CSV file should be stored.
    header_prefix : str, default="Event\\tLatitude\\tLongitude\\tDate/Time"
        Prefix that identifies the actual table header line.
    encoding : str, default="utf-8"
        Encoding used to read and write files.
    verbose : bool, default=False
        If True, print detailed processing information.

    Returns
    -------
    Path
        Path to the generated CSV file.

    Raises
    ------
    FileNotFoundError
        If the input file does not exist.
    ValueError
        If the tabular header cannot be found.
    pd.errors.ParserError
        If pandas cannot parse the tabular part of the file.
    OSError
        If the output file cannot be written.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    header_line_index = find_table_header_line(
        file_path=input_path,
        header_prefix=header_prefix,
        encoding=encoding,
        verbose=verbose,
    )

    if verbose:
        print(f"Reading tabular data from: {input_path}")
        print(f"Skipping metadata lines: {header_line_index}")

    dataframe = pd.read_csv(
        input_path,
        sep="\t",
        skiprows=header_line_index,
        encoding=encoding,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    dataframe.to_csv(
        output_path,
        index=False,
        encoding=encoding,
    )

    if verbose:
        print("Conversion completed successfully.")
        print(f"Output file: {output_path}")
        print(f"Dataframe shape: {dataframe.shape}")
        print("First columns:")
        for column in dataframe.columns[:10]:
            print(f"  - {column}")

    return output_path


def main(verbose: bool = True) -> None:
    """
    Convert the downloaded raw PANGAEA N2O dataset into a Data Wrangler friendly CSV file.

    Parameters
    ----------
    verbose : bool, default=True
        If True, print detailed script progress.

    Returns
    -------
    None
        This function writes the cleaned CSV file to disk.
    """
    input_path = Path("data/raw/pangaea_987301_n2o_africa.txt")
    output_path = Path("data/processed/n2o_africa_clean.csv")

    convert_pangaea_textfile_to_csv(
        input_path=input_path,
        output_path=output_path,
        verbose=verbose,
    )


if __name__ == "__main__":
    main(verbose=True)