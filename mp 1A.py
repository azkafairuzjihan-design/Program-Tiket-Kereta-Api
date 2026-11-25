import csv
import os

NAMA_FILE = "dataset_tiket_kereta.readable.csv"


def muat_data():
    data = []
    if not os.path.exists(NAMA_FILE):
        print(f"Error: File '{NAMA_FILE}' tidak ditemukan!")
        return data

    with open(NAMA_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["Harga Tiket"] = int(row["Harga Tiket"])
            row["Kursi Tersedia"] = int(row["Kursi Tersedia"])
            data.append(row)
    return data


def pilih_dari_daftar(judul, daftar_pilihan):
    print(f"\n--- {judul} ---")
    for idx, item in enumerate(daftar_pilihan, start=1):
        print(f"{idx}. {item}")

    while True:
        try:
            pilihan = int(input("Masukkan nomor pilihan Anda: "))
            if 1 <= pilihan <= len(daftar_pilihan):
                return daftar_pilihan[pilihan - 1]
            else:
                print("Nomor tidak valid. Silakan pilih nomor yang tersedia.")
        except ValueError:
            print("Input harus berupa angka!")


def menu_pencarian_kereta(data_kereta, role="PENUMPANG"):
    print(f"----------SELAMAT DATANG {role.upper()}----------")

    daftar_asal = sorted(list(set(row["Stasiun Asal"] for row in data_kereta)))
    print("\nDaftar Stasiun Asal yang tersedia:")
    for asal in daftar_asal:
        print(f"- {asal}")

    stasiun_asal = input("\nMasukkan Stasiun Asal: ").strip()

    data_asal = [
        row
        for row in data_kereta
        if row["Stasiun Asal"].lower() == stasiun_asal.lower()
    ]

    if not data_asal:
        print(f"Maaf, tidak ada jadwal keberangkatan dari '{stasiun_asal}'.")
        return

    daftar_tujuan = sorted(list(set(row["Stasiun Tujuan"] for row in data_asal)))
    stasiun_tujuan = pilih_dari_daftar("PILIH STASIUN TUJUAN", daftar_tujuan)

    data_rute = [
        row for row in data_asal if row["Stasiun Tujuan"] == stasiun_tujuan
    ]

    daftar_jadwal = sorted(
        list(
            set(
                f"{row['Tanggal Berangkat']} | Jam {row['Jam Berangkat']}"
                for row in data_rute
            )
        )
    )
    jadwal_terpilih = pilih_dari_daftar(
        "PILIH TANGGAL & WAKTU BERANGKAT", daftar_jadwal
    )

    tgl_pilih, jam_teks = jadwal_terpilih.split(" | Jam ")

    data_jadwal = [
        row
        for row in data_rute
        if row["Tanggal Berangkat"] == tgl_pilih
        and row["Jam Berangkat"] == jam_teks
    ]

    while True:
        try:
            harga_maks = int(
                input("\nMasukkan harga maksimal tiket (Rp): ").strip()
            )
            break
        except ValueError:
            print("Harap masukkan angka nominal harga tanpa titik/koma!")

    kereta_sesuai_budget = [
        row for row in data_jadwal if row["Harga Tiket"] <= harga_maks
    ]

    if not kereta_sesuai_budget:
        print(
            f"\nMaaf, tidak ada kereta untuk jadwal tersebut dengan harga di bawah Rp {harga_maks:,}."
        )
        return

    print("\n--- PILIH KERETA & KELAS TERSEDIA ---")
    for idx, k in enumerate(kereta_sesuai_budget, start=1):
        print(
            f"{idx}. {k['Nama Kereta']} | Kelas: {k['Kelas']} | Harga: Rp {k['Harga Tiket']:,}"
        )

    while True:
        try:
            pilih_ka = int(input("\nPilih nomor kereta yang diinginkan: "))
            if 1 <= pilih_ka <= len(kereta_sesuai_budget):
                kereta_final = kereta_sesuai_budget[pilih_ka - 1]
                break
            else:
                print("Pilihan tidak valid.")
        except ValueError:
            print("Masukkan angka!")

    print("\n---HASIL PENGECEKAN KURSI---")
    print(f"Nama Kereta    : {kereta_final['Nama Kereta']}")
    print(
        f"Rute           : {kereta_final['Stasiun Asal']} -> {kereta_final['Stasiun Tujuan']}"
    )
    print(
        f"Jadwal         : {kereta_final['Tanggal Berangkat']} pukul {kereta_final['Jam Berangkat']}"
    )
    print(f"Kelas          : {kereta_final['Kelas']}")
    print(f"Harga Tiket    : Rp {kereta_final['Harga Tiket']:,}")
    print("-" * 40)

    if (
        kereta_final["Status"].lower() == "tersedia"
        and kereta_final["Kursi Tersedia"] > 0
    ):
        print(
            f"STATUS         : TERSEDIA (Sisa {kereta_final['Kursi Tersedia']} kursi)"
        )
    else:
        print("STATUS         : TIDAK TERSEDIA / PENUH")
    print("-" * 40)


def menu_admin(data_kereta):
    print("-----PANEL ADMIN-----")
    password = input("Masukkan password admin (default: admin123): ")
    if password != "admin123":
        print("Password salah! Akses ditolak.")
        return

    while True:
        print("\nMenu Admin:")
        print("1. Lihat Ringkasan Total Data Kereta")
        print("2. Tambah Jadwal Kereta Baru")
        print("3. Kembali ke Menu Utama")

        pilihan = input("Pilih menu (1-3): ")
        if pilihan == "1":
            print(f"\nTotal data jadwal kereta dalam sistem: {len(data_kereta)}")
            print("5 Data Teratas:")
            for row in data_kereta[:5]:
                print(
                    f"- {row['Nama Kereta']} ({row['Stasiun Asal']}-{row['Stasiun Tujuan']}) | {row['Tanggal Berangkat']} | Kursi: {row['Kursi Tersedia']}"
                )
        elif pilihan == "2":
            print("\n--- Tambah Data Kereta Baru ---")
            nama = input("Nama Kereta: ")
            asal = input("Stasiun Asal: ")
            tujuan = input("Stasiun Tujuan: ")
            tgl = input("Tanggal Berangkat (YYYY-MM-DD): ")
            jam = input("Jam Berangkat (HH:MM): ")
            kelas = input("Kelas (Eksekutif/Bisnis/Ekonomi): ")
            harga = int(input("Harga Tiket: "))
            kursi = int(input("Kursi Tersedia: "))

            data_baru = {
                "S.no.": str(len(data_kereta)),
                "Nama Kereta": nama,
                "Stasiun Asal": asal,
                "Stasiun Tujuan": tujuan,
                "Tanggal Berangkat": tgl,
                "Jam Berangkat": jam,
                "Kelas": kelas,
                "Harga Tiket": harga,
                "Kursi Tersedia": kursi,
                "Status": "Tersedia" if kursi > 0 else "Penuh",
                "Tahun Operasional": "2026",
                "Umur Kereta Tahun": "0",
            }
            data_kereta.append(data_baru)

            with open(NAMA_FILE, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=data_baru.keys())
                writer.writerow(data_baru)
            print("Data berhasil ditambahkan!")
        elif pilihan == "3":
            break
        else:
            print("Pilihan tidak valid.")


def main():
    data_kereta = muat_data()
    if not data_kereta:
        return

    while True:
        print("-----SISTEM PENGECEKAN KURSI KERETA API-----")
        print("Login sebagai:")
        print("1. Penumpang")
        print("2. Petugas")
        print("3. Admin")
        print("4. Keluar")

        role = input("Masukkan pilihan (1/2/3/4): ").strip()

        if role == "1":
            menu_pencarian_kereta(data_kereta, role="PENUMPANG")
        elif role == "2":
            menu_pencarian_kereta(data_kereta, role="PETUGAS")
        elif role == "3":
            menu_admin(data_kereta)
        elif role == "4":
            print("Terima kasih telah menggunakan sistem ini.")
            break
        else:
            print("Pilihan tidak valid, silakan masukkan 1, 2, 3, atau 4.")


if __name__ == "__main__":
    main()
