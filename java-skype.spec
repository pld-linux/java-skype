#
# Conditional build:
%bcond_with	tests		# don't build and run tests

%define		srcname		skype-java-api
%include	/usr/lib/rpm/macros.java
Summary:	Skype API for Java, based on Skype4Java library
Name:		java-skype
Version:	1.4
Release:	1
License:	Apache v2.0, EPL v1.0
Group:		Libraries/Java
Source0:	https://github.com/taksan/skype-java-api/tarball/%{srcname}-%{version}/%{srcname}-%{version}.tgz
# Source0-md5:	35de3010cb61e6e39544d8732fd0b958
Patch0:		jni-link.patch
Patch1:		tests-no-win32.patch
%{?with_tests:BuildRequires:	maven}
URL:		http://taksan.github.com/skype-java-api/
BuildRequires:	dbus-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	java-commons-lang >= 2.1
BuildRequires:	java-junit >= 3.8.2
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.553
BuildRequires:	xorg-lib-libX11-devel
Requires:	jpackage-utils
# Not noarch, because we compile only specific platform and arch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Skype API for Java is a library to use Skype API in Java. This library
wraps the transport layer of Skype API and contains application level
APIs.

%prep
%setup -qc
mv taksan-%{srcname}-*/* .
%patch0 -p1
%patch1 -p1

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

# imports win32 stuff
%{__rm} src/test/java/com/skype/connector/ConnectorUtilsTest.java

%build
export JAVA_HOME="%{java_home}"
required_jars='commons-lang'
CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH

install -d target/{classes,test-classes}

%javac -g -encoding UTF-8 -d target/classes $(find src/main -type f -name "*.java")

%if %{with tests}
required_jars='junit'
CLASSPATH=$(build-classpath $required_jars):target/classes
%javac -g -encoding UTF-8 -d target/test-classes $(find src/test -type f -name "*.java")
%endif

# native lib needs classes first
%{__make} -C src-native/src_linux \
	CC="%{__cc}" \
	LINK="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC -I../commons $(pkg-config --cflags dbus-1 dbus-glib-1)" \
	JDK_DIR=%{_jvmdir}/java \
	LFLAGS="%{rpmldflags} -shared" \
	TARGET=$(pwd) \
	X86='libskype_$(IMPLEMENTATION).so' \
	X64='' \
	%{nil}


cd target/classes
%jar cf ../%{srcname}-%{version}.jar $(find -name '*.class')
cd -

%if %{with tests}
# note: src/test/java/com/skype/connector/test/TestConnector fails
mvn test
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_libdir}}

install -p libskype*.so $RPM_BUILD_ROOT%{_libdir}
cp -p target/%{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}

ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar
# old lib names
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/skype4java-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/skype4java.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libskype_dbus.so
%attr(755,root,root) %{_libdir}/libskype_x11.so
%{_javadir}/%{srcname}-%{version}.jar
%{_javadir}/%{srcname}.jar
%{_javadir}/skype4java-%{version}.jar
%{_javadir}/skype4java.jar
