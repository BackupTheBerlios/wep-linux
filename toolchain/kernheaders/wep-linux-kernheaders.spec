# $Id: wep-linux-kernheaders.spec,v 1.1 2003/05/28 11:41:00 telka Exp $

Summary: Kernel headers for wep-linux.
Name: wep-linux-kernheaders
Version: 2.4.19
Release: 7.1.1.1
License: GPL
Group: Development/System
Packager: Marcel Telka <marcel@telka.sk>
Source: ftp://ftp.kernel.org/pub/linux/kernel/v2.4/linux-2.4.19.tar.bz2
Patch0: ftp://ftp.arm.linux.org.uk/pub/linux/arm/kernel/v2.4/patch-2.4.19-rmk7.bz2
Patch1: ftp://ftp.arm.linux.org.uk/pub/linux/arm/people/nico/diff-2.4.19-rmk7-pxa1.gz
Patch2: http://download.berlios.de/wep-linux/patch-2.4.19-rmk7-pxa1-wep1.gz

Buildroot: %{_tmppath}/wep-linux-kernheaders-root

BuildRequires: cross-gcc-nolibc-arm-linux

%define _prefix /opt/wep-linux
%define _infodir %{_prefix}/info
%define _mandir %{_prefix}/man

%description
This is a package with kernel header files for wep-linux.

%prep
%setup -q -c
cd linux-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
export PATH="/opt/cross/bin:$PATH"
cd linux-%{version}
make wepep250_config
make oldconfig
make include/config/MARKER

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix}/include
cp -rp linux-%{version}/include/linux %{buildroot}%{_prefix}/include
cp -rp linux-%{version}/include/asm %{buildroot}%{_prefix}/include
cp -rp linux-%{version}/include/asm-arm %{buildroot}%{_prefix}/include

%files
%defattr(-,root,root)
%{_prefix}/include

%clean
rm -rf %{buildroot}

%changelog
* Wed May 28 2003 Marcel Telka <marcel@telka.sk> 2.4.19-7.1.1.1
- initial spec file
