import parsix
import unittest

class Test_Parsix(unittest.TestCase):
    def test_correct(self):
        '''Тест корректного выполнения работы парсером.
        '''
        p = parsix.Parsix()
        test_line = b'a|b b|cc|d d d|e|f|g| key1=value1 key2=value2 key3=value3'
        correct_dict = {'param0': 'a', 'param1': 'b b', 'param2': 'cc', 'param3': 'd d d', 'param4': 'e', 
                        'param5': 'f', 'param6': 'g', 'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
        self.assertDictEqual(p.parse_line(test_line), correct_dict)

    def test_number_of_pipes(self):
        '''Тест с неправильным количеством разделителей.
        '''
        p = parsix.Parsix()
        test_line = b'a|b b|cc|d d d|e|f| key1=value1'
        self.assertDictEqual(p.parse_line(test_line), {})

    def test_empty_value(self):
        '''Тест пустого значение внутри разделителей.
        '''
        p = parsix.Parsix()
        test_line = b'a|b b|cc||e|f|g| key1=value1'
        correct_dict = {'param0': 'a', 'param1': 'b b', 'param2': 'cc', 'param3': '', 'param4': 'e', 
                        'param5': 'f', 'param6': 'g', 'key1': 'value1'}
        self.assertDictEqual(p.parse_line(test_line), correct_dict)

    def test_escaped_pipe(self):
        '''Тест с экранированным разделителем.
        '''
        p = parsix.Parsix()
        test_line = b'a|b b|cc|d d\| d|e|f|g| key1=value1'
        correct_dict = {'param0': 'a', 'param1': 'b b', 'param2': 'cc', 'param3': 'd d\| d', 'param4': 'e', 
                        'param5': 'f', 'param6': 'g', 'key1': 'value1'}
        self.assertDictEqual(p.parse_line(test_line), correct_dict)

    def test_escaped_equals_sign(self):
        '''Тест с экранированным знаком равенства.
        '''
        p = parsix.Parsix()
        test_line = b'a|b b|cc|d d d|e|f|g| key1=value\\=1 key2=value2 key3=value3\\='
        correct_dict = {'param0': 'a', 'param1': 'b b', 'param2': 'cc', 'param3': 'd d d', 'param4': 'e', 
                        'param5': 'f', 'param6': 'g', 'key1': 'value\\=1', 'key2': 'value2', 'key3': 'value3\\='}
        self.assertDictEqual(p.parse_line(test_line), correct_dict)

    def test_space_in_value(self):
        '''Тест пробела в значении.
        '''
        p = parsix.Parsix()
        test_line = b'a|b b|cc|d d d|e|f|g| key1=value with space 1 key2=value 2'
        correct_dict = {'param0': 'a', 'param1': 'b b', 'param2': 'cc', 'param3': 'd d d', 'param4': 'e', 
                        'param5': 'f', 'param6': 'g', 'key1': 'value with space 1', 'key2': 'value 2'}
        self.assertDictEqual(p.parse_line(test_line), correct_dict)
    
    def test_long_line(self):
        '''Тест длинной строки.
        '''
        p = parsix.Parsix()
        test_line =  b'a|b b|cc|d d d|e|f|g| key1=value1 key2=value2' + b'value2'*2000
        self.assertDictEqual(p.parse_line(test_line), {})
        