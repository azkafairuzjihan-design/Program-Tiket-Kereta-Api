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
			row["Kursi Awal"] = row["Kursi Tersedia"]
			data.append(row)
	return data


def simpan_semua_data(data_kereta):
	if not data_kereta:
		return
	fieldnames = [k for k in data_kereta[0].keys() if k != "Kursi Awal"]
	with open(NAMA_FILE, mode="w", newline="", encoding="utf-8") as file:
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writeheader()
		for row in data_kereta:
			baris_simpan = {k: v for k, v in row.items() if k != "Kursi Awal"}
			writer.writerow(baris_simpan)


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


def tanya_lanjut(pesan):
	while True:
		jawab = input(f"\n{pesan} (y/n): ").strip().lower()
		if jawab in ["y", "n"]:
			return jawab == "y"
		print("Input tidak valid! Masukkan 'y' untuk ya atau 'n' untuk tidak.")


def menu_pencarian_kereta(data_kereta, role="PENUMPANG"):
	while True:
		print(f"\n----------SELAMAT DATANG {role.upper()}----------")

		daftar_asal = sorted(list(set(row["Stasiun Asal"] for row in data_kereta)))
		print("\nDaftar Stasiun Asal yang tersedia:")
		for asal in daftar_asal:
			print(f"- {asal}")

		stasiun_asal = input("\nMasukkan Stasiun Asal: ").strip()

		data_asal = [
			row
			for row in data_kereta
			if row["Stasiun Asal"].lower() == stasiun_asal.lower()]

		if not data_asal:
			print(f"Maaf, tidak ada jadwal keberangkatan dari '{stasiun_asal}'.")
			if not tanya_lanjut("Apakah masih mau pesan/cek kursi lagi?"):
				break
			continue

		daftar_tujuan = sorted(list(set(row["Stasiun Tujuan"] for row in data_asal)))
		stasiun_tujuan = pilih_dari_daftar("PILIH STASIUN TUJUAN", daftar_tujuan)

		data_rute = [row for row in data_asal if row["Stasiun Tujuan"] == stasiun_tujuan]

		daftar_jadwal = sorted(list(set(f"{row['Tanggal Berangkat']} | Jam {row['Jam Berangkat']}"
					for row in data_rute)))
		jadwal_terpilih = pilih_dari_daftar("PILIH TANGGAL & WAKTU BERANGKAT", daftar_jadwal)

		tanggal_pilih, jam_teks = jadwal_terpilih.split(" | Jam ")

		data_jadwal = [
			row
			for row in data_rute
			if row["Tanggal Berangkat"] == tanggal_pilih
			and row["Jam Berangkat"] == jam_teks]

		while True:
			try:
				harga_maks = int(input("\nMasukkan harga maksimal tiket (Rp): ").strip())
				break
			except ValueError:
				print("Harap masukkan angka nominal harga tanpa titik/koma!")

		kereta_sesuai_budget = [row for row in data_jadwal if row["Harga Tiket"] <= harga_maks]

		if not kereta_sesuai_budget:
			print(f"\nMaaf, tidak tersedia ada kereta untuk jadwal tersebut dengan harga di bawah Rp {harga_maks:,}.")
			if not tanya_lanjut("Apakah masih mau pesan/cek kursi lagi?"):
				break
			continue

		print("\n--- PILIH KERETA & KELAS TERSEDIA ---")
		for idx, k in enumerate(kereta_sesuai_budget, start=1):
			print(f"{idx}. {k['Nama Kereta']} | Kelas: {k['Kelas']} | Harga: Rp {k['Harga Tiket']:,}")

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
		print(f"Rute           : {kereta_final['Stasiun Asal']} -> {kereta_final['Stasiun Tujuan']}")
		print(f"Jadwal         : {kereta_final['Tanggal Berangkat']} pukul {kereta_final['Jam Berangkat']}")
		print(f"Kelas          : {kereta_final['Kelas']}")
		print(f"Harga Tiket    : Rp {kereta_final['Harga Tiket']:,}")
		print("-" * 40)

		if (kereta_final["Status"].lower() == "tersedia"
			and kereta_final["Kursi Tersedia"] > 0):
			print(f"STATUS         : TERSEDIA (Sisa {kereta_final['Kursi Tersedia']} kursi)")
			print("-" * 40)

			while True:
				try:
					jumlah_pesan = int(input("Masukkan jumlah kursi yang mau dipesan (0 untuk batal): "))
					if jumlah_pesan == 0:
						print("Pemesanan dibatalkan.")
						break
					elif 1 <= jumlah_pesan <= kereta_final["Kursi Tersedia"]:
						kereta_final["Kursi Tersedia"] -= jumlah_pesan
						if kereta_final["Kursi Tersedia"] == 0:
							kereta_final["Status"] = "Penuh"
						simpan_semua_data(data_kereta)
						total_bayar = jumlah_pesan * kereta_final["Harga Tiket"]
						print("\nPemesanan berhasil!")
						print(f"Jumlah Kursi Dipesan : {jumlah_pesan} kursi")
						print(f"Total Harga          : Rp {total_bayar:,}")
						print(f"Sisa Kursi Sekarang  : {kereta_final['Kursi Tersedia']} kursi")
						break
					else:
						print(f"Jumlah tidak valid! Maksimal kursi tersedia adalah {kereta_final['Kursi Tersedia']}.")
				except ValueError:
					print("Input harus berupa angka!")
		else:
			print("STATUS         : TIDAK TERSEDIA / PENUH")
			print("-" * 40)

		if not tanya_lanjut("Apakah masih mau pesan kursi lagi?"):
			break


