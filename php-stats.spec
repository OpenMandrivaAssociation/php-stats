%define modname stats
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A51_%{modname}.ini

Summary:	Extension with routines for statistical computation for PHP
Name:		php-%{modname}
Version:	1.0.3
Release:	2
Group:		Development/PHP
License:	PHP License
URL:		https://pecl.php.net/package/stats/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
BuildRequires:	php-devel

%description
Extension that provides few dozens routines for statistical computation for
PHP.

%prep

%setup -qn %{modname}-%{version}
[ "../package.xml" != "/" ] && mv ../package*.xml .

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

%files 
%doc tests CREDITS TODO package*.xml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
