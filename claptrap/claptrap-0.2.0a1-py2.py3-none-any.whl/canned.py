from random import choice, sample


def wub(length=50):
    if length < 1:
        return ValueError("length must be positive")
    if length == 1:
        return choice("wW")
    if length == 2:
        return choice("wW") + choice("uUbB.!?")
    if length == 3:
        return choice("wW") + choice("uU") + choice("bB")
    if length == 4:
        return wub(3) + choice("bB.!?")
    if length == 5:
        return (
            choice("wW") + choice("uU") + choice("uUbB") + choice("bB") + choice(".!?")
        )
    if length == 6:
        return wub(3) + wub(3)
    if length == 10:
        return wub(3) + choice(",.:;") + " " + wub(5)

    n_wubs, pad = divmod(length + 1, 4)

    pad_indexes = sample(range(n_wubs), pad)
    wubs = [wub(3) for _ in range(n_wubs)]

    for idx in pad_indexes:
        if idx == n_wubs - 1:
            char = choice(".!?")
        else:
            char = choice(".,;:")
        wubs[idx] = wubs[idx] + char

    return " ".join(wubs)
