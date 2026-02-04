# lotto_engine.py

class LottoEngine:

    def __init__(self, normal_ball_max=69, normal_ball_count=5, power_ball_max=26):
        self.normal_ball_max = normal_ball_max
        self.normal_ball_count = normal_ball_count
        self.power_ball_max = power_ball_max

    def _normalize(self, first, last, payload):
        first = (first or "").strip().lower()
        last = (last or "").strip().lower()
        payload = (payload or "").strip()
        return f"{first}|{last}|{payload}"

    def _text_to_seed(self, text):
        # Build a stable large integer from the text using char codes + mixing.
        # No hashing. Fully deterministic.
        seed = 0
        for i, ch in enumerate(text):
            c = ord(ch)
            seed = seed * 131 + c + i  # 131 is a common mixing base
            seed &= (1 << 128) - 1     # keep it bounded (portable + stable)
        return seed or 1  # avoid zero seed

    def _next(self, x):
        # A simple PRNG step (LCG variant). Deterministic.
        return (x * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)

    def generate(self, first, last, payload):
        seed_text = self._normalize(first, last, payload)
        x = self._text_to_seed(seed_text)

        # Pull unique "normal" numbers
        normals = set()
        while len(normals) < self.normal_ball_count:
            x = self._next(x)
            n = (x % self.normal_ball_max) + 1
            normals.add(n)

        # Powerball from additional PRNG steps (still no hash)
        x = self._next(x)
        x = self._next(x)
        power = (x % self.power_ball_max) + 1

        return {
            "seed_preview": seed_text[:80] + ("..." if len(seed_text) > 80 else ""),
            "numbers": sorted(normals),
            "powerball": power
        }