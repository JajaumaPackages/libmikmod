Summary: A MOD music file player library
Name: libmikmod
Version: 3.1.11
Release: 3%{?dist}
License: GPLv2 and LGPLv2+
Group: Applications/Multimedia
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: esound-devel
URL: http://mikmod.raphnet.net/
Source0: http://mikmod.raphnet.net/files/libmikmod-%{version}.tar.gz
# patch has been updated to ship only fuctional stuff
Patch0:  http://mikmod.raphnet.net/files/libmikmod-%{version}-a.diff
Patch1:  libmikmod-esd.patch
Patch2:  libmikmod-64bit.patch
Patch3:  libmikmod-strip-lib.patch
Patch4:  libmikmod-rpath.patch
Patch5:  libmikmod-multilib.patch

%description
libmikmod is a library used by the mikmod MOD music file player for
UNIX-like systems. Supported file formats include MOD, STM, S3M, MTM,
XM, ULT and IT.

%package devel
Group: Development/Libraries
Summary: Header files and documentation for compiling mikmod applications
Requires: %{name} = %{version}-%{release}

%description devel
This package includes the header files you will need to compile
applications for mikmod.

%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .esd
%patch2 -p1 -b .64bit
%patch3 -p1 -b .lib-strip
%patch4 -p1 -b .rpath
%patch5 -p1 -b .multilib

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
* Wed Oct 24 2007 Jindrich Novy <jnovy@redhat.com> 3.1.11-3
- add multilib patch

* Tue Oct 23 2007 Jindrich Novy <jnovy@redhat.com> 3.1.11-2
- update description
- add smp_flags to make
- don't ship static library
- update upstream patch, drop texinfo dependency (thanks to Stepan Kasal)

* Wed Oct 18 2007 Jindrich Novy <jnovy@redhat.com> 3.1.11-1
- package libmikmod
