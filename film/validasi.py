#validasi.py : pengecekan input dan data


class DataTidakValid(Exception):
    #Exception buatan sendiri untuk data yang tidak valid.
    pass


def cek_record(record):
    #Cek satu record (dict). Jika salah, munculkan DataTidakValid.
    #Semua field wajib terisi
    for nama_field, isi in record.items():
        if str(isi).strip() == "":
            raise DataTidakValid(f"Field '{nama_field}' tidak boleh kosong")

    #Tahun harus masuk akal
    if record["tahun"] < 1888:
        raise DataTidakValid("Tahun film tidak valid")

    #Rating hanya boleh 0 sampai 10 (tidak boleh negatif)
    if record["rating"] < 0 or record["rating"] > 10:
        raise DataTidakValid("Rating harus antara 0 sampai 10")
    return record


def cek_baris(baris):
    #Ubah satu baris teks 'judul,genre,tahun,rating' menjadi dict.
    bagian = baris.strip().split(",")
    if len(bagian) != 4:
        raise DataTidakValid("Jumlah kolom harus 4")

    # int() dan float() menimbulkan ValueError jika bukan angka
    record = {
        "judul": bagian[0].strip(),
        "genre": bagian[1].strip(),
        "tahun": int(bagian[2]),
        "rating": float(bagian[3]),
    }
    return cek_record(record)


# Pengujian lokal: hanya jalan jika file ini dijalankan langsung
if __name__ == '__main__':
    print(cek_baris("Inception,Sci-Fi,2010,8.8"))
    try:
        cek_baris("Film Rusak,Drama,2020,15")
    except DataTidakValid as e:
        print("Error tertangkap:", e)
