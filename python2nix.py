#!/usr/bin/env python2.7
import sys
import requests
import pip_deps

PACKAGE = """\
  {attr} = pythonPackages.buildPythonPackage rec {{
    name = "{name}";

    propagatedBuildInputs = [ {inputs} ];

    src = fetchurl {{
      url = "{url}";
      md5 = "{md5}";
    }};

    meta = with stdenv.lib; {{
      description = "{description}";
      homepage = {homepage};
      license = {license};
    }};
  }};

"""

LICENSE_MAP = {
    'http://www.opensource.org/licenses/mit-license.php': 'licenses.mit',
    'MIT': 'licenses.mit',
    'PSF': 'licenses.psfl'
}

_missing = object()
def guess_license(info):
    l = info['info']['license']
    license = LICENSE_MAP.get(l, _missing)
    if license is _missing:
        sys.stderr.write('WARNING: unknown license (please update LICENSE_MAP): ' + l + '\n')
        return 'unknown'
    return license

def nix_mangle_attr(name):
    name_parts = name.replace('.', '_').split('-')
    attr_parts = name_parts[0:1] + [n.capitalize() for n in name_parts[1:]]
    return ''.join(attr_parts)

_pip_dependency_cache = {}

def pip_dump_dependencies(name): # memoized version
    if name in _pip_dependency_cache:
        return _pip_dependency_cache[name]
    ret = pip_deps.pip_dump_dependencies(name)
    _pip_dependency_cache[name] = ret
    return ret

def build_inputs(name):
    reqs, vsns = pip_dump_dependencies(name)

    def vsn(name):
        vsn = vsns.get(name)
        if not vsn:
            name = name.replace('_', '-') # pypi workaround ?
            vsn = vsns.get(name)

        if vsn:
            vsn = "_" + vsn
        return vsn or ''

    return [nix_mangle_attr(name + vsn(name)) for name, specs in reqs[name]]

def package_to_info(package):
    url = "https://pypi.python.org/pypi/{}/json".format(package)
    r = requests.get(url)
    return r.json()

def info_to_expr(info):
    name_only = info['info']['name']
    version = info['info']['version']

    name = name_only + "-" + version
    attr = nix_mangle_attr(name_only + "_" + version)
    inputs = ' '.join(build_inputs(name_only))

    url = info['urls'][0]['url']
    md5 = info['urls'][0]['md5_digest']

    description = info['info']['description'].split('\n')[0]
    homepage = info['info']['home_page']
    license = guess_license(info)

    return PACKAGE.format(**locals())


if __name__ == '__main__':
    print info_to_expr(package_to_info(sys.argv[1]))
