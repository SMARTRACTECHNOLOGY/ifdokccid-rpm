Name:           hid-omnikey-5421-pcsc-drivers
Version:        4.0.5.5
Release:        1
Summary:        Lifecycles HID OMNIKEY 5421 PCSC Drivers Configuration

Group:          System Environment/Base
License:        Commercial Private License
Vendor:         hid-omnikey
Packager:       Smartrac Technology Fletcher, Inc.
URL:            https://lifecycles.io
BuildArch:      x86_64

Source0:        https://www.hidglobal.com/sites/default/files/drivers/ifdokccid_linux_x86_64-v%{version}.tar.gz

Requires:       bash
Requires:       libusb
Requires:       lshw
Requires:       pcsc-lite
Requires:       fxload
Requires:       pcsc-tools
Requires:       java >= 1.8
BuildRequires:  systemd

%description
Lifecycles HID OMNIKEY 5421 PCSC Drivers and PCSC Configuration

%prep
%autosetup

%build
echo "Nothing to build"

%install
%make_install

%files


%post
%systemd_post pcscd.service

%preun
%systemd_preun pcscd.service

%postun
%systemd_postun_with_restart pcscd.service


%changelog
* Sun Apr 16 2017 Robert Van Voorhees <robert.vanvoorhees@smartrac-group.com> - 1-1
- Initial RPM release
