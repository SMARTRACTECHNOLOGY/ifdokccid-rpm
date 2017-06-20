Name:           ifdokccid
Version:        4.2.8
Release:        4
Summary:        HID OMNIKEY 5421 PCSC Drivers Configuration

Group:          System Environment/Base
License:        Commercial Private License
Vendor:         HID Global
Packager:       Smartrac Technology Fletcher, Inc.
URL:            https://www.hidglobal.com
BuildArch:      x86_64

Source0:        https://www.hidglobal.com/sites/default/files/drivers/%{name}_linux_x86_64-v%{version}.tar.gz

Requires:       bash
Requires:       patch
Requires:       libusb
Requires:       pcsc-lite
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
%setup -q -n %{name}_linux_%{buildarch}-v%{version}

#install -m644 %{_topdir}/Info.plist.patch1 %{_sourcedir}
#install -m644 %{_topdir}/Info.plist.fixed %{_sourcedir}

%build
echo "Nothing to build"

%install
QA_RPATHS=$(( 0x0001|0x0002|0x0010 ))

#
# Install the omnikey.ini file
#
install -d -m755 -p %{buildroot}/%{_sysconfdir}
install -m600 %{_builddir}/%{name}_linux_%{buildarch}-v%{version}/omnikey.ini %{buildroot}/%{_sysconfdir}/omnikey.ini

#
# Install the bundle
#
install -d -m775 -p %{buildroot}/usr/lib64/pcsc/drivers/ifd-ccid.bundle/
cp -r %{_builddir}/%{name}_linux_%{buildarch}-v%{version}/%{name}_linux_%{buildarch}-v%{version}.bundle/Contents %{buildroot}/usr/lib64/pcsc/drivers/ifd-ccid.bundle/
# Relocate the Info.plist to avoid overwriting
mv %{buildroot}/usr/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/Info.plist %{buildroot}/usr/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/Info.plist.fixed

#
# Install udev rules
#
install -d -m755 -p %{buildroot}/%{_sysconfdir}/udev/rules.d/
install -m600 %{_builddir}/%{name}_linux_%{buildarch}-v%{version}/z98_omnikey.rules %{buildroot}/%{_sysconfdir}/udev/rules.d/z98_omnikey.rules

#
# Copy corrected Info.plist to PCSC driver data directory
#
install -d -m755 -p %{buildroot}/%{_prefix}/lib64/pcsc/drivers/ifd-ccid.bundle/Contents

#
# Copy 90-default-privs.rules to /usr/share/polkit-1/rules.d
#
install -d -m755 -p %{buildroot}/%{_prefix}/share/polkit-1/rules.d
install -m644 %{_sourcedir}/90-default-privs.rules %{buildroot}/%{_prefix}/share/polkit-1/rules.d/90-default-privs.rules

%files
%{_sysconfdir}/omnikey.ini
%{_sysconfdir}/udev/rules.d/z98_omnikey.rules
%{_prefix}/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/Info.plist.fixed
%{_prefix}/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/Linux/ifdokccid.so
%{_prefix}/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/tools/ifdok_bugreport
%{_prefix}/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/tools/ifdok_xmled
%{_prefix}/share/polkit-1/rules.d/90-default-privs.rules

%post
getent group hidreader >/dev/null || groupadd -r hidreader
# patch -p1 %{_prefix}/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/Info.plist < %{_prefix}/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/Info.plist.patch1
# Make a backup
cp %{_prefix}/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/Info.plist %{_prefix}/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/Info.plist.rpmnew.%{version}
# Copy the Info.plist.fixed file over the Info.plist
cp %{_prefix}/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/Info.plist.fixed %{_prefix}/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/Info.plist
chmod 644 %{_prefix}/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/Info.plist

# Handle issue where previous folder structure is not removed:
rm -rf /usr/lib64/pcsc/drivers/ifdokccid_linux_x86_64-v4.0.5.5.bundle
rm -rf /usr/lib64/pcsc/drivers/ifdokccid_linux_x86_64-v4.2.8.bundle

%systemd_post pcscd.service

%preun
%systemd_preun pcscd.service

%postun
# Move back original file.
cp %{_prefix}/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/Info.plist.rpmnew.%{version} %{_prefix}/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/Info.plist
rm -rf %{_prefix}/lib64/pcsc/drivers/ifd-ccid.bundle/Contents/Info.plist.rpmnew.%{version}

%systemd_postun_with_restart pcscd.service

%changelog
* Tue Jun 20 2017 Robert Van Voorhees <robert.vanvoorhees@smartrac-group.com> - 4.2.8-4
- Try and more closely resemble ifd-ccid.bundle

* Tue Jun 20 2017 Robert Van Voorhees <robert.vanvoorhees@smartrac-group.com> - 4.2.8-3
- Remove the folder structures on RPM uninstall.

* Tue Jun 20 2017 Robert Van Voorhees <robert.vanvoorhees@smartrac-group.com> - 4.2.8-2
- Overwrite the old Info.plist in a similar fashion.

* Tue Jun 20 2017 Robert Van Voorhees <robert.vanvoorhees@smartrac-group.com> - 4.2.8-1
- Creating an updated version of the drivers.

* Wed May 31 2017 Joe Chromo <joe.chromo@smartrac-group.com> - 1-1
- Added 90-default-privs.rules to provision access to hid reader to smartcomsos user

* Fri May 19 2017 Robert Van Voorhees <robert.vanvoorhees@smartrac-group.com> - 4.0.5.5-3
- Remove unused patch, properly identify Source1, increment release to facilitate proper upgrading.

* Sun Apr 16 2017 Robert Van Voorhees <robert.vanvoorhees@smartrac-group.com> - 1-1
- Initial RPM release
