#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
#
Summary:	A tool to manage Windows dynamic disks
Summary(pl.UTF-8):	Narzędzie do zarządzania dynamicznymi dyskami Windows
Name:		libldm
Version:	0.2.5
Release:	1
License:	LGPL v3+ (libldm), GPL v3+ (ldmtool)
Group:		Libraries
Source0:	https://github.com/mdbooth/libldm/archive/%{name}-%{version}.tar.gz
# Source0-md5:	ab38c1a47275eebb9c9cbcaf16220636
URL:		https://github.com/mdbooth/libldm/
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake >= 1.6
BuildRequires:	device-mapper-devel >= 1.0
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	json-glib-devel >= 0.14.0
BuildRequires:	libtool >= 2:2
BuildRequires:	libuuid-devel >= 2.21.0
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	zlib-devel >= 1.2.5
Requires:	device-mapper >= 1.0
Requires:	glib2 >= 1:2.32.0
Requires:	json-glib >= 0.14.0
Requires:	libuuid >= 2.21.0
Requires:	zlib >= 1.2.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libldm is a library for managing Microsoft Windows dynamic disks,
which use Microsoft's LDM metadata. It can inspect them, and also
create and remove device-mapper block devices which can be mounted. It
includes ldmtool, which exposes this functionality as a command-line
tool.

%description -l pl.UTF-8
libldm to biblioteka do zarządzania dyskami dynamicznymi Microsoft
Windows, wykorzystującymi metadane Microsoft LDM. Biblioteka potrafi
odczytywać informacje o nich, a także tworzyć i usuwać urządzenia
blokowe device-mappera, które następnie można zamontować. Pakiet
zawiera także program ldmtool, udostępniający funkcjonalność
biblioteki w postaci narzędzia linii poleceń.

%package devel
Summary:	Header files for libldm library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libldm
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	device-mapper-devel >= 1.0
Requires:	glib2-devel >= 1:2.32.0
Requires:	json-glib-devel >= 0.14.0
Requires:	libuuid-devel >= 2.21.0
Requires:	zlib-devel >= 1.2.5

%description devel
Header files for libldm library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libldm.

%package static
Summary:	Static libldm library
Summary(pl.UTF-8):	Statyczna biblioteka libldm
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libldm library.

%description static -l pl.UTF-8
Statyczna biblioteka libldm.

%package apidocs
Summary:	libldm API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libldm
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
API documentation for libldm library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libldm.

%prep
%setup -q -n %{name}-%{name}-%{version}

%build
sed -i -e 's/-Werror //' src/Makefile.*
%{__gtkdocize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_apidocs:--enable-gtk-doc} \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libldm-1.0.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ldmtool
%attr(755,root,root) %{_libdir}/libldm-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libldm-1.0.so.0
%{_mandir}/man1/ldmtool.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libldm-1.0.so
%{_includedir}/ldm.h
%{_pkgconfigdir}/ldm-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libldm-1.0.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libldm
%endif