def menu_admin(data_kereta):
	print("-----PANEL ADMIN-----")
	password = input("Masukkan password admin (default: admin123): ")
	if password != "admin123":
		print("Password salah! Akses ditolak.")
		return

	while True:
		print("\nMenu Admin:")
		print("1. Lihat Ringkasan Data Kereta")
		print("2. Tambah Jadwal Kereta Baru")
		print("3. Kembali ke Menu Utama")

		pilihan = input("Pilih menu (1-3): ").strip()
		if pilihan == "1":
			while True:
				print("\n--- PILIH RINGKASAN DATA KERETA ---")
				print("1. Ringkasan kereta yang sudah berlalu")
				print("2. Ringkasan kelas dan kursi tersedia")
				print("3. Ringkasan 5 kereta dengan kursi paling sedikit")
				print("4. Kembali ke Menu Admin")

				sub_pilihan = input("Pilih jenis ringkasan (1-4): ").strip()

				if sub_pilihan == "1":
					tgl_batas = input("Masukkan tanggal batas (YYYY-MM-DD): ").strip()
					kereta_berlalu = [
						row
						for row in data_kereta
						if row["Tanggal Berangkat"] < tgl_batas]
					print(f"\n--- DAFTAR KERETA SEBELUM TANGGAL {tgl_batas} ({len(kereta_berlalu)} jadwal) ---")
					if not kereta_berlalu:
						print("Tidak ada data kereta sebelum tanggal tersebut.")
					else:
						for row in kereta_berlalu:
							print(f"- {row['Nama Kereta']} ({row['Stasiun Asal']} -> {row['Stasiun Tujuan']}) | Tgl: {row['Tanggal Berangkat']} {row['Jam Berangkat']} | Kelas: {row['Kelas']} | Sisa Kursi: {row['Kursi Tersedia']}")

				elif sub_pilihan == "2":
					nama_cari = input("Masukkan nama kereta: ").strip()
					hasil_kereta = [
						row
						for row in data_kereta
						if nama_cari.lower() in row["Nama Kereta"].lower()]
					print(f"\n--- RINGKASAN KERETA '{nama_cari.upper()}' ---")
					if not hasil_kereta:
						print("Nama kereta tidak ditemukan.")
					else:
						for row in hasil_kereta:
							print(f"- {row['Nama Kereta']} ({row['Stasiun Asal']} -> {row['Stasiun Tujuan']}) | Tanggal: {row['Tanggal Berangkat']} | Kelas: {row['Kelas']} | Kursi Tersedia: {row['Kursi Tersedia']} (Awal: {row['Kursi Awal']})")

				elif sub_pilihan == "3":
					urutan_kursi = sorted(data_kereta, key=lambda x: x["Kursi Tersedia"])
					lima_tersedikit = urutan_kursi[:5]
					print("\n--- 5 KERETA DENGAN KURSI PALING SEDIKIT ---")
					for idx, row in enumerate(lima_tersedikit, start=1):
						print(f"{idx}. {row['Nama Kereta']} ({row['Stasiun Asal']} -> {row['Stasiun Tujuan']}) | Tanggal: {row['Tanggal Berangkat']} | Kelas: {row['Kelas']} | Sisa Kursi: {row['Kursi Tersedia']} (Kursi Awal: {row['Kursi Awal']})")

				elif sub_pilihan == "4":
					break
				else:
					print("Pilihan ringkasan tidak valid.")

				if sub_pilihan in ["1", "2", "3"]:
					if not tanya_lanjut("Apakah masih ingin melihat ringkasan lainnya?"):
						break

		elif pilihan == "2":
			while True:
				print("\n--- Tambah Data Kereta Baru ---")
				nama = input("Nama Kereta: ")
				asal = input("Stasiun Asal: ")
				tujuan = input("Stasiun Tujuan: ")
				tanggal = input("Tanggal Berangkat (YYYY-MM-DD): ")
				jam = input("Jam Berangkat (HH:MM): ")
				kelas = input("Kelas (Eksekutif/Bisnis/Ekonomi): ")
				harga = int(input("Harga Tiket: "))
				kursi = int(input("Kursi Tersedia: "))

				data_baru = {
					"S.no.": str(len(data_kereta)),
					"Nama Kereta": nama,
					"Stasiun Asal": asal,
					"Stasiun Tujuan": tujuan,
					"Tanggal Berangkat": tanggal,
					"Jam Berangkat": jam,
					"Kelas": kelas,
					"Harga Tiket": harga,
					"Kursi Tersedia": kursi,
					"Kursi Awal": kursi,
					"Status": "Tersedia" if kursi > 0 else "Penuh",
					"Tahun Operasional": "2026",
					"Umur Kereta Tahun": "0",}
				data_kereta.append(data_baru)
				simpan_semua_data(data_kereta)
				print("Data berhasil ditambahkan!")

				if not tanya_lanjut("Apakah masih ingin menambah jadwal kereta lagi?"):
					break

		elif pilihan == "3":
			break
		else:
			print("Pilihan tidak valid.")


def main():
	data_kereta = muat_data()
	if not data_kereta:
		return

	while True:
		print("\n-----SISTEM PENGECEKAN KURSI KERETA API-----")
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
