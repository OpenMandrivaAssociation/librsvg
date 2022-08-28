# rsvg is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define url_ver %(echo %{version}|cut -d. -f1,2)

%define api 2
%define major 2
%define gimajor 2.0
%define libname %mklibname rsvg %{api} %{major}
%define devname %mklibname -d rsvg %{api}
%define girname %mklibname rsvg-gir %{gimajor}
%define lib32name %mklib32name rsvg %{api} %{major}
%define dev32name %mklib32name -d rsvg %{api}

# mozilla plugin requires xulruuner 1.8 not 1.9
%define build_mozilla 0
%define _disable_rebuild_configure 1

Summary:	Raph's SVG library
Name:		librsvg
Version:	2.54.5
Release:	1
License:	LGPLv2+ and GPLv2+
Group:		Graphics
Url:		http://librsvg.sourceforge.net/
Source0:	http://download.gnome.org/sources/librsvg/%{url_ver}/%{name}-%{version}.tar.xz
# This is the last version that doesn't use rust. Needed while
# rust fails badly at crosscompiling or any other -m32 alternative.
Source1:	http://download.gnome.org/sources/librsvg/2.40/librsvg-2.40.21.tar.xz
BuildRequires:	gdk-pixbuf2.0
BuildRequires:	vala
BuildRequires:	vala-tools
BuildRequires:	vala-devel
BuildRequires:	pkgconfig(vapigen)
BuildRequires:	rust
BuildRequires:	cargo
BuildRequires:	pkgconfig(cairo) >= 1.15.4
BuildRequires:	pkgconfig(cairo-png) >= 1.15.4
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gi-docgen)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0) >= 2.4.0
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libcroco-0.6)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(lzo2)
BuildRequires:	python3dist(docutils)
Provides:	%{name}%{api} = %{version}-%{release}
Requires:	%{libname} >= %{version}
Requires:	python
%if %{with compat32}
BuildRequires:	devel(libcairo)
BuildRequires:	devel(libgio-2.0)
BuildRequires:	devel(libglib-2.0)
BuildRequires:	devel(libcroco-0.6)
BuildRequires:	devel(libtiff)
BuildRequires:	devel(libxml2)
BuildRequires:	devel(libz)
BuildRequires:	devel(libbz2)
BuildRequires:	devel(libffi)
BuildRequires:	devel(libblkid)
BuildRequires:	devel(libmount)
BuildRequires:	devel(libuuid)
BuildRequires:	devel(libgdk_pixbuf-2.0)
BuildRequires:	devel(libpangocairo-1.0)
BuildRequires:	devel(libpangoft2-1.0)
BuildRequires:	devel(libpng16)
BuildRequires:	devel(libpango-1.0)
BuildRequires:	devel(libfreetype)
BuildRequires:	devel(libfontconfig)
BuildRequires:	devel(libharfbuzz)
BuildRequires:	devel(libfribidi)
BuildRequires:	devel(libexpat)
BuildRequires:	devel(libjpeg)
BuildRequires:	devel(libXrender)
BuildRequires:	devel(libXft)
BuildRequires:	devel(libpixman-1)
BuildRequires:	devel(libxcb-shm)
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libxcb-render)
BuildRequires:	devel(libX11)
BuildRequires:	devel(libXext)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libXdmcp)
BuildRequires:	devel(liblzo2)
%endif

%description
A library that uses libart and pango to render svg files.

%package -n %{libname}
Summary:	Raph's SVG library
Group:		System/Libraries
Requires(post):	gdk-pixbuf2.0
Requires(postun):gdk-pixbuf2.0

%description -n %{libname}
A library that uses libart and pango to render svg files.

%package -n %{devname}
Summary:	Libraries and include files for developing with librsvg
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}%{api}-devel = %{version}-%{release}
Obsoletes:	%{mklibname -d rsvg 2 2} < 2.36.1

%description -n %{devname}
This package provides the necessary development libraries and include
files to allow you to develop with librsvg.

%package vala-devel
Summary:	VALA bindings for librsvg
Group:		Development/Other
Requires:	%{devname} = %{EVRD}

%description vala-devel
VALA bindings for librsvg

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n %{girname}
GObject Introspection interface description for %{name}.

%if %{build_mozilla}
%package mozilla
Summary:	Mozilla plugin for displaying SVG files
Group:		Networking/WWW
BuildRequires:	xulrunner-devel

%description mozilla
This package provides the necessary development libraries and include
files to allow you to develop with librsvg.
%endif

%if %{with compat32}
%package -n %{lib32name}
Summary:	Raph's SVG library
Group:		System/Libraries

%description -n %{lib32name}
A library that uses libart and pango to render svg files.

%package -n %{dev32name}
Summary:	Libraries and include files for developing with librsvg
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}

%description -n %{dev32name}
This package provides the necessary development libraries and include
files to allow you to develop with librsvg.
%endif

%prep
%autosetup -p1 -b 1
%if %{with compat32}
REALTOP="$(pwd)"
cd ../librsvg-2.40.21
export CONFIGURE_TOP="$(pwd)"
mkdir build32
cd build32
%configure32 \
	--host=i686-unknown-linux-gnu \
	--target=i686-unknown-linux-gnu \
	--disable-introspection \
	--disable-gtk-doc \
	--disable-vala \
	--enable-pixbuf-loader
cd "${REALTOP}"
%endif

export CONFIGURE_TOP="$(pwd)"
mkdir build
cd build
%configure \
	--enable-introspection=yes \
	--disable-gtk-doc \
	--enable-vala \
	--enable-pixbuf-loader

%build
%if %{with compat32}
%make_build -C ../librsvg-2.40.21/build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C ../librsvg-2.40.21/build32
%endif
%make_install -C build

#remove unpackaged files
rm -fr %{buildroot}%{_docdir}/librsvg
%if %{build_mozilla}
rm -f %{buildroot}%{_libdir}/mozilla/
%endif
rm -f %{buildroot}%{_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders
rm -f %{buildroot}%{_datadir}/pixmaps/svg-viewer.svg

#find_lang %{name}

%files
%doc AUTHORS NEWS* README.md
%{_bindir}/rsvg-convert
#{_bindir}/rsvg-view-3
#{_libdir}/gtk-2.0/*/engines/*.so
#{_datadir}/themes/bubble/gtk-2.0/*
%{_datadir}/thumbnailers/*.thumbnailer
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/gdk-pixbuf-2.0/*/loaders/*.so
%{_libdir}/librsvg-%{api}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Rsvg-%{gimajor}.typelib

%files -n %{devname}
%{_libdir}/*.so
%{_includedir}/librsvg-2.0
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/Rsvg-2.0.gir
%optional %{_datadir}/gtk-doc/html/*

%files vala-devel
%{_datadir}/vala/vapi/librsvg-2.0.vapi

%if %{build_mozilla}
%files mozilla
%{_libdir}/mozilla/plugins/*.so
%endif

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/gdk-pixbuf-2.0/*/loaders/*.so
%{_prefix}/lib/librsvg-%{api}.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/*.so
%{_prefix}/lib/pkgconfig/*
%endif
