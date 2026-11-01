# Sistem Pemeringkatan Siswa Eligible SNBP
Dokumen: Product Requirements Document (PRD)  
Versi: 1.0 (draft untuk disepakati tim)  
Tanggal: 25 Oktober 2026  
Mata kuliah: Dasar Pemrograman, UAS Praktikum  
Penyusun: Tim 1  
Anggota:  
1. Ghaida Hanan Mutia | J0404261007  
2. Muhammad Rafliza Ardiansa | J0404261041  
3. Muhammad Fadli Al Faruq | J04042611  

---

## 1. Ringkasan Singkat
Aplikasi ini adalah program terminal berbasis Python yang mensimulasikan cara sekolah menentukan siswa kelas 12 yang berstatus eligible (berhak mendaftar SNBP). Aplikasi memeriksa dulu apakah siswa mengikuti TKA, menghitung skor dari nilai rapor semester 1 sampai 5, mengurutkan peringkat, lalu menandai setiap siswa dengan warna: hijau, kuning, atau abu-abu.

Dalam satu kalimat: masukkan data siswa, lalu aplikasi memberi tahu siapa yang eligible, siapa yang kalah poin, dan siapa yang gugur karena tidak ikut TKA.

Aplikasi ini adalah simulasi dengan data fiktif, bukan alat penetapan resmi.

---

## 2. Latar Belakang dan Masalah
SNBP adalah jalur masuk perguruan tinggi negeri berdasarkan prestasi rapor, tanpa ujian tulis. Tidak semua siswa boleh mendaftar. Hanya siswa yang dinyatakan eligible oleh sekolah, yaitu siswa dengan peringkat terbaik di sekolahnya dalam batas kuota. Besar kuota berupa persentase dari jumlah siswa kelas 12 dan bergantung pada akreditasi sekolah. Selain itu, menurut informasi dari media pendidikan, siswa juga wajib mengikuti TKA (Tes Kemampuan Akademik). Aturan ini perlu diverifikasi ke pedoman resmi SNPMB.

Masalahnya: menghitung skor, mengurutkan, dan menentukan batas kuota secara manual untuk puluhan sampai ratusan siswa itu lambat dan rawan salah, terutama ketika ada nilai yang sama persis.

Solusinya: aplikasi terminal yang membaca data siswa (input manual atau file CSV), menghitung otomatis, dan menampilkan hasil berwarna dengan alasan yang jelas.

Mengapa topik ini untuk UAS: topik ini secara alami memakai koleksi data, fungsi, searching dan sorting, serta pengolahan string, sesuai penilaian kompleksitas UAS.

---

## 3. Tujuan dan Ukuran Keberhasilan

| Kode | Tujuan | Ukuran keberhasilan |
|---|---|---|
| T1 | Hasil perhitungan benar | Contoh pada bagian 8 menghasilkan hasil persis sama; dijadikan tes otomatis |
| T2 | Memasukkan banyak data dengan cepat | Impor 150 siswa dari CSV selesai kurang dari 2 detik |
| T3 | Tahan terhadap data salah | File CSV bermasalah tidak membuat program berhenti; setiap kesalahan dilaporkan dengan nomor baris |
| T4 | Mudah dipahami dan dijelaskan | Setiap anggota tim bisa menjelaskan alur lengkap saat tanya jawab |
| T5 | Memenuhi ketentuan UAS | Seluruh butir pada bagian 14 terpenuhi |

Bukan tujuan: menjadi alat resmi, terhubung ke sistem SNPMB atau PDSS, atau menyimpan data siswa sungguhan.

---

## 4. Ruang Lingkup

