%global commit0 5c4d4db08d39673b98ce953f1ab1d1368eeb2f44

%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%global __python %{__python3}

Name:           icestorm
Version:        0
Release:        0.3.20170914git%{shortcommit0}%{?dist}
Summary:        Lattice iCE40 FPGA bitstream creation/analysis/programming tools
License:        ISC
URL:            http://www.clifford.at/%{name}/
Source0:        https://github.com/cliffordwolf/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

# Fedora-specific patch for datadir
Patch1:         %{name}-datadir.patch

BuildRequires:  python%{python3_pkgversion} libftdi-devel

%description
Project IceStorm aims at documenting the bitstream format of Lattice iCE40
FPGAs and providing simple tools for analyzing and creating bitstream files.

%prep
%setup -q -n %{name}-%{commit0}
%patch1 -p1 -b .datadir
# fix shebang lines in Python scripts
find . -name \*.py -exec sed -i 's|/usr/bin/env python3|/usr/bin/python3|' {} \;
# get rid of .gitignore files in examples
find . -name \.gitignore -delete

%build
%global moreflags -I/usr/include/libftdi1 -DPREFIX='\\\"%{_prefix}\\\"' -DCHIPDB_SUBDIR='\\\"%{_datarootdir}/%{name}\\\"'
make %{?_smp_mflags} \
     CFLAGS="%{optflags} %{moreflags}" \
     CXXFLAGS="%{optflags} %{moreflags}" \
     LDFLAGS="$RPM_LD_FLAGS"

%install
%make_install PREFIX="%{_prefix}"
chmod +x %{buildroot}%{_bindir}/icebox.py
mv %{buildroot}%{_datarootdir}/icebox %{buildroot}%{_datarootdir}/%{name}
mv %{buildroot}%{_bindir}/iceboxdb.py %{buildroot}%{_datarootdir}/%{name}

# We could do a minimal check section by running make in the example
# directories, but that depends on arachne-pnr, which depends on this
# package, so it would create a circular dependency.

%files
%license README
%doc examples
%{_bindir}/*
%{_datarootdir}/%{name}

%changelog
* Thu Sep 14 2017 Eric Smith <brouhaha@fedoraproject.org> 0-0.3.20170914git5c4d4db
- Updated per review comments.
- Updated to latest upstream.

* Sat Dec 10 2016 Eric Smith <brouhaha@fedoraproject.org> 0-0.2.20161101git01b9822
- Updated per review comments.
- Updated to latest upstream.

* Mon Sep 12 2016 Eric Smith <brouhaha@fedoraproject.org> 0-0.1.20160904git0b4b038
- Initial version.