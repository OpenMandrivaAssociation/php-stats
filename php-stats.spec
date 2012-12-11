%define modname stats
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A51_%{modname}.ini

Summary:	Extension with routines for statistical computation for PHP
Name:		php-%{modname}
Version:	1.0.2
Release:	%mkrel 32
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/stats/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tar.bz2
Patch0:		stats-1.0.2-php54x.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Extension that provides few dozens routines for statistical computation for
PHP.

%prep

%setup -q -n %{modname}-%{version}
[ "../package.xml" != "/" ] && mv ../package*.xml .

%patch0 -p0

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc tests CREDITS TODO package*.xml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-32mdv2012.0
+ Revision: 797016
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-31
+ Revision: 761298
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-30
+ Revision: 696473
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-29
+ Revision: 695468
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-28
+ Revision: 646688
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-27mdv2011.0
+ Revision: 629873
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-26mdv2011.0
+ Revision: 628193
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-25mdv2011.0
+ Revision: 600533
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-24mdv2011.0
+ Revision: 588871
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-23mdv2010.1
+ Revision: 514660
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-22mdv2010.1
+ Revision: 485486
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-21mdv2010.1
+ Revision: 468257
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-20mdv2010.0
+ Revision: 451360
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1.0.2-19mdv2010.0
+ Revision: 397607
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-18mdv2010.0
+ Revision: 377030
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-17mdv2009.1
+ Revision: 346637
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-16mdv2009.1
+ Revision: 341802
- rebuilt against php-5.2.9RC2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-15mdv2009.1
+ Revision: 323090
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-14mdv2009.1
+ Revision: 310310
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-13mdv2009.0
+ Revision: 238431
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-12mdv2009.0
+ Revision: 200271
- rebuilt for php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-11mdv2008.1
+ Revision: 162241
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-10mdv2008.1
+ Revision: 107722
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-9mdv2008.0
+ Revision: 77578
- rebuilt against php-5.2.4

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-8mdv2008.0
+ Revision: 39525
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-7mdv2008.0
+ Revision: 33877
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-6mdv2008.0
+ Revision: 21357
- rebuilt against new upstream version (5.2.2)


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-5mdv2007.0
+ Revision: 117632
- rebuilt against new upstream version (5.2.1)

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-4mdv2007.0
+ Revision: 79297
- rebuild
- rebuilt for php-5.2.0
- Import php-stats

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-2
- rebuilt for php-5.1.6

* Fri Jun 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-1mdv2007.0
- initial Mandriva package

