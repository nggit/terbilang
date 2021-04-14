# terbilang
terbilang adalah sebuah alat yang berfungsi untuk mengubah angka menjadi huruf terbilang. terbilang ditulis dengan Python dan dapat menerima masukan angka hingga 72 digit (999+ miliar [novemdesiliun](https://id.wikipedia.org/wiki/Daftar_bilangan_di_atas_triliun)).
## Instalasi
```
pip install terbilang
```
## Penggunaan
terbilang dapat dijalankan langsung sebagai skrip Python:
```
python -m terbilang
```
Jika anda adalah pengembang, terbilang juga bisa digunakan sebagai modul:
```python
from terbilang import Terbilang

t = Terbilang()

t.parse('1001')
print(t.getresult()) # seribu satu

t.parse('121001')
print(t.getresult()) # seratus dua puluh satu ribu satu
```
terbilang dibuat agar memiliki jangkauan yang lebar, tetapi diharapkan dapat membaca angka dengan lebih *luwes*. Sebagai contoh, "1000 triliun" tidak dibaca sebagai "satu kuadriliun" tetapi "seribu triliun". Sedangkan "1000 juta" tentu akan dibaca sebagai "satu miliar". terbilang akan menampilkan tanda koma jika bilangan sudah mencapai triliunan atau lebih untuk meningkatkan keterbacaan:
```python
t.parse('19000000000000000000071000002011000000')
print(t.getresult()) # sembilan belas undesiliun, tujuh puluh satu ribu triliun, dua miliar sebelas juta
```
