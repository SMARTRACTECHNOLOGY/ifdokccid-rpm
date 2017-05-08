Name:           ifdokccid_linux_x86_64
Version:        v4.0.5.5
Release:        1
Summary:        Lifecycles HID OMNIKEY 5421 PCSC Drivers Configuration

Group:          System Environment/Base
License:        Commercial Private License
Vendor:         SMARTRACTECHNOLOGY
Packager:       Smartrac Technology Fletcher, Inc.
URL:            https://lifecycles.io
BuildArch:      x86_64

Source0:        https://www.hidglobal.com/sites/default/files/drivers/ifdokccid_linux_x86_64-v4.0.5.5.tar.gz
Source1:        Info.plist.patch1

Requires:       bash
Requires:       libusb
Requires:       lshw
Requires:       pcsc-lite
Requires:       fxload
Requires:       pcsc-tools
Requires:       java >= 1.8
BuildRequires:  systemd

%define debug_package %{nil}

%description
Lifecycles HID OMNIKEY 5421 PCSC Drivers and PCSC Configuration

%clean
echo "Cleaning ..."
rm -rf %{buildroot}

%prep
echo "Prep ..."
# Auto extract the tar gz file
%setup -q

install -m644 %{_topdir}/Info.plist.patch1 %{_sourcedir}

%build
echo "Nothing to build"

%install
QA_RPATHS=$(( 0x0001|0x0002|0x0010 ))

#
# Install the omnikey.ini file
#
install -d -m755 -p %{buildroot}/%{_sysconfdir}
install -m600 %{_builddir}/%{name}-%{version}/omnikey.ini %{buildroot}/%{_sysconfdir}/omnikey.ini

#
# Install the bundle
#
install -d -m775 -p %{buildroot}/usr/lib64/pcsc/drivers/
cp -r %{_builddir}/%{name}-%{version}/%{name}-%{version}.bundle %{buildroot}/usr/lib64/pcsc/drivers/

#
# Install udev rules
#
install -d -m755 -p %{buildroot}/%{_sysconfdir}/udev/rules.d/
install -m600 %{_builddir}/%{name}-%{version}/z98_omnikey.rules %{buildroot}/%{_sysconfdir}/udev/rules.d/z98_omnikey.rules

#
# Copy corrected Info.plist to PCSC driver data directory
#
install -d -m755 -p %{buildroot}/%{_prefix}/lib64/pcsc/drivers/ifd-ccid.bundle/Contents
install -m644 %{_sourcedir}/Info.plist.patch1 %{buildroot}/%{_prefix}/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/Info.plist.patch1

%files
%{_prefix}/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/Info.plist.patch1
%{_sysconfdir}/omnikey.ini
%{_sysconfdir}/udev/rules.d/z98_omnikey.rules
%{_prefix}/lib64/pcsc/drivers/%{name}-%{version}.bundle/Contents/Info.plist
%{_prefix}/lib64/pcsc/drivers/%{name}-%{version}.bundle/Contents/Linux/ifdokccid.so

%post
patch -p1 %{_prefix}/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/Info.plist < %{_prefix}/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/Info.plist.patch1
%systemd_post pcscd.service

%preun
%systemd_preun pcscd.service

%postun
%systemd_postun_with_restart pcscd.service

%changelog
* Sun Apr 16 2017 Robert Van Voorhees <robert.vanvoorhees@smartrac-group.com> - 1-1
- Initial RPM release
