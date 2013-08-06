Summary:	Graph, mesh and hypergraph partitioning library
Name:		scotch
Version:	6.0.0
Release:	3%{?dist}
License:	CeCILL-C
Group:		Development/Libraries
URL:		http://www.labri.fr/perso/pelegrin/scotch/
Source0:	https://gforge.inria.fr/frs/download.php/31831/%{name}_%{version}.tar.gz
Source1:	scotch-Makefile.inc.in
BuildRequires:	flex bison mpich-devel zlib-devel bzip2-devel lzma-devel

%description
Scotch is a software package for graph and mesh/hypergraph partitioning and
sparse matrix ordering. 

%package devel
Summary:	Development libraries for scotch
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains development libraries for scotch.

%prep
%setup -q -n scotch_%{version}
sed s/@RPMFLAGS@/'%{optflags} -fPIC'/ < %SOURCE1 > src/Makefile.inc

%build
cd src/
make %{?_smp_mflags}
gcc -shared -Wl,-soname=libscotcherr.so.0 -o ../lib/libscotcherr.so.0.0	\
	libscotch/library_error.o
gcc -shared -Wl,-soname=libscotcherrexit.so.0 -o	\
	../lib/libscotcherrexit.so.0.0	libscotch/library_error_exit.o
rm -f libscotch/library_error*.o
gcc -shared -Wl,-soname=libscotch.so.0 -o ../lib/libscotch.so.0.0	\
	libscotch/*.o ../lib/libscotcherr.so.0.0 -lpthread -lgfortran -lz -lbz2 -llzmadec -lrt
gcc -shared -Wl,-soname=libscotchmetis.so.0 -o ../lib/libscotchmetis.so.0.0\
	libscotchmetis/*.o ../lib/libscotch.so.0.0 ../lib/libscotcherr.so.0.0

%{_mpich_load}
make %{?_smp_mflags} ptscotch
mpicc -shared -Wl,-soname=libptscotcherr.so.0 -o ../lib/libptscotcherr.so.0.0\
	libscotch/library_error.o
mpicc -shared -Wl,-soname=libptscotcherrexit.so.0 -o	\
	../lib/libptscotcherrexit.so.0.0  libscotch/library_error_exit.o
rm -f libscotch/library_error*.o
mpicc -shared -Wl,-soname=libptscotch.so.0 -o ../lib/libptscotch.so.0.0	\
	libscotch/*.o ../lib/libptscotcherr.so.0.0 -lgfortran -lz -lbz2 -llzmadec
mpicc -shared -Wl,-soname=libptscotchparmetis.so.0 -o	\
	../lib/libptscotchparmetis.so.0.0 libscotchmetis/*.o	\
	../lib/libptscotch.so.0.0 ../lib/libptscotcherr.so.0.0
%{_mpich_unload}

%install
rm -rf %{buildroot}
pushd src/
make install prefix=%{buildroot}%{_prefix} libdir=%{buildroot}%{_libdir} \
             includedir=%{buildroot}%{_includedir}/%{name}-%{_arch}/

popd
cp -pr include/*metis.h %{buildroot}%{_includedir}/%{name}-%{_arch}/

pushd lib
	for static_libs in lib*scotch*.a ; do
		libs=`basename $static_libs .a`
		ln -s $libs.so.0.0 $libs.so.0
		ln -s $libs.so.0.0 $libs.so
                rm -f $static_libs
	done
	cp -dp lib*scotch*.so* %{buildroot}%{_libdir}/
popd
rm -f %{buildroot}%{_libdir}/*.a

rm -f %{buildroot}%{_bindir}/*
rm -f %{buildroot}%{_mandir}/man1/*
pushd man/man1
	for progs in *.1 ; do
		prog=`basename $progs .1`
		cp -dp ../../bin/$prog %{buildroot}%{_bindir}/scotch_$prog
		cp -dp $progs %{buildroot}%{_mandir}/man1/scotch_$progs
	done
popd
pushd %{buildroot}%{_bindir}
	rm -f scotch_dgpart && ln -s ./scotch_dgmap scotch_dgpart
	rm -f scotch_gpart && ln -s ./scotch_gmap scotch_gpart
popd

# Convert the license files to utf8
pushd doc
iconv -f iso8859-1 -t utf-8 < CeCILL-C_V1-en.txt > CeCILL-C_V1-en.txt.conv
iconv -f iso8859-1 -t utf-8 < CeCILL-C_V1-fr.txt > CeCILL-C_V1-fr.txt.conv
mv -f CeCILL-C_V1-en.txt.conv CeCILL-C_V1-en.txt
mv -f CeCILL-C_V1-fr.txt.conv CeCILL-C_V1-fr.txt
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README.txt doc/*
%{_bindir}/*
%{_libdir}/lib*scotch*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*scotch*.so
%{_includedir}/%{name}-%{_arch}/*scotch*.h
%{_includedir}/%{name}-%{_arch}/*metis.h

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Deji Akingunola <dakingun@gmail.com> - 6.0.0-2
- Rename mpich2 sub-packages to mpich and rebuild for mpich-3.0

* Thu Jun 13 2013 Deji Akingunola <dakingun@gmail.com> - 6.0.0-1
- Update to 6.0.0
- Configured to run with 2 threads (for now)
- Install the headers in arch-dependent sub-directories

* Sat Nov 17 2012 Deji Akingunola <dakingun@gmail.com> - 5.1.12-1.b
- Update to 5.1.12b

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

* Sat Nov 21 2008 Deji Akingunola <dakingun@gmail.com> - 5.1.2-1
- Update to 5.1.2

* Tue Sep 19 2008 Deji Akingunola <dakingun@gmail.com> - 5.1.1-1
- initial package creation
