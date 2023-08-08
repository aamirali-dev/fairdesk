Name:       fairdesk 
Version:    1.1.9
Release:    0
Summary:    RPM package
License:    GPL-3.0
Requires:   gtk3 libxcb1 xdotool libXfixes3 alsa-utils libXtst6 libayatana-appindicator3-1 libvdpau1 libva2 pam gstreamer-plugins-base gstreamer-plugin-pipewire

%description
The best open-source remote desktop client software, written in Rust. 

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/lib/fairdesk/
mkdir -p %{buildroot}/usr/share/fairdesk/files/
install -m 755 $HBB/target/release/fairdesk %{buildroot}/usr/bin/fairdesk
install $HBB/libsciter-gtk.so %{buildroot}/usr/lib/fairdesk/libsciter-gtk.so
install $HBB/res/fairdesk.service %{buildroot}/usr/share/fairdesk/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/fairdesk/files/fairdesk.png
install $HBB/res/fairdesk.desktop %{buildroot}/usr/share/fairdesk/files/
install $HBB/res/fairdesk-link.desktop %{buildroot}/usr/share/fairdesk/files/

%files
/usr/bin/fairdesk
/usr/lib/fairdesk/libsciter-gtk.so
/usr/share/fairdesk/files/fairdesk.service
/usr/share/fairdesk/files/fairdesk.png
/usr/share/fairdesk/files/fairdesk.desktop
/usr/share/fairdesk/files/fairdesk-link.desktop

%changelog
# let's skip this for now

# https://www.cnblogs.com/xingmuxin/p/8990255.html
%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop fairdesk || true
  ;;
esac

%post
cp /usr/share/fairdesk/files/fairdesk.service /etc/systemd/system/fairdesk.service
cp /usr/share/fairdesk/files/fairdesk.desktop /usr/share/applications/
cp /usr/share/fairdesk/files/fairdesk-link.desktop /usr/share/applications/
systemctl daemon-reload
systemctl enable fairdesk
systemctl start fairdesk
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop fairdesk || true
    systemctl disable fairdesk || true
    rm /etc/systemd/system/fairdesk.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/fairdesk.desktop || true
    rm /usr/share/applications/fairdesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
