#
# Conditional build:
%bcond_with	gnome		# GNOME 2.x desktop entry and vfs backends

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
Patch1:		%{name}-waf.patch
Patch2:		%{name}-vala.patch
URL:		https://launchpad.net/libdesktop-agnostic
BuildRequires:	GConf2-devel >= 2.0
BuildRequires:	gettext-tools
BuildRequires:	glade-devel >= 3
BuildRequires:	glib2-devel >= 1:2.18.0
%{?with_gnome:BuildRequires:	gnome-desktop2-devel >= 2.0}
%{?with_gnome:BuildRequires:	gnome-vfs2-devel >= 2.6.0}
BuildRequires:	gobject-introspection-devel >= 0.6.3
BuildRequires:	gtk+2-devel >= 2:2.12.0
BuildRequires:	intltool
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	python-pygobject-devel >= 2.15.2
BuildRequires:	python-pygtk-devel >= 2:2.12.0
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	vala >= 0.10
BuildRequires:	waf >= 2
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
# Use gladeui-2.0, not glade-1.0
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
export CFLAGS="%{rpmcflags}"
export LINKFLAGS="%{rpmldflags} -fcommon"
export WAFDIR=/usr/share/waf3
PYTHONDIR=%{py_sitedir} \
%{__python} /usr/bin/waf configure \
	  --prefix=%{_prefix} \
	  --libdir=%{_libdir} \
	  --sysconfdir=%{_sysconfdir} \
	  --enable-debug \
	  --config-backends=gconf \
	  --desktop-entry-backends=glib%{?with_gnome:,gnome} \
	  --vfs-backends=gio%{?with_gnome:,gnome} \
	  --with-glade

%{__python} /usr/bin/waf -v build

%install
rm -rf $RPM_BUILD_ROOT

export WAFDIR=/usr/share/waf3

DESTDIR=$RPM_BUILD_ROOT \
%{__python} /usr/bin/waf install

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

# fix permissions so debuginfo is stripped from .so files
find $RPM_BUILD_ROOT%{_libdir} -name *.so -exec chmod 755 {} \;

# joke locale
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/en_US@piglatin

#%%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
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
%dir /etc/xdg/libdesktop-agnostic
%config(noreplace) /etc/xdg/libdesktop-agnostic/desktop-agnostic.ini

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

%files devel
%defattr(644,root,root,755)
%{_libdir}/libdesktop-agnostic-ui.so
%{_libdir}/libdesktop-agnostic-cfg.so
%{_libdir}/libdesktop-agnostic-fdo.so
%{_libdir}/libdesktop-agnostic-vfs.so
%{_libdir}/libdesktop-agnostic.so
%{_includedir}/libdesktop-agnostic-1.0
%{_pkgconfigdir}/desktop-agnostic.pc
%{_datadir}/pygtk/2.0/defs/desktopagnostic*defs
%{_datadir}/vala/vapi/desktop-agnostic*
%{_datadir}/glade/catalogs/desktop-agnostic.xml

%files -n python-desktop-agnostic
%defattr(644,root,root,755)
%dir %{py_sitedir}/desktopagnostic
%attr(755,root,root) %{py_sitedir}/desktopagnostic/config.so
%attr(755,root,root) %{py_sitedir}/desktopagnostic/desktopagnostic.so
%attr(755,root,root) %{py_sitedir}/desktopagnostic/fdo.so
%attr(755,root,root) %{py_sitedir}/desktopagnostic/ui.so
%attr(755,root,root) %{py_sitedir}/desktopagnostic/vfs.so
%{py_sitedir}/desktopagnostic/*.py[co]
