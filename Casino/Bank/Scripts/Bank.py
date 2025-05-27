class ChipData:
    chip5_chips = []
    chip10_chips = []
    chip50_chips = []
    chip100_chips = []
    chip500_chips = []
    chip1000_chips = []
    chip5000_chips = []

    chip_config_data = [
        {"value": 5, "count": 1, "list": chip5_chips},
        {"value": 10, "count": 50, "list": chip10_chips},
        {"value": 50, "count": 25, "list": chip50_chips},
        {"value": 100, "count": 25, "list": chip100_chips},
        {"value": 500, "count": 20, "list": chip500_chips},
        {"value": 1000, "count": 10, "list": chip1000_chips},
        {"value": 5000, "count": 5, "list": chip5000_chips}
    ]

    @staticmethod
    def get_all_chips():
        return (
            ChipData.chip5_chips +
            ChipData.chip10_chips +
            ChipData.chip50_chips +
            ChipData.chip100_chips +
            ChipData.chip500_chips +
            ChipData.chip1000_chips +
            ChipData.chip5000_chips
        )

    @staticmethod
    def chip_configs():
        return ChipData.chip_config_data

    @staticmethod
    def update_chip_count(value, new_count):
        for config in ChipData.chip_config_data:
            if config["value"] == value:
                config["count"] = new_count
                break