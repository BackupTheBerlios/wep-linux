# $Id: cross-binutils.spec,v 1.1 2003/05/14 13:27:49 telka Exp $

Summary: Cross GNU collection of binary utilities.
Name: cross-binutils
Version: 2.13.2.1
Release: 1
License: GPL
Group: Development/Tools
URL: http://sources.redhat.com/binutils
Packager: Marcel Telka <marcel@telka.sk>
Source: ftp://sources.redhat.com/pub/binutils/releases/binutils-2.13.2.1.tar.bz2

Buildroot: /var/tmp/cross-binutils
BuildRequires: texinfo >= 4.0

%define _prefix /opt/cross

%description
This is a collection of binary utlities cross compiled for various targets.

%package -n cross-binutils-common
Summary: Common cross GNU collection of binary utilities.
Group: Development/Tools

%description -n cross-binutils-common
This is a common package for collection of binary utlities cross compiled for various targets.

%package -n cross-binutils-arm-linux
Summary: Cross GNU collection of binary utilities for arm-linux target.
Group: Development/Tools
Requires: cross-binutils-common = %{version}-%{release}

%description -n cross-binutils-arm-linux
This is a collection of binary utlities cross compiled for arm-linux target.

%prep
%setup -q -c

%build
mkdir build-arm-linux
cd build-arm-linux
../binutils-%{version}/configure --target=arm-linux --prefix=%{_prefix}
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cd build-arm-linux
%makeinstall
rm -rf %{buildroot}/usr/share/info

%files -n cross-binutils-common
%defattr(-,root,root)
%{_prefix}/lib/libiberty.a
%{_prefix}/share/locale/*

%files -n cross-binutils-arm-linux
%defattr(-,root,root)
%{_prefix}/arm-linux/*
%{_prefix}/bin/*
%doc %{_mandir}/*

%clean
rm -rf build-arm-linux
rm -rf %{buildroot}

%changelog
* Wed May 14 2003 Marcel Telka <marcel@telka.sk> 2.13.2.1-1
- initial spec file
