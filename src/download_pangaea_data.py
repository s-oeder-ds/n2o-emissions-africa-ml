from pathlib import Path
from typing import Union

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


def main(verbose: bool = True) -> None:
    """
    Download the PANGAEA N2O Africa dataset into the local raw data directory.

    Parameters
    ----------
    verbose : bool, default=True
        If True, print detailed script progress.

    Returns
    -------
    None
        The function saves the raw dataset file locally.
    """
    dataset_url = "https://doi.pangaea.de/10.1594/PANGAEA.987301?format=textfile"
    output_path = Path("data/raw/pangaea_987301_n2o_africa.txt")

    download_file(
        url=dataset_url,
        output_path=output_path,
        overwrite=False,
        timeout=60,
        verbose=verbose,
    )


if __name__ == "__main__":
    main(verbose=True)