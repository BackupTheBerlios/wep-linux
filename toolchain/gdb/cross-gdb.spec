# $Id: cross-gdb.spec,v 1.3 2003/07/23 20:40:10 telka Exp $

Summary: Cross compiled The GNU Project Debugger.
Name: cross-gdb
Version: 5.3
Release: 3
License: GPL
Group: Development/Debuggers
URL: http://sources.redhat.com/gdb
Packager: Marcel Telka <marcel@telka.sk>
Source: ftp://sources.redhat.com/pub/gdb/releases/gdb-5.3.tar.bz2

Buildroot: /var/tmp/cross-gdb

%define _prefix /opt/cross
%define _mandir %{_prefix}/man

%description
This is The GNU Project Debugger cross compiled for various targets.

%package common
Summary: Common files for The GNU Project Debugger cross compiled.
Group: Development/Debuggers

%description common
This is a common package for The GNU Project Debugger cross compiled for various targets.

%package arm-elf
Summary: The GNU Project Debugger cross compiled for arm-elf target.
Group: Development/Debuggers
Requires: cross-gdb-common = %{version}-%{release}

%description arm-elf
This is The GNU Project Debugger cross compiled for arm-elf target.

%package arm-linux
Summary: The GNU Project Debugger cross compiled for arm-linux target.
Group: Development/Debuggers
Requires: cross-gdb-common = %{version}-%{release}

%description arm-linux
This is The GNU Project Debugger cross compiled for arm-linux target.

%prep
%setup -q -c

%build
mkdir build-arm-elf
cd build-arm-elf
../gdb-%{version}/configure --target=arm-elf --prefix=%{_prefix}
make
cd ..
mkdir build-arm-linux
cd build-arm-linux
../gdb-%{version}/configure --target=arm-linux --prefix=%{_prefix}
make
cd ..

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cd build-arm-elf
%makeinstall
cd ../build-arm-linux
%makeinstall
rm -rf %{buildroot}/usr/share/info
rm -rf %{buildroot}%{_prefix}/info
rm -f %{buildroot}%{_prefix}/lib/libiberty.a
rm -rf %{buildroot}%{_prefix}/share

%files common
%defattr(-,root,root)
%{_prefix}/lib/libmmalloc.a

%files arm-elf
%defattr(-,root,root)
%{_prefix}/bin/arm-elf-*
%{_prefix}/lib/libarm-elf-sim.a
%doc %{_mandir}/man1/arm-elf-*

%files arm-linux
%defattr(-,root,root)
%{_prefix}/bin/arm-linux-*
%{_prefix}/lib/libarm-linux-sim.a
%doc %{_mandir}/man1/arm-linux-*

%clean
rm -rf build-arm-elf
rm -rf build-arm-linux
rm -rf %{buildroot}

%changelog
* Wed Jul 23 2003 Marcel Telka <marcel@telka.sk> 5.3-3
- removed info documentation from Cygwin builds

* Thu May 15 2003 Marcel Telka <marcel@telka.sk> 5.3-2
- fixed path for man documentation

* Wed May 14 2003 Marcel Telka <marcel@telka.sk> 5.3-1
- initial spec file
