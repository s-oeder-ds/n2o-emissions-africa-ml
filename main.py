from src.download_pangaea_data import download_pangaea_bundle


def main(verbose: bool = True) -> None:
    """
    Run the main project workflow.

    Parameters
    ----------
    verbose : bool, default=True
        If True, print detailed workflow progress.

    Returns
    -------
    None
        Executes the configured workflow steps.
    """
    if verbose:
        print("Starting N2O emissions Africa workflow.")

    extracted_files = download_pangaea_bundle(verbose=verbose)

    if verbose:
        print("Downloaded and extracted files:")
        for file_path in extracted_files:
            print(f"  - {file_path}")

        print("Workflow finished successfully.")


if __name__ == "__main__":
    main(verbose=True)