### Termasuk dalam proyek:
- Profil sekolah: bentuk satuan pendidikan (SMA, SMK, atau MA), nama sekolah, akreditasi, dan pilihan prestasi sebagai acuan pemeringkatan (ya atau tidak).
- Pengaturan mata pelajaran per semester (1 sampai 5) untuk setiap peminatan atau jurusan.
- Kelola data siswa: tambah, lihat, ubah, hapus; setiap siswa terhubung ke satu jurusan.
- Input nilai rapor per mata pelajaran per semester, status TKA (ikut atau tidak ikut), dan prestasi (deskripsi dan tingkat) bila diaktifkan.
- Impor banyak siswa sekaligus dari file CSV, dengan template otomatis per jurusan, serta file CSV prestasi terpisah.
- Pemeriksaan TKA, penghitungan skor, pemeringkatan, penentuan kuota, dan pewarnaan status.
- Pencarian dan filter

### Tidak termasuk:
- Tampilan grafis (GUI) dan database (DBMS); keduanya dilarang oleh ketentuan UAS.
- Koneksi internet atau integrasi dengan sistem resmi.
- Data siswa sungguhan; seluruh demo memakai data fiktif.
- Nilai TKA; yang dicatat hanya ikut atau tidak ikut.
- Verifikasi bukti prestasi (sertifikat atau piagam); aplikasi mempercayai isian operator.
- Prestasi di bawah tingkat kabupaten/kota, misalnya tingkat sekolah atau kecamatan.
- Status TKA selain ikut dan tidak ikut.
- Login banyak pengguna.

---

## 5. Pengguna dan Skenario

### Pengguna:
- Operator sekolah (misalnya guru BK atau tata usaha): Pengguna utama: memasukkan data dan membaca hasil.
- Penguji (dosen atau asisten praktikum): Menilai demo dan kualitas projek.

### User Stories:
- **US-1**: Sebagai Operator, saya ingin mengimpor data siswa dari satu file CSV agar tidak perlu mengetik satu per satu.
- **US-2**: Sebagai Operator, saya ingin melihat daftar berwarna lengkap dengan peringkat agar cepat tahu siapa yang eligible.
- **US-3**: Sebagai Operator, saya ingin membaca alasan status seorang siswa agar bisa menjelaskan hasilnya ke siswa atau orang tua.
- **US-4**: Sebagai Operator, saya ingin mencoba skenario berbeda (misalnya akreditasi berubah) agar tahu dampaknya sebelum keputusan diambil.
- **US-5**: Sebagai Penguji, saya ingin melihat instalasi, demo, dan algoritma yang ditulis sendiri agar dapat menilai pemahaman tim.

---

## 6. Istilah Penting (untuk Orang Awam)
- **SNBP**: Seleksi masuk PTN lewat prestasi rapor, tanpa ujian tulis.
- **Eligible**: Berhak mendaftar SNBP karena masuk peringkat dalam kuota sekolah.
- **Kuota**: Jumlah maksimal siswa eligible di satu sekolah.
- **Akreditasi**: Peringkat mutu sekolah (A, B, C); memengaruhi persentase kuota.
- **TKA**: Tes Kemampuan Akademik; keikutsertaannya menjadi syarat eligible.
- **Rapor**: Buku nilai siswa per semester.
- **Peminatan atau jurusan**: Kelompok siswa di sekolah (misalnya IPA, IPS, atau Bahasa); tiap jurusan punya daftar mata pelajaran sendiri.
- **Prestasi**: Pencapaian siswa di sekolah yang dicatat dengan deskripsi dan tingkat (kabupaten/kota, provinsi, nasional, atau internasional); hanya dipakai jika sekolah mengaktifkannya.
- **Poin prestasi**: Angka tambahan pada skor, dihitung dari tingkat tiap prestasi dan dibatasi maksimal.
- **Skor akhir**: Rata-rata nilai rapor semester 1 sampai 5, ditambah poin prestasi bila diaktifkan, yang dipakai untuk peringkat.
- **CSV**: File tabel sederhana (bisa dibuat di Excel) berisi data siswa.
- **CRUD**: Empat operasi dasar data: tambah, lihat, ubah, hapus.
- **Simulasi**: Perhitungan percobaan, bukan keputusan resmi.

---

