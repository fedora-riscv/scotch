Summary:	Graph, mesh and hypergraph partitioning library
Name:		scotch
Version:	6.0.0
Release:	8%{?dist}
License:	CeCILL-C
Group:		Development/Libraries
URL:		http://www.labri.fr/perso/pelegrin/scotch/
Source0:	https://gforge.inria.fr/frs/download.php/27583/%{name}_%{version}.tar.gz
Source1:	scotch-Makefile.static.inc.in
Source2:	scotch-Makefile.shared.inc.in
BuildRequires:	flex bison zlib-devel bzip2-devel lzma-devel
Requires:	%{name}-doc = %{version}-%{release}

%description
Scotch is a software package for graph and mesh/hypergraph partitioning and
sparse matrix ordering. The parallel scotch lbrariries are packaged in the
ptscotch sub-packages.

%package devel
Summary:	Development libraries for scotch
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains development libraries for scotch.

%package static
Summary:	Development libraries for scotch
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains libscotch static libraries.

%package doc
Summary:	Documentations and example for scotch and ptscotch
Group:		Documentation
BuildArch:	noarch

%description doc
Contains documentations and example for scotch and ptscotch

%package -n ptscotch-mpich
Summary:	PT-Scotch libraries compiled against mpich
Group:		Development/Libraries
BuildRequires:	mpich-devel
Requires:	environment-modules mpich
Requires:	%{name}-doc = %{version}-%{release}

%description -n ptscotch-mpich
Scotch is a software package for graph and mesh/hypergraph partitioning and
sparse matrix ordering. This sub-package provides parallelized scotch libraries
compiled with mpich

%package -n ptscotch-mpich-devel
Summary: 	Development libraries for PT-Scotch (mpich)
Group:		Development/Libraries
Requires:	pt%{name}-mpich = %{version}-%{release}

%description -n ptscotch-mpich-devel
This package contains development libraries for PT-Scotch, compiled against
mpich.

%package -n ptscotch-mpich-static
Summary:	Static PT-Scotch libraries compiled against mpich
Group:		Development/Libraries
Requires:	pt%{name}-mpich-devel = %{version}-%{release}

%description -n ptscotch-mpich-static
This package contains static libraries for Scotch, compiled against mpich.

%package -n ptscotch-openmpi
Summary:	PT-Scotch libraries compiled against openmpi
Group:		Development/Libraries
BuildRequires:	openmpi-devel
Requires:	environment-modules openmpi
Requires:	%{name}-doc = %{version}-%{release}

%description -n ptscotch-openmpi
Scotch is a software package for graph and mesh/hypergraph partitioning and
sparse matrix ordering. This sub-package provides parallelized scotch libraries
compiled with openmpi

%package -n ptscotch-openmpi-devel
Summary:	Development libraries for PT-Scotch (openmpi)
Group:		Development/Libraries
Requires:	pt%{name}-openmpi = %{version}-%{release}

%description -n ptscotch-openmpi-devel
This package contains development libraries for PT-Scotch, compiled against openmpi.

%package -n ptscotch-openmpi-static
Summary:	Static PT-Scotch libraries compiled against openmpi
Group:		Development/Libraries
Requires:	pt%{name}-openmpi-devel = %{version}-%{release}

%description -n ptscotch-openmpi-static
This package contains static libraries for Scotch, compiled against openmpi.

%prep
%setup -c -q -n scotch_%{version}
pushd scotch_%{version}
sed s/@RPMFLAGS@/'%{optflags} -fPIC'/ < %SOURCE1 > src/Makefile.static.inc
sed s/@RPMFLAGS@/'%{optflags} -fPIC'/ < %SOURCE2 > src/Makefile.shared.inc
popd

cp -ap scotch_%{version} scotch_%{version}_mpich
cp -ap scotch_%{version} scotch_%{version}_openmpi

%build
module purge

%define dosingle() \
rm -f Makefile.inc; \
ln -s Makefile.static.inc Makefile.inc; \
make %{?_smp_mflags}; \
rm -f Makefile.inc; \
ln -s Makefile.shared.inc Makefile.inc; \
make %{?_smp_mflags}

