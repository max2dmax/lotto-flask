# lotto_engine.py
import hashlib

class LottoEngine:
    """
    Deterministic lottery number generator.
    Same inputs => same outputs.
    """

    def __init__(self, normal_ball_max=69, normal_ball_count=5, power_ball_max=26):
        self.normal_ball_max = normal_ball_max
        self.normal_ball_count = normal_ball_count
        self.power_ball_max = power_ball_max

    def _hash_bytes(self, text):
        # Stable, repeatable hash
        return hashlib.sha256(text.encode("utf-8")).digest()

    def _normalize(self, first, last, payload):
        first = (first or "").strip().lower()
        last = (last or "").strip().lower()
        payload = (payload or "").strip()
        return f"{first}|{last}|{payload}"

    def generate(self, first, last, payload):
        seed = self._normalize(first, last, payload)
        digest = self._hash_bytes(seed)

        # Turn digest into a big integer we can consume
        big = int.from_bytes(digest, "big")

        # Generate unique normal balls
        normals = set()
        x = big
        while len(normals) < self.normal_ball_count:
            x = (x * 1103515245 + 12345) & ((1 << 64) - 1)  # simple LCG step
            n = (x % self.normal_ball_max) + 1
            normals.add(n)

        normals = sorted(normals)

        # Powerball derived from a different slice
        digest2 = self._hash_bytes(seed + "|power")
        power_big = int.from_bytes(digest2, "big")
        power = (power_big % self.power_ball_max) + 1

        return {
            "seed_preview": seed[:80] + ("..." if len(seed) > 80 else ""),
            "numbers": normals,
            "powerball": power
        }