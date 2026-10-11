# testing.py : pengujian program dengan library unittest
import os
import unittest

from .validasi import cek_baris, cek_record, DataTidakValid
from .processing import Analisis, buat_record
from .fileio import PengelolaFile


class TestFilm(unittest.TestCase):
    #Kumpulan pengujian untuk program daftar film.

    def setUp(self):
        #Dijalankan sebelum tiap test: siapkan data contoh
        self.data = [
            buat_record("Inception", "Sci-Fi", 2010, 8.8),
            buat_record("Parasite", "Drama", 2019, 8.5),
            buat_record("Interstellar", "Sci-Fi", 2014, 8.6),
        ]
        self.analisis = Analisis(self.data)

    def test_rata_rata_rating(self):
        self.assertAlmostEqual(self.analisis.hitung_rata_rata(), 8.63, places=2)

    def test_rata_rata_args(self):
        self.assertEqual(self.analisis.hitung_rata_rata(6, 8, 10), 8)

    def test_jumlah_per_genre(self):
        self.assertEqual(self.analisis.jumlah_per_genre()["Sci-Fi"], 2)

    def test_urutkan_rating(self):
        hasil = self.analisis.urutkan_film(berdasarkan="rating")
        self.assertEqual(hasil[0]["judul"], "Inception")

    def test_urutkan_tahun(self):
        hasil = self.analisis.urutkan_film(berdasarkan="tahun")
        self.assertEqual(hasil[0]["judul"], "Parasite")

    def test_urutkan_judul(self):
        hasil = self.analisis.urutkan_film(berdasarkan="judul", menurun=False)
        self.assertEqual(hasil[0]["judul"], "Inception")

    def test_urutkan_pilihan_salah(self):
        with self.assertRaises(ValueError):
            self.analisis.urutkan_film(berdasarkan="warna")

    def test_data_bukan_list_memicu_assert(self):
        with self.assertRaises(AssertionError):
            Analisis("bukan list")

    def test_filter_genre(self):
        self.assertEqual(len(self.analisis.filter_genre("Drama")), 1)

    def test_rating_di_luar_batas_ditolak(self):
        with self.assertRaises(DataTidakValid):
            cek_record(buat_record("Film X", "Drama", 2020, 15))

    def test_baris_tahun_bukan_angka(self):
        with self.assertRaises(ValueError):
            cek_baris("Film X,Drama,dua ribu,8")

    def test_file_tidak_ada(self):
        pengelola = PengelolaFile("file_tidak_ada.txt")
        self.assertEqual(pengelola.baca_data(), [])

    def test_judul_ada_koma_tetap_terbaca(self):
        nama = "data_uji2.txt"
        if os.path.exists(nama):
            os.remove(nama)
        pengelola = PengelolaFile(nama)
        pengelola.buat_file()
        pengelola.tambah_data(buat_record("Film, Satu", "Aksi", 2020, 7))
        self.assertEqual(len(pengelola.baca_data()), 1)
        os.remove(nama)

    def test_tulis_dan_baca_file(self):
        nama = "data_uji.txt"
        if os.path.exists(nama):
            os.remove(nama)
        pengelola = PengelolaFile(nama)
        pengelola.buat_file()
        pengelola.tambah_data(buat_record("Joker", "Drama", 2019, 8.4))
        self.assertEqual(len(pengelola.baca_data()), 1)
        os.remove(nama)  # bersihkan file uji


if __name__ == '__main__':
    unittest.main()
