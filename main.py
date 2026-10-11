# main.py : file utama untuk menjalankan program
from film.fileio import PengelolaFile
from film.processing import Analisis, buat_record
from film.validasi import DataTidakValid


def tampilkan_film(daftar):
    #Mencetak daftar film dengan nomor urut.
    if len(daftar) == 0:
        print("Belum ada film.")
        return
    for nomor, film in enumerate(daftar, start=1):
        print(f"{nomor}. {film['judul']} | {film['genre']} | "
              f"{film['tahun']} | rating {film['rating']}")


def tambah_film(pengelola):
    #Menu 1: minta input pengguna lalu simpan ke file.
    try:
        judul = input("Judul film   : ")
        genre = input("Genre        : ")
        tahun = int(input("Tahun rilis  : "))
        rating = float(input("Rating (0-10): "))
        #keyword argument pada pemanggilan fungsi
        record = buat_record(judul=judul, genre=genre, tahun=tahun, rating=rating)
        pengelola.tambah_data(record)
        print("Film berhasil disimpan.")
    except ValueError:
        print("Tahun dan rating harus berupa angka!")
    except DataTidakValid as error:
        print("Data ditolak:", error)


def cari_genre(pengelola):
    #Menu 3: tampilkan film dengan genre tertentu.
    analisis = Analisis(pengelola.baca_data())
    genre = input("Masukkan genre: ")
    hasil = analisis.filter_genre(genre)
    if len(hasil) == 0:
        print(f"Tidak ada film dengan genre '{genre}'.")
    else:
        tampilkan_film(hasil)


def urutkan_film(pengelola):
    #Menu 4: urutkan film berdasarkan rating, tahun, atau judul.
    analisis = Analisis(pengelola.baca_data())
    print("Urutkan berdasarkan: 1. Rating  2. Tahun  3. Judul")
    pilihan = input("Pilih: ")

    if pilihan == "1":
        hasil = analisis.urutkan_film(berdasarkan="rating", menurun=True)
    elif pilihan == "2":
        hasil = analisis.urutkan_film(berdasarkan="tahun", menurun=True)
    elif pilihan == "3":
        hasil = analisis.urutkan_film(berdasarkan="judul", menurun=False)
    else:
        print("Pilihan tidak tersedia.")
        return
    tampilkan_film(hasil)


def buat_laporan(pengelola):
    #Menu 5: buat laporan lalu simpan ke file txt.
    analisis = Analisis(pengelola.baca_data())
    teks = analisis.buat_teks_laporan()
    print(teks)
    pengelola.tulis_laporan(teks)


def main():
    pengelola = PengelolaFile(nama_file="daftar_film.txt")
    pengelola.buat_file()  # mode 'x': dibuat hanya jika belum ada

    while True:
        print("\n=== DAFTAR FILM ===")
        print("1. Tambah film")
        print("2. Lihat semua film")
        print("3. Cari film berdasarkan genre")
        print("4. Urutkan film")
        print("5. Buat laporan")
        print("0. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tambah_film(pengelola)
        elif pilihan == "2":
            tampilkan_film(pengelola.baca_data())
        elif pilihan == "3":
            cari_genre(pengelola)
        elif pilihan == "4":
            urutkan_film(pengelola)
        elif pilihan == "5":
            buat_laporan(pengelola)
        elif pilihan == "0":
            print("Terima kasih!")
            break
        else:
            print("Menu tidak tersedia.")


if __name__ == '__main__':
    main()
