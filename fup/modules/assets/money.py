from fup.core.module import AssetModule


class Money(AssetModule):
    def add_info(self, info_dict):
        info_dict["money"] = self.money_value

