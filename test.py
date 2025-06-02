from app import common

data=""
data_new = bytes.fromhex(data)
print(len(data_new))

print(common.read_packet(data_new))
