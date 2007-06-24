%define	name	ntfs-3g
%define	version	1.616
%define	release	%mkrel 1
%define	major	4
%define	libname	%mklibname %{name} %major

Summary:	Read-write ntfs driver
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Base
Source: 	http://ntfs-3g.org/%{name}-%{version}.tgz
URL:		http://ntfs-3g.org/
Buildrequires:  fuse-devel >= 2.5.0
Requires:	fuse >= 2.5.0
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

%package -n	%{libname}-devel
Summary:	Header files and static libraries for ntfs-3g
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{libname}-devel
You should install this package if you wish to develop applications that
use ntfs-3g.


%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}

sed -i -e 's|/sbin/ldconfig|true|' src/Makefile
%makeinstall_std
cat > README.install.urpmi << EOF	 
WARNING :
Install dkms-fuse with kernels older than 2.6.20.2 or not all features will
work properly. 
EOF

%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr (-,root,root)
%doc README ChangeLog AUTHORS CREDITS INSTALL NEWS README.install.urpmi
%{_bindir}/ntfs-3g
%{_mandir}/man8/*
/sbin/mount.ntfs-3g

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libntfs-3g.so.%{major}*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/libntfs-3g.so
%{_includedir}/ntfs-3g
%{_libdir}/libntfs-3g*a


