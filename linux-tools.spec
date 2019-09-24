Name:           linux-tools
Version:        5.1
Release:        364
License:        GPL-2.0
Summary:        The Linux kernel tools (perf)
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://www.kernel.org/pub/linux/kernel/v5.x/linux-5.1.tar.xz

Requires: binutils

BuildRequires:  bash
BuildRequires:  bc
BuildRequires:  binutils-dev
BuildRequires:  elfutils
BuildRequires:  elfutils-dev
BuildRequires:  kmod
BuildRequires:  make
BuildRequires:  openssl
BuildRequires:  openssl-dev
BuildRequires:  flex bison
BuildRequires:  ncurses-dev
BuildRequires:  binutils-dev
BuildRequires:  slang-dev
BuildRequires:  libunwind-dev
BuildRequires:  libunwind-dev32
BuildRequires:  python-dev
BuildRequires:  zlib-dev
BuildRequires:  xz-dev
BuildRequires:  numactl-dev
BuildRequires:  perl
BuildRequires:  xmlto
BuildRequires:  asciidoc
BuildRequires:  util-linux
BuildRequires:  libxml2-dev
BuildRequires:  libxslt
BuildRequires:  docbook-xml
BuildRequires:  audit-dev
BuildRequires:  python3-dev
BuildRequires:  babeltrace-dev

Patch1: turbostat.patch
Patch2: vmlinux-location.patch
Patch3: werror.patch

%description
The Linux kernel tools perf/trace.

%package hyperv
License:        GPL-2.0
Summary:        The Linux kernel hyperv daemon files
Group:          kernel

%description hyperv
Linux kernel hyperv daemon files

%prep
%setup -q -n linux-5.1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
export AR=gcc-ar
export RANLIB=gcc-ranlib
export NM=gcc-nm
unset LD_AS_NEEDED
BuildTools() {
    pushd tools/perf
    sed -i '/# Define NO_GTK2/a NO_GTK2 = 1' Makefile.perf
    
    #sed -i '/# Define NO_DEMANGLE if/a NO_DEMANGLE = 1' Makefile.perf

    make -s %{?sparse_mflags}
    popd
    pushd tools/power/x86/turbostat
    make
    popd
    pushd tools/power/x86/x86_energy_perf_policy
    make
    popd
}

BuildHyperVDaemons() {
    pushd tools/hv
    make
    popd
}

BuildTools
BuildHyperVDaemons

%install

InstallTools() {
    pushd tools/perf
    %make_install prefix=/usr
	pushd Documentation
	make man
	make DESTDIR=%{buildroot} mandir=/usr/share/man install
	popd
    popd
    pushd tools/power/x86/turbostat
    %make_install prefix=/usr
    popd
    pushd tools/kvm/kvm_stat
	make
	make INSTALL_ROOT=%{buildroot} install
    popd
    pushd tools/power/x86/x86_energy_perf_policy
    %make_install prefix=/usr
    popd
}

InstallHyperVDaemons() {
    pushd tools/hv
    mkdir -p %{buildroot}/usr/bin
    cp hv_fcopy_daemon %{buildroot}/usr/bin
    cp hv_kvp_daemon %{buildroot}/usr/bin
    cp hv_vss_daemon %{buildroot}/usr/bin
    popd
}

InstallTools
InstallHyperVDaemons

# Move bash-completion
mkdir -p %{buildroot}/usr/share/bash-completion/completions
mv %{buildroot}/etc/bash_completion.d/perf %{buildroot}/usr/share/bash-completion/completions/perf
rmdir %{buildroot}/etc/bash_completion.d
rmdir %{buildroot}/etc
mkdir -p %{buildroot}/usr/share

chmod 0644 %{buildroot}/usr/share/man/man8/*

%files
/usr/bin/trace
/usr/bin/perf
/usr/libexec/perf-core
/usr/lib64/traceevent/plugins/
/usr/share/bash-completion/completions/*
/usr/bin/turbostat
/usr/share/man/man8/turbostat.8
/usr/share/man/man1
/usr/share/doc/perf-tip/tips.txt
/usr/bin/kvm_stat
/usr/bin/x86_energy_perf_policy
/usr/share/man/man8/x86_energy_perf_policy.8
/usr/share/perf-core/strace/groups/file
/usr/lib/perf/examples/bpf/5sec.c
/usr/lib/perf/examples/bpf/augmented_syscalls.c
/usr/lib/perf/examples/bpf/empty.c
/usr/lib/perf/examples/bpf/hello.c
/usr/lib/perf/examples/bpf/sys_enter_openat.c
/usr/lib/perf/include/bpf/bpf.h
/usr/lib/perf/include/bpf/stdio.h
/usr/lib/perf/examples/bpf/augmented_raw_syscalls.c
/usr/lib/perf/examples/bpf/etcsnoop.c
/usr/lib/perf/include/bpf/linux/socket.h
/usr/lib/perf/include/bpf/pid_filter.h
/usr/lib/perf/include/bpf/unistd.h

%files hyperv
/usr/bin/hv_fcopy_daemon
/usr/bin/hv_kvp_daemon
/usr/bin/hv_vss_daemon
