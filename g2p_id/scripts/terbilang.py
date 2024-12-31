satuan = ['', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh',
          'delapan', 'sembilan', 'sepuluh', 'sebelas']

puluh = 10
ratus = 10 ** 2
ribu = 10 ** 3
juta = 10 ** 6
miliar = 10 ** 9
triliun = 10 ** 12
biliun = 10 ** 15


def terbilang_(n):
    n = int(n)
    if n >= 0 and n <= 11:
        hasil = [satuan[n]]
    elif n >= 12 and n <= 19:
        hasil = terbilang_(n % puluh) + ['belas']
    elif n >= 20 and n < ratus:
        hasil = terbilang_(n / puluh) + ['puluh'] + terbilang_(n % puluh)
    elif n >= ratus and n <= 199:
        hasil = ['seratus'] + terbilang_(n - ratus)
    elif n >= 200 and n < ribu:
        hasil = terbilang_(n / ratus) + ['ratus'] + terbilang_(n % ratus)
    elif n >= ribu and n <= 1999:
        hasil = ['seribu'] + terbilang_(n - ribu)
    elif n >= 2000 and n < juta:
        hasil = terbilang_(n / ribu) + ['ribu'] + terbilang_(n % ribu)
    elif n >= juta and n < miliar:
        hasil = terbilang_(n / juta) + ['juta'] + terbilang_(n % juta)
    elif n >= miliar and n < triliun:
        hasil = terbilang_(n / miliar) + ['miliar'] + terbilang_(n % miliar)
    elif n >= triliun and n < biliun:
        hasil = terbilang_(n / triliun) + ['triliun'] + terbilang_(n % triliun)
    else:
        hasil = terbilang_(n / biliun) + ['biliun'] + terbilang_(n % biliun)
    return hasil


def terbilang(n):
    if n == 0:
        return 'nol'
    t = terbilang_(n)
    while '' in t:
        t.remove('')
    return ' '.join(t)


if __name__ == '__main__':
    n = [0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 19, 20, 21, 50, 99, 100, 102,
         989, 1000, 1001, 9891, 10 * ribu, 100 * ribu, 200001, 987123, juta,
         10 * juta, 10 * miliar, triliun, biliun]

    for i in n:
        s = '{:,}'.format(i)
        s = s.replace(',', '.')
        print('{i} -> {t}'.format(i=s, t=[terbilang(i)]))
