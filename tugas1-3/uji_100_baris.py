from dataclasses import dataclass, field


@dataclass
class TugasKuliah:
    kode: str
    judul: str
    bobot: int
    selesai: bool = False
    catatan: list[str] = field(default_factory=list)

    def tandai_selesai(self) -> None:
        self.selesai = True
        self.catatan.append("Status diubah menjadi selesai.")

    def tambah_catatan(self, teks: str) -> None:
        bersih = teks.strip()
        if bersih:
            self.catatan.append(bersih)

    def ringkasan(self) -> str:
        status = "SELESAI" if self.selesai else "PROSES"
        return f"[{self.kode}] {self.judul} ({self.bobot}%) -> {status}"


class ManajerTugas:
    def __init__(self, nama_mahasiswa: str) -> None:
        self.nama_mahasiswa = nama_mahasiswa
        self.daftar_tugas: list[TugasKuliah] = []

    def tambah_tugas(self, tugas: TugasKuliah) -> None:
        self.daftar_tugas.append(tugas)

    def cari_berdasarkan_kode(self, kode: str) -> TugasKuliah | None:
        for item in self.daftar_tugas:
            if item.kode == kode:
                return item
        return None

    def total_bobot_selesai(self) -> int:
        total = 0
        for item in self.daftar_tugas:
            if item.selesai:
                total += item.bobot
        return total

    def total_bobot_keseluruhan(self) -> int:
        total = 0
        for item in self.daftar_tugas:
            total += item.bobot
        return total

    def hitung_persentase_progres(self) -> float:
        total_semua = self.total_bobot_keseluruhan()
        if total_semua == 0:
            return 0.0
        selesai = self.total_bobot_selesai()
        return round((selesai / total_semua) * 100, 2)

    def daftar_belum_selesai(self) -> list[TugasKuliah]:
        hasil: list[TugasKuliah] = []
        for item in self.daftar_tugas:
            if not item.selesai:
                hasil.append(item)
        return hasil

    def cetak_laporan(self) -> None:
        print(f"Laporan Progres: {self.nama_mahasiswa}")
        print("-" * 45)
        for item in self.daftar_tugas:
            print(item.ringkasan())
            for note in item.catatan:
                print(f"   - {note}")
        persen = self.hitung_persentase_progres()
        print("-" * 45)
        print(f"Total bobot selesai: {self.total_bobot_selesai()}/{self.total_bobot_keseluruhan()}")
        print(f"Persentase progres: {persen}%")


def buat_data_awal() -> ManajerTugas:
    manajer = ManajerTugas("Sahla")
    manajer.tambah_tugas(TugasKuliah("T1", "Membaca Pohon Sintaks", 10, True))
    manajer.tambah_tugas(TugasKuliah("T2", "Penjelajah Node Rekursif", 15, True))
    manajer.tambah_tugas(TugasKuliah("T3", "Query AST (.scm)", 15, False))
    manajer.tambah_tugas(TugasKuliah("T4", "Grammar & Test Suite", 20, False))
    manajer.tambah_tugas(TugasKuliah("T5", "Syntax Highlighting", 10, False))
    manajer.tambah_tugas(TugasKuliah("T6", "Pemeriksa Repo Nyata", 20, False))
    manajer.tambah_tugas(TugasKuliah("LAP", "Laporan & Catatan AI", 10, False))
    return manajer


def proses_demo() -> None:
    manajer = buat_data_awal()
    tugas_t1 = manajer.cari_berdasarkan_kode("T1")
    if tugas_t1 is not None:
        tugas_t1.tambah_catatan("Prediksi pohon dan uji ERROR/MISSING sudah dicek.")

    tugas_t2 = manajer.cari_berdasarkan_kode("T2")
    if tugas_t2 is not None:
        tugas_t2.tambah_catatan("Diuji pada file lebih dari 100 baris.")

    belum = manajer.daftar_belum_selesai()
    print(f"Jumlah tugas tersisa: {len(belum)}")
    for item in belum:
        if item.bobot >= 15:
            item.tambah_catatan("Prioritas tinggi karena bobot >= 15.")

    manajer.cetak_laporan()


if __name__ == "__main__":
    proses_demo()