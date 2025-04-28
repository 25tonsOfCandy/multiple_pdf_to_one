import tabula


class TablesToCSVTransformer():
    def __init__(self, tables: tabula.read_pdf, path):
        self.tables = tables
        self.path = path


    def _to_csv(self, table: tabula.read_pdf, name):
        table.to_csv(f'{self.path}/{name}')


    def transform(self, is_return_file_list=False):
        index = 0
        file_list = []
        for table in self.tables:
            table = table.dropna(axis="rows", how="all")

            if table.empty:
                continue
            else:
                self._to_csv(table, f"table_{index}.csv")
                if is_return_file_list:
                    file_list.append(f"{self.path}/table_{index}.csv")
                index += 1

        if is_return_file_list:
            return file_list
