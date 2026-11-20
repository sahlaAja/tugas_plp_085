# `cek.py` — Detektor TODO, Fungsi Panjang, dan Syntax Error

Alat CLI sederhana berbasis `tree-sitter` untuk memeriksa berkas kode secara statis dengan tiga fitur:
1. **Komentar `TODO` / `FIXME`**: mendeteksi komentar yang mengandung `TODO` atau `FIXME` beserta nama berkas dan nomor baris.
2. **Fungsi panjang (> 30 baris)**: mendeteksi fungsi yang jumlah barisnya lebih dari 30 baris berdasarkan `start_point` dan `end_point`.
3. **Syntax error (`ERROR` / `MISSING`)**: mendeteksi pohon sintaks yang bermasalah beserta baris awal node error/missing pertama.

---

## Cara Memasang Dependensi

Aktifkan lingkungan Python terlebih dahulu, lalu pasang dependensi utama:

```bash
pip install tree-sitter tree-sitter-python
```

## Cara Menjalankan 
```bash
python cek.py <folder>
```

## Contoh Output
uji\komentar.py:1: # TODO: rapikan validasi input
uji\komentar.py:2: # FIXME: tangani kasus kosong
uji\panjang.py:1: fungsi 'fungsi_panjang' panjangnya 37 baris (> 30)
uji\rusak.py:1: terdapat syntax MISSING