%define	name	ntfs-3g
%define	version	2012.1.15
%define	release 1

%define build_external_fuse 1
# flag to allow local users to mount partitions. This is *really* not a good
# idea, because all users who have access to the device can do whatever they
# want with the data, and it also adds a root setuid binary to your system, so
# use it on your own risk. Refer to
# http://www.tuxera.com/community/ntfs-3g-faq/#useroption for details.
%define allow_unsafe_mount 0
%if %allow_unsafe_mount
# user mount only works if ntfs-3g is using internal fuse library
%define build_external_fuse 0
%endif

Summary:	Read-write ntfs driver
Name:		ntfs-3g
Version:	2012.1.15
Release:	2
License:	GPLv2+
Group:		System/Base
Source0: 	http://tuxera.com/opensource/%{name}_ntfsprogs-%{version}.tgz
URL:		http://www.tuxera.com/community/ntfs-3g-download/
Obsoletes:      %mklibname ntfs-3g 0
Obsoletes:      %mklibname ntfs-3g 2
Obsoletes:      %mklibname ntfs-3g 10
Obsoletes:      %mklibname ntfs-3g 14
Obsoletes:      %mklibname ntfs-3g 16
Obsoletes:      %mklibname ntfs-3g 23
%rename ntfsprogs
BuildRequires:	attr-devel
%if %build_external_fuse
Buildrequires:  fuse-devel >= 2.8
Requires:	fuse >= 2.8
Requires(pre):	fuse >= 2.8
%else
Requires:	kmod(fuse)
%endif
Conflicts:	ntfsprogs < 2.0.0-6

%description
The ntfs-3g package contains NTFS filesystem driver with read and 
write support. It provides safe and fast handling of MS Windows Vista, 
XP, 2000 and Server 2003 NTFS file systems. Most POSIX file system 
operations are supported.

%define	major	83
%define	libname	%mklibname %{name} %{major}
%package -n	%{libname}
Summary:	Library for reading & writing on NTFS filesystems
Group:		System/Base
Conflicts:	%{name} < 2012.1.15-2

%description -n	%{libname}
This is the library package for ntfs-3g.

%define	devname	%mklibname -d %{name}
%package -n	%{devname}
Summary:	Header files and static libraries for ntfs-3g
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname -d %name
Obsoletes:	%mklibname -d %name 0
Obsoletes:      %mklibname -d %name 2
Obsoletes:      %mklibname -d %name 4
%rename		%{name}-devel

%description -n	%{devname}
You should install this package if you wish to develop applications that
use ntfs-3g.

%prep
%setup -qn %{name}_ntfsprogs-%{version}

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
sed -i -e 's|/sbin/ldconfig|true|' src/Makefile
%makeinstall_std

# make the symlink an actual copy to avoid confusion
rm -rf %buildroot/sbin/mount.ntfs-3g
cp -a %buildroot/bin/ntfs-3g %buildroot/sbin/mount.ntfs-3g
ln -sf /sbin/mount.ntfs-3g %buildroot/sbin/mount.ntfs
ln -sf /sbin/mount.ntfs-3g %buildroot/sbin/mount.ntfs-fuse
mkdir -p %buildroot/%_bindir
ln -sf /sbin/mount.ntfs-3g %buildroot/%_bindir/ntfsmount

# .pc file should always be there
mkdir -p %buildroot%_libdir
mv -f %buildroot/%_lib/pkgconfig %buildroot%_libdir/pkgconfig

# remove doc files, as we'll cp them later
rm -fr %buildroot/%_datadir/doc

%files
%doc README AUTHORS CREDITS NEWS
%{_bindir}/ntfsmount
/bin/lowntfs-3g
/bin/ntfs-3g
/bin/ntfs-3g.probe
/bin/ntfs-3g.secaudit
/bin/ntfs-3g.usermap
/bin/ntfscat
/bin/ntfscluster
/bin/ntfscmp
/bin/ntfsfix
/bin/ntfsinfo
/bin/ntfsls
/sbin/mkfs.ntfs
/sbin/mkntfs
/sbin/ntfsclone
/sbin/ntfscp
/sbin/ntfslabel
/sbin/ntfsresize
/sbin/ntfsundelete
%{_mandir}/man8/*
%if %allow_unsafe_mount
%attr(4755,root,root) /sbin/mount.ntfs-3g
%else
%attr(754,root,root) /sbin/mount.ntfs-3g
%endif
/sbin/mount.ntfs
/sbin/mount.lowntfs-3g
/sbin/mount.ntfs-fuse

%files -n %{libname}
/%{_lib}/libntfs-3g.so.*

%files -n %{devname}
%doc ChangeLog
/%{_lib}/libntfs-3g.so
%{_includedir}/ntfs-3g
%{_libdir}/pkgconfig/*.pc
