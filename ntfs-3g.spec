# ntfs-3g is currently incompatible with fuse 3.x
%define build_external_fuse 0
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

%define major 88
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}

Summary:	Read-write ntfs driver
Name:		ntfs-3g
Version:	2017.3.23
Release:	4
License:	GPLv2+
Group:		System/Base
Source0:	http://tuxera.com/opensource/%{name}_ntfsprogs-%{version}.tgz
Patch0:		ntfs3g-2017.3.23-big-sectors.patch
Patch1:		ntfs3g-2017.3.23-check-mftmirr.patch
Patch2:		ntfs3g-2017.3.23-full-clusters.patch
Url:		http://www.tuxera.com/community/ntfs-3g-download/
%rename ntfsprogs
BuildRequires:	pkgconfig(libattr)
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(uuid)
%if %build_external_fuse
Buildrequires:	pkgconfig(fuse3)
Requires:	fuse >= 2.8
Requires(pre):	fuse >= 2.8
%else
Requires:	(kmod(fuse) or kernel-release-clang)
Suggests:	kmod(fuse)
%endif
Conflicts:	ntfsprogs < 2.0.0-6
# (tpg) needed for Windows 10
Recommends:	ntfs-3g-system-compression

%description
The ntfs-3g package contains NTFS filesystem driver with read and 
write support. It provides safe and fast handling of MS Windows Vista, 
XP, 2000 and Server 2003 NTFS file systems. Most POSIX file system 
operations are supported.

%package -n %{libname}
Summary:	Library for reading & writing on NTFS filesystems
Group:		System/Base
Conflicts:	%{name} < 2012.1.15-2

%description -n %{libname}
This is the library package for ntfs-3g.

%package -n %{devname}
Summary:	Header files and static libraries for ntfs-3g
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n	%{devname}
You should install this package if you wish to develop applications that
use ntfs-3g.

%prep
%setup -qn %{name}_ntfsprogs-%{version}
%autopatch -p1

%build
for i in $(find . -name config.guess -o -name config.sub) ; do
    [ -f /usr/share/libtool/config/$(basename $i) ] && /bin/rm -f $i && /bin/cp -fv /usr/share/libtool/config//$(basename $i) $i ;
done ;

%configure \
	CC="gcc -fuse-ld=bfd" \
	CFLAGS="%{optflags} -fPIC" \
	--disable-static \
	--disable-ldconfig \
	--enable-posix-acls \
	--enable-xattr-mappings \
	--enable-crypto \
	--enable-extras \
	--enable-quarantined \
%if %build_external_fuse
	--with-fuse=external
%else
	--with-fuse=internal
%endif

%make_build

%install
%make_install

ln -sf %{_sbindir}/mount.ntfs-3g %{buildroot}/sbin/mount.ntfs
ln -sf %{_sbindir}/mount.ntfs-3g %{buildroot}/sbin/mount.ntfs-fuse
mkdir -p %{buildroot}%{_bindir}
ln -sf %{_sbindir}/mount.ntfs-3g %{buildroot}%{_bindir}/ntfsmount
ln -sf %{_bindir}/ntfsck %{buildroot}%{_sbindir}/fsck.ntfs

# remove doc files, as we'll cp them later
rm -r %{buildroot}%{_datadir}/doc

%files
%doc README AUTHORS CREDITS NEWS
%{_bindir}/ntfsmount
%{_bindir}/lowntfs-3g
%{_bindir}/ntfs-3g
%{_bindir}/ntfs-3g.probe
%{_bindir}/ntfscat
%{_bindir}/ntfscluster
%{_bindir}/ntfscmp
%{_bindir}/ntfsfix
%{_bindir}/ntfsinfo
%{_bindir}/ntfsls
# Extras
%{_bindir}/ntfsck
%{_bindir}/ntfsdecrypt
%{_bindir}/ntfsdump_logfile
%{_bindir}/ntfsfallocate
%{_bindir}/ntfsmftalloc
%{_bindir}/ntfsmove
%{_bindir}/ntfsrecover
%{_bindir}/ntfstruncate
%{_bindir}/ntfswipe
%{_sbindir}/fsck.ntfs
%{_sbindir}/mkfs.ntfs
%{_sbindir}/mkntfs
%{_sbindir}/ntfsclone
%{_sbindir}/ntfscp
%{_sbindir}/ntfslabel
%{_sbindir}/ntfsresize
%{_sbindir}/ntfsundelete
%{_mandir}/man8/*
%if %allow_unsafe_mount
%attr(4755,root,root) %{_sbindir}/mount.ntfs-3g
%else
%attr(754,root,root) %{_sbindir}/mount.ntfs-3g
%endif
%{_sbindir}/mount.ntfs
%{_sbindir}/mount.lowntfs-3g
%{_sbindir}/mount.ntfs-fuse

%files -n %{libname}
%{_libdir}/libntfs-3g.so.%{major}*

%files -n %{devname}
%doc ChangeLog
%{_libdir}/libntfs-3g.so
%{_includedir}/ntfs-3g
%{_libdir}/pkgconfig/*.pc
