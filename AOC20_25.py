from time import perf_counter


class Crypto:
    subject_number = 7
    divisor = 20201227

    def __init__(self, public_key: int) -> None:
        self.public_key = public_key

    def loop_size(self) -> int:
        """Return loopsize for given public key"""
        cur_value = 1
        loops = 0
        while cur_value != self.public_key:
            cur_value = cur_value * self.subject_number
            cur_value = cur_value % self.divisor
            loops += 1
        return loops

    def secret_key(self, loop_size_other: int) -> int:
        """
        Return secret key calculated from public key
        and given loop size.
        """
        cur_value = self.public_key
        loops = 0
        while loops < loop_size_other - 1:
            cur_value = cur_value * self.public_key
            cur_value = cur_value % self.divisor
            loops += 1
        return cur_value


def handshake(pk_key: int, pk_door: int) -> int:
    """
    Execute cryptographic handshake between key and door.
    Return the encryption key.
    """
    key = Crypto(pk_key)
    door = Crypto(pk_door)
    key_loops = key.loop_size()
    return door.secret_key(key_loops)


if __name__ == "__main__":
    print("calculating...\n")
    test_key = Crypto(5764801)
    test_door = Crypto(17807724)
    assert test_key.loop_size() == 8
    assert test_door.loop_size() == 11
    assert test_key.secret_key(11) == 14897079
    assert test_door.secret_key(8) == 14897079

    start = perf_counter()
    solution = handshake(2959251, 4542595)
    end = perf_counter()
    runtime = round(end - start, 1)
    print(f"The solution is: {solution}")
    print(f"runtime: {runtime} seconds")
