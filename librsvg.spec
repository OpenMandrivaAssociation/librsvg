%define api_version 2
%define lib_major 2
%define lib_name %mklibname rsvg %{api_version} %{lib_major}
%define libnamedev %mklibname -d rsvg %{api_version}

# mozilla plugin requires xulruuner 1.8 not 1.9
%define build_mozilla 0
%define build_gtk3 0

Name:		librsvg
Summary:	Raph's SVG library
Version:	2.34.0
Release: 	%mkrel 2
License: 	LGPLv2+ and GPLv2+
Group:		Graphics
Source0: 	ftp://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
URL: 		http://librsvg.sourceforge.net/
Requires:	%{lib_name} >= %{version}
BuildRequires:	gtk+2-devel >= 2.4.0
%if %build_gtk3
BuildRequires:	gtk+3.0-devel
%endif
BuildRequires:	libcroco0.6-devel
BuildRequires:	libxml2-devel
BuildRequires:	gtk-doc >= 0.9
BuildRequires:	docbook-dtd31-sgml
Requires:	python
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
A library that uses libart and pango to render svg files.

#-----------------------------------------------------------

%package -n %{lib_name}
Summary:	Raph's SVG library
Group:		System/Libraries
Provides:	%{name}%{api_version} = %{version}-%{release}
Conflicts: %name < 2.16.1-2

%description -n %{lib_name}
A library that uses libart and pango to render svg files.

#-----------------------------------------------------------

%package -n %{libnamedev}
Summary:	Libraries and include files for developing with librsvg
Group:		Development/C
Requires:	%{lib_name} = %{version}-%{release}
Provides:	%{name}%{api_version}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname -d rsvg 2 2

%description -n %{libnamedev}
This package provides the necessary development libraries and include
files to allow you to develop with librsvg.

#-----------------------------------------------------------
%if %build_gtk3
%package gtk3
Summary:        gtk3 related stuff of librsvg
Group:          Graphics
Requires:       %{lib_name} = %{version}-%{release}

%description gtk3
This package provides gtk3 version of rsvg-viewer and themes.
%endif

#-----------------------------------------------------------
%if %build_mozilla
%package mozilla
Summary:        Mozilla plugin for displaying SVG files
Group:          Networking/WWW
BuildRequires:	xulrunner-devel

%description mozilla
This package provides the necessary development libraries and include
files to allow you to develop with librsvg.
%endif

#-----------------------------------------------------------

%prep
%setup -q

%build
%configure2_5x --enable-gtk-doc
%make

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT
%makeinstall_std

#remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/*/*/*/*.{la,a} \
%if %build_mozilla
 $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins/*.{la,a} \
%endif
 $RPM_BUILD_ROOT%{_docdir}/librsvg

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

#-----------------------------------------------------------

%files 
%defattr(-, root, root)
%doc AUTHORS COPYING COPYING.LIB ChangeLog NEWS README
%{_bindir}/rsvg
%{_bindir}/rsvg-convert
%{_bindir}/rsvg-view
%{_datadir}/pixmaps/*
%{_datadir}/themes/bubble/gtk-2.0/*
%{_mandir}/man1/*

%files -n %{lib_name}
%defattr(-, root, root)
%{_libdir}/librsvg-%{api_version}.so.%{lib_major}*
%{_libdir}/gtk-2.0/*/engines/*.so
%{_libdir}/gdk-pixbuf-2.0/*/loaders/*.so

%files -n %{libnamedev}
%defattr(-,root,root)
%attr(644,root,root) %{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/librsvg-2.0
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc/html/*

%if %build_gtk3
%files gtk3
%defattr(-,root,root)
%{_bindir}/rsvg-view-3
%{_datadir}/themes/bubble/gtk-3.0/*
%endif

%if %build_mozilla
%files mozilla
%defattr(-,root,root)
%{_libdir}/mozilla/plugins/*.so
%endif
