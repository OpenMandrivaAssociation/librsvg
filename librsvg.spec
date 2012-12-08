%define api	2
%define major	2
%define gimajor	2.0
%define libname	%mklibname rsvg %{api} %{major}
%define devname	%mklibname -d rsvg %{api}
%define girname	%mklibname rsvg-gir %{gimajor}

# mozilla plugin requires xulruuner 1.8 not 1.9
%define build_mozilla 0

Summary:	Raph's SVG library
Name:		librsvg
Version:	2.36.4
Release:	2
License:	LGPLv2+ and GPLv2+
Group:		Graphics
URL:		http://librsvg.sourceforge.net/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.xz
Patch0:		10_rsvg-gz.patch
Patch1:		20_rsvg_compat.patch
BuildRequires:	pkgconfig(gtk+-2.0) >= 2.4.0
BuildRequires:	gdk-pixbuf2.0
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libcroco-0.6)
BuildRequires:	pkgconfig(libxml-2.0)
#BuildRequires:	docbook-dtd31-sgml
BuildRequires:	vala-tools
BuildRequires:	vala-devel

Provides:	%{name}%{api} = %{version}-%{release}
Requires:	%{libname} >= %{version}
Requires:	python

%description
A library that uses libart and pango to render svg files.

%package -n %{libname}
Summary:	Raph's SVG library
Group:		System/Libraries

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
%setup -q
%apply_patches

%build

%configure2_5x \
	--disable-static \
	--enable-introspection=yes \
	--disable-gtk-doc \
	--enable-vala \
	--enable-pixbuf-loader \
	--disable-gtk-theme

%make

%install
%makeinstall_std

