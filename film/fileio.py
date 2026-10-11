# fileio.py : baca / tulis / tambah file
from .validasi import cek_baris, cek_record, DataTidakValid


class PengelolaFile:
    #Class untuk mengelola file data film (format .txt).

    def __init__(self, nama_file="daftar_film.txt"):
        self.nama_file = nama_file

    def buat_file(self):
        #Mode 'x': membuat file data pertama kali (gagal jika sudah ada).
        try:
            with open(self.nama_file, "x") as file:
                file.write("judul,genre,tahun,rating\n")
            print("File data berhasil dibuat.")
        except FileExistsError:
            print("File data sudah ada, tidak dibuat ulang.")

    def tambah_data(self, record):
        #Mode 'a': menambah film baru di akhir file tanpa menghapus data lama.
        cek_record(record)  #validasi dulu sebelum disimpan
        #koma dihapus dari judul dan genre karena koma dipakai sebagai pemisah kolom
        judul = record["judul"].replace(",", " ")
        genre = record["genre"].replace(",", " ")
        with open(self.nama_file, "a") as file:
            file.write(f"{judul},{genre},"
                       f"{record['tahun']},{record['rating']}\n")

    def baca_data(self):
        #Mode 'r': membaca file baris per baris, baris rusak dilewati.
        data = []
        try:
            with open(self.nama_file, "r") as file:
                for nomor, baris in enumerate(file, start=1):
                    if nomor == 1:      #baris 1 adalah header
                        continue
                    if baris.strip() == "":   #baris kosong diabaikan
                        continue
                    try:
                        data.append(cek_baris(baris))
                    except (ValueError, DataTidakValid) as error:
                        print(f"Baris {nomor} dilewati: {error}")
        except FileNotFoundError:
            print(f"File '{self.nama_file}' belum ada. Buat dulu dengan buat_file().")
        return data

    def tulis_laporan(self, isi, nama_laporan="hasil_laporan.txt"):
        #Mode 'w': menulis laporan (isi lama ditimpa dengan laporan terbaru).
        with open(nama_laporan, "w") as file:
            file.write(isi)
        print(f"Laporan disimpan di {nama_laporan}")
