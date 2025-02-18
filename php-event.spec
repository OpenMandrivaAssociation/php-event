%define modname event
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A35_%{modname}.ini

Summary:	Event Scheduling Engine for PHP
Name:		php-%{modname}
Version:	1.8.1
Release:	2
Group:		Development/PHP
License:	PHP License
URL:		https://pecl.php.net/package/event
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	pkgconfig(libevent)
Epoch:		1

%description
This is an extension to efficiently schedule IO, time and signal based events
using the best available IO notification mechanism for your system. This is a
port of libevent to the PHP infrastructure; the API is similar but not
identical.

%prep
%setup -q -n event-%{version}

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

%clean
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%doc CREDITS
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
