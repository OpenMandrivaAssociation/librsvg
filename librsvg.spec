%define url_ver %(echo %{version}|cut -d. -f1,2)

%define api 2
%define major 2
%define gimajor 2.0
%define libname %mklibname rsvg %{api} %{major}
%define devname %mklibname -d rsvg %{api}
%define girname %mklibname rsvg-gir %{gimajor}

# mozilla plugin requires xulruuner 1.8 not 1.9
%define build_mozilla 0
%define _disable_rebuild_configure 1

Summary:	Raph's SVG library
Name:		librsvg
Version:	2.48.4
Release:	1
License:	LGPLv2+ and GPLv2+
Group:		Graphics
Url:		http://librsvg.sourceforge.net/
Source0:	http://download.gnome.org/sources/librsvg/%{url_ver}/%{name}-%{version}.tar.xz
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
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0) >= 2.4.0
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libcroco-0.6)
BuildRequires:	pkgconfig(libxml-2.0)
Provides:	%{name}%{api} = %{version}-%{release}
Requires:	%{libname} >= %{version}
Requires:	python

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
Provides:	%{name}-devel = %{version}-%{release}
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

%prep
%autosetup -p1

%build
%configure \
	--disable-static \
	--enable-introspection=yes \
	--disable-gtk-doc \
	--enable-vala \
	--enable-pixbuf-loader

%make_build

%install
%make_install

#remove unpackaged files
rm -fr %{buildroot}%{_docdir}/librsvg
%if %{build_mozilla}
rm -f %{buildroot}%{_libdir}/mozilla/
%endif
rm -f %{buildroot}%{_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders
rm -f %{buildroot}%{_datadir}/pixmaps/svg-viewer.svg

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS NEWS README.md
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
%{_datadir}/gtk-doc/html/*

%files vala-devel
%{_datadir}/vala/vapi/librsvg-2.0.vapi

%if %{build_mozilla}
%files mozilla
%{_libdir}/mozilla/plugins/*.so
%endif

