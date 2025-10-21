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
    _words = ('', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh',
              'delapan', 'sembilan', 'sepuluh', 'sebelas')
    _suffixes = (
        ('belas', 'puluh'), ('', 'ratus'), ('', 'ribu', 'juta', 'miliar'),
        ('', 'triliun', 'septiliun', 'undesiliun', 'kuindesiliun',
         'novemdesiliun')
    )

    def __init__(self, num='', sep=','):
        self.separator = sep
        self._separators = (',', '.')
        self._result = []

        try:
            self._input = raw_input
        except NameError:
            self._input = input

        if num:
            self.parse(num, sep)

    def getresult(self, result=()):
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
        self._result.clear()

        for n in num:
            if ord(n) >= 48 and ord(n) <= 57:
                if n == '0':
                    self._result.append('nol')
                else:
                    self._result.append(self._words[int(n)])

        return self

    def _read(self, num, level=12):
        if level == 12:
            num = self.filter_num(num)

            if num.startswith('0'):
                return self.spell(num)

            if len(num) > 72:
                raise ValueError('Angka yang anda masukkan terlalu besar')

        i = (len(num) - 1) // level
        part = num[:len(num) - i * level]

        if level == 12:
            self._read(part, 3)
            self._result.append(self._suffixes[3][i] + ',')  # triliun, ...
        elif level == 3:
            self._read(part, 2)
            self._result.append(self._suffixes[2][i])  # ribu, juta, miliar
        elif level == 2:
            if int(part) < len(self._words):
                self._result.append(
                    (self._words[int(part)] + ' ' +
                     self._suffixes[1][i]).rstrip()
                )  # ratus
            else:
                if int(part[0]) == 1:
                    self._result.append(self._words[int(part[1])] + ' ' +
                                        self._suffixes[0][0])  # belas
                else:
                    self._result.append(
                        (self._words[int(part[0])] + ' ' +
                         self._suffixes[0][1] + ' ' +
                         self._words[int(part[1])]).rstrip() + ';'
                    )  # puluh

        num = num[len(num) - i * level:].lstrip('0')

        if num == '':
            return self

        return self._read(num, level)

    def parse(self, num='', sep=''):
        if sep == '':
            sep = self.separator

        if sep not in self._separators:
            raise ValueError('Harap gunakan koma atau titik sebagai pemisah')

        num = str(num).strip(' ,.')

        if num == '':
            return self

        self._result.clear()
        result = []

        if num.startswith('-') and num.strip(',-.0') != '':
            result.append('minus')

        sep_pos = num.rfind(sep)

        if sep_pos > 0:
            result.append(self.getresult(self._read(num[:sep_pos])._result))
            result.append('koma')
            result.append(self.spell(num[sep_pos:]).getresult())
        else:
            sep_alt = self._separators[self._separators.index(sep) ^ 1]
            sep_alt_pos = num.find(sep_alt)

            if (sep_alt_pos > 0 and num.startswith('0') or
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

    def run(self):
        """ markicob """
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