%define dobuild() \
rm -f Makefile.inc; \
ln -s Makefile.static.inc Makefile.inc; \
make %{?_smp_mflags} ptscotch; \
rm Makefile.inc; \
ln -s Makefile.shared.inc Makefile.inc; \
make %{?_smp_mflags} ptscotch

pushd scotch_%{version}/src/
%dosingle
popd

pushd scotch_%{version}_mpich/src/
%{_mpich_load}
%dobuild
%{_mpich_unload}
popd

module purge

pushd scotch_%{version}_openmpi/src/
%{_openmpi_load}
%dobuild
%{_openmpi_unload}
popd

%install
rm -rf %{buildroot}
module purge

%define doinst() \
pushd src/; \
rm -f Makefile.inc; \
ln -s Makefile.static.inc Makefile.inc; \
make %{?_smp_mflags} install %*; \
rm -f Makefile.inc; \
ln -s Makefile.shared.inc Makefile.inc; \
make %{?_smp_mflags} install %*; \
popd \
pushd $libdir; \
for lib in *.so; do \
	mv $lib $lib.0.0; \
	ln -s $lib.0.0 $lib; \
	ln -s $lib.0.0 $lib.0; \
done; \
popd

pushd scotch_%{version}/
export libdir=%{buildroot}%{_libdir}
%doinst prefix=%{buildroot}%{_prefix} libdir=%{buildroot}%{_libdir}

pushd %{buildroot}%{_bindir}/
for prog in *; do
	mv $prog scotch_$prog
done
popd
pushd %{buildroot}%{_mandir}/man1/
rm -f d*
for prog in *; do
	mv $prog scotch_$prog
done
popd
pushd %{buildroot}%{_bindir}
	rm -f scotch_gpart && ln -s ./scotch_gmap scotch_gpart
popd

# Convert the license files to utf8
pushd doc
iconv -f iso8859-1 -t utf-8 < CeCILL-C_V1-en.txt > CeCILL-C_V1-en.txt.conv
iconv -f iso8859-1 -t utf-8 < CeCILL-C_V1-fr.txt > CeCILL-C_V1-fr.txt.conv
mv -f CeCILL-C_V1-en.txt.conv CeCILL-C_V1-en.txt
mv -f CeCILL-C_V1-fr.txt.conv CeCILL-C_V1-fr.txt
popd

popd

pushd scotch_%{version}_mpich
%{_mpich_load}
export libdir=%{buildroot}/${MPI_LIB}
%doinst prefix=%{buildroot}/${MPI_HOME} libdir=%{buildroot}/${MPI_LIB} includedir=%{buildroot}/${MPI_INCLUDE} mandir=%{buildroot}/${MPI_MAN} bindir=%{buildroot}/${MPI_BIN}

pushd bin
for prog in *; do
	mv $prog %{buildroot}/${MPI_BIN}/scotch_${prog}
done
popd

pushd %{buildroot}/${MPI_MAN}/man1/
rm -f {a,g,m}*
for man in *; do
	mv ${man} scotch_${man}
done
popd
%{_mpich_unload}
popd

module purge

pushd scotch_%{version}_openmpi
%{_openmpi_load}
export libdir=%{buildroot}/${MPI_LIB}
%doinst prefix=%{buildroot}/${MPI_HOME} libdir=%{buildroot}/${MPI_LIB} includedir=%{buildroot}/${MPI_INCLUDE} mandir=%{buildroot}/${MPI_MAN} bindir=%{buildroot}/${MPI_BIN}

pushd bin
for prog in *; do
	mv $prog %{buildroot}/${MPI_BIN}/scotch_${prog}
done
popd

pushd %{buildroot}/${MPI_MAN}/man1/
rm -f {a,g,m}*
for man in *; do
	mv ${man} scotch_${man}
done
popd
%{_openmpi_unload}
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n ptscotch-mpich -p /sbin/ldconfig

%postun -n ptscotch-mpich -p /sbin/ldconfig

%post -n ptscotch-openmpi -p /sbin/ldconfig

%postun -n ptscotch-openmpi -p /sbin/ldconfig

