# EBPF for Tracing How Firefox Uses Page Faults to Load Libraries

Modern browsers are some of the most complicated programs ever written. For example, the main Firefox library on my system is over 130Mbytes. Doing 130MB of IO poorly can be quite a performance hit, even with SSDs! :). 

Few people seem to understand how memory-mapped IO works. There are no pre-canned tools to observe it on Linux, even fewer know how to observe it. Years ago, when I was working on Firefox startup performance, I discovered that libraries were loaded backwards ([paper](https://arxiv.org/pdf/1010.2196.pdf), GCC [bug](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46770), [deleted blog](https://news.ycombinator.com/item?id=1385994)) on Linux. Figuring this out was super-painful, involved learning SystemTap and a setting up a just-right kernel with headers and symbols.

I decided to use above example to investigate solving this problem using modern EBPF. Noticed that there wasn't any bpf that I could google for tracing mmap-IO. This is now documented in [github](https://github.com/tarasglek/bpftrace_pagefaults).

## Theory

Linux libraries reside in files on disk. Dynamic library loader calls `open()` and `mmap()` to make certain parts of those libraries executable. `mmap()` lets one treat files as memory. Page-faults are the hardware mechanism that passes program execution to allow the kernel to backfill information from disk when accessed as memory. Some pointers, get adjusted, various callbacks get called to initialize the libraries(eg code to initilize global variables). Then various code in library can be called. Combination of initializing library and running code within in it causes some or all of the library to be loaded from disk. 

EBPF in Linux lets you inject limited hooks into various parts of kernel and userspace. [bpftrace](https://github.com/iovisor/bpftrace) is the toolchain for that. We use bpftrace to trace open(), mmap() and page-faults, then reverse-engineer the file mapping via bit of python in `process.py`.


## Practice:

1. Install bpftrace with `apt-get install -y bpftrace` 

2. Find the relevant hooks with `bpftrace -l '*syscalls*mmap*'  -v`.

3. Run the analysis script with `sudo bpftrace mmap_pagefault_snoop.bt > faults.py`. In another terminal start `firefox` command. This generates pseudo-python function call of the IO trace that we can use to analyze data.

4. Post-process, with something like `grep firefox-60792 faults.py | ./process.py | grep libxul.so |cut -d\  -f2 > /tmp/xul.csv`. `firefox-60792` is the first Firefox pid that ran during my trace. `process.py` matches up open(), mmap() syscalls with following page-faults such that we can figure out which offset in the mmaped-file was read. `grep libxul.so` + `cut` command dumps the data so we can graph in a spreadsheet.

5. Post-process results a little, graph the results as a time series. See libxul.ods
![Look, ](https://github.com/tarasglek/bpftrace_pagefaults/blob/main/artifacts/chart.png?raw=true)

6. Can observe that the first part of the library is loaded sequentially(eg, from lower addresses to higher ones). This is likely the C++ static initializers. This is good, means the toolchain bug I discovered has stayed fixed! (The paper I linked above talks about optimizing initializers with full-program-optimization). 

## Limitations

1. We can trace mmap() syscalls for loading libraries, but there isn't an mmap syscall when the initial executable gets mapped by Linux(happens as part of exec syscall, need to trace something else for that?). This can also be worked-around by parsing `/proc/#pid#/smaps`.

2. This doesn't actually trace how the pages are loaded from disk. We'd have to add more ebpf tracepoints to better understand file IO. Eg we are paging in 4KB increments on x86, but Linux ammortizes some of the away by doing IO in read-ahead chunks of some multiple of that.

3. Had to do this on x86 as my arm64 VM is missing the `tracepoint:exceptions:page_fault_user` all of the exception tracepoints. What the hell, why?