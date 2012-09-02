%define api_version	2
%define lib_major	2
%define gir_major	2.0
%define lib_name	%mklibname rsvg %{api_version} %{lib_major}
%define develname	%mklibname -d rsvg %{api_version}
%define girname		%mklibname rsvg-gir %{gir_major}

# mozilla plugin requires xulruuner 1.8 not 1.9
%define build_mozilla 0

Name:		librsvg
Summary:	Raph's SVG library
Version:	2.36.3
Release: 	1
License: 	LGPLv2+ and GPLv2+
Group:		Graphics
Source0: 	ftp://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.xz
URL: 		http://librsvg.sourceforge.net/
BuildRequires:	pkgconfig(gtk+-2.0) >= 2.4.0
BuildRequires:  gdk-pixbuf2.0
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libcroco-0.6)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	docbook-dtd31-sgml

Provides:	%{name}%{api_version} = %{version}-%{release}
Requires:	%{lib_name} >= %{version}
Requires:	python

%description
A library that uses libart and pango to render svg files.

%package -n %{lib_name}
Summary:	Raph's SVG library
Group:		System/Libraries

%description -n %{lib_name}
A library that uses libart and pango to render svg files.

%package -n %{develname}
Summary:	Libraries and include files for developing with librsvg
Group:		Development/C
Requires:	%{lib_name} = %{version}-%{release}
Provides:	%{name}%{api_version}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname -d rsvg 2 2

%description -n %{develname}
This package provides the necessary development libraries and include
files to allow you to develop with librsvg.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Requires:	%{lib_name} = %{version}-%{release}

%description -n %{girname}
GObject Introspection interface description for %{name}.

%if %build_mozilla
%package mozilla
Summary:        Mozilla plugin for displaying SVG files
Group:          Networking/WWW
BuildRequires:	xulrunner-devel

%description mozilla
This package provides the necessary development libraries and include
files to allow you to develop with librsvg.
%endif

%prep
%setup -q

%build
%configure2_5x \
	--disable-static \
	--enable-introspection=yes

%make

%install
rm -rf %{buildroot}
%makeinstall_std
find %{buildroot} -name "*.la" -delete

#remove unpackaged files
rm -fr %{buildroot}%{_docdir}/librsvg

%files 
%doc AUTHORS COPYING COPYING.LIB ChangeLog NEWS README
%{_bindir}/rsvg-convert
%{_bindir}/rsvg-view-3
%{_libdir}/gtk-2.0/*/engines/*.so
%{_datadir}/themes/bubble/gtk-2.0/*
%{_mandir}/man1/*

%files -n %{lib_name}
%{_libdir}/gdk-pixbuf-2.0/*/loaders/*.so
%{_libdir}/librsvg-%{api_version}.so.%{lib_major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Rsvg-%{gir_major}.typelib

%files -n %{develname}
%{_libdir}/*.so
%{_includedir}/librsvg-2.0
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/Rsvg-2.0.gir
%{_datadir}/gtk-doc/html/*

%if %build_mozilla
%files mozilla
%{_libdir}/mozilla/plugins/*.so
%endif

