
```
sudo bpftrace -l '*syscalls*mmap*'  -v

sudo bpftrace mmap_pagefault_snoop.bt -c `which ls` | grep '(' | ./process.py

```