import datetime
import os


def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')


def format_rupiah(angka):
    return f'Rp {angka:,.0f}'.replace(',', '.')


def tampilkan_menu(daftar_menu):
    print('\n--- DAFTAR MENU ---')
    for kode, item in daftar_menu.items():
        print(f"{kode}. {item['nama']:<27} {format_rupiah(item['harga']):>12}")
    print('-' * 45)


def main():
    keranjang = []
    nama_toko = 'MIE AYAM SAFIRNA'
    alamat_toko = 'Jl. Sudirman No. 123, Jakarta'

    daftar_menu = {
        '1': {'nama': 'Mie Ayam Original', 'harga': 10000},
        '2': {'nama': 'Mie Ayam Bakso', 'harga': 13000},
        '3': {'nama': 'Teh Tawar Panas/Dingin', 'harga': 2000},
        '4': {'nama': 'Teh Manis Panas', 'harga': 3000},
        '5': {'nama': 'Teh Manis Dingin', 'harga': 4000},
        '6': {'nama': 'Air Jeruk Panas/Dingin', 'harga': 4000},
    }

    bersihkan_layar()
    print('=' * 45)
    print(f'{nama_toko:^45}')
    print(f'{alamat_toko:^45}')
    print('=' * 45)
    tampilkan_menu(daftar_menu)

    # 1. Input Pesanan Berdasarkan Nomor Menu
    while True:
        print('\n(Ketik nomor menu 1-6, atau "s" untuk bayar)')
        pilihan = input('Pilih Menu  : ').strip()

        if pilihan.lower() == 's':
            if not keranjang:
                print('Keranjang masih kosong! Pilih minimal 1 menu.')
                continue
            break

        if pilihan not in daftar_menu:
            print('Nomor menu tidak tersedia! Silakan pilih 1 sampai 6.')
            continue

        try:
            jumlah = int(input('Jumlah Beli : '))
            if jumlah <= 0:
                print('Jumlah harus lebih dari 0!')
                continue
        except ValueError:
            print('Input jumlah harus berupa angka!')
            continue

        menu_terpilih = daftar_menu[pilihan]
        nama_barang = menu_terpilih['nama']
        harga = menu_terpilih['harga']
        subtotal_item = harga * jumlah

        # Gabungkan jumlah jika menu yang sama sudah ada di keranjang
        sudah_ada = False
        for item in keranjang:
            if item['nama'] == nama_barang:
                item['jumlah'] += jumlah
                item['subtotal'] += subtotal_item
                sudah_ada = True
                break

        if not sudah_ada:
            keranjang.append({
                'nama': nama_barang,
                'harga': harga,
                'jumlah': jumlah,
                'subtotal': subtotal_item,
            })

        print(
            f'-> Ditambahkan: {nama_barang} ({jumlah}x) ='
            f' {format_rupiah(subtotal_item)}'
        )

    # 2. Perhitungan Total, Diskon, dan Pajak
    subtotal = sum(item['subtotal'] for item in keranjang)

    print('\n' + '=' * 45)
    print(f'Subtotal Pesanan : {format_rupiah(subtotal)}')

    try:
        persen_diskon = float(input('Diskon (%) [0 jika tidak ada] : ') or 0)
        persen_pajak = float(input('PPN (%)    [0 jika tidak ada] : ') or 0)
    except ValueError:
        print('Input tidak valid, diskon & pajak diatur ke 0%.')
        persen_diskon = 0
        persen_pajak = 0

    nominal_diskon = subtotal * (persen_diskon / 100)
    setelah_diskon = subtotal - nominal_diskon
    nominal_pajak = setelah_diskon * (persen_pajak / 100)
    total_akhir = setelah_diskon + nominal_pajak

    print('-' * 45)
    print(f'TOTAL BAYAR      : {format_rupiah(total_akhir)}')
    print('-' * 45)

   # 3. Pembayaran & Kembalian
    while True:
        try:
            # Menghapus titik/koma jika kasir mengetik "20.000" atau "20,000"
            input_uang = (
                input('Uang Tunai Pembeli : Rp ')
                .replace('.', '')
                .replace(',', '')
            )
            uang_bayar = float(input_uang)
            if uang_bayar < total_akhir:
                kurang = total_akhir - uang_bayar
                print(f'Uang kurang {format_rupiah(kurang)}! Silakan input ulang.')
            else:
                kembalian = uang_bayar - total_akhir
                break
        except ValueError:
            print('Masukkan nominal angka yang valid!')

    # 4. Cetak Struk
    waktu_sekarang = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    bersihkan_layar()

    print('=' * 45)
    print(f'{nama_toko:^45}')
    print(f'{alamat_toko:^45}')
    print(f'Waktu: {waktu_sekarang}')
    print('=' * 45)

    for item in keranjang:
        print(f"{item['nama']}")
        detail = f"  {item['jumlah']} x {format_rupiah(item['harga'])}"
        print(f"{detail:<28} {format_rupiah(item['subtotal']):>16}")

    print('-' * 45)
    print(f"{'Subtotal':<25} {format_rupiah(subtotal):>19}")
    if persen_diskon > 0:
        print(
            f"{f'Diskon ({persen_diskon:g}%)':<25}"
            f' -{format_rupiah(nominal_diskon):>18}'
        )
    if persen_pajak > 0:
        print(
            f"{f'PPN ({persen_pajak:g}%)':<25}"
            f' +{format_rupiah(nominal_pajak):>18}'
        )
    print('=' * 45)
    print(f"{'TOTAL':<25} {format_rupiah(total_akhir):>19}")
    print(f"{'TUNAI':<25} {format_rupiah(uang_bayar):>19}")
    print(f"{'KEMBALI':<25} {format_rupiah(kembalian):>19}")
    print('=' * 45)
    print(f"{'Terima Kasih Telah Berkunjung!':^45}")
    print('=' * 45)

    # Tambahkan baris ini agar layar tidak langsung tertutup:
    input('\nTekan ENTER untuk keluar...')
    # 4. Cetak Struk
    waktu_sekarang = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    bersihkan_layar()

    print('=' * 45)
    print(f'{nama_toko:^45}')
    print(f'{alamat_toko:^45}')
    print(f'Waktu: {waktu_sekarang}')
    print('=' * 45)

    for item in keranjang:
        print(f"{item['nama']}")
        detail = f"  {item['jumlah']} x {format_rupiah(item['harga'])}"
        print(f"{detail:<28} {format_rupiah(item['subtotal']):>16}")

    print('-' * 45)
    print(f"{'Subtotal':<25} {format_rupiah(subtotal):>19}")
    if persen_diskon > 0:
        print(
            f"{f'Diskon ({persen_diskon:g}%)':<25}"
            f' -{format_rupiah(nominal_diskon):>18}'
        )
    if persen_pajak > 0:
        print(
            f"{f'PPN ({persen_pajak:g}%)':<25}"
            f' +{format_rupiah(nominal_pajak):>18}'
        )
    print('=' * 45)
    print(f"{'TOTAL':<25} {format_rupiah(total_akhir):>19}")
    print(f"{'TUNAI':<25} {format_rupiah(uang_bayar):>19}")
    print(f"{'KEMBALI':<25} {format_rupiah(kembalian):>19}")
    print('=' * 45)
    print(f"{'Terima Kasih Telah Berkunjung!':^45}")
    print('=' * 45)


if __name__ == '__main__':
    main()