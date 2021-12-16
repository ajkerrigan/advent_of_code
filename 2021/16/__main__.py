import sys
from io import StringIO


def parse_number(buf):
    chunks = []
    keep_reading = True
    while keep_reading:
        keep_reading = buf.read(1) == "1"
        chunks.append(buf.read(4))
    return int("".join(chunks), 2)


def parse_packet(buf):
    packet = {}
    header = buf.read(6)
    if not len(header) == 6:
        return None
    packet["version"] = int(header[:3], 2)
    packet["type"] = int(header[3:6], 2)
    if buf.tell() == len(buf.getvalue()):
        return None
    print(packet)
    match packet["type"]:
        case 4:
            packet["number"] = parse_number(buf)
        case _:
            try:
                length_type = int(buf.read(1))
                if length_type == 0:
                    subpacket_length = (int(buf.read(15), 2), "bits")
                else:
                    subpacket_length = (int(buf.read(11), 2), "count")
                packet["subpackets"] = []
                if subpacket_length[1] == "bits":
                    sub_buf = StringIO(buf.read(subpacket_length[0]))
                    packet["subpackets"].extend(list(parse_packets(sub_buf)))
                else:
                    while len(packet["subpackets"]) < subpacket_length[0]:
                        subpacket = parse_packet(buf)
                        if not subpacket:
                            break
                        packet["subpackets"].append(subpacket)
            except ValueError:
                return None
    return packet


def version_sum(packet):
    return sum(
        (packet["version"], *(version_sum(p) for p in packet.get("subpackets", ())))
    )


bits = "".join(f"{int(c, 16):04b}" for c in sys.stdin.read().strip())
print(bits)
buf = StringIO(bits)


def parse_packets(buf):
    while packet := parse_packet(buf):
        print(packet)
        yield packet


packets = list(parse_packets(buf))

print(sum(version_sum(packet) for packet in packets))
