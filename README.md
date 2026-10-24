# CUTSAPAY VPN — Izin IP GitHub

Repo SC: **jmsstore/cutsapay**. SC menggunakan daftar izin IPv4 di
[permission/izin-ip](https://github.com/jmsstore/permission/blob/main/izin-ip).

## OS yang Didukung

- Ubuntu 20.04, 22.04, 24.04, 26.04, dan 26.10.
- Debian 12 dan 13, amd64/x86_64 dengan systemd.

## Persiapan Sebelum Install

- VPS baru/bersih, login sebagai root, domain DNS A menuju IPv4 VPS, dan email SSL.
- Cloudflare DNS only; buka TCP 80 dan 443.
- Daftarkan IPv4 publik sebenarnya pada repo **jmsstore/permission**, file **izin-ip**:

```text
### Nama YYYY-MM-DD IP-VPS
```

Ganti tanggal dan IP dengan data sebenarnya. Nama boleh memakai spasi.
Tanggal berlaku sampai akhir hari UTC+7. `lifetime` dapat menggantikan tanggal.
Hapus baris contoh yang salah. IP tidak terdaftar, kedaluwarsa, atau file salah
format akan ditolak. Pemeriksaan berkala berjalan setiap lima menit.
Gangguan jaringan dapat memakai cache izin aktif maksimal 24 jam, tetap dibatasi
tanggal berakhir. Instalasi baru wajib berhasil memeriksa daftar online.
Jika izin tidak aktif, layanan VPN yang dikelola dihentikan; SSH root/admin tetap
tersedia dan data akun tidak dihapus. Pemulihan izin menyalakan kembali layanan
yang sebelumnya dihentikan oleh pemeriksa izin.

## Perintah Instalasi

```bash
apt-get update && apt-get install -y curl ca-certificates &&
curl -4 -fsSL https://raw.githubusercontent.com/jmsstore/cutsapay/main/setup.sh -o /root/cutsapay-setup.sh &&
chmod +x /root/cutsapay-setup.sh &&
/root/cutsapay-setup.sh
```

Setelah berhasil, installer dan source sementara dihapus otomatis. Jika gagal,
keduanya disimpan untuk pemeriksaan. Jalankan `menu` untuk membuka SC.
Update Script memakai repo ini dan kembali ke menu otomatis.
Versi ini untuk pemasangan baru. Perpindahan dari SC gratis/versi website lama
memerlukan aktivasi terpisah. Updater gratis lama akan menolak protokol baru
sebelum menulis file; akun dan konfigurasi lama tidak diganti diam-diam.

Instalasi berhasil dilaporkan melalui website ke bot khusus admin, berisi IP,
domain, nama VPS, versi dan waktu. Password dan Auth Key tidak dikirim.
Kegagalan laporan/notifikasi tidak menggagalkan instalasi VPN.
Bot, PPOB, dan penyimpanan backup dikonfigurasi dengan akun masing-masing.
File setup.sh adalah executable Linux ELF amd64, meskipun memakai ekstensi .sh.
GitHub menampilkan file sebagai binary, bukan source Bash. Jalankan langsung
setelah chmod +x; jangan menjalankannya dengan bash setup.sh. Kode runtime
lainnya berada dalam arsip bersandi dan dibuka otomatis oleh installer.
Binary tetap bisa dianalisis oleh pemilik VPS; ini bukan DRM.
