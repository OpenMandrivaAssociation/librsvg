%define api_version 2
%define lib_major 2
%define gtkbinaryver %(if $([ -x %{_bindir}/pkg-config ] && pkg-config --exists gtk+-2.0); then pkg-config --variable=gtk_binary_version gtk+-2.0; else echo 0; fi)
%define gtkver %(if $([ -x %{_bindir}/pkg-config ] && pkg-config --exists gtk+-2.0); then pkg-config --modversion gtk+-2.0; else echo 0; fi)
%define lib_name %mklibname rsvg %{api_version} %{lib_major}
%define libnamedev %mklibname -d rsvg %{api_version}

Name:		librsvg
Summary:	Raph's SVG library
Version:	2.22.2
Release: 	%mkrel 3
License: 	LGPL
Group:		System/Libraries
Source0: 	ftp://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
URL: 		http://librsvg.sourceforge.net/
Requires:	%{lib_name} >= %{version}
BuildRequires:	gtk+2-devel >= 2.4.0
BuildRequires:	libart_lgpl-devel
BuildRequires:	libgsf-devel
BuildRequires:	libcroco0.6-devel
BuildRequires:	gtk-doc >= 0.9
BuildRequires:	docbook-dtd31-sgml
BuildRequires:	mozilla-firefox-devel
BuildRequires:	glib2-devel >= 2.11
BuildRequires:	libxt-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
A library that uses libart and pango to render svg files.

#-----------------------------------------------------------

%package -n %{lib_name}
Summary:	Raph's SVG library
Group:		System/Libraries
Provides:	%{name}%{api_version} = %{version}-%{release}
Conflicts: %name < 2.16.1-2
Requires:		gtk+2.0 >= %gtkver
Requires(post):		gtk+2.0 >= %gtkver
Requires(postun):	gtk+2.0 >= %gtkver

%description -n %{lib_name}
A library that uses libart and pango to render svg files.

%post -n %{lib_name}
%if %mdkversion < 200900
/sbin/ldconfig
%endif
%{_bindir}/gdk-pixbuf-query-loaders %_lib > %{_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders.%_lib

%postun -n %{lib_name}
%if %mdkversion < 200900
/sbin/ldconfig
%endif
#only update on uninstall, upgrade will be done by post of new package
if [ "$1" = "0" -a -x %{_bindir}/gdk-pixbuf-query-loaders ]; then 
  [ -x %{_bindir}/gdk-pixbuf-query-loaders ] && %{_bindir}/gdk-pixbuf-query-loaders %_lib > %{_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders.%_lib
fi

#-----------------------------------------------------------

%package -n %{libnamedev}
Summary:	Libraries and include files for developing with librsvg
Group:		Development/C
Requires:	%{lib_name} = %{version}
Provides:	%{name}%{api_version}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:  %mklibname -d rsvg %{api_version} %{lib_major}

%description -n %{libnamedev}
This package provides the necessary development libraries and include
files to allow you to develop with librsvg.

#-----------------------------------------------------------

%package mozilla
Summary:        Mozilla plugin for displaying SVG files
Group:          Networking/WWW

%description mozilla
This package provides the necessary development libraries and include
files to allow you to develop with librsvg.

#-----------------------------------------------------------

%prep
%setup -q

%build
export LIBS="-lm"

%configure2_5x --enable-gtk-doc
%make

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT
%makeinstall_std

#remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/%{gtkbinaryver}/*/*.{la,a} \
 $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins/*.{la,a} \
 $RPM_BUILD_ROOT%{_docdir}/librsvg

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT


#-----------------------------------------------------------

%files 
%defattr(-, root, root)
%doc AUTHORS COPYING COPYING.LIB ChangeLog NEWS README
%{_bindir}/rsvg*
%{_datadir}/pixmaps/*
%{_mandir}/man1/*

%files -n %{lib_name}
%defattr(-, root, root)
%{_libdir}/librsvg-%{api_version}.so.%{lib_major}*
%{_libdir}/gtk-2.0/%{gtkbinaryver}/engines/*.so
%{_libdir}/gtk-2.0/%{gtkbinaryver}/loaders/*.so

%files -n %{libnamedev}
%defattr(-,root,root)
%attr(644,root,root) %{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/librsvg-%{api_version}
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc/html/*

%files mozilla
%defattr(-,root,root)
%{_libdir}/mozilla/plugins/*.so
