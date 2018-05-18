import subprocess

existent_binaries = [
    ('uwsgi', '--version', ''),
    ('alembic', '--help', 'current'),
    ('pserve', '--help', 'development.ini'),
]

functional_binaries = [
    ('uwsgi', ''),
    ('alembic', 'current'),
    ('pserve', 'development.ini'),
]


def run(binary, argument):
    result = subprocess.run([binary, argument], stdout=subprocess.PIPE).stdout.decode('utf-8')
    assert 'not found' not in result


# check for binaries
for (binary, argument1, argument2) in existent_binaries:
    print('Run: {} {}'.format(binary, argument1))
    run(binary, argument1)

    print('Execute: {} {}'.format(binary, argument2))
    run(binary, argument2)
