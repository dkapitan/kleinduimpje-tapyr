import marimo

__generated_with = "0.18.1"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    from fsspec.implementations.github import GithubFileSystem


    DATA_FOLDER = "data"

    GithubFileSystem(org="dkapitan", repo="kleinduimpje-tapyr").glob(DATA_FOLDER + "/*.gpx")
    return


@app.cell
def _():
    from kleinduimpje.logic.utils import GitHubFS, fetch_and_parse_gpx

    fs = GitHubFS()
    fetch_and_parse_gpx(fs.gpx_files[0], fs)


    return


if __name__ == "__main__":
    app.run()
