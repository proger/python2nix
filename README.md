## python2nix

Put a PyPI package name in, get a Nix expression out to add to [nixpkgs](https://github.com/NixOS/nixpkgs) or your private build scripts.

### Quick start

* Choose your favorite package from PyPI (like https://pypi.python.org/pypi/thumbor)
* Feed its name to python2nix: `python -mpython2nix thumbor`
* Use code from stdout as the base for Nix expression (it may need manual tweaks).

### Known issues

* Tested only with pip==1.5.6.
* May ignore lots of the metadata (e.g. doesn't handle `tests_require`).

### Contributors

* @proger
* @phunehehe
