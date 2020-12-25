class HandShake:
    subject_number = 7
    divisor = 20201227

    def __init__(self, public_key: int) -> None:
        self.public_key = public_key

    def loop_size(self):
        cur_value = 1
        loops = 0
        while cur_value != self.public_key:
            # s1 = cur_value * self.subject_number
            cur_value = cur_value * self.subject_number
            # s2 = s1 % self.divisor
            cur_value = cur_value % self.divisor
            # cur_value = s2
            loops += 1
        return loops

    def secret_key(self, loop_size_other: int) -> int:
        cur_value = self.public_key
        loops = 0
        while loops != loop_size_other:
            s1 = cur_value * self.public_key
            s2 = s1 % self.divisor
            cur_value = s2
            # print("cur val = ", cur_value)
            loops += 1
        return cur_value


def compute(subject_number, public_key, loops=100):
    divisor = 20201227
    cur_value = 1
    for i in range(loops):
        # print(f"loop: {i}")
        s1 = cur_value * subject_number
        # print(f"value after step 1: {s1}")
        s2 = s1 % divisor
        # print(f"value after step 2: {s2}")
        cur_value = s2
        if cur_value == public_key:
            return f"loopsize = {i + 1}"
    return cur_value


print(compute(7, 5764801))
# print()
# print(compute(7, 17807724))

print(compute(5764801, 17807724, 11))
# print(compute(17807724, 5764801, 8))

t0 = HandShake(5764801)
# print(t0.loop_size())
# print(t0.secret_key(10))
# t1 = HandShake(17807724)
# print(t1.loop_size())

# solution p1
day25 = (2959251, 4542595)
ls_key = compute(7, day25[0], 100000000)
ls_door = compute(7, day25[1], 100000000)
print(ls_key)
print(ls_door)
print(compute(day25[0], 666, 16473833))
print(compute(day25[1], 666, 7731677))
