#!/usr/bin/env python3

mmap_entries = {}

# mmap("ls", fd=3, fname="/etc/ld.so.cache",off=0, len=31189, ret=0x79E65000)

def mmap(comm, fd, fname, off, len, ret):
    if fname == "":
        fname = str(fd)
    mmap_entries[ret] = (ret + len, fname)
    # print(off + len)

def page_fault_user(comm, address, ip):
    # print(mmap_entries)
    for base_addr in mmap_entries:
        # print(base_addr)
        end_fname = mmap_entries[base_addr]
        end = end_fname[0]
        if address >= base_addr and address < end:
            print(end_fname[1], address - base_addr)
            return
    print(f"{address} not found")

if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        eval(line)
    # eval((sys.stdin.read()))
    # page_fault_user("bpftrace", address=0x65687408, ip=0x6F32185C)
    # page_fault_user("ls", address=0x7FF2B0D0, ip=0x7FF2B0D0)
