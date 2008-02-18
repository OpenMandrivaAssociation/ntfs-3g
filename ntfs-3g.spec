%define	name	ntfs-3g
%define	version	1.2216
%define	release	%mkrel 1
%define	major	23
%define	libname	%mklibname %{name} %major
%define	libnamedev %mklibname -d %{name}

Summary:	Read-write ntfs driver
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		System/Base
Source: 	http://ntfs-3g.org/%{name}-%{version}.tgz
Source1:	10-ntfs-3g-policy.fdi
URL:		http://ntfs-3g.org/
%if %mdkversion > 200800
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


%package -n	%{libname}
Summary:	Ntfs-3g driver library
Group:		System/Libraries

%description -n	%{libname}
Library for ntfs-3g driver.

%package -n	%{libnamedev}
Summary:	Header files and static libraries for ntfs-3g
Group:		Development/C
Obsoletes: %mklibname -d %name 4
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{libnamedev}
You should install this package if you wish to develop applications that
use ntfs-3g.


%prep
%setup -q

%build
%configure2_5x \
	--exec-prefix=/ \
	--bindir=/bin \
	--libdir=/%_lib \
	--sbindir=/sbin \
%if %mdkversion > 200800
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

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr (-,root,root)
%doc README AUTHORS CREDITS NEWS
/bin/ntfs-3g
/bin/ntfs-3g.probe
%{_mandir}/man8/*
%attr(754,root,fuse) /sbin/mount.ntfs-3g
%{_datadir}/hal/fdi/policy/10osvendor/10-ntfs-3g-policy.fdi

%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/libntfs-3g.so.%{major}*

%files -n %{libnamedev}
%defattr(-,root,root)
%doc ChangeLog
/%{_lib}/libntfs-3g.so
%{_includedir}/ntfs-3g
/%{_lib}/libntfs-3g*a
%{_libdir}/pkgconfig/*.pc