## 7. Aturan Bisnis (Inti Sistem)
- **BR-01**: Status TKA hanya dua: *ikut* atau *tidak ikut*. Wajib diisi untuk setiap siswa; tidak ada status lain.
- **BR-02**: TKA diperiksa lebih dulu. Siswa yang tidak ikut TKA langsung ditandai abu-abu dan skornya tidak dihitung. Tanpa TKA, siswa tidak bisa eligible, berapa pun nilai rapornya.
- **BR-03**: Skor semester = rata-rata semua nilai mata pelajaran pada semester itu (daftar mapel mengikuti jurusan siswa). Skor rapor = rata-rata skor semester 1 sampai 5. Skor akhir = skor rapor, ditambah poin prestasi jika diaktifkan (BR-11), dibulatkan 2 angka desimal. Nilai rapor berupa bilangan bulat, sedangkan poin prestasi boleh berkoma. Karena memakai rata-rata, jurusan dengan jumlah mapel berbeda tetap dinilai adil.
- **BR-04**: Siswa yang ikut TKA diurutkan dari skor akhir tertinggi. Skor dibandingkan pada ketelitian 2 desimal.
- **BR-05**: Jika skor sama persis:
  - (a) skor semester 5 tertinggi menang, lalu semester 4, 3, 2, 1;
  - (b) jika masih sama, urutan abjad nama A ke Z;
  - (c) jika nama pun sama persis, ID terkecil.
  Aturan abjad memastikan selalu ada satu pemenang, tidak ada yang seri.
- **BR-06**: Kuota = persentase kuota × jumlah seluruh siswa kelas 12 (termasuk yang tidak ikut TKA), dibulatkan ke bawah. Persentase per akreditasi disimpan di pengaturan, bukan di kode.
- **BR-07**: Siswa yang ikut TKA dan berperingkat dalam kuota ditandai hijau beserta peringkatnya. Yang berperingkat di luar kuota ditandai kuning (kalah poin). Peringkat juga ditampilkan untuk kuning agar terlihat selisihnya.
- **BR-08**: Jika siswa yang ikut TKA lebih sedikit dari kuota, semuanya hijau dan layar menampilkan "kuota terisi X dari Y". Kuota tidak dipaksa penuh.
- **BR-09**: Data rapor harus lengkap sesuai jurusan siswa: semester 1 sampai 5, semua mata pelajaran yang terdaftar untuk jurusan dan semester itu, nilai bilangan bulat 0 sampai 100. Baris yang tidak lengkap atau tidak valid ditolak saat impor dan dilaporkan. Tidak ada status "data belum lengkap".
- **BR-10**: Semua hasil diberi label SIMULASI. Bukan penetapan resmi.
- **BR-11**: Pilihan prestasi di profil sekolah menentukan apakah prestasi dipakai. Jika ya, setiap prestasi siswa dicatat dengan deskripsi (teks) dan tingkat (kabupaten/kota, provinsi, nasional, atau internasional; minimal kabupaten/kota). Poin per prestasi: kabupaten/kota 0,25; provinsi 0,50; nasional 1,00; internasional 1,50. Total poin seorang siswa dibatasi maksimal 2,00, lalu ditambahkan ke skor rapor. Jika tidak, prestasi diabaikan dan tidak diminta. Bobot dan batas disimpan di pengaturan. Satu siswa mencatat maksimal 5 prestasi. Rapor tetap dominan: selisih rapor lebih dari 2 poin tidak bisa dibalik oleh prestasi.
- **BR-12**: Setiap siswa terhubung ke satu jurusan yang sudah terdaftar di pengaturan mata pelajaran. ID siswa dibuat otomatis, dan siswa dianggap ganda jika nama dan kelasnya sama. Jurusan menentukan mata pelajaran yang harus diisi. Jurusan tidak dikenal ditolak.

### Arti Warna:
- **Abu-abu**: Tidak ikut TKA, otomatis tidak eligible. Peringkat: Tidak ada (tanda "—").
- **Hijau**: Ikut TKA dan lolos kuota (eligible). Peringkat: Ditampilkan.
- **Kuning**: Ikut TKA tetapi kalah poin, di luar kuota. Peringkat: Ditampilkan.

