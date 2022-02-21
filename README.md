# EBPF for Tracing How Firefox Loads Libraries

Few people seem to understand how memory-mapped IO works, fewer know how to observe it. Years ago when I was working on Firefox startup performance, I noticed that libraries were loaded backwards ([paper](https://arxiv.org/pdf/1010.2196.pdf), GCC [bug](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46770), [deleted blog](https://news.ycombinator.com/item?id=1385994)) on Linux. Figuring this out was super-painful, involved learning SystemTap and a setting up a just-right kernel with headers and symbols.

I decided to use above example to investigate solving this problem using EBPF. This is documented in [github](https://github.com/tarasglek/bpftrace_pagefaults).

Here is the process:

1. Install [bpftrace](https://github.com/iovisor/bpftrace) with `apt-get install -y bpftrace` 

2. Find the relevant hooks with `bpftrace -l '*syscalls*mmap*'  -v`.

3. Run the analysis script with `sudo bpftrace mmap_pagefault_snoop.bt > faults.py`. In another terminal start `firefox` command. This generates pseudo-python function call of the IO trace that we can use to analyze data.

4. Post-process, with something like `grep firefox-60792 faults.py | ./process.py | grep libxul.so |cut -d\  -f2 > /tmp/xul.csv`. `firefox-60792` is the first Firefox pid that ran during my trace. `process.py` matches up open(), mmap() syscalls with following page-faults such that we can figure out which offset in the mmaped-file was read. `grep libxul.so` + `cut` command dumps the data so we can graph in a spreadsheet.

5. Post-process results a little, graph the results as a time series.
![Look, ](https://github.com/tarasglek/bpftrace_pagefaults/blob/main/artifacts/chart.png?raw=true)


```
sudo bpftrace -l '*syscalls*mmap*'  -v

sudo bpftrace mmap_pagefault_snoop.bt -c `which ls` | grep '(' | ./process.py
sudo bpftrace mmap_pagefault_snoop.bt -c  | grep '(' | ./process.py
grep firefox-60792 xul.py | ./process.py |grep xul|cut -d\  -f2 > /tmp/xul.csv

```