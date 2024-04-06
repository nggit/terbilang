#!/usr/bin/env python
# terbilang - Mengubah Angka Menjadi Huruf Terbilang.
# https://github.com/nggit/terbilang
# Copyright (c) 2021 nggit.
#
import sys

if sys.platform == 'win32':
    GREEN = ''
    NORMAL = ''
else:
    GREEN = '\033[92m'
    NORMAL = '\033[0m'


class Terbilang:
    def __init__(self, num='', sep=','):
        self._num_str = [
            '', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh',
            'delapan', 'sembilan', 'sepuluh', 'sebelas'
        ]
        self._suffixes = [
            'belas', 'puluh', ['', 'ratus'], ['', 'ribu', 'juta', 'miliar'],
            ['', 'triliun', 'septiliun', 'undesiliun', 'kuindesiliun',
                'novemdesiliun']
        ]
        self._result = []
        self._separators = [',', '.']
        self.separator = sep
        self.parse(num)

        try:
            self._input = raw_input
        except NameError:
            self._input = input

    def getresult(self, result=[]):
        if result:
            return ' '.join(
                v for v in result if v != ''
            ).rstrip(' ,').replace('satu r', 'ser').replace(';', '')

        return ' '.join(self._result)

    def filter_num(self, num=''):
        for i in range(len(num)):
            if ord(num[i]) < 48 or ord(num[i]) > 57:
                num = num[:i] + ' ' + num[i + 1:]

        return num.replace(' ', '')

    def spell(self, num=''):
        del self._result[:]

        for n in num:
            if ord(n) >= 48 and ord(n) <= 57:
                if n == '0':
                    self._result.append('nol')
                else:
                    self._result.append(self._num_str[int(n)])

        return self

    def _read(self, num=''):
        num = self.filter_num(num)

        if num.find('0') == 0:
            return self.spell(num)

        if len(num) > 72:
            raise ValueError('Maaf, angka yang anda masukkan terlalu besar')

        del self._result[:]

        while num != '':
            s_index = (len(num) - 1) // 12
            num1 = num[:len(num) - s_index * 12]

            while num1 != '':
                s_index1 = (len(num1) - 1) // 3
                num2 = num1[:len(num1) - s_index1 * 3]

                while num2 != '':
                    s_index2 = (len(num2) - 1) // 2
                    num3 = num2[:len(num2) - s_index2 * 2]

                    if int(num3) < len(self._num_str):
                        self._result.append(
                            (self._num_str[int(num3)] + ' ' +
                                self._suffixes[2][s_index2]).rstrip()
                        )  # ratus
                    else:
                        if int(num3[0]) == 1:
                            self._result.append(
                                self._num_str[int(num3[1])] + ' ' +
                                self._suffixes[0]
                            )  # belas
                        else:
                            self._result.append(
                                (self._num_str[int(num3[0])] + ' ' +
                                    self._suffixes[1] + ' ' +
                                    self._num_str[int(num3[1])]).rstrip() + ';'
                            )  # puluh

                    num2 = num2[len(num2) - s_index2 * 2:].lstrip('0')

                # ribu, juta, miliar
                self._result.append(self._suffixes[3][s_index1])
                num1 = num1[len(num1) - s_index1 * 3:].lstrip('0')

            # triliun, septiliun, ..., novemdesiliun
            self._result.append(self._suffixes[4][s_index] + ',')
            num = num[len(num) - s_index * 12:].lstrip('0')

        return self

    def parse(self, num='', sep=''):
        if num == '':
            return self

        if sep == '':
            sep = self.separator

        if sep not in self._separators:
            raise ValueError('Harap gunakan koma atau titik sebagai pemisah')

        result = []
        num = str(num).strip(' ,.')

        if num.find('-') == 0 and num.strip(',-.0') != '':
            result.append('minus')

        sep_pos = num.rfind(sep)

        if sep_pos > 0:
            result.append(self.getresult(self._read(num[:sep_pos])._result))
            result.append('koma')
            result.append(self.spell(num[sep_pos:]).getresult())
        else:
            sep_alt = self._separators[self._separators.index(sep) ^ 1]
            sep_alt_pos = num.find(sep_alt)

            if (sep_alt_pos > 0 and num.find('0') == 0 or
                    num.count(sep_alt) == 1 and len(num[sep_alt_pos:]) != 4):
                result.append(
                    self.getresult(self._read(num[:sep_alt_pos])._result)
                )
                result.append('koma')
                result.append(self.spell(num[sep_alt_pos:]).getresult())
            else:
                result.append(self.getresult(self._read(num)._result))

        self._result[:] = result
        return self

    """ markicob """
    def run(self):
        num = 0
        sep = ','

        for i in range(len(sys.argv)):
            if sys.argv[i - 1] == '-n' or sys.argv[i - 1] == '--n':
                num = sys.argv[i]
            elif sys.argv[i - 1] == '-s' or sys.argv[i - 1] == '--s':
                sep = sys.argv[i]

            if sys.argv[i] == sys.argv[-1] and len(sys.argv) > 2:
                print(self.parse(num, sep).getresult())
                return

        while num != '':
            num = self._input(
                ' Masukkan angka (maks. 72 digit) -->|'.rjust(72, '-') + '\n'
            )
            print('%s%s%s' % (GREEN, self.parse(num, sep).getresult(), NORMAL))

        print(
            'terbilang - https://github.com/nggit/terbilang\n\nPenggunaan:\n'
            '   python -m terbilang\n   python -m terbilang -n 1.000,00'
        )


if __name__ == '__main__':
    t = Terbilang()
    t.run()
