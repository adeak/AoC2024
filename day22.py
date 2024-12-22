from collections import defaultdict, deque


def day22(inp, only_part1=False):
    buyers = list(map(int, inp.splitlines()))

    part1 = part2 = 0
    prices_by_deltas = defaultdict(dict)  # 4-tuple -> {buyer id -> first price}
    deltas = deque(maxlen=4)
    for buyer_id, buyer in enumerate(buyers):
        secret = buyer
        for _ in range(2000):
            next_secret = evolve(secret)
            if only_part1:
                # for testing
                secret = next_secret
                continue

            # part 2: record prices
            deltas.append(next_secret % 10 - secret % 10)
            if len(deltas) == 4:
                deltas_key = tuple(deltas)
                if buyer_id not in prices_by_deltas[deltas_key]:
                    prices_by_deltas[deltas_key][buyer_id] = next_secret % 10
            secret = next_secret
        part1 += secret

    if only_part1:
        return part1, None
    
    # part 2: find most lucrative sequence
    part2 = max(
        sum(price_dict.values())
        for price_dict in prices_by_deltas.values()
    )

    return part1, part2


def mix(secret, other):
    return secret ^ other


def prune(secret):
    return secret % 16777216


def evolve(secret):
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    return prune(mix(secret, secret * 2048))


if __name__ == "__main__":
    testinp = open('day22.testinp').read()
    testinp2 = open('day22.testinp2').read()
    print(day22(testinp, only_part1=True)[0], day22(testinp2)[1])
    inp = open('day22.inp').read()
    print(day22(inp))
