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
%define	major	87

Summary:	Read-write ntfs driver
Name:		ntfs-3g
Version:	2016.2.22
Release:	1
License:	GPLv2+
Group:		System/Base
Source0:	http://tuxera.com/opensource/%{name}_ntfsprogs-%{version}.tgz
Url:		http://www.tuxera.com/community/ntfs-3g-download/
%rename ntfsprogs
BuildRequires:	attr-devel
%if %build_external_fuse
Buildrequires:	pkgconfig(fuse)
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

%description -n	%{devname}
You should install this package if you wish to develop applications that
use ntfs-3g.

%prep
%setup -qn %{name}_ntfsprogs-%{version}

%build
for i in $(find . -name config.guess -o -name config.sub) ; do
         [ -f /usr/share/libtool/config/$(basename $i) ] && /bin/rm -f $i && /bin/cp -fv /usr/share/libtool/config//$(basename $i) $i ;
done ;

%configure \
	CC="gcc -fuse-ld=bfd" \
	CFLAGS="%{optflags} -fPIC" \
	--disable-static \
	--exec-prefix=/ \
	--bindir=/bin \
	--sbindir=/sbin \
	--disable-ldconfig \
%if %build_external_fuse
	--with-fuse=external
%else
	--with-fuse=internal
%endif
%make

%install
%makeinstall_std
install -d %{buildroot}/%{_lib}
for l in libntfs-3g.so; do
	rm %{buildroot}%{_libdir}/${l}
	mv %{buildroot}%{_libdir}/${l}.%{major}* %{buildroot}/%{_lib}
	ln -sr %{buildroot}/%{_lib}/${l}.%{major}.* %{buildroot}%{_libdir}/${l}
done

ln -sf /sbin/mount.ntfs-3g %{buildroot}/sbin/mount.ntfs
ln -sf /sbin/mount.ntfs-3g %{buildroot}/sbin/mount.ntfs-fuse
mkdir -p %{buildroot}%{_bindir}
ln -sf /sbin/mount.ntfs-3g %{buildroot}%{_bindir}/ntfsmount

# remove doc files, as we'll cp them later
rm -r %{buildroot}%{_datadir}/doc

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
/%{_lib}/libntfs-3g.so.%{major}*

%files -n %{devname}
%doc ChangeLog
%{_libdir}/libntfs-3g.so
%{_includedir}/ntfs-3g
%{_libdir}/pkgconfig/*.pc