---

## 8. Contoh Perhitungan Lengkap

### Contoh 1 (Tanpa Prestasi):
Sekolah fiktif berakreditasi A, persentase kuota 40%, e-rapor dan prestasi tidak diaktifkan, jumlah siswa kelas 12 ada 10 orang. Kuota = 40% × 10 = 4.

| Siswa (fiktif) | TKA | Skor akhir | Peringkat | Status |
|---|---|---|---|---|
| Alya | Tidak ikut | tidak dihitung | — | Abu-abu |
| Bima | Ikut | 92,40 | 1 | Hijau |
| Citra | Ikut | 91,80 | 2 | Hijau |
| Dina | Tidak ikut | tidak dihitung | — | Abu-abu |
| Eka | Ikut | 90,25 | 3 | Hijau |
| Farhan | Ikut | 88,60 | 4 | Hijau |
| Gita | Ikut | 88,60 | 5 | Kuning |
| Hana | Ikut | 85,10 | 6 | Kuning |
| Indra | Ikut | 83,40 | 7 | Kuning |
| Joko | Ikut | 80,00 | 8 | Kuning |

Cara membacanya:
1. Alya dan Dina tidak ikut TKA, jadi langsung abu-abu dan tidak dihitung.
2. Delapan siswa lainnya dihitung skornya dan diurutkan.
3. Empat teratas masuk kuota, jadi hijau.
4. Farhan dan Gita punya skor sama persis (skor semester 5 mereka juga sama). Aturan BR-05 menentukan urutan abjad: F sebelum G, sehingga Farhan hijau dan Gita kuning.
5. Sisanya kuning karena kalah poin.

Dasar kuota adalah seluruh siswa kelas 12 (10 siswa). Jika dihitung hanya dari yang ikut TKA, kuotanya 3 dan Farhan menjadi kuning. Contoh ini dijadikan tes otomatis.

### Contoh 2 (Dengan Prestasi Aktif):
Sekolah memilih "ya" untuk prestasi. Bobot: kabupaten/kota 0,25; provinsi 0,50; nasional 1,00; internasional 1,50; batas total 2,00.

| Siswa (fiktif) | Skor rapor | Prestasi | Poin prestasi | Skor akhir | Urutan |
|---|---|---|---|---|---|
| Fani | 93,00 | tidak ada | 0 | 93,00 | 1 |
| Eko | 90,00 | 1 nasional | 1,00 | 91,00 | 2 |
| Dara | 90,50 | tidak ada | 0 | 90,50 | 3 |
| Gani | 89,00 | 1 kab/kota & 1 prov | 0,75 | 89,75 | 4 |

---

## 9. Alur Kerja Sistem
1. Operator melengkapi profil sekolah.
2. Operator mengisi mata pelajaran per semester (1 s.d. 5) untuk setiap jurusan.
3. Operator mengisi data siswa.
4. Sistem memeriksa data. ID dibuat otomatis.
5. Sistem memisahkan siswa berdasarkan TKA.
6. Sistem menghitung skor rapor siswa yang ikut TKA + poin prestasi jika diaktifkan.
7. Sistem mengurutkan siswa dengan algoritma merge sort buatan sendiri (BR-04, BR-05).
8. Sistem menghitung kuota (BR-06).
9. Sistem memberi peringkat dan menandai hijau atau kuning.
10. Hasil ditampilkan; operator dapat mencari.

---

