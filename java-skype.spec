%define		srcname		skype4java
%include	/usr/lib/rpm/macros.java
Summary:	Skype4Java - Skype API for Java
Summary(pl.UTF-8):	-
Name:		java-%{srcname}
Version:	1.0
Release:	0.1
License:	CPL v1.0
Group:		Libraries/Java
#Source0:	http://sourceforge.jp/frs/redir.php?m=iij&f=%2Fskype%2F21999%2Fskype_1.0.zip
Source0:	http://iij.dl.sourceforge.jp/skype/21999/skype_%{version}.zip
# Source0-md5:	16eaa53ec0c977bc49cd2d009cde42bf
URL:		http://sourceforge.jp/projects/skype/
BuildRequires:	eclipse-swt
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.553
%if %(locale -a | grep -q '^en_US$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Skype4Java (a.k.a Skype API for Java) is a library to use Skype API in
Java. This library wraps the transport layer of Skype API and contains
application level APIs.

%prep
%setup -qc

find -name '*.class' | xargs rm -v
find -name '*.jar' | xargs rm -v
find -name '*.dll' | xargs rm -v
find -name '*.zip' | xargs rm -v

find -name windows | xargs rm -vr
find -name src_win | xargs rm -vr
find -name osx | xargs rm -vr
find -name src_osx | xargs rm -vr

# add empty dirs for build.xml
install -d skype/lib/osx

%build
cd skype
%ant

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p skype/release/%{srcname}_linux.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_javadir}/%{srcname}-%{version}.jar
%{_javadir}/%{srcname}.jar
