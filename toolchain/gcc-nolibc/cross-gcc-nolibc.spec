# $Id: cross-gcc-nolibc.spec,v 1.2 2003/08/09 11:49:06 telka Exp $

Summary: Cross GNU Compiler Collection.
Name: cross-gcc-nolibc
Version: 3.3.1
Release: 1
License: GPL
Group: Development/Languages
URL: http://gcc.gnu.org/
Packager: Marcel Telka <marcel@telka.sk>
Source: ftp://sources.redhat.com/pub/gcc/releases/gcc-3.3.1/gcc-core-3.3.1.tar.bz2

Buildroot: /var/tmp/cross-gcc-nolibc

BuildRequires: cross-binutils-arm-elf, cross-binutils-arm-linux

%define _prefix /opt/cross
%define _infodir %{_prefix}/info
%define _mandir %{_prefix}/man

%description
This is GNU Compiler Collection cross compiled for various targets.

%package common
Summary: Common cross GNU Compiler Collection.
Group: Development/Languages

%description common
This is a common package for GNU Compiler Collections cross compiled for various targets.

%package arm-elf
Summary: Cross GNU Compiler Collection compiled for arm-elf target.
Group: Development/Languages
Requires: cross-gcc-nolibc-common = %{version}-%{release}

%description arm-elf
This is GNU Compiler Collection cross compiled for arm-elf target.

%package arm-linux
Summary: Cross GNU Compiler Collection compiler for arm-linux target.
Group: Development/Languages
Requires: cross-gcc-nolibc-common = %{version}-%{release}

%description arm-linux
This is GNU Compiler Collection cross compiled for arm-linux target.

%prep
%setup -q -c

%build
export PATH="%{_prefix}/bin:$PATH"
mkdir build-arm-elf
cd build-arm-elf
../gcc-%{version}/configure --target=arm-elf --prefix=%{_prefix} --disable-shared --enable-languages=c --with-gnu-as --with-gnu-ld --disable-threads
make
cd ..
mkdir build-arm-linux
cd build-arm-linux
../gcc-%{version}/configure --target=arm-linux --prefix=%{_prefix} --disable-shared --enable-languages=c --with-gnu-as --with-gnu-ld --disable-threads
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cd build-arm-elf
%makeinstall
cd ../build-arm-linux
%makeinstall
#rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_prefix}/lib/libiberty.a

%files common
%defattr(-,root,root)
%{_prefix}/share/locale/*
%doc %{_infodir}
%doc %{_mandir}/man1/cpp.1
%doc %{_mandir}/man1/gcov.1
%doc %{_mandir}/man7

%files arm-elf
%defattr(-,root,root)
%{_prefix}/bin/arm-elf-*
%{_prefix}/lib/gcc-lib/arm-elf
%doc %{_mandir}/man1/arm-elf-*

%files arm-linux
%defattr(-,root,root)
%{_prefix}/bin/arm-linux-*
%{_prefix}/lib/gcc-lib/arm-linux
%doc %{_mandir}/man1/arm-linux-*

%clean
rm -rf build-arm-elf
rm -rf build-arm-linux
rm -rf %{buildroot}

%changelog
* Sat Aug 09 2003 Marcel Telka <marcel@telka.sk> 3.3.1-1
- updated for GCC version 3.3.1

* Wed May 21 2003 Marcel Telka <marcel@telka.sk> 3.3-1
- initial spec file
