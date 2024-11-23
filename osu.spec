%global __os_install_post %{nil}
%undefine _disable_source_fetch
%define debug_package %{nil}
# RPMBuild actually generates alot of requirements that we do not actually use and doesn't actually exist. So we have to disable it. Weird .NET issue.
# We will provide what we have but not require all the weird stuff.
# exclude everything in /opt/osu/ with regex
%global __requires_exclude_from ^/opt/osu/.*$
Name:           osu
Version:        2024.1115.3
Release:        %autorelease
Summary:        A free-to-win rhythm game.

License:        MIT
URL:            https://osu.ppy.sh/
Source1:        osu.desktop
Source2:        sh.ppy.osu.appdata.xml
Source3:        x-osu.xml
BuildRequires:  dotnet-sdk-8.0
BuildRequires:  libappstream-glib
BuildRequires:  wget2
Requires:       dotnet-runtime-8.0

%description
osu! is a free-to-play rhythm game inspired by Osu! Tatakae! Ouendan.

This is the new experimental release of osu! called osu!lazer which is rewritten from the ground up using .NET 5.0.

%prep
cd %_sourcedir
wget2 https://github.com/ppy/osu/archive/refs/tags/2024.1115.3.tar.gz
cd %_builddir
rm -rf osu-%{version}
gzip -dc %_sourcedir/%{version}.tar.gz | tar -xvvf -
mv osu-%{version}/* ./

%build
# dotnet build osu.Desktop -p:Configuration=Release -p:GenerateFullPaths=true -m -verbosity:m
DOTNET_CLI_TELEMETRY_OPTOUT="1" dotnet publish osu.Desktop \
    --framework net8.0 \
    --configuration Release \
    --use-current-runtime \
    --no-self-contained \
    --output output \
    /property:Version="%{version}"

%install
rm -rf $RPM_BUILD_ROOT
# install .NET output
mkdir -p $RPM_BUILD_ROOT/opt/
cp -ax output/ $RPM_BUILD_ROOT/opt/osu/

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

ln -sf /usr/lib/libdl.so.2 "$RPM_BUILD_ROOT/opt/osu/libdl.so"

%files
/opt/osu/*
%{_datadir}/icons/hicolor/1024x1024/apps/osu.png
%{_datadir}/applications/osu.desktop
%{_datadir}/appdata/sh.ppy.osu.appdata.xml
%{_datadir}/mime/application/x-osu.xml

%changelog
%autochangelog
