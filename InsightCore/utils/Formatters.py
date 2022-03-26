class Formatters(object):
    @classmethod
    def short_str_isk(cls, isk_value: float):
        if isk_value >= 1000000000:
            num = float(isk_value / 1000000000)
            return f"{num:.1f}b"
        elif isk_value >= 1000000:
            num = float(isk_value / 1000000)
            return f"{num:.1f}m"
        else:
            num = float(isk_value / 10000)
            return f"{num:.1f}k"
