import re


def persian_numbers(string):
    latins = range(ord("0"), ord("9") + 1)
    gap = ord("۴") - ord("4")
    return "".join([chr(gap + ord(l)) if ord(l) in latins else l for l in string])


class ParsedAge:
    def __init__(self, raw):
        self.raw = raw
        self.parsed = self._parse()

    @property
    def latin(self):
        if self.parsed is None:
            return ""
        elif isinstance(self.parsed, int):
            return self.parsed
        elif isinstance(self.parsed, list):
            return " ".join([str(l) for l in self.parsed])
        raise NotImplementedError()

    @property
    def persian(self):
        if self.parsed is None:
            return ""
        if isinstance(self.parsed, int):
            return persian_numbers(str(self.parsed))
        else:
            return persian_numbers(self.raw)

    def _parse(self):
        if self.raw == "نامشخص":
            return None
        try:
            return int(self.raw)
        except ValueError:
            two_opts = self.raw.split("یا")
            try:
                assert len(two_opts) == 2
                return [int(two_opts[0]), "or", int(two_opts[1])]
            except AssertionError:
                pass
            two_opts = self.raw.split("تا")
            try:
                assert len(two_opts) == 2
                return [int(two_opts[0]), "to", int(two_opts[1])]
            except AssertionError:
                pass
            try:
                probable_age_l = re.findall(r"احتمالا (\d+)", self.raw)
                assert len(probable_age_l) == 1
                return ["Probably", probable_age_l[0]]
            except Exception:
                pass
            try:
                probable_age_l = re.findall(r"احتمالا زیر (\d+)", self.raw)
                assert len(probable_age_l) == 1
                return ["Probably", "under", probable_age_l[0]]
            except Exception:
                pass
            try:
                probable_age_l = re.findall(r"زیر (\d+)", self.raw)
                assert len(probable_age_l) == 1
                return ["Under", int(probable_age_l[0])]
            except Exception:
                raise NotImplementedError()
