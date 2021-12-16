import operator
import sys
from contextlib import suppress
from functools import reduce
from io import StringIO

OPTYPES = {
    0: operator.add,
    1: operator.mul,
    2: lambda x, y: min((x, y)),
    3: lambda x, y: max((x, y)),
    5: operator.gt,
    6: operator.lt,
    7: operator.eq,
}


def parse_number(buf):
    chunks = []
    keep_reading = True
    while keep_reading:
        keep_reading = buf.read(1) == "1"
        chunks.append(buf.read(4))
    return int("".join(chunks), 2)


def parse_operator(buf):
    packets = []
    with suppress(ValueError):
        length_type = int(buf.read(1))
        if length_type == 0:
            subpacket_length = (int(buf.read(15), 2), "bits")
        else:
            subpacket_length = (int(buf.read(11), 2), "count")
        if subpacket_length[1] == "bits":
            sub_buf = StringIO(buf.read(subpacket_length[0]))
            packets.extend(list(parse_packets(sub_buf)))
        else:
            while len(packets) < subpacket_length[0]:
                subpacket = parse_packet(buf)
                if not subpacket:
                    break
                packets.append(subpacket)
    return packets


def parse_packet(buf):
    packet = {}
    header = buf.read(6)
    if not len(header) == 6:
        return None
    packet["version"] = int(header[:3], 2)
    packet["type"] = int(header[3:6], 2)
    if packet["type"] == 4:
        packet["value"] = parse_number(buf)
    else:
        packet["subpackets"] = parse_operator(buf)
        nums = [p["value"] for p in packet["subpackets"]]
        packet["value"] = reduce(OPTYPES[packet["type"]], nums) if nums else None
    return packet


def version_sum(packet):
    return sum(
        (packet["version"], *(version_sum(p) for p in packet.get("subpackets", ())))
    )


def parse_packets(buf):
    while packet := parse_packet(buf):
        yield packet


if __name__ == "__main__":
    bits = "".join(f"{int(c, 16):04b}" for c in sys.stdin.read().strip())
    buf = StringIO(bits)
    packets = list(parse_packets(buf))

    print(f"Part 1: {sum(version_sum(packet) for packet in packets)}")
    print(f'Part 2: {packets[0]["value"]}')
