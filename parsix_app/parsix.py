import jsonlines
import re

class Parsix:
    """Класс для обработки логов и сохранения в формате JSON."""
    def __init__(self, length=10000) -> None:
        self.count_unicode = 0
        self.count_longline = 0
        self.count_not_enough_params = 0
        self.max_line_length = length
    
    def parse_line(self, line: bytes) -> dict:
        """Парсер строк.
        
        На входе получает строку, возвращает словарь ключей-значений.
        """ 
        param_dict = {}
        if len(line) > self.max_line_length:      # Проверка длины строки
            self.count_longline += 1
            return param_dict

        try:
            decoded_line = line.decode('8859')    # Кодировка 8859 
        except UnicodeDecodeError:
            self.count_unicode += 1
            return param_dict

        # Обработка разделителей | с помощью regex выражения
        groups = [x.group() for x in re.finditer(r'(?:[^\\|]|\\\|?)*\|', decoded_line)]

        if len(groups) >= 7:                      # Проверка количества параметров
            for i in range(7):
                param_dict['param'+str(i)] = groups[i][:-1]
        else:
            self.count_not_enough_params += 1
            return param_dict

        # Обработка пар key=value с помощью regex выражения
        matches = [x for x in re.finditer(r'(\b\w+)=(.*?(?=\s\w+=|$))', decoded_line)]
        for match in matches:
            param_dict[match.group(1)] = match.group(2)
            
        return param_dict

    def parse_file(self, file, jsonl_file, error_log) -> tuple:
        """Метод, обрабатывающий файл.

        Cохраняет ошибочные строки в error_log, а результат в JSONL формате.
        Возращает количество обработанных и ошибочных строк.
        """
        with jsonlines.open(jsonl_file, mode='w') as writer, open(error_log, mode='wb') as mis_writer:
            parsed_lines = 0
            not_parsed_lines = 0
            for line in file:
                data = self.parse_line(line)
                if data:
                    writer.write(data)
                    parsed_lines += 1
                else:
                    mis_writer.write(line)
                    not_parsed_lines +=1
        print(f"Number of lines with decode error:\t {self.count_unicode}")                    
        print(f"Number of lines exceeding max length:\t {self.count_longline}")            
        print(f"Number of lines without 7 parameters:\t {self.count_not_enough_params}")
        return parsed_lines, not_parsed_lines
