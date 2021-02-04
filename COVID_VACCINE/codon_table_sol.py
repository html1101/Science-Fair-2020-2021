import python_codon_tables


def reader(s):
    return s.strip().split(",")


def codons(*args, n=3):
    yield from (tuple(s[i : i + n] for s in args) for i in range(0, len(args[0]), n))


def pc_match(s1, s2, as_codons=False):
    div = 3 if as_codons else 1
    it = codons(s1, s2, n=div)
    return sum(a == b for a, b in it) / (len(s1) / div)


if __name__ == "__main__":
    res = [["species", "bases", "codons"]]
    for species in ["h_sapiens_9606", "m_musculus_10090"]:
        freq = python_codon_tables.get_codons_table(species)
        # Map codons to most frequent codon in this species this
        # does the same as the  `use_most_frequent` function
        subs = {k: max(d, key=d.get) for d in freq.values() for k in d.keys()}
        conv = {k: r for r, t in freq.items() for k in t.keys()}

        new_seq, vac_seq = [], []
        with open("COVID_VACCINE/side-by-side.csv") as fh:
            _ = next(fh)  # Skip headers
            for _, vir, vac in map(reader, fh):
                if conv[vir] != conv[vac]:
                    vir = vac
                new_seq.append(subs[vir])
                vac_seq.append(vac)

        new_prot = "".join(map(conv.get, new_seq))
        vac_prot = "".join(map(conv.get, vac_seq))
        new_seq = "".join(new_seq)
        vac_seq = "".join(vac_seq)
        assert new_prot == vac_prot
        res.append(
            [
                f"{species}",
                f"{pc_match(vac_seq, new_seq):.2%}",
                f"{pc_match(vac_seq, new_seq, True):.2%}",
            ]
        )
    m = list(max(map(len, x)) + 2 for x in list(map(list, zip(*res))))
    m[0] -= 2
    s = "{:>{}}" * len(m)
    for x in res:
        c = x + m
        c[::2] = x
        c[1::2] = m
        print(s.format(*c))