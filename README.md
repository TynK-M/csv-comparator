# CSV Comparator

A small Python CLI to compare CSV files and report where they have the same values, rows and columns.

Table of contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

## Overview

csv-comparator helps you find an report the points in common between two CSV datasets. It is designed for data validation, quick checks, and integration into pipelines where CSVs need to be compared by one or more key columns.

## Features

- Compare two CSV files
- Output results in human-readable text
- Designed to integrate easily into scripts or run from the command line

Future features:

- Option to compare the header differencies
- Option to compare the footer differencies

## Requirements

- Python >3.9
- See `pyproject.toml` for dependency and packaging information

## Contributing

Contributions are welcome. A suggested workflow:

1. Fork the repository
2. Create a feature branch
3. Run tests and linters (add tests if none exist)
4. Open a pull request describing your changes

Please follow standard Python packaging and formatting guidelines. If you plan to add features, update this RADME and the `pyproject.toml` as needed.

## License

This project includes a [LICENSE](LICENSE) file. Please refer to it for license terms.

