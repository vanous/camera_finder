# Camera Finder

Install `uv` on your system. `uv` will manage python and dependencies
installation and will also run the application.

- [uv](https://docs.astral.sh/uv/)

## Installation

Clone the [repository](https://github.com/vanous/camera_finder) or [download
it](https://github.com/vanous/camera_finder/archive/refs/heads/master.zip) and uzip.

## Run the application

Inside the downloaded/unzipped repository, run:

```bash
uv run run_finder.py
```

To emulate the camera, run:

```bash
uv run run_camera.py
```

To get a list of network interfaces, run:

```bash
uv run get_network.py
```

## Development

### Requires

- uv

## Contributions

- Format Python code with [ruff](https://docs.astral.sh/ruff/)
- Add/update code license headers with
  [hawkeye](https://github.com/korandoru/hawkeye)
    - `hawkeye format`

## Dependencies

- [uv](https://docs.astral.sh/uv/)
- [ifaddr](https://github.com/ifaddr/ifaddr)
