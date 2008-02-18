Summary: A MOD music file player library
Name: libmikmod
Version: 3.2.0
Release: 2.beta2%{?dist}
License: GPLv2 and LGPLv2+
Group: Applications/Multimedia
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: esound-devel
URL: http://mikmod.raphnet.net/
Source0: http://mikmod.raphnet.net/files/libmikmod-%{version}-beta2.tar.bz2
Patch0:  libmikmod-64bit.patch
Patch1:  libmikmod-esd.patch
Patch2:  libmikmod-strip-lib.patch
Patch3:  libmikmod-multilib.patch
Patch4:  libmikmod-autoconf.patch

%description
libmikmod is a library used by the mikmod MOD music file player for
UNIX-like systems. Supported file formats include MOD, STM, S3M, MTM,
XM, ULT and IT.

%package devel
Group: Development/Libraries
Summary: Header files and documentation for compiling mikmod applications
Requires: %{name} = %{version}-%{release}
Provides: mikmod-devel = 3.2.2-4
Obsoletes: mikmod-devel < 3.2.2-4

%description devel
This package includes the header files you will need to compile
applications for mikmod.

%prep
%setup -q -n %{name}-%{version}-beta2
%patch0 -p1 -b .64bit
%patch1 -p1 -b .esd
%patch2 -p1 -b .strip-lib
%patch3 -p1 -b .multilib
%patch4 -p1 -b .autoconf

%build
%configure
make %{?_smp_flags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT%{_infodir}/dir $RPM_BUILD_ROOT%{_libdir}/*.a
find $RPM_BUILD_ROOT | grep "\\.la$" | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%post devel
[ -x /sbin/install-info ] && /sbin/install-info %{_infodir}/mikmod.info %{_infodir}/dir || :

%postun -p /sbin/ldconfig

%postun devel
if [ $1 = 0 ] ; then
	[ -x /sbin/install-info ] && /sbin/install-info  --delete %{_infodir}/mikmod.info %{_infodir}/dir || :
fi

%files
%defattr(-, root, root)
%doc AUTHORS COPYING.LIB COPYING.LESSER NEWS README TODO
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root)
%{_bindir}/*-config
%{_libdir}/*.so
%{_datadir}/aclocal/*
%{_includedir}/*
%{_infodir}/mikmod*
%{_mandir}/man1/libmikmod-config*

%changelog
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

* Wed Oct 18 2007 Jindrich Novy <jnovy@redhat.com> 3.1.11-1
- package libmikmod
