import subprocess

existent_binaries = [
    ('uwsgi', '--version'),
    ('alembic', '--help'),
    ('pserve', '--help'),
]

functional_binaries = [
    ('uwsgi', '-s 1337'),
    ('alembic', 'current'),
    ('pserve', 'development.ini'),
]

# check for binaries
for (binary, argument) in existent_binaries:
    print('Run: {} {}'.format(binary, argument))
    result = subprocess.run([binary, argument], stdout=subprocess.PIPE).stdout.decode('utf-8')
    assert 'not found' not in result

# test binaries
for (binary, argument) in functional_binaries:
    print('Test: {} {}'.format(binary, argument))
    result = subprocess.run([binary, argument], stdout=subprocess.PIPE).stdout.decode('utf-8')
    assert 'not found' not in result

