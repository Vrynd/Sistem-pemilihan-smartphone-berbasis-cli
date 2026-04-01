class CalculationMethod:
    # Initialize CalculationMethod object
    def __init__(self, smartphones: list, criteria_list: list):
        self.smartphones = smartphones
        self.criteria_list = criteria_list

    # Create decision matrix from smartphone data
    def create_decision_matrix(self) -> list:
        matrix = []
        for sp in self.smartphones:
            row = []
            for cr in self.criteria_list:
                row.append(sp.get_nilai(cr.kode))
            matrix.append(row)
        return matrix

    # Normalize decision matrix (cost: min/Xij, benefit: Xij/max)
    def normalization(self) -> list:
        matrix = self.create_decision_matrix()
        if not matrix:
            return []

        num_criteria = len(self.criteria_list)
        num_alternatives = len(matrix)

        col_min = []
        col_max = []
        for j in range(num_criteria):
            col_values = [matrix[i][j] for i in range(num_alternatives)]
            col_min.append(min(col_values))
            col_max.append(max(col_values))

        normalized = []
        for i in range(num_alternatives):
            row = []
            for j in range(num_criteria):
                xij = matrix[i][j]
                criteria_type = self.criteria_list[j].jenis

                if criteria_type == "cost":
                    rij = col_min[j] / xij if xij != 0 else 0
                else:
                    rij = xij / col_max[j] if col_max[j] != 0 else 0

                row.append(round(rij, 4))
            normalized.append(row)

        return normalized

    # Calculate preference values (Vi) for each alternative
    def calculate_preferences(self) -> list:
        normalized = self.normalization()
        if not normalized:
            return []

        results = []
        for i, sp in enumerate(self.smartphones):
            vi = 0
            for j, cr in enumerate(self.criteria_list):
                wj = cr.bobot / 100.0
                rij = normalized[i][j]
                vi += wj * rij

            vi_percent = round(vi * 100, 4)

            results.append({
                "kode": sp.kode,
                "nama": sp.nama,
                "nilai_vi": vi_percent,
            })

        return results

    # Rank alternatives by preference value (highest first)
    def ranking(self) -> list:
        result = self.calculate_preferences()
        result_sorted = sorted(result, key=lambda x: x["nilai_vi"], reverse=True)
        for idx, item in enumerate(result_sorted, start=1):
            item["ranking"] = idx

        return result_sorted
