#!/usr/bin/env python
# terbilang - Mengubah Angka Menjadi Huruf Terbilang.
# https://github.com/nggit/terbilang
# Copyright (c) 2021 nggit.
#
import sys

if sys.platform == 'win32':
    GREEN  = ''
    NORMAL = ''
else:
    GREEN  = '\033[92m'
    NORMAL = '\033[0m'

class Terbilang:
    def __init__(self, num=''):
        self._num_str  = ['', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh', 'delapan', 'sembilan', 'sepuluh', 'sebelas']
        self._suffixes = [
            'puluh', 'belas', ['', 'ratus'], ['', 'ribu', 'juta', 'miliar'], ['', 'triliun', 'septiliun', 'undesiliun', 'kuindesiliun', 'novemdesiliun']
        ]
        self._result   = []
        self.parse(num)
        try:
            self._input = raw_input
        except NameError:
            self._input = input

    def getresult(self):
        return ' '.join([r for r in self._result if r != '']).rstrip(', ').replace('satu ratus', 'seratus') \
                                                                          .replace('satu ribu', 'seribu') \
                                                                          .replace(';', '')

    def spell(self, num=''):
        del self._result[:]
        for n in num:
            if n == '0':
                self._result.append('nol')
            else:
                self._result.append(self._num_str[int(n)])
        return self

    def parse(self, num=''): # FIXME: sederhanakan ini
        num = str(num).strip()
        if num != num.lstrip('0'):
            return self.spell(num)
        if len(num) > 72:
            raise ValueError('Maaf, angka yang anda masukkan terlalu besar')
        del self._result[:]
        while num != '':
            s_index = (len(num) - 1) // 12
            num_    = num[:len(num) - s_index * 12]
            while num_ != '':
                s_index_ = (len(num_) - 1) // 3
                num__    = num_[:len(num_) - s_index_ * 3]
                while num__ != '':
                    s_index__ = (len(num__) - 1) // 2
                    num___    = num__[:len(num__) - s_index__ * 2]
                    if int(num___) < len(self._num_str):
                        self._result.append((self._num_str[int(num___)] + ' ' + self._suffixes[2][s_index__]).rstrip()) # ratus
                    elif len(num___) == 2:
                        if int(num___[0]) == 1:
                            self._result.append(self._num_str[int(num___[1])] + ' ' + self._suffixes[1]) # belas
                        else:
                            self._result.append((self._num_str[int(num___[0])] + ' ' + self._suffixes[0] + ' ' + self._num_str[int(num___[1])]).rstrip() + ';') # puluh
                    num__ = num__[len(num__) - s_index__ * 2:].lstrip('0')
                self._result.append(self._suffixes[3][s_index_]) # ribu, juta, miliar
                num_ = num_[len(num_) - s_index_ * 3:].lstrip('0')
            self._result.append(self._suffixes[4][s_index] + ',') # triliun, septiliun, ..., novemdesiliun
            num = num[len(num) - s_index * 12:].lstrip('0')
        return self

    """ markicob """
    def run(self):
        num = 0
        while num != '':
            num = self._input(' Masukkan angka (maks. 72 digit) -->|'.rjust(72, '-') + '\n')
            print('%s%s%s' % (GREEN, self.parse(num).getresult(), NORMAL))
        return None

if __name__ == '__main__':
    t = Terbilang()
    t.run()
