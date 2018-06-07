from dbas.strings.lib import start_with_capital, start_with_small

assert start_with_capital('') == ''
assert start_with_capital('asd') == 'Asd'
assert start_with_capital('Asd') == 'Asd'
assert start_with_capital('ASD') == 'ASD'

assert start_with_small('') == ''
assert start_with_small('asd') == 'asd'
assert start_with_small('aSD') == 'aSD'
assert start_with_small('Asd') == 'asd'
assert start_with_small('ASD') == 'aSD'
