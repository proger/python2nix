#!/usr/bin/env python2.7
import sys
import requests
import pip_deps

PACKAGE = """\
  {name_only} = pythonPackages.buildPythonPackage rec {{
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

    return [name + vsn(name) for name, specs in reqs[name]]

def package_to_info(package):
    url = "https://pypi.python.org/pypi/{}/json".format(package)
    r = requests.get(url)
    return r.json()

def info_to_expr(info):
    name_only = info['info']['name']
    version = info['info']['version']

    name = name_only + "-" + version
    inputs = ' '.join(build_inputs(name_only))

    url = None
    md5 = None
    for url_item in info['urls']:
        url_ext = url_item['url']
        if url_ext.endswith('zip') or url_ext.endswith('tar.gz'):
            url = url_item['url']
            md5 = url_item['md5_digest']
            break
    if url is None:
      raise Exception('No download url found :-(')

    description = info['info']['description'].split('\n')[0]
    homepage = info['info']['home_page']
    license = guess_license(info)

    return PACKAGE.format(**locals())


if __name__ == '__main__':
    print info_to_expr(package_to_info(sys.argv[1]))