%files
%{_bindir}/*
%{_libdir}/libscotch*.so.*
%{_mandir}/man1/*

%files devel
%{_libdir}/libscotch*.so
%{_includedir}/*scotch*.h

%files static
%{_libdir}/libscotch*.a

%files -n ptscotch-mpich
%{_libdir}/mpich/lib/lib*.so.*
%{_libdir}/mpich/bin/*
%{_mandir}/mpich/*

%files -n ptscotch-openmpi
%{_libdir}/openmpi/lib/lib*.so.*
%{_libdir}/openmpi/bin/*
%{_mandir}/openmpi*/*

%files -n ptscotch-mpich-devel
%{_includedir}/mpich*/*scotch*.h
%{_libdir}/mpich/lib/lib*.so

%files -n ptscotch-openmpi-devel
%{_includedir}/openmpi*/*scotch*.h
%{_libdir}/openmpi/lib/lib*.so

%files -n ptscotch-mpich-static
%{_libdir}/mpich/lib/lib*.a

%files -n ptscotch-openmpi-static
%{_libdir}/openmpi/lib/lib*.a

%files doc
%doc scotch_%{version}/README.txt scotch_%{version}/doc/*

%changelog
* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 05 2014 Sandro Mani <manisandro@gmail.com> - 6.0.0-7
- Fix under-linked libraries (#1098680)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 27 2014 Deji Akingunola <dakingun@gmail.com> - 6.0.0-5
- Slightly modified Erik Zeek spec re-write (See 2012-10-08 below)
- Rename mpich and openmpi subpackages as ptscotch-(mpich/openmpi) (Laurence Mcglashan)

* Mon Feb 24 2014 Deji Akingunola <dakingun@gmail.com> - 6.0.0-4
- Rebuild for mpich-3.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Deji Akingunola <dakingun@gmail.com> - 6.0.0-2
- Rename mpich2 sub-packages to mpich and rebuild for mpich-3.0

* Thu Jun 13 2013 Deji Akingunola <dakingun@gmail.com> - 6.0.0-1
- Update to 6.0.0
- Configured to run with 2 threads (for now)
- Install the headers in arch-dependent sub-directories

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.12-2.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Deji Akingunola <dakingun@gmail.com> - 5.1.12-1.b
- Update to 5.1.12b

* Mon Oct 08 2012 Erik Zeek <eczeek@sandia.gov> - 5.1.11-4
- Use internal build machinery to build shared libraries.
- A bunch of MPI love.
-   Install Mpich2 libraries in the proper path.
-   Provide Mpich2 and OpenMPI libraries.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 29 2011 Deji Akingunola <dakingun@gmail.com> - 5.1.11-1
- Update to 5.1.11

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.10b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 19 2010 Deji Akingunola <dakingun@gmail.com> - 5.1.10b-1
- Update to 5.1.10b

* Thu Aug 12 2010 Deji Akingunola <dakingun@gmail.com> - 5.1.9-1
- Update to 5.1.9
- No more static builds

* Tue Apr 27 2010 Deji Akingunola <dakingun@gmail.com> - 5.1.8-1
- Update to 5.1.8

* Wed Nov 04 2009 Deji Akingunola <dakingun@gmail.com> - 5.1.7-2
- Fix the Source url

* Sun Sep 20 2009 Deji Akingunola <dakingun@gmail.com> - 5.1.7-1
- Update to 5.1.7
- Put the library under libdir

* Thu Jun 11 2009 Deji Akingunola <dakingun@gmail.com> - 5.1.6-3
- Further spec fixes from package review (convert license files to utf8)
- Prefix binaries and their corresponding manpages with scotch_ .
- Link in appropriates libraries when creating shared libs

* Thu Jun 04 2009 Deji Akingunola <dakingun@gmail.com> - 5.1.6-2
- Add zlib-devel as BR

* Wed May 13 2009 Deji Akingunola <dakingun@gmail.com> - 5.1.6-1
- Update to 5.1.6

* Fri Nov 21 2008 Deji Akingunola <dakingun@gmail.com> - 5.1.2-1
- Update to 5.1.2

* Fri Sep 19 2008 Deji Akingunola <dakingun@gmail.com> - 5.1.1-1
- initial package creation
