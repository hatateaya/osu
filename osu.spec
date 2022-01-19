%global __os_install_post %{nil}
%define __spec_install_post %{nil}
%undefine _disable_source_fetch
%define debug_package %{nil}
Name:           osu
Version:        2022.118.0
Release:        1%{?dist}
Summary:        A free-to-win rhythm game.

License:        MIT
URL:            https://osu.ppy.sh/
Source0:        https://github.com/ppy/osu/archive/refs/tags/%{version}.tar.gz
Source1:        osu.desktop
Source2:        sh.ppy.osu.appdata.xml
Source3:        x-osu.xml
BuildRequires:  dotnet-sdk-6.0
BuildRequires:  libappstream-glib
Requires:       dotnet

%description
osu! is a free-to-play rhythm game inspired by Osu! Tatakae! Ouendan.

This is the new experimental release of osu! called osu!lazer which is rewritten from the ground up using .NET 5.0.

%prep
%autosetup -n %{name}-%{version}


%build
dotnet build osu.Desktop -p:Configuration=Release -p:GenerateFullPaths=true -m -verbosity:m


%install
rm -rf $RPM_BUILD_ROOT
# install .NET output
mkdir -p $RPM_BUILD_ROOT/opt/osu
cp -r osu.Desktop/bin/Release/net5.0/* $RPM_BUILD_ROOT/opt/osu

#install desktop icons
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/1024x1024/apps/
cp assets/lazer.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/1024x1024/apps/osu.png
# desktop file
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/applications
cp %{SOURCE1} $RPM_BUILD_ROOT/%{_datadir}/applications/osu.desktop

# AppStream metadata
mkdir -p $RPM_BUILD_ROOT/usr/share/appdata
cp -v %{SOURCE2} %{buildroot}/%{_datadir}/appdata/
appstream-util validate-relax --nonet  %{buildroot}/%{_datadir}/appdata/*

# desktop integration
mkdir -p %{buildroot}%{_datadir}/mime/application/
cp -v %{SOURCE3} %{buildroot}%{_datadir}/mime/application/


%files
/opt/osu/*
%{_datadir}/icons/hicolor/1024x1024/apps/osu.png
%{_datadir}/applications/osu.desktop
%{_datadir}/appdata/sh.ppy.osu.appdata.xml
%{_datadir}/mime/application/x-osu.xml

%changelog
* Wed Jan 19 2022 Cappy Ishihara <cappy@cappuchino.xyz>
- Initial release
