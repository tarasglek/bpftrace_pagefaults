#!/usr/bin/env python3
import bisect

mmap_entries = {}
mmap_keys = []
# mmap("ls", fd=3, fname="/etc/ld.so.cache",off=0, len=31189, ret=0x79E65000)

def mmap(comm, fd, fname, off, len, ret):
    if fname == "":
        fname = str(fd)
    mmap_entries[ret] = (ret + len, fname)
    global mmap_keys
    bisect.insort(mmap_keys, ret)

def page_fault_user(comm, address, ip):
    # print(mmap_entries)
    pos = bisect.bisect_left(mmap_keys, address)
    if pos >=0 and len(mmap_keys) > pos:
        if mmap_keys[pos] != address:
            pos = pos - 1
        if pos >= 0:
            base_address = mmap_keys[pos]
            (end, fname) = mmap_entries[base_address]
            # print('bisect', hex(address), hex(mmap_keys[pos]), address >= mmap_keys[pos] and address < end, fname, address - base_address)
            if end > address:
                print(fname, hex(address - base_address))
                return
    print(f"{address} not found")

if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        eval(line)
    # prev = 0
    # for key, value in sorted(mmap_entries.items()):
    #     (end, fname) = value
    #     if 'libc' in fname:
    #         if prev:
    #             if prev >= key:
    #                 print('hmm')
    #         print(hex(key), hex(end),end-key, fname)
    #         prev = end
    # eval((sys.stdin.read()))
    # page_fault_user("bpftrace", address=0x65687408, ip=0x6F32185C)
    # page_fault_user("ls", address=0x7FF2B0D0, ip=0x7FF2B0D0)
