## python2nix

Helper to build python [nix packages](https://github.com/NixOS/nixpkgs) that generates nix-expressions.

Quick start:

* `./python2nix.py thumbor`
* double-check dependencies in nixpkgs
* re-run for missing dependencies
* copy-paste
* ???
* PROFIT!

Don't consider these scripts to be stable.

### Known issues

Apparently pip doesn't handle `tests_require`.
