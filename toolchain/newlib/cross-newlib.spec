# $Id: cross-newlib.spec,v 1.1 2003/05/28 15:56:27 telka Exp $

Summary: Cross newlib.
Name: cross-newlib
Version: 1.11.0
Release: 1
License: GPL
Group: Development/Libraries
URL: http://sources.redhat.com/newlib/
Packager: Marcel Telka <marcel@telka.sk>
Source: ftp://sources.redhat.com/pub/newlib/newlib-1.11.0.tar.gz

Buildroot: %{_tmppath}/cross-newlib

BuildRequires: cross-binutils-arm-elf, cross-gcc-nolibc-arm-elf

%define _prefix /opt/cross
%define _infodir %{_prefix}/info
%define _mandir %{_prefix}/man

%description
This is a GNU Compiler Collection cross compiled for various targets.

%package arm-elf
Summary: Cross newlib for arm-elf.
Group: Development/Libraries

%description arm-elf
This is newlib package cross compiled for arm-elf.

%prep
%setup -q -c

%build
export PATH="%{_prefix}/bin:$PATH"
rm -rf build-arm-elf
mkdir build-arm-elf
cd build-arm-elf
../newlib-%{version}/configure --target=arm-elf --prefix=%{_prefix}
make

%install
export PATH="%{_prefix}/bin:$PATH"
rm -rf %{buildroot}
mkdir -p %{buildroot}
cd build-arm-elf
%makeinstall
rm -rf %{buildroot}%{_prefix}/info
rm -f %{buildroot}%{_prefix}/arm-elf/lib/libg.a
ln libc.a -s %{buildroot}%{_prefix}/arm-elf/lib/libg.a
rm -f %{buildroot}%{_prefix}/arm-elf/lib/thumb/libg.a
ln libc.a -s %{buildroot}%{_prefix}/arm-elf/lib/thumb/libg.a

%files arm-elf
%defattr(-,root,root)
%{_prefix}/arm-elf

%clean
rm -rf build-arm-elf
rm -rf %{buildroot}

%changelog
* Wed May 28 2003 Marcel Telka <marcel@telka.sk> 1.11.0-1
- initial spec file
