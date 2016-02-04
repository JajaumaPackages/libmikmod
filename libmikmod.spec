Summary:        A MOD music file player library
Name:           libmikmod
Version:        3.3.8
Release:        2%{?dist}
License:        GPLv2 and LGPLv2+
Group:          Applications/Multimedia
URL:            http://mikmod.sourceforge.net/
Source0:        http://downloads.sourceforge.net/mikmod/libmikmod-%{version}.tar.gz
Patch0:         libmikmod-64bit.patch
Patch1:         libmikmod-multilib.patch
Patch2:         libmikmod-cflags.patch
BuildRequires:  alsa-lib-devel pulseaudio-libs-devel

%description
libmikmod is a library used by the mikmod MOD music file player for
UNIX-like systems. Supported file formats include MOD, STM, S3M, MTM,
XM, ULT and IT.


%package devel
Group:          Development/Libraries
Summary:        Header files and documentation for compiling mikmod applications
Provides:       mikmod-devel = %{version}-%{release}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pulseaudio-libs-devel%{?_isa}
Requires(post): info
Requires(preun): info

%description devel
This package includes the header files you will need to compile
applications for mikmod.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1


%build
%configure --enable-dl --enable-alsa --disable-simd
make %{?_smp_flags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT%{_infodir}/dir $RPM_BUILD_ROOT%{_libdir}/*.a
find $RPM_BUILD_ROOT | grep "\\.la$" | xargs rm -f


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%post devel
/sbin/install-info %{_infodir}/mikmod.info %{_infodir}/dir || :

%postun devel
if [ $1 = 0 ] ; then
  /sbin/install-info --delete %{_infodir}/mikmod.info %{_infodir}/dir || :
fi


%files
%doc AUTHORS COPYING.LIB COPYING.LESSER NEWS README TODO
%{_libdir}/*.so.*

%files devel
%{_bindir}/*-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/aclocal/*
%{_includedir}/*
%{_infodir}/mikmod*
%{_mandir}/man1/libmikmod-config*


%changelog
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 16 2015 Hans de Goede <hdegoede@redhat.com> - 3.3.8-1
- New upstream release 3.3.8

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Sep 10 2014 Hans de Goede <hdegoede@redhat.com> - 3.3.7-1
- New upstream release 3.3.7 (rhbz#1139002)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 27 2014 Hans de Goede <hdegoede@redhat.com> - 3.3.6-2
- Add missing requires pulseaudio-libs-devel to the -devel pkg (rhbz#1081142)

* Sat Mar 22 2014 Hans de Goede <hdegoede@redhat.com> - 3.3.6-1
- New upstream release 3.3.6
- Fixes alsa output not working when alsa-devel is not installes (rhbz#1076966)
- Add BR pulseaudio-libs-devel to enable building of pa output (rhbz#1079527)

* Sat Mar  8 2014 Hans de Goede <hdegoede@redhat.com> - 3.3.5-1
- New upstream release 3.3.5

* Wed Dec 25 2013 Hans de Goede <hdegoede@redhat.com> - 3.3.4-1
- New upstream release 3.3.4

* Sun Oct 20 2013 Hans de Goede <hdegoede@redhat.com> - 3.3.3-1
- New upstream release 3.3.3
- Drop a bunch of merged patches

* Mon Oct 14 2013 Hans de Goede <hdegoede@redhat.com> - 3.3.2-2
- Disable SSE2 use even on x86_64, as upstream advises against using it

* Mon Oct 14 2013 Hans de Goede <hdegoede@redhat.com> - 3.3.2-1
- New upstream and new upstream release 3.3.2
- Drop a bunch of merged patches

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Apr  6 2013 Hans de Goede <hdegoede@redhat.com> - 3.2.0-21
- Fix stuttering sound and hang on exit for apps using libmikmod's alsa driver
- Remove non standard options configure adds to CFLAGS
- Run autoreconf for aarch64 support (rhbz#925794)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 26 2012 Hans de Goede <hdegoede@redhat.com> - 3.2.0-19
- Fix an array overflow caused by libmikmod-CVE-2007-6720.patch (rhbz#859050)
- Cleanup the specfile a bit

* Sat Sep  8 2012 Hans de Goede <hdegoede@redhat.com> - 3.2.0-18
- Fix a crash in align_pointer() (rhbz#855130)

* Sun Aug  5 2012 Hans de Goede <hdegoede@redhat.com> - 3.2.0-17
- Fix a crash in Player_Start() (rhbz#845782)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.2.0-15
- Bump NVR to 15 so it's higher than the betas
- Drop ancient esound, enable alsa
- Modernise spec

* Wed Jun 06 2012 Jindrich Novy <jnovy@redhat.com> 3.2.0-1
- update to stable libmikmod-3.2.0

* Sun May 13 2012 Karsten Hopp <karsten@redhat.com> 3.2.0-14.beta4.1
- disable altivec (used on PPC only) 

* Sun May 13 2012 Jindrich Novy <jnovy@redhat.com> - 3.2.0-13.beta4
- update to 3.2.0-beta4

* Tue Apr 10 2012 Jindrich Novy <jnovy@redhat.com> - 3.2.0-13.beta3
- update to 3.2.0-beta3
- drop upstreamed patches, forwardport the rest

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-13.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-12.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 20 2010 Jindrich Novy <jnovy@redhat.com> 3.2.0-11.beta2
- update the CVE-2009-3995,3996 patch and fix its naming

* Thu Jul 15 2010 Jindrich Novy <jnovy@redhat.com> 3.2.0-10.beta2
- fix CVE-2009-3995,3996 (#614643)

* Mon Nov 23 2009 Hans de Goede <hdegoede@redhat.com> 3.2.0-9.beta2
- Fix CVE-2007-6720 fix, it causes mods to sound wrong, and even causes
  crashes under certain circumstances (#540234), see:
  http://bugzilla.libsdl.org/show_bug.cgi?id=506

* Fri Aug 28 2009 Jindrich Novy <jnovy@redhat.com> 3.2.0-8.beta2
- fix CVE-2009-0179 (#519992)

* Fri Aug 28 2009 Jindrich Novy <jnovy@redhat.com> 3.2.0-7.beta2
- fix CVE-2007-6720 (#519990)

* Tue Aug 11 2009 Jindrich Novy <jnovy@redhat.com> 3.2.0-6.beta2
- don't complain if installing with --excludedocs (#515953)
- add missing requires

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-5.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-4.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 3.2.0-3.beta2
- Fix MikMod_InfoLoader() and MikMod_InfoDriver() functions, fixing mikmod -n
  output

* Mon Feb 18 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 3.2.0-2.beta2
- Replace completely braindead (hint to author, drink coffee first, then code)
  esd non blocking patch with one that actually works. This fixes using mikmod
  with pulseaudio (bz 247865)
- Note: this makes the 2 supported output devices oss and esd (and pulseaudio's
  esd emulation) alsa is not supported, this requires a rewrite of the mikmod
  alsa code which was written for alsa-0.5 and never updated for the new alsa
  0.9/1.0 api

* Fri Feb 15 2008 Jindrich Novy <jnovy@redhat.com> 3.2.0-1
- update to libmikmod-3.2.0-beta2
- fix playback on 64bit arches

* Thu Feb 14 2008 Jindrich Novy <jnovy@redhat.com> 3.1.11-5
- fix rpath patch so that there are no undefined symbols in
  libmikmod.so (#431745)

* Thu Oct 25 2007 Jindrich Novy <jnovy@redhat.com> 3.1.11-4
- virtually provide mikmod-devel

* Wed Oct 24 2007 Jindrich Novy <jnovy@redhat.com> 3.1.11-3
- add multilib patch

* Tue Oct 23 2007 Jindrich Novy <jnovy@redhat.com> 3.1.11-2
- update description
- add smp_flags to make
- don't ship static library
- update upstream patch, drop texinfo dependency (thanks to Stepan Kasal)

* Thu Oct 18 2007 Jindrich Novy <jnovy@redhat.com> 3.1.11-1
- package libmikmod
