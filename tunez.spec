%define wwwtunez %{_var}/www/%{name}

# TODO rewrite configure_tunez in perl to avoid the duplication of configuration
# try to have more autodetection and stuff like good default value

Summary: MP3/Ogg Vorbis jukebox that works with a voting system
Name:    tunez
Version: 1.21
Release: 12
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
Requires(pre):  apache-conf >= 2.0.54
Requires(pre):  apache-mpm >= 2.0.54
Requires(pre):	rpm-helper
Requires:       apache-mod_php php-xml
Requires:	php-curl
Requires:	php-mysql
Requires:	ices

%define debug_package %{nil}

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
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_mandir}/man1/
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
mkdir -p %{buildroot}/%{_datadir}/tunez
mkdir -p %{buildroot}/%wwwtunez

#Installing Tunez
mv html/* %{buildroot}/%wwwtunez
rm -rf html

cp %SOURCE1 %{buildroot}/%{_datadir}/tunez
cp tmixer/smixer %{buildroot}/%{_bindir}
cp tmixer/smixer.conf %{buildroot}/%{_sysconfdir}
cp tmixer/man/smixer.1 %{buildroot}/%{_mandir}/man1
cp detach-1.2/detach %{buildroot}/%{_bindir}
cp detach-1.2/detach.1 %{buildroot}/%{_mandir}/man1

rm -rf detach-1.2
rm -rf tmixer
# useless code
rm -Rf tunezsrv

cp -av * %{buildroot}/%{_datadir}/tunez
rm -f %{buildroot}/%{_datadir}/tunez/README.urpmi

mv %{buildroot}/%_datadir/%{name}/config.inc.php %{buildroot}/%{_sysconfdir}/%{name}/
ln -s %{_sysconfdir}/%{name}/config.inc.php %{buildroot}/%_datadir/%{name}/config.inc.php

cp %SOURCE3 %{buildroot}/%{_sysconfdir}/%{name}/


# apache configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf <<EOF
Alias /%{name} %{wwwtunez}
<Directory %{wwwtunez}>
    Allow from all
    php_value max_execution_time  120
</Directory>
EOF

%pre
%_pre_useradd tunez / /bin/false


%postun
%_postun_userdel tunez

%files
%doc README.urpmi INSTALL README HOWTO-Icecast TODO CREDITS UPGRADE ChangeLog
%{wwwtunez}
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/smixer.conf
%config(noreplace) %{_sysconfdir}/%{name}/
%_bindir/detach
%_bindir/smixer
%_mandir/man1/*
%_datadir/%{name}/*
#% attr(0640,root,apache)%_datadir/%{name}/config.inc.php
