# TODO
# - rename just to java-skype ?
# - drop .jar extracing for shared lib, load it directly:
#   src/main/java/com/skype/connector/ConnectorUtils.java (loadLibrary)
%define		srcname		skype4java
%include	/usr/lib/rpm/macros.java
Summary:	Skype4Java - Skype API for Java
Name:		java-%{srcname}
Version:	1.3
Release:	0.1
License:	Apache v2.0, EPL v1.0
Group:		Libraries/Java
Source0:	https://github.com/taksan/skype-java-api/tarball/skype-java-api-%{version}/skype-java-api-%{version}.tgz
# Source0-md5:	7358dc4381a7d594a7b799422810cdf5
# http://mvnrepository.com/artifact/com.github.taksan/skype-java-api
URL:		http://taksan.github.com/skype-java-api/
#BuildRequires:	eclipse-swt
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.553
BuildRequires:	java-commons-lang >= 2.1
BuildRequires:	java-junit >= 3.8.2
%if %(locale -a | grep -q '^en_US$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
Requires:	jpackage-utils
# Not noarch, because we compile only specific platform and arch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Skype4Java (a.k.a Skype API for Java) is a library to use Skype API in
Java. This library wraps the transport layer of Skype API and contains
application level APIs.

%prep
%setup -qc
mv taksan-skype-java-api-*/* .

find -name '*.class' | xargs -r rm -v
find -name '*.jar' | xargs -r rm -v
find -name '*.dll' | xargs -r rm -v
find -name '*.zip' | xargs -r rm -v
find -name '*.so' | xargs -r rm -v
find -name '*.jnilib' | xargs -r rm -v
find -name 'Skype.Framework' | xargs -r rm -v

find -name windows | xargs -r rm -vr
find -name src_win32 | xargs -r rm -vr
find -name win32 | xargs -r rm -vr
find -name osx | xargs rm -vr
find -name src_osx | xargs rm -vr

%build
export JAVA_HOME="%{java_home}"

# compile classes
mvn compile test-compile

# native lib needs classes first
%ifarch %{ix86}
target=x86
%endif
%ifarch %{x8664}
target=x64
%endif
%{__make} -C src-native/src_linux libskype_$target.so \
	CC="%{__cc} %{rpmcppflags} %{rpmcflags} -fPIC" \
	LINK="%{__cc}" \
	LFLAGS="%{rpmldflags} -shared"

# make final jar
mvn package

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p target/skype-java-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
ln -s skype-java-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/skype-java-api.jar
# old lib names
ln -s skype-java-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s skype-java-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%{_javadir}/%{srcname}-%{version}.jar
%{_javadir}/%{srcname}.jar
%{_javadir}/skype-java-api-%{version}.jar
%{_javadir}/skype-java-api.jar
