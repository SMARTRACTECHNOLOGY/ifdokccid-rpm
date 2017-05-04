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
Source1:        https://github.com/SMARTRACTECHNOLOGY/rpm-hid-omnikey-5421-pcsc-drivers/blob/master/Info.plist

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

%clean
echo "Cleaning ..."
rm -rf %{buildroot}

%prep
echo "Prep ..."
# Auto extract the tar gz file
#%autosetup
%setup -q -n %{Source0}

%build
echo "Nothing to build"

%install

# Install HID OMNIKey Drivers
./install

# Create PCSC driver data directory
install -d -m655 -p /usr/lib64/pcsc/drivers/ifd-ccid.bundle/Contents

# Copy corrected Info.plist to PCSC driver data directory
install -m 0644 %{Source1} %{buildroot}/usr/lib64/pcsc/drivers/ifd-ccid.bundle/Contents


%files
/usr/lib64/pcsc/drivers/ifdokccid_linux_x86_64-v4.0.5.5.bundle/Contents/Linux/ifdokccid.so
/usr/lib64/pcsc/drivers/ifdokccid_linux_x86_64-v4.0.5.5.bundle/Contents/Info.plist


%post
%systemd_post pcscd.service

%preun
%systemd_preun pcscd.service

%postun
%systemd_postun_with_restart pcscd.service


%changelog
* Sun Apr 16 2017 Robert Van Voorhees <robert.vanvoorhees@smartrac-group.com> - 1-1
- Initial RPM release
