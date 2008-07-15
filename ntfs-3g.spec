%define	name	ntfs-3g
%define	version	1.2712
%define	release	%mkrel 1

Summary:	Read-write ntfs driver
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		System/Base
Source: 	http://ntfs-3g.org/%{name}-%{version}.tgz
Source1:	10-ntfs-3g-policy.fdi
Patch0:		ntfs-3g-1.2216-nomtab.patch
URL:		http://ntfs-3g.org/
Obsoletes:      %mklibname ntfs-3g 0
Obsoletes:      %mklibname ntfs-3g 2
Obsoletes:      %mklibname ntfs-3g 10
Obsoletes:      %mklibname ntfs-3g 14
Obsoletes:      %mklibname ntfs-3g 16
Obsoletes:      %mklibname ntfs-3g 23
%if %mdkversion > 200900
Buildrequires:  fuse-devel >= 2.7.2
Requires:	fuse >= 2.7.2
%else
Requires:	kmod(fuse)
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The ntfs-3g package contains NTFS filesystem driver with read and 
write support. It provides safe and fast handling of MS Windows Vista, 
XP, 2000 and Server 2003 NTFS file systems. Most POSIX file system 
operations are supported, with the exceptions of full file 
ownership and access right support.

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
%patch0 -p1

%build
%configure2_5x \
	--exec-prefix=/ \
	--bindir=/bin \
	--libdir=/%_lib \
	--sbindir=/sbin \
	--disable-ldconfig \
%if %mdkversion > 200900
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
rm -fr %buildroot/share/doc/%name

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
/bin/ntfs-3g.probe
%{_mandir}/man8/*
%attr(754,root,fuse) /sbin/mount.ntfs-3g
%{_datadir}/hal/fdi/policy/10osvendor/10-ntfs-3g-policy.fdi
/%{_lib}/libntfs-3g.so.*

%files devel
%defattr(-,root,root)
%doc ChangeLog
/%{_lib}/libntfs-3g.so
%{_includedir}/ntfs-3g
/%{_lib}/libntfs-3g*a
%{_libdir}/pkgconfig/*.pc
