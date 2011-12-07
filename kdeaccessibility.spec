Summary: KDE Accessibility
Name: kdeaccessibility
Epoch: 1
Version: 4.3.4
Release: 4%{?dist}

Group: User Interface/Desktops
License: GPLv2
URL: http://accessibility.kde.org/
Source0: ftp://ftp.kde.org/pub/kde/stable/%{version}/src/kdeaccessibility-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# upstream patches
Patch100: kdeaccessibility-4.3.5.patch

BuildRequires: alsa-lib-devel
BuildRequires: desktop-file-utils
BuildRequires: festival
BuildRequires: kdelibs4-devel >= %{version}

Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires: festival

Obsoletes: kdeaccessibility-devel < 1:3.5.8
Obsoletes: kdeaccessibility < 1:4.3.0-2

Provides: mono-icon-theme = %{version}-%{release}

%description
Included with this package are:
* kmag: a screen magnifier
* kmousetool: a program for people whom it hurts to click the mouse
* kmouth: program that allows people who have lost their voice
* ktts: text to speech support

%package libs
Summary: Runtime libraries for %{name}
Group: System Environment/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: kdelibs4%{?_isa} >= %{version}

%description libs
%{summary}.


%prep
%setup -q

# upstream patches
%patch100 -p1 -b .kde435

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# hack around HTML doc multilib conflicts
for doxy_hack in kmousetool kmouth kttsd ; do
pushd %{buildroot}%{_kde4_docdir}/HTML/en/${doxy_hack}
bunzip2 index.cache.bz2
sed -i -e 's!<a name="id[0-9]*"></a>!!g' index.cache
bzip2 -9 index.cache
done
popd

# unpackaged files
rm -vf %{buildroot}%{_kde4_libdir}/libkttsd.so


