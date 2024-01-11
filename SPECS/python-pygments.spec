%global debug_package %{nil}
# python2X and python3X are built form the same module, so we need a conditional
# for python[23] bits the state of the conditional is not important in the spec,
# it is set in modulemd
%bcond_without python2
%bcond_without python3
%bcond_with python36_module

%if %{without python3}
%bcond_with doc
%else
%bcond_without doc
%endif

%bcond_without tests

%global upstream_name Pygments
%global srcname pygments
%global sum Syntax highlighting engine written in Python

Name:           python-pygments
Version:        2.2.0
Release:        22%{?dist}
Summary:        %{sum}

License:        BSD
URL:            http://pygments.org/
Source0:        https://pypi.org/packages/source/P/%{upstream_name}/%{upstream_name}-%{version}.tar.gz
Patch0:         import-directive.patch
BuildArch:      noarch

# Fix CVE-2021-20270: infinite loop in SML lexer which may lead to DoS
# Resolved upstream: https://github.com/pygments/pygments/commit/f91804ff4772e3ab41f46e28d370f57898700333
Patch1:         CVE-2021-20270-infinite-loop-in-SML-lexer.patch

# CVE-2021-27291: ReDos via crafted malicious input
# Tracking bugzilla: https://bugzilla.redhat.com/show_bug.cgi?id=CVE-2021-27291
# Upstream fix: https://github.com/pygments/pygments/commit/2e7e8c4a7b318f4032493773732754e418279a14
Patch2:         CVE-2021-27291.patch

%if %{with python3}
BuildRequires:  python3-sphinx
%endif

%description
Pygments is a generic syntax highlighter for general use in all kinds
of software such as forum systems, wikis or other applications that
need to prettify source code. Highlights are:

  * a wide range of common languages and markup formats is supported
  * special attention is paid to details that increase highlighting
    quality
  * support for new languages and formats are added easily; most
    languages use a simple regex-based lexing mechanism
  * a number of output formats is available, among them HTML, RTF,
    LaTeX and ANSI sequences
  * it is usable as a command-line tool and as a library
  * ... and it highlights even Brainf*ck!


%if %{with python2}
%package -n python2-%{srcname}
BuildRequires:  python2-devel >= 2.4
BuildRequires:  python2-setuptools
BuildRequires:  python2-nose
Summary:        %{sum}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
Pygments is a generic syntax highlighter for general use in all kinds
of software such as forum systems, wikis or other applications that
need to prettify source code. Highlights are:

  * a wide range of common languages and markup formats is supported
  * special attention is paid to details that increase highlighting
    quality
  * support for new languages and formats are added easily; most
    languages use a simple regex-based lexing mechanism
  * a number of output formats is available, among them HTML, RTF,
    LaTeX and ANSI sequences
  * it is usable as a command-line tool and as a library
  * ... and it highlights even Brainf*ck!
%endif


%if %{with python3}
%package -n python3-%{srcname}
%if %{with python36_module}
BuildRequires:  python36-devel
BuildRequires:  python36-rpm-macros
%else
BuildRequires:  python3-devel
%endif
BuildRequires:  python3-setuptools, python3-nose
Summary:        %{sum}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
Pygments is a generic syntax highlighter for general use in all kinds
of software such as forum systems, wikis or other applications that
need to prettify source code. Highlights are:

  * a wide range of common languages and markup formats is supported
  * special attention is paid to details that increase highlighting
    quality
  * support for new languages and formats are added easily; most
    languages use a simple regex-based lexing mechanism
  * a number of output formats is available, among them HTML, RTF,
    LaTeX and ANSI sequences
  * it is usable as a command-line tool and as a library
  * ... and it highlights even Brainf*ck!
%endif

%prep
%setup -q -n %{upstream_name}-%{version}
%patch0 -p 1
%patch1 -p1
%patch2 -p1

%build
%{__sed} -i 's/\r//' LICENSE
%{?with_python2:%py2_build}
%{?with_python3:%py3_build}
%{?with_doc:%{__python3} setup.py build_sphinx}

%install
# Python 2 install
# NOTE: sphinx is built on Python 3 and packages with python2 and python3
%if %{with python2}
%py2_install
mv %{buildroot}%{_bindir}/pygmentize{,-%{python2_version}}
ln -s pygmentize-%{python2_version} %{buildroot}%{_bindir}/pygmentize-2
%endif

