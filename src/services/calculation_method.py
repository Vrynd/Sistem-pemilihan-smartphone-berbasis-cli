"""
Modul perhitungan metode Simple Additive Weighting (SAW).
Berisi logika inti: normalisasi matriks dan perhitungan nilai preferensi.
"""


class SAWCalculator:
    """
    Kalkulator metode SAW (Simple Additive Weighting).

    Langkah perhitungan:
    1. Buat matriks keputusan dari data alternatif
    2. Normalisasi matriks (cost: min/Xij, benefit: Xij/max)
    3. Hitung nilai preferensi Vi = Σ(Wj × rij)
    4. Ranking berdasarkan Vi tertinggi
    """

    def __init__(self, smartphones: list, kriteria_list: list):
        """
        Args:
            smartphones: List objek Smartphone (alternatif)
            kriteria_list: List objek Kriteria
        """
        self.smartphones = smartphones
        self.kriteria_list = kriteria_list

    def buat_matriks_keputusan(self) -> list:
        """
        Membuat matriks keputusan (X) dari data smartphone.

        Returns:
            List of list: matriks [alternatif][kriteria]
            Contoh: [[1, 2, 1, 3, 2], [2, 2, 2, 4, 3], ...]
        """
        matriks = []
        for sp in self.smartphones:
            baris = []
            for kr in self.kriteria_list:
                baris.append(sp.get_nilai(kr.kode))
            matriks.append(baris)
        return matriks

    def normalisasi(self) -> list:
        """
        Melakukan normalisasi matriks keputusan.

        Rumus:
        - Cost:    rij = min(kolom j) / Xij
        - Benefit: rij = Xij / max(kolom j)

        Returns:
            List of list: matriks ternormalisasi [alternatif][kriteria]
        """
        matriks = self.buat_matriks_keputusan()

        if not matriks:
            return []

        jumlah_kriteria = len(self.kriteria_list)
        jumlah_alternatif = len(matriks)

        # Hitung min dan max per kolom (kriteria)
        min_kolom = []
        max_kolom = []
        for j in range(jumlah_kriteria):
            nilai_kolom = [matriks[i][j] for i in range(jumlah_alternatif)]
            min_kolom.append(min(nilai_kolom))
            max_kolom.append(max(nilai_kolom))

        # Normalisasi
        matriks_normal = []
        for i in range(jumlah_alternatif):
            baris = []
            for j in range(jumlah_kriteria):
                xij = matriks[i][j]
                jenis = self.kriteria_list[j].jenis

                if jenis == "cost":
                    # Cost: min / Xij
                    rij = min_kolom[j] / xij if xij != 0 else 0
                else:
                    # Benefit: Xij / max
                    rij = xij / max_kolom[j] if max_kolom[j] != 0 else 0

                baris.append(round(rij, 4))
            matriks_normal.append(baris)

        return matriks_normal

    def hitung_preferensi(self) -> list:
        """
        Menghitung nilai preferensi (Vi) untuk setiap alternatif.

        Rumus: Vi = Σ(Wj × rij)
        Di mana Wj = bobot kriteria j (dalam desimal), rij = nilai ternormalisasi

        Returns:
            List of dict: [{"kode": "A1", "nama": "...", "nilai_vi": float}, ...]
        """
        matriks_normal = self.normalisasi()

        if not matriks_normal:
            return []

        hasil = []
        for i, sp in enumerate(self.smartphones):
            vi = 0
            for j, kr in enumerate(self.kriteria_list):
                # Bobot dalam persen, konversi ke desimal tidak diperlukan
                # karena kita ingin hasil akhir dalam skala 100
                wj = kr.bobot / 100.0
                rij = matriks_normal[i][j]
                vi += wj * rij

            # Kalikan 100 agar hasilnya dalam skala persentase
            vi_persen = round(vi * 100, 4)

            hasil.append({
                "kode": sp.kode,
                "nama": sp.nama,
                "nilai_vi": vi_persen,
            })

        return hasil

    def ranking(self) -> list:
        """
        Mengurutkan alternatif berdasarkan nilai preferensi (Vi) dari tertinggi.

        Returns:
            List of dict: hasil diurutkan dari Vi tertinggi, dengan tambahan field "ranking"
        """
        hasil = self.hitung_preferensi()

        # Urutkan dari nilai Vi tertinggi
        hasil_sorted = sorted(hasil, key=lambda x: x["nilai_vi"], reverse=True)

        # Tambahkan nomor ranking
        for idx, item in enumerate(hasil_sorted, start=1):
            item["ranking"] = idx

        return hasil_sorted
