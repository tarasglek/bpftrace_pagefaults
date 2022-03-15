# Hooking ext4 with bpf to trace mmap reads

This approach is based on my prior work using SystemTap. For an in-depth discussion of that see this [paper](https://arxiv.org/pdf/1403.6997.pdf)

## Usage
`apt-get install -y bpftrace`

`bpftrace ext4.bt  > /tmp/log.txt # run this in background`

and to trace `rustc` IO do:

`sysctl -w vm.drop_caches=3; rustc`

Sample output: [log.txt](https://github.com/tarasglek/bpftrace_pagefaults/files/8246432/log.txt)
