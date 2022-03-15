# Tracing IO done via page-faults using bpftrace

Note that at the time of writing bpf is really new. This worked for me with 5.13 kernel running on amd64. bpftrace was not able to hook anything on arm64 or some older kernels.

## Obvious, but complicated way

My first attempt to do this was via proper hooks as exposed by the `page_fault_user` tracepoint. This is documented under [page_fault_user](page_fault_user/README.md).

Upside: you get exact addresses that faulted. Eg you can correlate them exactly with current-instruction, etc.

Downside: this requires a lot of syscall-tracking machinery and post-processing and is thus error-prone. The biggest, most obvious hole is that it doesn't capture memory mapping that happens during program creation(eg the executable itself).


## Reliable, tied to ext4 way

Idea here is to hook ext4 mmap-handler. Documented under [ext4](ext4/REAME.md).

Upside: This is guaranteed to catch every mmap IO.

Downsides: block-IO level granularity. Tied to ext4 internals.