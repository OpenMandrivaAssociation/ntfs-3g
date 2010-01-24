%define	name	ntfs-3g
%define	version	2010.1.16
%define	release	%mkrel 2

%define build_external_fuse 0
%if %mdkversion > 201000
%define build_external_fuse 1
%endif

Summary:	Read-write ntfs driver
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		System/Base
Source: 	http://tuxera.com/opensource/%{name}-%{version}.tgz
Source1:	10-ntfs-3g-policy.fdi
Patch0:		ntfs-3g-2009.3.8-nomtab.patch
URL:		http://www.tuxera.com/community/ntfs-3g-download/
Obsoletes:      %mklibname ntfs-3g 0
Obsoletes:      %mklibname ntfs-3g 2
Obsoletes:      %mklibname ntfs-3g 10
Obsoletes:      %mklibname ntfs-3g 14
Obsoletes:      %mklibname ntfs-3g 16
Obsoletes:      %mklibname ntfs-3g 23
BuildRequires:	attr-devel
%if %build_external_fuse
Buildrequires:  fuse-devel >= 2.8
Requires:	fuse >= 2.8
Requires(pre):	fuse >= 2.8
%else
Requires:	kmod(fuse)
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The ntfs-3g package contains NTFS filesystem driver with read and 
write support. It provides safe and fast handling of MS Windows Vista, 
XP, 2000 and Server 2003 NTFS file systems. Most POSIX file system 
operations are supported.

%package	devel
Summary:	Header files and static libraries for ntfs-3g
Group:		Development/C
Requires:	%{name} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname -d %name
Obsoletes:	%mklibname -d %name 0
Obsoletes:      %mklibname -d %name 2
Obsoletes:      %mklibname -d %name 4

%description devel
You should install this package if you wish to develop applications that
use ntfs-3g.


%prep
%setup -q
%patch0 -p1 -b .nomtab

%build
export CFLAGS="%{optflags} -fPIC"
%configure2_5x \
	--disable-static \
	--exec-prefix=/ \
	--bindir=/bin \
	--libdir=/%_lib \
	--sbindir=/sbin \
	--disable-ldconfig \
%if %build_external_fuse
	--with-fuse=external
%else
	--with-fuse=internal
%endif
%make

%install
rm -rf %{buildroot}
sed -i -e 's|/sbin/ldconfig|true|' src/Makefile
%makeinstall_std

# make the symlink an actual copy to avoid confusion
rm -rf %buildroot/sbin/mount.ntfs-3g
cp -a %buildroot/bin/ntfs-3g %buildroot/sbin/mount.ntfs-3g

# .pc file should always be there
mkdir -p %buildroot%_libdir
mv -f %buildroot/%_lib/pkgconfig %buildroot%_libdir/pkgconfig

# remove doc files, as we'll cp them later
rm -fr %buildroot/%_datadir/doc

mkdir -p %{buildroot}/%{_datadir}/hal/fdi/policy/10osvendor/
install -m 644 %SOURCE1 %{buildroot}/%{_datadir}/hal/fdi/policy/10osvendor/

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post  -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun  -p /sbin/ldconfig
%endif

%files
%defattr (-,root,root)
%doc README AUTHORS CREDITS NEWS
/bin/ntfs-3g
/bin/ntfs-3g.*
%{_mandir}/man8/*
%attr(754,root,root) /sbin/mount.ntfs-3g
%{_datadir}/hal/fdi/policy/10osvendor/10-ntfs-3g-policy.fdi
/%{_lib}/libntfs-3g.so.*

%files devel
%defattr(-,root,root)
%doc ChangeLog
/%{_lib}/libntfs-3g.so
%{_includedir}/ntfs-3g
/%{_lib}/libntfs-3g*a
%{_libdir}/pkgconfig/*.pc
