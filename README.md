
```
sudo bpftrace -l '*syscalls*mmap*'  -v

sudo bpftrace opensnoop.bt -c `which ls`

```