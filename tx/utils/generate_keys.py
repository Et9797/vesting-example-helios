from pycardano import *
import sys


def main(n: int) -> None:
    for i in range(n):
        PaymentSigningKey.generate().save(f"keys/usr{i+1}.skey")
        skey = PaymentSigningKey.load(f"keys/usr{i+1}.skey")
        vkey = PaymentVerificationKey.from_signing_key(skey)
        addr = Address(vkey.hash(), network=Network.TESTNET)
        with open(f"keys/usr{i+1}.addr", "w") as f:
            f.write(str(addr))


if __name__ == "__main__":
    if not sys.argv[1].isdigit():
        sys.exit("Not a digit.")
    n = int(sys.argv[1])
    assert 0 < n < 1001, "Can only generate between 1-1000 keys."
    main(n)
