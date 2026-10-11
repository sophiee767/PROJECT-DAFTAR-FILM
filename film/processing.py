# processing.py : perhitungan dan analisis data


def buat_record(judul, genre, tahun, rating, **tambahan):
    #Membuat satu data film (dict).
    #**tambahan dipakai untuk atribut opsional, misalnya sutradara.
    record = {
        "judul": judul,
        "genre": genre,
        "tahun": tahun,
        "rating": rating,
    }
    record.update(tambahan)  #masukkan atribut tambahan jika ada
    return record


class Analisis:
    #Class untuk mengolah dan menganalisis daftar film.

    def __init__(self, data):
        # assert: memastikan data yang masuk berupa list.
        # Jika bukan list, program berhenti dan menampilkan pesan di kanan.
        assert isinstance(data, list), "data harus berupa list"
        self.data = data  # data berupa list yang isinya dict film

    def hitung_rata_rata(self, *angka):
        #*args: menerima angka sebanyak apa pun.
        # Jika tidak diberi angka, hitung rata-rata rating semua film.
        if not angka:
            angka = [film["rating"] for film in self.data]
        if len(angka) == 0:
            return 0
        return sum(angka) / len(angka)

    def jumlah_per_genre(self):
        #Menghitung banyak film untuk setiap genre.
        hasil = {}
        for film in self.data:
            genre = film["genre"]
            hasil[genre] = hasil.get(genre, 0) + 1
        return hasil

    def urutkan_film(self, berdasarkan="rating", menurun=True):
        #Mengurutkan film berdasarkan 'rating', 'tahun', atau 'judul'.
        #menurun=True artinya dari besar ke kecil.
        if berdasarkan == "rating":
            kunci = lambda film: film["rating"]
        elif berdasarkan == "tahun":
            kunci = lambda film: film["tahun"]
        elif berdasarkan == "judul":
            kunci = lambda film: film["judul"].lower()
        else:
            raise ValueError("Pilihan urutan: rating, tahun, atau judul")
        return sorted(self.data, key=kunci, reverse=menurun)

    def filter_genre(self, genre):
        #Mengambil film yang genre-nya sama (huruf besar/kecil tidak masalah)."""
        return list(filter(lambda film: film["genre"].lower() == genre.lower(),
                           self.data))

    def buat_teks_laporan(self):
        #Menyusun teks laporan yang nanti ditulis ke file.
        baris = ["=== LAPORAN DAFTAR FILM ==="]
        baris.append(f"Jumlah film      : {len(self.data)}")
        baris.append(f"Rata-rata rating: {self.hitung_rata_rata():.2f}")
        baris.append("\nJumlah per genre:")
        for genre, jumlah in self.jumlah_per_genre().items():
            baris.append(f"  - {genre}: {jumlah} film")
        if self.data:
            baris.append("\nPeringkat film:")
            for nomor, film in enumerate(self.urutkan_film(), start=1):
                baris.append(f"  {nomor}. {film['judul']} ({film['tahun']}) "
                             f"- rating {film['rating']}")
        return "\n".join(baris)


# Pengujian lokal: hanya jalan jika file ini dijalankan langsung
if __name__ == '__main__':
    contoh = [
        buat_record("Inception", "Sci-Fi", 2010, 8.8),
        buat_record("Parasite", "Drama", 2019, 8.5, sutradara="Bong Joon-ho"),
    ]
    analisis = Analisis(contoh)
    # assert: cek hasil hitungan sesuai harapan (8.8 dan 8.5 -> rata-rata 8.65)
    assert analisis.hitung_rata_rata() == 8.65, "rata-rata rating salah"
    assert len(analisis.filter_genre("Drama")) == 1, "filter genre salah"
    print(analisis.buat_teks_laporan())