#remove unpackaged files
rm -fr %{buildroot}%{_docdir}/librsvg
%if %{build_mozilla}
rm -f %{buildroot}%{_libdir}/mozilla/
%endif
rm -f %{buildroot}%{_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders
rm -f %{buildroot}%{_datadir}/pixmaps/svg-viewer.svg

%files
%doc AUTHORS COPYING COPYING.LIB ChangeLog NEWS README
%{_bindir}/rsvg-convert
%{_bindir}/rsvg-view-3
#{_libdir}/gtk-2.0/*/engines/*.so
#{_datadir}/themes/bubble/gtk-2.0/*
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
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/librsvg-2.0.vapi

%if %{build_mozilla}
%files mozilla
%{_libdir}/mozilla/plugins/*.so
%endif

%changelog
* Wed May 02 2012 Guilherme Moro <guilherme@mandriva.com> 2.36.1-2
+ Revision: 795193
+ rebuild (emptylog)

* Sun Apr 29 2012 Guilherme Moro <guilherme@mandriva.com> 2.36.1-1
+ Revision: 794414
- Updated to version 2.36.1

* Sun Nov 20 2011 Matthew Dawkins <mattydaw@mandriva.org> 2.34.2-1
+ Revision: 732084
- added missing gir file & major
- fixed rm .la cmd
- new version 2.34.2
- removed defattr
- added build for gir and split out pkg
- enabled gtk3 by default merged unbuilt pkg into main pkg
- properly removed all .la files
- disabled static build
- moved modules & engines from lib pkg to main pkg
- moved provides nameapi_verion to main pkg
- removed mkrel & BuildRoot
- converted BRs to pkgconfig provides
- cleaned up spec
- removed old conflicts

* Wed Sep 28 2011 Götz Waschk <waschk@mandriva.org> 2.34.1-2
+ Revision: 701667
- rebuild for new libpng

* Wed Sep 07 2011 Götz Waschk <waschk@mandriva.org> 2.34.1-1
+ Revision: 698512
- new version
- xz tarball

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 2.34.0-2
+ Revision: 662411
- mass rebuild

* Mon Apr 04 2011 Funda Wang <fwang@mandriva.org> 2.34.0-1
+ Revision: 650123
- new version 2.34.0

* Sun Nov 14 2010 Götz Waschk <waschk@mandriva.org> 2.32.1-1mdv2011.0
+ Revision: 597521
- update to new version 2.32.1

* Mon Sep 27 2010 Funda Wang <fwang@mandriva.org> 2.32.0-1mdv2011.0
+ Revision: 581173
- update to new version 2.32.0

* Mon Aug 09 2010 Funda Wang <fwang@mandriva.org> 2.31.0-2mdv2011.0
+ Revision: 567900
- /usr/bin/rsvg2 is a python script

* Fri Jul 30 2010 Funda Wang <fwang@mandriva.org> 2.31.0-1mdv2011.0
+ Revision: 563261
- New version 2.31.0
- adopt to splitting on gtk and gdk_pixbuff

* Mon May 03 2010 Götz Waschk <waschk@mandriva.org> 2.26.3-1mdv2010.1
+ Revision: 541704
- update to new version 2.26.3

* Tue Mar 30 2010 Götz Waschk <waschk@mandriva.org> 2.26.2-1mdv2010.1
+ Revision: 528963
- update to new version 2.26.2

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 2.26.0-3mdv2010.1
+ Revision: 520902
- rebuilt for 2010.1

* Sun Oct 04 2009 Funda Wang <fwang@mandriva.org> 2.26.0-2mdv2010.0
+ Revision: 453343
- disable mozilla plugin as it requires xulrunner 1.8

* Mon Mar 16 2009 Götz Waschk <waschk@mandriva.org> 2.26.0-1mdv2009.1
+ Revision: 355970
- update to new version 2.26.0

* Tue Sep 23 2008 Götz Waschk <waschk@mandriva.org> 2.22.3-1mdv2009.0
+ Revision: 287353
- new version
- build with xulrunner
- fix group
- fix license

* Sat Jun 28 2008 Oden Eriksson <oeriksson@mandriva.com> 2.22.2-3mdv2009.0
+ Revision: 229864
- fix build (-lm)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Mar 04 2008 Götz Waschk <waschk@mandriva.org> 2.22.2-1mdv2008.1
+ Revision: 178712
- new version

* Mon Feb 25 2008 Götz Waschk <waschk@mandriva.org> 2.22.1-1mdv2008.1
+ Revision: 174557
- new version

* Thu Feb 21 2008 Götz Waschk <waschk@mandriva.org> 2.22.0-1mdv2008.1
+ Revision: 173717
- new version

* Sun Jan 20 2008 Götz Waschk <waschk@mandriva.org> 2.20.0-1mdv2008.1
+ Revision: 155297
- new version

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Thu Aug 30 2007 Götz Waschk <waschk@mandriva.org> 2.18.2-1mdv2008.0
+ Revision: 75142
- new version

* Tue Aug 21 2007 Götz Waschk <waschk@mandriva.org> 2.18.1-1mdv2008.0
+ Revision: 68239
- new version
- new devel name

* Tue Jul 24 2007 Götz Waschk <waschk@mandriva.org> 2.18.0-1mdv2008.0
+ Revision: 55028
- new version
- fix mozilla plugin build


* Wed Nov 22 2006 Götz Waschk <waschk@mandriva.org> 2.16.1-3mdv2007.0
+ Revision: 86442
- add conflict to fix upgrade

* Wed Nov 22 2006 Colin Guthrie <cguthrie@mandriva.org> 2.16.1-2mdv2007.1
+ Revision: 86240
- Libify the engines for the benefit of x86_64 users

* Fri Nov 03 2006 Götz Waschk <waschk@mandriva.org> 2.16.1-1mdv2007.1
+ Revision: 76075
- another fix for the gtk macros
- fix macros with pkgconfig calls again
- fix gtkbinaryver macro
- Import librsvg

* Fri Nov 03 2006 Götz Waschk <waschk@mandriva.org> 2.16.1-1mdv2007.1
- New version 2.16.1

* Fri Sep 01 2006 Götz Waschk <waschk@mandriva.org> 2.16.0-1mdv2007.0
- New release 2.16.0

* Wed Aug 02 2006 Frederic Crozat <fcrozat@mandriva.com> 2.15.90-3mdv2007.0
- Rebuild with latest dbus

* Mon Jul 31 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.15.90-2
- fix building in autobuilders that install only strictly necessary build deps
- add BuildRequires: libxt-devel

* Fri Jul 28 2006 Götz Waschk <waschk@mandriva.org> 2.15.90-1
- New release 2.15.90

* Fri May 12 2006 Götz Waschk <waschk@mandriva.org> 2.14.4-1mdk
- New release 2.14.4

* Tue Mar 07 2006 Götz Waschk <waschk@mandriva.org> 2.12.7-6mdk
- rebuild for new libgsf

* Mon Feb 27 2006 Frederic Crozat <fcrozat@mandriva.com> 2.12.7-5mdk
- Fortify package uninstall

* Fri Feb 24 2006 Frederic Crozat <fcrozat@mandriva.com> 2.12.7-4mdk
- Use mkrel

* Mon Nov 14 2005 Oden Eriksson <oeriksson@mandriva.com> 2.12.7-3mdk
- rebuilt against openssl-0.9.8a

* Wed Oct 12 2005 Götz Waschk <waschk@mandriva.org> 2.12.7-2mdk
- rebuild for new libgsf

* Mon Oct 10 2005 Götz Waschk <waschk@mandriva.org> 2.12.7-1mdk
- New release 2.12.7

* Sat Oct 08 2005 Frederic Crozat <fcrozat@mandriva.com> 2.12.6-1mdk
- Release 2.12.6

* Sat Oct 08 2005 Frederic Crozat <fcrozat@mandriva.com> 2.12.4-2mdk
- Enforce post dependency
- don't run gdk-pixbuf-query-loaders in postun when upgrading

* Fri Oct 07 2005 Frederic Crozat <fcrozat@mandriva.com> 2.12.4-1mdk
- Release 2.14.4
- Remove patch0 (merged upstream)

* Sat Aug 27 2005 Götz Waschk <waschk@mandriva.org> 2.9.5-2mdk
- replace prereq

* Thu Apr 21 2005 Frederic Crozat <fcrozat@mandriva.com> 2.9.5-1mdk 
- Release 2.9.5 (based on G�tz Waschk package)

* Mon Mar 14 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.1-5mdk 
- Rebuild with firefox

* Wed Jan 05 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.1-4mdk 
- Rebuild with latest howl

* Mon Dec 13 2004 Abel Cheung <deaddog@mandrake.org> 2.8.1-3mdk
- Remove wrong or outdated requirements

* Fri Nov 12 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.8.1-2mdk
- add BuildRequires: mozilla-devel

* Wed Oct 20 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.1-1mdk
- New release 2.8.1

* Thu Aug 05 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.6.5-2mdk
- biarch support

* Sun May 02 2004 Götz Waschk <waschk@linux-mandrake.com> 2.6.5-1mdk
- don't libtoolize
- fix url
- New release 2.6.5

* Fri Apr 23 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.4-4mdk
- Fix again BuildRequires

* Thu Apr 22 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.4-3mdk
- Fix Buildrequires for documentation generation

* Thu Apr 08 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.4-2mdk
- Rebuild with latest libcroco

* Tue Apr 06 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.4-1mdk
- Release 2.6.4 (with Götz Waschk help)

* Tue Apr 06 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.4.0-2mdk
- rebuild for gtk+2.4.0 (because of svg pixbuf loader)