## 10. Kebutuhan Fungsional (FR)
- **FR-01**: Mengatur profil sekolah: bentuk satuan pendidikan (SMA, SMK, MA), nama, akreditasi, status e-rapor, dan pilihan prestasi (ya atau tidak) [Wajib]
- **FR-02**: Mengatur mata pelajaran per semester (1 sampai 5) untuk setiap peminatan atau jurusan: tambah dan hapus jurusan, tambah dan hapus mapel, serta salin mapel dari semester atau jurusan lain [Wajib]
- **FR-03**: Tambah, lihat, ubah, dan hapus data siswa (CRUD), termasuk jurusannya [Wajib]
- **FR-04**: Input nilai rapor per mata pelajaran per semester, status TKA, dan prestasi (deskripsi dan tingkat, maksimal 5 per siswa) jika diaktifkan [Wajib]
- **FR-05**: Impor banyak siswa dari CSV: template otomatis per jurusan, deteksi pemisah dan encoding, pratinjau hasil pemeriksaan, pilihan penanganan siswa ganda (lewati, timpa, batal), dan file laporan baris error; prestasi diimpor dari file CSV terpisah [Wajib]
- **FR-06**: Memproses TKA, skor, pengurutan, kuota, dan status sesuai bagian 7 [Wajib]
- **FR-07**: Menampilkan hasil berwarna lengkap dengan peringkat dan label SIMULASI [Wajib]
- **FR-08**: Mencari dan memfilter siswa berdasarkan nama, kelas, jurusan, dan status warna [Wajib]
- **FR-09**: Detail siswa berisi rincian skor per semester, poin prestasi per tingkat, dan kalimat penjelasan status [Penting]
- **FR-10**: Simulasi "bagaimana jika" (ubah akreditasi, e-rapor, pilihan prestasi, atau status TKA seorang siswa) dan tampilkan siapa yang berubah status [Penting]
- **FR-12**: Pembuat data fiktif dengan nilai acak tetap (seed): jurusan, mata pelajaran, siswa, dan prestasi untuk demo dan pengujian [Penting]
- **FR-13**: Menu benchmark: merge sort buatan sendiri dibandingkan dengan sorted() bawaan [Opsional]

---

## 11. Kebutuhan Non-Fungsional (NFR)
- **Platform**: Terminal, tanpa GUI dan tanpa DBMS.
- **Penyimpanan**: Data di file (JSON dan CSV); penulisan aman: tulis ke file sementara lalu ganti, plus cadangan .bak.
- **Keandalan**: Input salah tidak membuat program berhenti; tampilkan pesan jelas dan ulangi pertanyaan; Ctrl+C ditangani tanpa pesan error teknis.
- **Performa**: 150 siswa diproses kurang dari 1 detik; 5.000 siswa tetap responsif.
- **Privasi**: Hanya data fiktif; folder impor dimasukkan ke .gitignore.
- **Kemudahan dijalankan**: Instalasi bersih: clone, buat venv, pip install, python main.py.
- **Kualitas kode**: Modular, memakai type hints dan docstring, dilengkapi tes otomatis dengan pytest.
- **Tampilan**: Library rich untuk tabel dan warna; konsisten: 0 = kembali, Enter kosong = lewati.

---

## 12. Data dan Format File
- `data/school.json`
- `data/config.json`
- `data/students.json`
- `data/import/`
- `generator/make_students.py`

Format CSV Siswa: `nama,kelas,jurusan,sem1_MTK,sem1_BIN,...,sem5_ING,tka_status`
Format CSV Prestasi: `nama,kelas,deskripsi,tingkat`

---

## 13. Alur Pengguna dan Tampilan
Menu utama: 1..9
Alur impor CSV: pilih jurusan -> buat template -> pratinjau -> penanganan ganda -> konfirmasi -> tulis laporan baris error jika ada.

---

## 14. Pemetaan ke Ketentuan UAS
- Aplikasi menarik dengan Python (rich)
- Kelompok maksimal 3 orang
- Topik konfirmasi ke dosen/asprak
- JSON dan CSV
- CRUD siswa, nilai, TKA, sekolah, mapel per jurusan
- Koleksi: list, dict bersarang, set, tuple, Counter
- Fungsi terpisah, satu tugas per fungsi
- Searching dan sorting: pencarian nama, binary search pada daftar terurut, merge sort sendiri
- String: normalisasi nama, parsing CSV dan TKA, format tabel
