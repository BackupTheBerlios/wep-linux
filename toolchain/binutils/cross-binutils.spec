# $Id: cross-binutils.spec,v 1.4 2003/06/19 09:12:01 telka Exp $

Summary: Cross GNU collection of binary utilities.
Name: cross-binutils
Version: 2.14
Release: 1
License: GPL
Group: Development/Tools
URL: http://sources.redhat.com/binutils
Packager: Marcel Telka <marcel@telka.sk>
Source: ftp://sources.redhat.com/pub/binutils/releases/binutils-2.14.tar.bz2

Buildroot: /var/tmp/cross-binutils

%define _prefix /opt/cross
%define _infodir %{_prefix}/info
%define _mandir %{_prefix}/man

%description
This is a collection of binary utlities cross compiled for various targets.

%package common
Summary: Common cross GNU collection of binary utilities.
Group: Development/Tools

%description common
This is a common package for collection of binary utlities cross compiled for various targets.

%package arm-elf
Summary: Cross GNU collection of binary utilities for arm-elf target.
Group: Development/Tools
Requires: cross-binutils-common = %{version}-%{release}

%description arm-elf
This is a collection of binary utlities cross compiled for arm-elf target.

%package arm-linux
Summary: Cross GNU collection of binary utilities for arm-linux target.
Group: Development/Tools
Requires: cross-binutils-common = %{version}-%{release}

%description arm-linux
This is a collection of binary utlities cross compiled for arm-linux target.

%prep
%setup -q -c

%build
mkdir build-arm-elf
cd build-arm-elf
../binutils-%{version}/configure --target=arm-elf --prefix=%{_prefix}
make
cd ..
mkdir build-arm-linux
cd build-arm-linux
../binutils-%{version}/configure --target=arm-linux --prefix=%{_prefix}
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cd build-arm-elf
%makeinstall
cd ../build-arm-linux
%makeinstall
rm -f %{buildroot}%{_infodir}/dir

%files common
%defattr(-,root,root)
%{_prefix}/lib/libiberty.a
%{_prefix}/share/locale/*
%doc %{_infodir}/*info*

%files arm-elf
%defattr(-,root,root)
%{_prefix}/arm-elf/*
%{_prefix}/bin/arm-elf-*
%doc %{_mandir}/man1/arm-elf-*

%files arm-linux
%defattr(-,root,root)
%{_prefix}/arm-linux/*
%{_prefix}/bin/arm-linux-*
%doc %{_mandir}/man1/arm-linux-*

%clean
rm -rf build-arm-elf
rm -rf build-arm-linux
rm -rf %{buildroot}

%changelog
* Thu Jun 19 2003 Marcel Telka <marcel@telka.sk> 2.14-1
- updated for binutils-2.14

* Thu May 15 2003 Marcel Telka <marcel@telka.sk> 2.13.2.1-3
- fixed path for man and info documentation
- removed invalid man documentation from packages

* Wed May 14 2003 Marcel Telka <marcel@telka.sk> 2.13.2.1-2
- added arm-elf target
- added info documentation into common package
- simplified package names
- removed texinfo from BuildRequires

* Wed May 14 2003 Marcel Telka <marcel@telka.sk> 2.13.2.1-1
- initial spec file
