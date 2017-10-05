## python2nix

Put a PyPI package name in, get a Nix expression out to add to [nixpkgs](https://github.com/NixOS/nixpkgs) or your private build scripts.

### Quick start

* Choose your favorite package from PyPI (like https://pypi.python.org/pypi/thumbor)
* Feed its name to python2nix: `python -mpython2nix thumbor`
* Use code from stdout as the base for Nix expression (it may need manual tweaks).

```
nix-shell -p pythonPackages.virtualenv
virtualenv env
env/bin/pip install -r pip.requirements
mkdir -p env/build
env/bin/python -mpython2nix thumbor | tee thumbor.nix
```

### Known issues

* Tested only with pip==1.5.6.
* May ignore lots of the metadata (e.g. doesn't handle `tests_require`).

### Contributors

* [@bjornfor](https://github.com/bjornfor)
* [@domenkozar](https://github.com/domenkozar)
* [@phunehehe](https://github.com/phunehehe)
* [@proger](https://github.com/proger)

### You may also like

* @tailhook's [reqtxt2nix](https://github.com/tailhook/reqtxt2nix) which lets you produce build environments (put your `requirements.txt` in, get a `myEnvFun` out)
