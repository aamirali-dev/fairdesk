Name:       fairdesk 
Version:    1.2.2
Release:    0
Summary:    RPM package
License:    GPL-3.0
Requires:   gtk3 libxcb libxdo libXfixes alsa-lib libappindicator-gtk3 libvdpau libva pam gstreamer1-plugins-base
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

%description
The best open-source remote desktop client software, written in Rust. 

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/lib/fairdesk" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/lib/fairdesk"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/fairdesk.service -t "%{buildroot}/usr/share/fairdesk/files"
install -Dm 644 $HBB/res/fairdesk.desktop -t "%{buildroot}/usr/share/fairdesk/files"
install -Dm 644 $HBB/res/fairdesk-link.desktop -t "%{buildroot}/usr/share/fairdesk/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/fairdesk/files/fairdesk.png"

%files
/usr/lib/fairdesk/*
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
ln -s /usr/lib/fairdesk/fairdesk /usr/bin/fairdesk 
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
    rm /usr/bin/fairdesk || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
