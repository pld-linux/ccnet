#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	A framework for writing networked applications in C
Name:		ccnet
Version:	6.1.8
Release:	1
License:	GPL v3
Group:		Libraries
Source0:	https://github.com/haiwen/ccnet/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4bab2537f68070d5af226fc80b79c859
Patch0:		codegen.patch
URL:		https://github.com/haiwen/ccnet
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib2-devel
BuildRequires:	libevent-devel
BuildRequires:	libsearpc-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	libzdb-devel >= 2.10.2
BuildRequires:	openssl-devel
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sqlite-devel
BuildRequires:	vala >= 0.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ccnet is a framework for writing networked applications in C. It
provides the following basic services:

- Peer identification
- Connection Management
- Service invocation
- Message sending

In ccnet network, there are two types of nodes, i.e., client and
server. Server has the following functions:

- User management
- Group management
- Cluster management

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel
Requires:	libevent-devel
Requires:	libsearpc-devel

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1

# meh is this?
sed -i -e 's/(DESTDIR)//' libccnet.pc.in

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__automake} --gnu
%{__autoconf}
%configure \
	--disable-static \
	--disable-compile-demo \

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_postclean

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libccnet.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.markdown HACKING LICENSE.txt
%attr(755,root,root) %{_libdir}/libccnet.so.*.*.*
%ghost %{_libdir}/libccnet.so.0
%attr(755,root,root) %{_bindir}/ccnet
%attr(755,root,root) %{_bindir}/ccnet-init
%{py_sitedir}/ccnet

%files devel
%defattr(644,root,root,755)
%doc LICENSE.txt
%{_includedir}/ccnet.h
%{_includedir}/ccnet
%{_libdir}/libccnet.so
%{_pkgconfigdir}/libccnet.pc
