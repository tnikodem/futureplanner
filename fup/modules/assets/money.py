from fup.core.module import AssetModule


# TODO change into Giro account with dispo credit, negative interest rate if above > 50k or 100k
class Money(AssetModule):
    def next_year(self):
        self.df_row["money"] = self.money_value
