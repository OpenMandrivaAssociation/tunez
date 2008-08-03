%define name tunez
%define version 1.21
%define release %mkrel 7
%define wwwtunez %{_var}/www/%{name}

# TODO rewrite configure_tunez in perl to avoid the duplication of configuration
# try to have more autodetection and stuff like good default value

Summary: MP3/Ogg Vorbis jukebox that works with a voting system
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
Source1: configure_tunez
Source2: README.urpmi.tunez
Source3: ices_config.pm
Patch0:  config.inc.php.patch.bz2
Patch1:	 tunez.inc.php.patch.bz2
Patch2:  tunezd.patch.bz2
Patch3:  tunez-ices_config.patch.bz2
License: GPL
Group:   Sound
Url: http://tunez.sf.net
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires(pre):  apache-conf >= 2.0.54
Requires(pre):  apache-mpm >= 2.0.54
Requires(pre):	rpm-helper
Requires:       apache-mod_php php-xml
Requires:	php-curl
Requires:	php-mysql
Requires:	ices

%description
Tunez in an mp3/ogg jukebox that works with a voting system that users access
through a web interface.  Each registered user can vote for the tracks he
wants and the Tunez daemon will take care of playing the most popular songs
either locally (through a soundcard) or through a streaming server, depending
on the setup.

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0

%build
make -C detach-1.2
make -C tmixer
cp %SOURCE2 README.urpmi

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1/
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/tunez
mkdir -p $RPM_BUILD_ROOT/%wwwtunez

#Installing Tunez
mv html/* $RPM_BUILD_ROOT/%wwwtunez
rm -rf html

cp %SOURCE1 $RPM_BUILD_ROOT/%{_datadir}/tunez
cp tmixer/smixer $RPM_BUILD_ROOT/%{_bindir}
cp tmixer/smixer.conf $RPM_BUILD_ROOT/%{_sysconfdir}
cp tmixer/man/smixer.1 $RPM_BUILD_ROOT/%{_mandir}/man1
cp detach-1.2/detach $RPM_BUILD_ROOT/%{_bindir}
cp detach-1.2/detach.1 $RPM_BUILD_ROOT/%{_mandir}/man1

rm -rf detach-1.2
rm -rf tmixer
# useless code
rm -Rf tunezsrv

cp -av * $RPM_BUILD_ROOT/%{_datadir}/tunez
rm -f $RPM_BUILD_ROOT/%{_datadir}/tunez/README.urpmi

mv $RPM_BUILD_ROOT/%_datadir/%{name}/config.inc.php $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/
ln -s %{_sysconfdir}/%{name}/config.inc.php $RPM_BUILD_ROOT/%_datadir/%{name}/config.inc.php

cp %SOURCE3 $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/


# apache configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf <<EOF
Alias /%{name} %{wwwtunez}
<Directory %{wwwtunez}>
    Allow from all
    php_value max_execution_time  120
</Directory>
EOF


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README.urpmi INSTALL README HOWTO-Icecast TODO CREDITS UPGRADE ChangeLog
%{wwwtunez}
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/smixer.conf
%config(noreplace) %{_sysconfdir}/%{name}/
%_bindir/detach
%_bindir/smixer
%_mandir/man1/*
%_datadir/%{name}/*
%attr(0640,root,apache)%_datadir/%{name}/config.inc.php

%pre
%_pre_useradd tunez / /bin/false

%postun
%_postun_userdel tunez
%_postun_webapp

%post
%_post_webapp
