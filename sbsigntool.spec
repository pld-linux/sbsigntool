
# Conditional build:
%bcond_with	tests		# build without tests

Summary:	Signing utility for UEFI secure boot
Name:		sbsigntool
Version:	0.6
Release:	0.1
License:	GPL v3
Group:		Applications
# git://kernel.ubuntu.com/jk/sbsigntool a7577f56b3c3c6e314576809cc9ce1bde94ae727
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	23d5b520a3dd26b45dbfc68b4466152f
# git://git.ozlabs.org/~ccan/ccan b1f28e
# git archive --format=tar --prefix=lib/ccan.git b1f28e | bzip2 > ccan-b1f28e.tar.bz2
Source1:	ccan-b1f28e.tar.bz2
# Source1-md5:	a93c0ea0c36241285cee8d60d396ed01
Patch0:		%{name}-efivars_magic.patch
URL:		https://wiki.ubuntu.com/UEFI/SecureBoot
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnu-efi
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Utilites for signing and verifying files for UEFI Secure Boot.

%prep
%setup -q -a1

%build

# from autogen.sh
ccan_modules="talloc read_write_all build_assert array_size"
lib/ccan.git/tools/create-ccan-tree \
	--build-type=automake lib/ccan $ccan_modules

%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
%ifarch %{ix86}
	CPPFLAGS="%{rpmcppflags} -I/usr/include/efi/ia32"
%endif
%{__make}

%{?with_tests:%{__make} -C tests test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_bindir}/sb*
%{_mandir}/man1/sb*.1*
