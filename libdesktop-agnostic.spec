Summary:	Provides an extensible configuration API
Summary(pl.UTF-8):	Rozszerzalne API konfiguracyjne
Name:		libdesktop-agnostic
Version:	0.3.92
Release:	6
License:	GPL v2+ and LGPL v2+
Group:		Libraries
Source0:	https://launchpad.net/libdesktop-agnostic/0.4/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	42374d226a21d57637f97173f6b105a1
Patch0:		gladeui.patch
URL:		https://launchpad.net/libdesktop-agnostic
BuildRequires:	GConf2-devel
BuildRequires:	gettext
BuildRequires:	glade-devel >= 3
BuildRequires:	gnome-desktop-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk+-devel
BuildRequires:	intltool
BuildRequires:	python-devel
BuildRequires:	python-pygtk-devel
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	vala
#BuildRequires:  waf
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library provides an extensible configuration API. A unified
virtual file system API, and a desktop item editor.

%description -l pl.UTF-8
Ta biblioteka udostępnia rozszerzalne API konfiguracyjne: ujednolicone
API wirtualnego systemu plików oraz edytor elementów pulpitu.

%package progs
Summary:	Helper applications for libdesktop-agnostic
Summary(pl.UTF-8):	Aplikacje pomocnicze dla biblioteki libdesktop-agnostic
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description progs
This package contains helper applications for libdesktop-agnostic,
such as a schema converter.

%description progs -l pl.UTF-8
Ten pakiet zawiera aplikacje pomocnicze dla biblioteki
libdesktop-agnostic, takie jak konwerter schematów.

%package devel
Summary:	Development files for libdesktop-agnostic library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libdesktop-agnostic
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-progs = %{version}-%{release}

%description devel
This package contains the header files for developing applications
that use libdesktop-agnostic library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę libdesktop-agnostic.

%package -n python-desktop-agnostic
Summary:	Python bindings for libdesktop-agnostic
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki libdesktop-agnostic
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description -n python-desktop-agnostic
This package contains the Python bindings for the core library.

%description -n python-desktop-agnostic -l pl.UTF-8
Ten pakiet zawiera wiązania Pythona do głównej biblioteki.

%prep
%setup -q
#Use gladeui-2.0, not glade-1.0
%patch0 -p1

%build
export CFLAGS="%{rpmcflags}"
PYTHONDIR=%{py_sitedir} \
./waf configure \
	  --prefix=%{_prefix} \
	  --libdir=%{_libdir} \
	  --sysconfdir=%{_sysconfdir} \
	  --enable-debug \
	  --config-backends=gconf \
	  --vfs-backends=gio \
	  --desktop-entry-backends=glib \
	  --with-glade
#	  --disable-gi

./waf -v build

%install
rm -rf $RPM_BUILD_ROOT

DESTDIR=$RPM_BUILD_ROOT \
./waf install

# install man files
#install -d $RPM_BUILD_ROOT%{_mandir}/man1/
#install -D -p -m 0644 debian/lda*1 $RPM_BUILD_ROOT%{_mandir}/man1

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

# fix permissions so debuginfo is stripped from .so files
find $RPM_BUILD_ROOT%{_libdir} -name *.so -exec chmod 755 {} \;

# noidea
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/en_US@piglatin

#%%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%dir /etc/xdg/libdesktop-agnostic
%config(noreplace) /etc/xdg/libdesktop-agnostic/desktop-agnostic.ini
%attr(755,root,root) %{_libdir}/libdesktop-agnostic.so.*.*.*
%ghost %{_libdir}/libdesktop-agnostic.so.0
%attr(755,root,root) %{_libdir}/libdesktop-agnostic-cfg.so.*.*.*
%ghost %{_libdir}/libdesktop-agnostic-cfg.so.0
%attr(755,root,root) %{_libdir}/libdesktop-agnostic-fdo.so.*.*.*
%ghost %{_libdir}/libdesktop-agnostic-fdo.so.0
%attr(755,root,root) %{_libdir}/libdesktop-agnostic-ui.so.*.*.*
%ghost %{_libdir}/libdesktop-agnostic-ui.so.0
%attr(755,root,root) %{_libdir}/libdesktop-agnostic-vfs.so.*.*.*
%ghost %{_libdir}/libdesktop-agnostic-vfs.so.0

%dir %{_libdir}/desktop-agnostic
%dir %{_libdir}/desktop-agnostic/modules
%attr(755,root,root) %{_libdir}/desktop-agnostic/modules/libda-cfg-gconf.so
%attr(755,root,root) %{_libdir}/desktop-agnostic/modules/libda-cfg-type-color.so
%attr(755,root,root) %{_libdir}/desktop-agnostic/modules/libda-fdo-glib.so
%attr(755,root,root) %{_libdir}/desktop-agnostic/modules/libda-module-guesser.so
%attr(755,root,root) %{_libdir}/desktop-agnostic/modules/libda-vfs-gio.so

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lda-desktop-entry-editor
%attr(755,root,root) %{_bindir}/lda-schema-to-gconf
#%{_mandir}/man1/lda*1.gz

%files devel
%defattr(644,root,root,755)
%{_includedir}/libdesktop-agnostic-1.0
%{_datadir}/pygtk/2.0/defs/desktopagnostic*defs
%{_datadir}/vala/vapi/desktop-agnostic*
%{_datadir}/glade/catalogs/desktop-agnostic.xml
%{_pkgconfigdir}/desktop-agnostic.pc
%{_libdir}/libdesktop-agnostic-ui.so
%{_libdir}/libdesktop-agnostic-cfg.so
%{_libdir}/libdesktop-agnostic-fdo.so
%{_libdir}/libdesktop-agnostic-vfs.so
%{_libdir}/libdesktop-agnostic.so

%files -n python-desktop-agnostic
%defattr(644,root,root,755)
%dir %{py_sitedir}/desktopagnostic
%{py_sitedir}/desktopagnostic/*.py[co]
%attr(755,root,root) %{py_sitedir}/desktopagnostic/config.so
%attr(755,root,root) %{py_sitedir}/desktopagnostic/desktopagnostic.so
%attr(755,root,root) %{py_sitedir}/desktopagnostic/fdo.so
%attr(755,root,root) %{py_sitedir}/desktopagnostic/ui.so
%attr(755,root,root) %{py_sitedir}/desktopagnostic/vfs.so
