import subprocess

# triplets of  binary, a parameter to check whether the binary is executable and a paramter to test its functionality
binaries = [
    ('uwsgi', '--version', ''),
    ('alembic', '--help', 'current'),
    ('pserve', '--help', 'development.ini'),
]

# string that should not be in the stdout
str_for_output = 'not found'

error_str_exec = 'The binary <{}> could not be executed.'
error_str_fnc = 'The binary <{}> could not be called with standard parameters.'


def run_subprocess(binary: str, argument: str) -> str:
    """
    Runs the binary with its argument as subprocess and returns the stdout.

    :param binary: Name of the binary as string
    :param argument: Arguments for the binary
    :return: Stdout decoded as utf-8
    """
    return subprocess.run([binary, argument], stdout=subprocess.PIPE).stdout.decode('utf-8')


def test_binary(binary: str, argument: str, error_str: str):
    """
    Executes the binary with argument and checks for a predefined string in the output. If this string is not found
    everything went well

    :param binary: Name of the binary as string
    :param argument: Arguments for the binary
    :param error_str: Error message which should be thrown
    :return:
    """
    print('Execute command: {} {}'.format(binary, argument))
    correct_output = str_for_output not in run_subprocess(binary, argument)
    if not correct_output:
        raise FileNotFoundError(error_str)


if __name__ == "__main__":
    for (binary, argument, _) in binaries:
        test_binary(binary, argument, error_str_exec.format(binary))

    for (binary, _, argument) in binaries:
        test_binary(binary, argument, error_str_fnc.format(binary))
