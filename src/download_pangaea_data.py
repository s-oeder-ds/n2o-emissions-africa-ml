from pathlib import Path
from typing import Union
from zipfile import BadZipFile, ZipFile

import requests


def download_file(
    url: str,
    output_path: Union[str, Path],
    overwrite: bool = False,
    timeout: int = 60,
    verbose: bool = False,
) -> Path:
    """
    Download a file from a URL and save it to a local path.

    Parameters
    ----------
    url : str
        Source URL of the file.
    output_path : Union[str, Path]
        Local path where the file should be saved.
    overwrite : bool, default=False
        If True, overwrite an existing file.
    timeout : int, default=60
        Timeout for the HTTP request in seconds.
    verbose : bool, default=False
        If True, print detailed progress information.

    Returns
    -------
    Path
        Path to the downloaded or already existing file.

    Raises
    ------
    ValueError
        If the URL is empty or the timeout is invalid.
    requests.RequestException
        If the HTTP request fails.
    OSError
        If the file cannot be written.
    """
    if not isinstance(url, str) or not url.strip():
        raise ValueError("The URL must be a non-empty string.")

    if timeout <= 0:
        raise ValueError("The timeout must be greater than zero.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and not overwrite:
        if verbose:
            print(f"File already exists: {output_path}")
            print("Skipping download because overwrite=False.")
        return output_path

    if verbose:
        print(f"Downloading from: {url}")
        print(f"Saving to: {output_path}")

    response = requests.get(url, timeout=timeout)
    response.raise_for_status()

    output_path.write_bytes(response.content)

    if verbose:
        print("Download finished successfully.")
        print(f"File size: {output_path.stat().st_size:,} bytes")

    return output_path


def validate_zip_file(
    zip_path: Union[str, Path],
    verbose: bool = False,
) -> Path:
    """
    Validate that a downloaded file is a readable ZIP archive.

    Parameters
    ----------
    zip_path : Union[str, Path]
        Path to the ZIP file that should be validated.
    verbose : bool, default=False
        If True, print detailed information about the ZIP content.

    Returns
    -------
    Path
        Path to the validated ZIP file.

    Raises
    ------
    FileNotFoundError
        If the ZIP file does not exist.
    BadZipFile
        If the file is not a valid ZIP archive.
    """
    zip_path = Path(zip_path)

    if not zip_path.exists():
        raise FileNotFoundError(f"ZIP file does not exist: {zip_path}")

    if verbose:
        print(f"Validating ZIP file: {zip_path}")

    try:
        with ZipFile(zip_path, "r") as zip_file:
            bad_file = zip_file.testzip()

            if bad_file is not None:
                raise BadZipFile(f"Corrupted file inside ZIP archive: {bad_file}")

            if verbose:
                file_names = zip_file.namelist()
                print("ZIP validation successful.")
                print(f"Number of files in ZIP archive: {len(file_names)}")
                print("First files in archive:")

                for file_name in file_names[:10]:
                    print(f"  - {file_name}")

    except BadZipFile:
        raise BadZipFile(f"The downloaded file is not a valid ZIP archive: {zip_path}")

    return zip_path

def extract_zip_file(
    zip_path: Union[str, Path],
    extract_to: Union[str, Path],
    overwrite: bool = False,
    verbose: bool = False,
) -> list[Path]:
    """
    Extract a ZIP archive into a target directory.

    Parameters
    ----------
    zip_path : Union[str, Path]
        Path to the ZIP file that should be extracted.
    extract_to : Union[str, Path]
        Target directory where the ZIP content should be extracted.
    overwrite : bool, default=False
        If True, existing extracted files may be overwritten.
    verbose : bool, default=False
        If True, print detailed extraction information.

    Returns
    -------
    list[Path]
        List of extracted file paths.

    Raises
    ------
    FileNotFoundError
        If the ZIP file does not exist.
    BadZipFile
        If the ZIP file is not readable.
    FileExistsError
        If one or more target files already exist and overwrite=False.
    OSError
        If extraction fails due to file system issues.
    """
    zip_path = Path(zip_path)
    extract_to = Path(extract_to)

    if not zip_path.exists():
        raise FileNotFoundError(f"ZIP file does not exist: {zip_path}")

    extract_to.mkdir(parents=True, exist_ok=True)

    if verbose:
        print(f"Extracting ZIP file: {zip_path}")
        print(f"Extraction target directory: {extract_to}")

    extracted_paths: list[Path] = []

    with ZipFile(zip_path, "r") as zip_file:
        zip_members = [
            member for member in zip_file.infolist()
            if not member.is_dir()
        ]

        target_paths = [
            extract_to / member.filename
            for member in zip_members
        ]

        existing_files = [
            target_path for target_path in target_paths
            if target_path.exists()
        ]

        if existing_files and not overwrite:
            if verbose:
                print("Some extracted files already exist.")
                print("Skipping extraction because overwrite=False.")
                print("Existing files:")

                for existing_file in existing_files[:10]:
                    print(f"  - {existing_file}")

            return existing_files

        for member in zip_members:
            zip_file.extract(member, path=extract_to)
            extracted_path = extract_to / member.filename
            extracted_paths.append(extracted_path)

            if verbose:
                print(f"Extracted: {extracted_path}")

    if verbose:
        print("ZIP extraction completed successfully.")
        print(f"Number of extracted files: {len(extracted_paths)}")

    return extracted_paths

def download_pangaea_bundle(verbose: bool = False) -> list[Path]:
    """
    Download, validate, and extract the PANGAEA bundled N2O Africa dataset.

    Parameters
    ----------
    verbose : bool, default=False
        If True, print detailed script progress.

    Returns
    -------
    list[Path]
        Paths to the extracted files.

    Raises
    ------
    requests.RequestException
        If the dataset cannot be downloaded.
    OSError
        If local files cannot be written or extracted.
    BadZipFile
        If the downloaded ZIP file is invalid.
    """
    dataset_url = "https://doi.pangaea.de/10.1594/PANGAEA.987298?format=zip"
    zip_path = Path("data/raw/pangaea_987298_n2o_ssa_bundle.zip")
    extract_to = Path("data/raw/pangaea_987298")

    downloaded_file = download_file(
        url=dataset_url,
        output_path=zip_path,
        overwrite=False,
        timeout=120,
        verbose=verbose,
    )

    validated_file = validate_zip_file(
        zip_path=downloaded_file,
        verbose=verbose,
    )

    extracted_files = extract_zip_file(
        zip_path=validated_file,
        extract_to=extract_to,
        overwrite=False,
        verbose=verbose,
    )

    return extracted_files

if __name__ == "__main__":
    download_pangaea_bundle(verbose=True)