class ChipData:
    chip5_chips = []
    chip10_chips = []
    chip50_chips = []
    chip100_chips = []
    chip500_chips = []
    chip1000_chips = []
    chip5000_chips = []

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
        return [
            {"value": 5, "count": 80, "list": ChipData.chip5_chips},
            {"value": 10, "count": 50, "list": ChipData.chip10_chips},
            {"value": 50, "count": 25, "list": ChipData.chip50_chips},
            {"value": 100, "count": 25, "list": ChipData.chip100_chips},
            {"value": 500, "count": 20, "list": ChipData.chip500_chips},
            {"value": 1000, "count": 10, "list": ChipData.chip1000_chips},
            {"value": 5000, "count": 5, "list": ChipData.chip5000_chips}
        ]
