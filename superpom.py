import subprocess
import xmltodict
from collections import OrderedDict

DEP_FILE = 'deps.txt'


def generate_tree():
    try:
        a = subprocess.call(['mvn', 'dependency:tree', '-Doutput={}'.format(DEP_FILE)])
    except FileNotFoundError:
        print('Looks like maven is not installed. Please check')
    return a


def parse_file():
    deplist = []
    with open(DEP_FILE) as f:
        data = f.read().replace('+-', '').replace('|', '').replace('\-', '').\
            replace(' ', '').rstrip().split('\n')
    for dependency in data:
        dependency = dependency.replace('\n', '').split(':')
        if len(dependency) == 5:
            dependency.pop(2)
            deplist.append(
                OrderedDict([('groupId', dependency[0]),
                             ('artifactId', dependency[1]), ('version', dependency[2])]))
    subprocess.call(['rm', '{}'.format(DEP_FILE)])
    return deplist


def parse_pomxml(deplist):
    with open('pom.xml') as f:
        data = f.read()
    dep_parsed = xmltodict.parse(data)
    dep_parsed['project']['dependencies']['dependency'] = deplist
    orig = xmltodict.unparse(dep_parsed, pretty=True)
    with open('superpom.xml', 'w') as f:
        f.write(orig)


if generate_tree() == 0:
    deplist = parse_file()
    parse_pomxml(deplist)