%check
for f in %{buildroot}%{_kde4_datadir}/applications/kde4/*.desktop ; do
  desktop-file-validate $f
done


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
touch --no-create %{_kde4_iconsdir}/mono &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null
  touch --no-create %{_kde4_iconsdir}/mono &> /dev/null
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null
  gtk-update-icon-cache %{_kde4_iconsdir}/mono &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/mono &> /dev/null || :

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING
%{_kde4_bindir}/*
%{_kde4_appsdir}/kmag/
%{_kde4_appsdir}/kmousetool/
%{_kde4_appsdir}/kmouth/
%{_kde4_appsdir}/kttsd/
%{_kde4_appsdir}/color-schemes/*.colors
%{_kde4_configdir}/*
%{_kde4_datadir}/applications/kde4/*.desktop
%{_kde4_datadir}/kde4/services/*
%{_kde4_datadir}/kde4/servicetypes/*
%{_kde4_docdir}/HTML/en/kmag/
%{_kde4_docdir}/HTML/en/kmousetool/
%{_kde4_docdir}/HTML/en/kmouth/
%{_kde4_docdir}/HTML/en/kttsd/
%{_kde4_iconsdir}/mono/
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_libdir}/kde4/*
%{_mandir}/man1/*.1*

%files libs
%defattr(-,root,root,-)
%{_kde4_libdir}/libkttsd.so.4*


%changelog
* Tue Mar 30 2010 Than Ngo <than@redhat.com> - 4.3.4-4
- rebuilt against qt-4.6.2

* Fri Jan 22 2010 Than Ngo <than@redhat.com> - 4.3.4-3
- update translation

* Sat Dec 12 2009 Than Ngo <than@redhat.com> - 4.3.4-2
- cleanup

* Tue Dec 01 2009 Than Ngo <than@redhat.com> - 4.3.4-1
- 4.3.4

* Wed Nov 11 2009 Than Ngo <than@redhat.com> - 4.3.3-2
- rhel cleanup, drop BR on flite-devel

* Sat Oct 31 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-1
- 4.3.3

* Sun Oct 04 2009 Than Ngo <than@redhat.com> - 4.3.2-1
- 4.3.2

* Fri Aug 28 2009 Than Ngo <than@redhat.com> - 4.3.1-1
- 4.3.1

* Sun Aug 02 2009 Rex Dieter <rdieter@fedoraproject.org> 1:4.3.0-3
- include epoch's in -libs-related Requires

* Sat Aug 01 2009 Rex Dieter <rdieter@fedoraproject.org> 1:4.3.0-2
- -libs subpkg: Multilib conflicts for index.cache.bz2 (#515085)
- %%check: desktop-file-validate

* Thu Jul 30 2009 Than Ngo <than@redhat.com> - 1:4.3.0-1
- 4.3.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.2.98-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Than Ngo <than@redhat.com> - 4.2.98-1
- 4.3rc3

* Thu Jul 09 2009 Than Ngo <than@redhat.com> - 4.2.96-1
- 4.3rc2

* Thu Jun 25 2009 Than Ngo <than@redhat.com> - 4.2.95-1
- 4.3 rc1

* Thu Jun 04 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 1:4.2.90-1
- KDE 4.3 beta 2

* Wed May 13 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.85-1
- KDE 4.3 beta 1

* Wed Apr 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.2-2
- Requires: festival (for kttsd)

* Mon Mar 30 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.2-1
- KDE 4.2.2

* Mon Mar 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.1-2
- scriptlet optimization

* Fri Feb 27 2009 Than Ngo <than@redhat.com> - 4.2.1-1
- 4.2.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Than Ngo <than@redhat.com> - 4.2.0-1
- 4.2.0

* Fri Jan 09 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 1:4.1.96-2
- rebuilt
- fix file list

* Wed Jan 07 2009 Than Ngo <than@redhat.com> - 4.1.96-1
- 4.2rc1

* Thu Dec 11 2008 Than Ngo <than@redhat.com> -  4.1.85-1
- 4.2beta2

* Thu Dec 04 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.80-4
- rebuild for fixed kde-filesystem (macros.kde4) (get rid of rpaths)

* Thu Dec 04 2008 Rex Dieter <rdieter@fedoraproject.or> 4.1.80-3
- drop (Build)Requires: kdebase-workspace(-devel)
- BR: plasma-devel
- better, versioned Obsoletes: kdeaccessibility-devel ...

* Thu Nov 20 2008 Than Ngo <than@redhat.com> 4.1.80-2
- remove duplicated BR on cmake, it's already done in kdelibs-devel

* Wed Nov 19 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 1:4.1.80-1
- 4.1.80
- BR cmake >= 2.6.2
- make install/fast

* Tue Nov 11 2008 Than Ngo <than@redhat.com> 4.1.3-1
- KDE 4.1.3

* Mon Sep 29 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-2
- make VERBOSE=1
- respin against new(er) kde-filesystem

* Fri Sep 26 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-1
- 4.1.2

* Fri Aug 29 2008 Than Ngo <than@redhat.com> 4.1.1-1
- 4.1.1

* Wed Jul 23 2008 Than Ngo <than@redhat.com> 4.1.0-1
- 4.1.0

* Fri Jul 18 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.99-1
- 4.0.99

* Fri Jul 11 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.98-1
- 4.0.98

* Sun Jul 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.85-1
- 4.0.85

* Fri Jun 27 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.84-1
- 4.0.84

* Thu Jun 19 2008 Than Ngo <than@redhat.com> 4.0.83-1
- 4.0.83 (beta2)

* Sun Jun 15 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.82-1
- 4.0.82

* Mon May 26 2008 Than Ngo <than@redhat.com> 4.0.80-1
- Beta 1

* Wed May 07 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.72-1
- update to 4.0.72

* Thu Apr 03 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-3
- rebuild (again) for the fixed %%{_kde4_buildtype}

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-2
- rebuild for NDEBUG and _kde4_libexecdir

* Fri Mar 28 2008 Than Ngo <than@redhat.com> 4.0.3-1
- 4.0.3

* Thu Feb 28 2008 Than Ngo <than@redhat.com> 4.0.2-1
- 4.0.2

* Thu Jan 31 2008 Rex Dieter <rdieter@fedoraproject.org> 1:4.0.1-1
- 4.0.1

* Tue Jan 08 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 1:4.0.0-1
- update to 4.0.0
- update file list

* Fri Dec 07 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1:3.97.0-2
- fix %%files (unpackaged mono/index.theme)

* Wed Dec 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1:3.97.0-1
- kde-3.97.0

* Tue Dec 04 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1:3.96.2-2
- minor touchups
- Provides: mono-icon-theme
- drop -libs,-devel subpkgs

* Fri Nov 30 2007 Sebastian Vahl <fedora@deadbabylon.de> 1:3.96.2-1
- kde-3.96.2

* Sat Nov 24 2007 Sebastian Vahl <fedora@deadbabylon.de> 1:3.96.1-1
- kde-3.96.1
- added epoch in changelog (also backwards)

* Thu Nov 22 2007 Sebastian Vahl <fedora@deadbabylon.de> 1:3.96.0-4
- libs subpkg

* Fri Nov 16 2007 Sebastian Vahl <fedora@deadbabylon.de> 1:3.96.0-3
- BR: kde-filesystem >= 4

* Fri Nov 16 2007 Sebastian Vahl <fedora@deadbabylon.de> 1:3.96.0-2
- BR: libXtst-devel
- fix copy&paste error in devel package

* Fri Nov 16 2007 Sebastian Vahl <fedora@deadbabylon.de> 1:3.96.0-1
- Initial version for Fedora

* Tue Oct 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1:3.5.8-3
- Obsoletes: %%name ... to help out multilib upgrades

* Sat Oct 13 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1:3.5.8-2
- Obsoletes: %%name-devel

* Sat Oct 13 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1:3.5.8-1
- kde-3.5.8
- omit -devel subpkg

* Mon Aug 20 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1:3.5.7-3
- License: GPLv2
- Provides: kdeaccessibility3(-devel)
- (Build)Requires: kdelibs3(-devel)

* Sat Jun 16 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1:3.5.7-2
- portability (rhel)
- omit .desktop patch (doesn't apply)

* Sat Jun 16 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1:3.5.7-1
- cleanup

* Thu Jun 07 2007 Than Ngo <than@redhat.com> - 1:3.5.7-0.1.fc7
- 3.5.7

* Mon Mar 12 2007 Than Ngo <than@redhat.com> 1:3.5.6-3.fc7
- fix broken dependencies

* Mon Feb 26 2007 Than Ngo <than@redhat.com> - 1:3.5.6-2.fc7
- cleanup specfile

* Wed Feb 07 2007 Than Ngo <than@redhat.com> 1:3.5.6-1.fc7
- 3.5.6

* Thu Aug 10 2006 Than Ngo <than@redhat.com> 1:3.5.4-1
- rebuild

* Mon Jul 24 2006 Than Ngo <than@redhat.com> 1:3.5.4-0.pre1
- prerelease of 3.5.4 (from the first-cut tag)

* Mon Jul 17 2006 Than Ngo <than@redhat.com> 1:3.5.3-2
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:3.5.3-1.1
- rebuild

* Fri Jun 02 2006 Than Ngo <than@redhat.com> 1:3.5.3-1
- update to 3.5.3

* Tue Apr 04 2006 Than Ngo <than@redhat.com> 1:3.5.2-1
- update to 3.5.2

* Wed Mar 01 2006 Karsten Hopp <karsten@redhat.de> 3.5.1-2
- BuildRequires: libXtst-devel

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:3.5.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:3.5.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Than Ngo <than@redhat.com> 1:3.5.1-1
- 3.5.1

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec 01 2005 Than Ngo <than@redhat.com> 1:3.5.0-1
- 3.5

* Tue Oct 25 2005 Than Ngo <than@redhat.com> 1:3.4.92-1
- update to 3.5 beta2

* Mon Oct 10 2005 Than Ngo <than@redhat.com> 1:3.4.91-1
- update to 3.5 beta 1

* Mon Aug 08 2005 Than Ngo <than@redhat.com> 1:3.4.2-1
- update to 3.4.2

* Tue Jun 28 2005 Than Ngo <than@redhat.com> 1:3.4.1-1
- 3.4.1
- fix gcc4 build problem

* Wed Mar 16 2005 Than Ngo <than@redhat.com> 1:3.4.0-1
- KDE 3.4.0 final

* Sun Feb 27 2005 Than Ngo <than@redhat.com> 1:3.4.0-0.rc1.1
- KDE 3.4.0 rc1

* Sun Feb 20 2005 Than Ngo <than@redhat.com> 1:3.3.92-0.1
- KDE 3.4 beta2

* Sun Dec 05 2004 Than Ngo <than@redhat.com> 3.3.2-0.1
- update to 3.3.2

* Fri Jun 04 2004 Than Ngo <than@redhat.com> 1:3.2.3-0.1
- update to 3.2.3

* Mon Apr 12 2004 Than Ngo <than@redhat.com> 1:3.2.2-0.1
- 3.2.2 release

* Sat Mar 06 2004 Than Ngo <than@redhat.com> 1:3.2.1-0.1
- 3.2.1 release

* Fri Feb 06 2004 Than Ngo <than@redhat.com> 1:3.2.0-0.2
- rebuilt against qt 3.3.0

* Mon Feb 02 2004 Than Ngo <than@redhat.com> 1:3.2.0-0.1
- 3.2.0 release

* Sun Dec 07 2003 Than Ngo <than@redhat.com> 6:3.1.94-0.1
- KDE 3.2 Beta 2

* Sat Nov 15 2003 Than Ngo <than@redhat.com> 6:3.1.93-0.1
- initial rpm for Fedora