%if %{with doc}
pushd doc
install -d %{buildroot}%{_mandir}/man1
mv pygmentize.1 $RPM_BUILD_ROOT%{_mandir}/man1/pygmentize.1
popd
cp -r doc/docs doc/reST
%endif

%if %{with python3}
%py3_install
cp %{buildroot}%{_bindir}/pygmentize{,-%{python3_version}}
ln -s pygmentize-%{python3_version} %{buildroot}%{_bindir}/pygmentize-3
%endif

%check
%if %{with tests}
%{?with_python2:make test PYTHON=%{__python2}}
%{?with_python3:make test PYTHON=%{__python3}}
%endif

%if %{with python2}
%files -n python2-pygments
%doc AUTHORS CHANGES TODO
%if %{with doc}
%doc build/sphinx/html doc/reST
%lang(en) %{_mandir}/man1/pygmentize.1*
%endif
%license LICENSE
%{python2_sitelib}/*
%{_bindir}/pygmentize-2
%{_bindir}/pygmentize-%{python2_version}
%endif

%if %{with python3}
%files -n python3-pygments
%doc AUTHORS CHANGES TODO
%if %{with doc}
%doc build/sphinx/html doc/reST
%lang(en) %{_mandir}/man1/pygmentize.1*
%endif
%license LICENSE
%{python3_sitelib}/*
%{_bindir}/pygmentize
%{_bindir}/pygmentize-3
%{_bindir}/pygmentize-%{python3_version}
%endif

%changelog
* Thu Apr 22 2021 Lumír Balhar <lbalhar@redhat.com> - 2.2.0-22
- Fix CVE-2021-27291: ReDos via crafted malicious input
Resolves: rhbz#1943459 rhbz#1943460

* Wed Mar 03 2021 Charalampos Stratakis <cstratak@redhat.com> - 2.2.0-21
- Fix CVE-2021-20270: infinite loop in SML lexer which may lead to DoS
Resolves: rhbz#1933876

* Thu Apr 25 2019 Tomas Orsava <torsava@redhat.com> - 2.2.0-20
- Bumping due to problems with modular RPM upgrade path
- Resolves: rhbz#1695587

* Mon Sep 17 2018 Lumír Balhar <lbalhar@redhat.com> - 2.2.0-19
- Get rid of unversioned Python dependencies
- Resolves: rhbz#1628242

* Wed Aug 08 2018 Lumír Balhar <lbalhar@redhat.com> - 2.2.0-18
- Remove unversioned binaries from python2 subpackage
- Resolves: rhbz#1613343

* Wed Aug 01 2018 Lumír Balhar <lbalhar@redhat.com> - 2.2.0-17
- Specfile cleanup
- Condition for tests
- Condition for doc

* Tue Jul 31 2018 Lumír Balhar <lbalhar@redhat.com> - 2.2.0-16
- Switch python3 coditions to bcond

* Wed Jul 18 2018 Tomas Orsava <torsava@redhat.com> - 2.2.0-15
- BuildRequire also python36-rpm-macros as part of the python36 module build

* Wed Jul 04 2018 Miro Hrončok <mhroncok@redhat.com> - 2.2.0-14
- Add a bcond for python2
- Fix the test invocation

* Thu Jun 14 2018 Tomas Orsava <torsava@redhat.com> - 2.2.0-13
- Switch to using Python 3 version of sphinx

* Mon Apr 30 2018 Tomas Orsava <torsava@redhat.com> - 2.2.0-12
- Require the python36-devel package when building for the python36 module

* Mon Mar 19 2018 Steve Milner <smilner@redhat.com> - 2.2.0-11
- Added import-directive.patch to work around a change in sphinx.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 2.2.0-9
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 22 2017 Steve Milner <smilner@redhat.com> - 2.2.0-7
- Fixed python2 sitelib in files section.

* Wed Mar 22 2017 Steve Milner <smilner@redhat.com> - 2.2.0-6
- Dropped python26 support.
- Spec clean up

* Mon Mar 20 2017 Steve Milner <smilner@redhat.com> - 2.2.0-5
- Updated for standards per BZ#1433650

* Mon Mar  6 2017 Steve Milner <smilner@redhat.com> - 2.2.0-4
- Added conflict per BZ#1429075

* Mon Mar  6 2017 Steve Milner <smilner@redhat.com> - 2.2.0-3
- Python3 package now houses the pygmentize binary
- Fixed Source0 url to point to pypi.org
- Made python3-nose a hard BuildRequirement for python3

* Thu Mar  2 2017 Steve Milner <smilner@redhat.com> - 2.2.0-2
- Update bin to come back into line with Fedora standards

* Thu Mar  2 2017 Steve Milner <smilner@redhat.com> - 2.2.0-1
- Update for upstream release.

* Thu Mar  2 2017 Steve Milner <smilner@redhat.com> - 2.1.3-5
- Split bin between versions.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 2.1.3-3
- Rebuild for Python 3.6
- Don't make rpmbuild fail on failed tests for now

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Mar  4 2016 Steve Milner <smilner@redhat.com> - 2.1.3-1
- Update for upstream release.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 12 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Oct 29 2015 Steve Milner <smilner@redhat.com> - 2.0.2-3
- Backport patch to fix font manager shell injection for BZ#1276321

* Mon Oct 12 2015 Robert Kuska <rkuska@redhat.com> - 2.0.2-2
- Rebuilt for Python3.5 rebuild
- Also remove python3-sphinx from BR as docs are built only with python2-sphinx

* Mon Aug 24 2015 Steve Milner <smilner@redhat.com> - 2.0.2-1
- update for upstream release.
- Added python-pygments/python3-pygments to BuildRequires.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 10 2014 Orion Poplawski <orion@cora.nwra.com> - 1.6-2
- Rebuild for Python 3.4

* Tue Nov 26 2013 Steve Milner <smilner@fedoraproject.org> - 1.6-1
- update for upstream release.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 1.4-7
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 1.4-6
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 13 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.4-3
- Really enable the python3 unittests.
- Fix python26 byte compilation (thanks to Jeffrey Ness)

* Sat Sep 10 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.4-2
- Fix python main package having dependencies for the python2.6 subpackage
- Fix places that used the default python instead of python26
- Attempt to make byte compilation more robust in case we add python3 to EPEL5
- Run unittests on python3 in F15+

* Fri Jun 24 2011 Steve Milner <smilner@fedoraproject.org> - 1.4-1
- update for upstream release
- Add python2.6 support done by Steve Traylen <steve.traylen@cern.ch>. BZ#662755.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.3.1-7
- update to most recent python guidelines
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu May  6 2010 Gareth Armstrong <gareth.armstrong@hp.com> - 1.3.1-5
- Enforce that Pygments requires Python 2.4 or later via an explicit BR
- Minor tweaks to spec file
- Deliver html and reST doc files to specifically named directories
- Align description with that of http://pygments.org/
- Add %%check section for Python2 and add BR on python-nose

* Fri Apr 23 2010 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.3.1-4
- switched with_python3 back to 1

* Fri Apr 23 2010 David Malcolm <dmalcolm@redhat.com> - 1.3.1-3
- add python3 subpackage (BZ#537244), ignoring soft-dep on imaging for now

* Tue Apr 13 2010 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.3.1-2
- added python-imaging as a dependency per BZ#581663.

* Sat Mar  6 2010 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.3.1-1
- Updated for release.

* Tue Sep 29 2009 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.1.1-1
- Updated for release.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 21 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.0-3
- Updated for release.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0-2
- Rebuild for Python 2.6

* Thu Nov 27 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.0-1
- Updated for upstream 1.0.

* Sun Sep 14 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 0.11.1-1
- Updated for upstream 0.11.

* Mon Jul 21 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 0.10-1
- Updated for upstream 0.10.

* Thu Nov 29 2007 Steve 'Ashcrow' Milner <me@stevemilner.org> - 0.9-2
- Added python-setuptools as a Requires per bz#403601.

* Mon Nov 12 2007 Steve 'Ashcrow' Milner <me@stevemilner.org> - 0.9-1
- Updated for upstream 0.9.

* Fri Aug 17 2007 Steve 'Ashcrow' Milner <me@stevemilner.org> - 0.8.1-2
- Removed the dos2unix build dependency.

* Thu Jun 28 2007 Steve 'Ashcrow' Milner <me@stevemilner.org> - 0.8.1-1
- Initial packaging for Fedora.
