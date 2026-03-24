%global optflags %{optflags} -Wno-incompatible-function-pointer-types
%undefine _debugsource_packages

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
BuildRequires:	meson
BuildRequires:	ninja
BuildRequires:	rust
BuildRequires:	cargo
BuildRequires:	cargo-c

# Rust target dla 32-bit
%if %{with compat32}
BuildRequires:	rust-std-static rust-src
%endif

BuildRequires:	gdk-pixbuf2.0
BuildRequires:	vala
BuildRequires:	vala-tools
BuildRequires:	vala-devel
BuildRequires:	pkgconfig(vapigen)

BuildRequires:	pkgconfig(cairo) >= 1.15.4
BuildRequires:	pkgconfig(cairo-png) >= 1.15.4
BuildRequires:	pkgconfig(dav1d)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gi-docgen)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libxml-2.0) >= 2.15.2
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(lzo2)
BuildRequires:	python3dist(docutils)

%if %{with compat32}
BuildRequires:	devel(libcairo)
BuildRequires:	devel(libgio-2.0)
BuildRequires:	devel(libglib-2.0)
BuildRequires:	devel(libtiff)
BuildRequires:	devel(libxml2) >= 2.15.2
BuildRequires:	devel(libz)
BuildRequires:	devel(libffi)
BuildRequires:	devel(libgdk_pixbuf-2.0)
BuildRequires:	devel(libpango-1.0)
BuildRequires:	devel(libpng16)
BuildRequires:	devel(libfreetype)
BuildRequires:	devel(libfontconfig)
BuildRequires:	devel(libharfbuzz)
BuildRequires:	devel(libfribidi)
BuildRequires:	devel(libexpat)
BuildRequires:	devel(libjpeg)
BuildRequires:	devel(libXrender)
BuildRequires:	devel(libXft)
BuildRequires:	devel(libpixman-1)
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libX11)
BuildRequires:	devel(libXext)
BuildRequires:	devel(liblzo2)
%endif

Provides:	%{name}%{api} = %{version}-%{release}

%description
A library that uses cairo and pango to render SVG files.

%package -n %{libname}
Summary:	Raph's SVG library
Group:		System/Libraries

%description -n %{libname}
A library that uses cairo and pango to render SVG files.

%package -n %{devname}
Summary:	Development files for librsvg
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
Development files for librsvg.

%package -n %{girname}
Summary:	GObject Introspection data for librsvg
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n %{girname}
GObject Introspection data.

%if %{with compat32}
%package -n %{lib32name}
Summary:	32-bit librsvg
Group:		System/Libraries

%description -n %{lib32name}
A library that uses cairo and pango to render SVG files.


%package -n %{dev32name}
Summary:	32-bit development files
Group:		Development/C
Requires:	%{lib32name} = %{version}-%{release}

%description -n %{dev32name}
A library that uses cairo and pango to render SVG files.

%endif

# --------------------

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

%files
%doc AUTHORS NEWS* README.md
%{_bindir}/rsvg-convert
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

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/gdk-pixbuf-2.0/*/loaders/*.so
%{_prefix}/lib/librsvg-%{api}.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/*.so
%{_prefix}/lib/pkgconfig/*
%endif
