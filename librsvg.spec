%global optflags %{optflags} -Wno-incompatible-function-pointer-types
%undefine _debugsource_packages

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

Summary:	Raph's SVG library
Name:		librsvg
Version:	2.62.1
Release:	1
License:	LGPLv2+ and GPLv2+
Group:		Graphics
Url:		https://librsvg.sourceforge.net/
Source0:	https://download.gnome.org/sources/librsvg/%{url_ver}/%{name}-%{version}.tar.xz
Source1:	vendor.tar.xz

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool-base
BuildRequires:	slibtool
BuildRequires:	make
BuildRequires:	gdk-pixbuf2.0
BuildRequires:	vala
BuildRequires:	vala-tools
BuildRequires:	vala-devel
BuildRequires:	pkgconfig(vapigen)
BuildRequires:	rust
BuildRequires:	cargo
BuildRequires:	cargo-c
BuildRequires:	meson
BuildRequires:	pkgconfig(cairo) >= 1.15.4
BuildRequires:	pkgconfig(cairo-png) >= 1.15.4
BuildRequires:	pkgconfig(dav1d)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gi-docgen)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0) >= 2.4.0
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libcroco-0.6)
BuildRequires:	pkgconfig(libxml-2.0) >= 2.15.2
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(lzo2)
BuildRequires:	python3dist(docutils)
%ifarch %{x86_64}
# FIXME without this, configure barfs on znver1. Need to find a proper fix.
BuildRequires:	libssh2.so.1()(64bit)
%endif
Provides:	%{name}%{api} = %{version}-%{release}
Requires:	%{libname} >= %{version}
Requires:	python
%if %{with compat32}
BuildRequires:	rust-std-static rust-src
BuildRequires:	devel(libcairo)
BuildRequires:	devel(libgio-2.0)
BuildRequires:	devel(libglib-2.0)
BuildRequires:	devel(libcroco-0.6)
BuildRequires:	devel(libtiff)
BuildRequires:	devel(libxml2) >= 2.15.2
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
BuildRequires:	devel(liblzma)
BuildRequires:	devel(libzstd)
%endif

Provides: rsvg = %{version}-%{release}

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

%if %{with compat32}
%package -n %{lib32name}
Summary:	32-bit Raph's SVG library
Group:		System/Libraries

%description -n %{lib32name}
A library that uses libart and pango to render svg files.

%package -n %{dev32name}
Summary:	32-bit development files
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}

%description -n %{dev32name}
This package provides the necessary development libraries and include
files to allow you to develop with librsvg.
%endif

%prep
%autosetup -p1

tar xf %{S:1}
mkdir .cargo
cat >>.cargo/config.toml <<EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

# --------------------

%build

# --- 64-bit ---
%meson \
    -Dintrospection=enabled \
    -Ddocs=enabled \
    -Dvala=enabled \
    -Dtests=false \
    -Davif=enabled \
    -Dpixbuf=enabled \
    -Dpixbuf-loader=enabled

%meson_build

%if %{with compat32}
# --- 32-bit ---
mkdir build32
pushd build32

export CC="gcc -m32"
export CXX="g++ -m32"
export PKG_CONFIG_LIBDIR=%{_prefix}/lib/pkgconfig

#export CARGO_BUILD_TARGET=i686-unknown-linux-gnu
export CARGO_TARGET_I686_UNKNOWN_LINUX_GNU_LINKER="gcc -m32"
export RUSTFLAGS="-C target-feature=-crt-static"

meson setup . .. \
    --libdir=%{_prefix}/lib \
    --prefix=%{_prefix} \
    -Dintrospection=disabled \
    -Ddocs=disabled \
    -Dvala=disabled \
    -Dtests=false \
    -Davif=enabled \
    -Dpixbuf=enabled \
    -Dpixbuf-loader=enabled

ninja %{?_smp_mflags}

popd
%endif

# --------------------

%install

%meson_install

%if %{with compat32}
pushd build32
DESTDIR=%{buildroot} ninja install
popd
%endif

rm -rf %{buildroot}%{_docdir}/librsvg

# --------------------

#remove unpackaged files
rm -fr %{buildroot}%{_docdir}/librsvg

%files
%doc AUTHORS NEWS* README.md
%{_bindir}/rsvg-convert
%{_datadir}/thumbnailers/*.thumbnailer
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/gdk-pixbuf-2.0/*/loaders/*.so
%{_libdir}/librsvg-%{api}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/*.typelib

%files -n %{devname}
%{_libdir}/*.so
%{_includedir}/librsvg-2.0
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/Rsvg-2.0.gir

%files vala-devel
%doc %{_docdir}/Rsvg-2.0
%{_datadir}/vala/vapi/librsvg-2.0.vapi
%{_datadir}/vala/vapi/librsvg-2.0.deps

%if %{with compat32}
%files -n %{lib32name}
#{_prefix}/lib/gdk-pixbuf-2.0/*/loaders/*.so
%{_prefix}/lib/librsvg-%{api}.so.%{major}*

%files -n %{dev32name}
%doc %{_datadir}/doc/Rsvg-2.0/
%{_prefix}/lib/*.so
%{_prefix}/lib/pkgconfig/*
%endif
