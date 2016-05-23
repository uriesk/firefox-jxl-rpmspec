# Use system nspr/nss?
%define system_nss        1

# Use system sqlite?
%define system_sqlite     1
%define system_ffi        1

# Build for Gtk3?
%define toolkit_gtk3      1

# Use system cairo?
%define system_cairo      0

# Use system libvpx?
%if 0%{?fedora} > 23
%define system_libvpx      1
%else
%define system_libvpx      0
%endif

# Use system libicu?
%if 0%{?fedora} > 23
%define system_libicu      1
%else
%define system_libicu      0
%endif

# Hardened build?
%if 0%{?fedora} > 20
%define hardened_build    1
%else
%define hardened_build    0
%endif

%define system_jpeg       1

%ifarch %{ix86} x86_64
%define run_tests         0
%else
%define run_tests         0
%endif

# Build as a debug package?
%define debug_build       0

%define default_bookmarks_file  %{_datadir}/bookmarks/default-bookmarks.html
%define firefox_app_id  \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}
# Minimal required versions
%global cairo_version 1.13.1
%global freetype_version 2.1.9
%global libnotify_version 0.7.0
%if %{?system_libvpx}
%global libvpx_version 1.4.0
%endif

%if %{?system_nss}
%global nspr_version 4.10.10
%global nspr_build_version %(pkg-config --silence-errors --modversion nspr 2>/dev/null || echo 65536)
%global nss_version 3.19.2
%global nss_build_version %(pkg-config --silence-errors --modversion nss 2>/dev/null || echo 65536)
%endif

%if %{?system_sqlite}
%global sqlite_version 3.8.4.2
# The actual sqlite version (see #480989):
%global sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo 65536)
%endif

%global mozappdir     %{_libdir}/%{name}
%global mozappdirdev  %{_libdir}/%{name}-devel-%{version}
%global langpackdir   %{mozappdir}/langpacks
%global tarballdir    %{name}-%{version}

%define official_branding       1
%define build_langpacks         1

%define enable_mozilla_crashreporter       0
%if !%{debug_build}
%ifarch %{ix86} x86_64
# Temporary disable to catch Gtk3 crashes in Fedora (mozbz#1239962)
%define enable_mozilla_crashreporter       0
%endif
%endif

Summary:        Mozilla Firefox Web browser
Name:           firefox
Version:        46.0.1
Release:        7%{?pre_tag}%{?dist}
URL:            https://www.mozilla.org/firefox/
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Internet
Source0:        https://archive.mozilla.org/pub/firefox/releases/%{version}%{?pre_version}/source/firefox-%{version}%{?pre_version}.source.tar.xz
%if %{build_langpacks}
Source1:        firefox-langpacks-%{version}%{?pre_version}-20160503.tar.xz
%endif
Source10:       firefox-mozconfig
Source12:       firefox-redhat-default-prefs.js
Source20:       firefox.desktop
Source21:       firefox.sh.in
Source23:       firefox.1
Source24:       mozilla-api-key
Source25:       firefox-symbolic.svg

#Build patches
Patch0:         firefox-install-dir.patch
Patch3:         mozilla-build-arm.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=814879#c3
Patch18:        xulrunner-24.0-jemalloc-ppc.patch
# workaround linking issue on s390 (JSContext::updateMallocCounter(size_t) not found)
Patch19:        xulrunner-24.0-s390-inlines.patch
Patch20:        firefox-build-prbool.patch
Patch21:        firefox-ppc64le.patch
Patch24:        firefox-debug.patch
Patch25:        rhbz-1219542-s390-build.patch

# Fedora specific patches
# Unable to install addons from https pages
Patch204:        rhbz-966424.patch
Patch215:        firefox-enable-addons.patch
Patch219:        rhbz-1173156.patch
Patch221:        firefox-fedora-ua.patch
Patch222:        firefox-gtk3-20.patch
Patch223:        rhbz-1291190-appchooser-crash.patch
Patch224:        mozilla-1170092.patch

# Upstream patches
Patch304:        mozilla-1253216.patch
Patch305:        mozilla-1245076.patch
Patch306:        mozilla-1245076-1.patch
Patch400:        mozilla-1255590.patch
Patch402:        mozilla-1196777.patch
Patch403:        mozilla-1216658.patch
Patch404:        mozilla-1270046.patch
# Remove when mozbz#1269319 lands
Patch405:        mozilla-1245783.patch

# Debian patches
Patch500:        mozilla-440908.patch

%if %{?system_nss}
BuildRequires:  pkgconfig(nspr) >= %{nspr_version}
BuildRequires:  pkgconfig(nss) >= %{nss_version}
BuildRequires:  nss-static >= %{nss_version}
%endif
%if %{?system_cairo}
BuildRequires:  pkgconfig(cairo) >= %{cairo_version}
%endif
BuildRequires:  pkgconfig(libpng)
%if %{?system_jpeg}
BuildRequires:  libjpeg-devel
%endif
BuildRequires:  zip
BuildRequires:  bzip2-devel
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libIDL-2.0)
%if %{toolkit_gtk3}
BuildRequires:  pkgconfig(gtk+-3.0)
%endif
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(krb5)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(freetype2) >= %{freetype_version}
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(hunspell)
BuildRequires:  pkgconfig(libstartup-notification-1.0)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(libnotify) >= %{libnotify_version}
BuildRequires:  pkgconfig(dri)
BuildRequires:  pkgconfig(libcurl)
%if %{?system_libvpx}
BuildRequires:  libvpx-devel >= %{libvpx_version}
%endif
BuildRequires:  autoconf213
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(gconf-2.0)
BuildRequires:  yasm

Requires:       mozilla-filesystem
%if %{?system_nss}
Requires:       nspr >= %{nspr_build_version}
Requires:       nss >= %{nss_build_version}
%endif

BuildRequires:  desktop-file-utils
BuildRequires:  system-bookmarks
%if %{?system_sqlite}
BuildRequires:  pkgconfig(sqlite3) >= %{sqlite_version}
Requires:       sqlite >= %{sqlite_build_version}
%endif

%if %{?system_ffi}
BuildRequires:  pkgconfig(libffi)
%endif

%if %{?run_tests}
BuildRequires:  xorg-x11-server-Xvfb
%endif

Obsoletes:      mozilla <= 37:1.7.13
Provides:       webclient

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

%if %{enable_mozilla_crashreporter}
%global moz_debug_prefix %{_prefix}/lib/debug
%global moz_debug_dir %{moz_debug_prefix}%{mozappdir}
%global uname_m %(uname -m)
%global symbols_file_name %{name}-%{version}.en-US.%{_os}-%{uname_m}.crashreporter-symbols.zip
%global symbols_file_path %{moz_debug_dir}/%{symbols_file_name}
%global _find_debuginfo_opts -p %{symbols_file_path} -o debugcrashreporter.list
%global crashreporter_pkg_name mozilla-crashreporter-%{name}-debuginfo
%package -n %{crashreporter_pkg_name}
Summary: Debugging symbols used by Mozilla's crash reporter servers
Group: Development/Debug
%description -n %{crashreporter_pkg_name}
This package provides debug information for Firefox, for use by
Mozilla's crash reporter servers.  If you are trying to locally
debug %{name}, you want to install %{name}-debuginfo instead.
%files -n %{crashreporter_pkg_name} -f debugcrashreporter.list
%defattr(-,root,root)
%endif

%if %{run_tests}
%global testsuite_pkg_name mozilla-%{name}-testresults
%package -n %{testsuite_pkg_name}
Summary: Results of testsuite
Group: Development/Debug
%description -n %{testsuite_pkg_name}
This package contains results of tests executed during build.
%files -n %{testsuite_pkg_name}
/test_results
%defattr(-,root,root)
%endif

#---------------------------------------------------------------------

%prep
%setup -q -c
cd %{tarballdir}

# Build patches, can't change backup suffix from default because during build
# there is a compare of config and js/config directories and .orig suffix is
# ignored during this compare.
%patch0  -p1

%patch18 -p2 -b .jemalloc-ppc
%patch19 -p2 -b .s390-inlines
%patch20 -p1 -b .prbool
%patch21 -p2 -b .ppc64le
%patch24 -p1 -b .debug
%ifarch s390
%patch25 -p1 -b .rhbz-1219542-s390
%endif

%patch3  -p1 -b .arm

# For branding specific patches.

# Fedora patches
%patch204 -p2 -b .966424
%patch215 -p1 -b .addons
%patch219 -p2 -b .rhbz-1173156
%patch221 -p2 -b .fedora-ua
%if 0%{?fedora} > 22
%patch223 -p1 -b .appchooser-crash
%endif
%patch224 -p1 -b .1170092
%if 0%{?fedora} > 23
%patch304 -p2 -b .1253216
%patch222 -p1 -b .gtk3-20
%endif
%patch305 -p1 -b .1245076
%patch306 -p1 -b .1245076-1
%patch400 -p1 -b .1255590
%patch402 -p1 -b .1196777
%patch403 -p1 -b .1216658
%patch404 -p1 -b .1270046
%patch405 -p1 -b .1245783

# Debian extension patch
%patch500 -p1 -b .440908

%{__rm} -f .mozconfig
%{__cp} %{SOURCE10} .mozconfig
%if %{official_branding}
echo "ac_add_options --enable-official-branding" >> .mozconfig
%endif
%{__cp} %{SOURCE24} mozilla-api-key

%if %{toolkit_gtk3}
echo "ac_add_options --enable-default-toolkit=cairo-gtk3" >> .mozconfig
%else
echo "ac_add_options --enable-default-toolkit=cairo-gtk2" >> .mozconfig
%endif

%if %{?system_nss}
echo "ac_add_options --with-system-nspr" >> .mozconfig
echo "ac_add_options --with-system-nss" >> .mozconfig
%else
echo "ac_add_options --without-system-nspr" >> .mozconfig
echo "ac_add_options --without-system-nss" >> .mozconfig
%endif

%if %{?system_sqlite}
echo "ac_add_options --enable-system-sqlite" >> .mozconfig
%else
echo "ac_add_options --disable-system-sqlite" >> .mozconfig
%endif

%if %{?system_cairo}
echo "ac_add_options --enable-system-cairo" >> .mozconfig
%else
echo "ac_add_options --disable-system-cairo" >> .mozconfig
%endif

%if %{?system_ffi}
echo "ac_add_options --enable-system-ffi" >> .mozconfig
%endif

%ifarch %{arm}
echo "ac_add_options --disable-elf-hack" >> .mozconfig
%endif

%if %{?debug_build}
echo "ac_add_options --enable-debug" >> .mozconfig
echo "ac_add_options --disable-optimize" >> .mozconfig
echo "ac_add_options --enable-dtrace" >> .mozconfig
%else
echo "ac_add_options --disable-debug" >> .mozconfig
%ifarch ppc64le aarch64
echo 'ac_add_options --enable-optimize="-g -O2"' >> .mozconfig
%else
echo "ac_add_options --enable-optimize" >> .mozconfig
%endif
%endif

# s390(x) fails to start with jemalloc enabled
%ifarch s390 s390x
echo "ac_add_options --disable-jemalloc" >> .mozconfig
%endif

%ifarch armv7hl
echo "ac_add_options --with-arch=armv7-a" >> .mozconfig
echo "ac_add_options --with-float-abi=hard" >> .mozconfig
echo "ac_add_options --with-fpu=vfpv3-d16" >> .mozconfig
echo "ac_add_options --disable-elf-hack" >> .mozconfig
echo "ac_add_options --disable-ion" >> .mozconfig
%endif
%ifarch armv7hnl
echo "ac_add_options --with-arch=armv7-a" >> .mozconfig
echo "ac_add_options --with-float-abi=hard" >> .mozconfig
echo "ac_add_options --with-fpu=neon" >> .mozconfig
echo "ac_add_options --disable-elf-hack" >> .mozconfig
echo "ac_add_options --disable-ion" >> .mozconfig
echo "ac_add_options --disable-yarr-jit" >> .mozconfig
%endif
%ifarch armv5tel
echo "ac_add_options --with-arch=armv5te" >> .mozconfig
echo "ac_add_options --with-float-abi=soft" >> .mozconfig
echo "ac_add_options --disable-elf-hack" >> .mozconfig
echo "ac_add_options --disable-ion" >> .mozconfig
echo "ac_add_options --disable-yarr-jit" >> .mozconfig
%endif

%ifnarch %{ix86} x86_64
echo "ac_add_options --disable-webrtc" >> .mozconfig
%endif

%if !%{enable_mozilla_crashreporter}
echo "ac_add_options --disable-crashreporter" >> .mozconfig
%endif

%if %{?run_tests}
echo "ac_add_options --enable-tests" >> .mozconfig
%endif

%if !%{?system_jpeg}
echo "ac_add_options --without-system-jpeg" >> .mozconfig
%else
echo "ac_add_options --with-system-jpeg" >> .mozconfig
%endif

%if %{?system_libvpx}
echo "ac_add_options --with-system-libvpx" >> .mozconfig
%else
echo "ac_add_options --without-system-libvpx" >> .mozconfig
%endif

%if %{?system_libicu}
echo "ac_add_options --with-system-icu" >> .mozconfig
%else
echo "ac_add_options --without-system-icu" >> .mozconfig
%endif

#---------------------------------------------------------------------

%build
%if %{?system_sqlite}
# Do not proceed with build if the sqlite require would be broken:
# make sure the minimum requirement is non-empty, ...
sqlite_version=$(expr "%{sqlite_version}" : '\([0-9]*\.\)[0-9]*\.') || exit 1
# ... and that major number of the computed build-time version matches:
case "%{sqlite_build_version}" in
  "$sqlite_version"*) ;;
  *) exit 1 ;;
esac
%endif

cd %{tarballdir}

# Update the various config.guess to upstream release for aarch64 support
find ./ -name config.guess -exec cp /usr/lib/rpm/config.guess {} ';'

# -fpermissive is needed to build with gcc 4.6+ which has become stricter
#
# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
#
# Disable C++ exceptions since Mozilla code is not exception-safe
#
MOZ_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS" | %{__sed} -e 's/-Wall//')
#rhbz#1037063
# -Werror=format-security causes build failures when -Wno-format is explicitly given
# for some sources
# Explicitly force the hardening flags for Firefox so it passes the checksec test;
# See also https://fedoraproject.org/wiki/Changes/Harden_All_Packages
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -Wformat-security -Wformat -Werror=format-security"
%if 0%{?fedora} > 23
# Disable null pointer gcc6 optimization in gcc6 (rhbz#1328045)
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -fno-delete-null-pointer-checks"
%endif
# Use hardened build?
%if %{?hardened_build}
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -fPIC -Wl,-z,relro -Wl,-z,now"
%endif
%if %{?debug_build}
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-O2//')
%endif
%ifarch s390
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-g/-g1/')
# If MOZ_DEBUG_FLAGS is empty, firefox's build will default it to "-g" which
# overrides the -g1 from line above and breaks building on s390
# (OOM when linking, rhbz#1238225)
export MOZ_DEBUG_FLAGS=" "
%endif
%ifarch s390 %{arm} ppc aarch64
MOZ_LINK_FLAGS="-Wl,--no-keep-memory -Wl,--reduce-memory-overheads"
%endif
export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS=$MOZ_OPT_FLAGS
export LDFLAGS=$MOZ_LINK_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

MOZ_SMP_FLAGS=-j1
# On x86 architectures, Mozilla can build up to 4 jobs at once in parallel,
# however builds tend to fail on other arches when building in parallel.
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le aarch64
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -ge 2 ] && MOZ_SMP_FLAGS=-j2
[ "$RPM_BUILD_NCPUS" -ge 4 ] && MOZ_SMP_FLAGS=-j4
[ "$RPM_BUILD_NCPUS" -ge 8 ] && MOZ_SMP_FLAGS=-j8
%endif

make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS" MOZ_SERVICES_SYNC="1"

# create debuginfo for crash-stats.mozilla.com
%if %{enable_mozilla_crashreporter}
#cd %{moz_objdir}
make -C objdir buildsymbols
%endif

%if %{?run_tests}
%if %{?system_nss}
ln -s /usr/bin/certutil objdir/dist/bin/certutil
ln -s /usr/bin/pk12util objdir/dist/bin/pk12util

%endif
mkdir test_results
./mach --log-no-times check-spidermonkey &> test_results/check-spidermonkey || true
./mach --log-no-times check-spidermonkey &> test_results/check-spidermonkey-2nd-run || true
./mach --log-no-times cppunittest &> test_results/cppunittest || true
xvfb-run ./mach --log-no-times crashtest &> test_results/crashtest || true
./mach --log-no-times gtest &> test_results/gtest || true
xvfb-run ./mach --log-no-times jetpack-test &> test_results/jetpack-test || true
# not working right now ./mach marionette-test &> test_results/marionette-test || true
xvfb-run ./mach --log-no-times mochitest-a11y &> test_results/mochitest-a11y || true
xvfb-run ./mach --log-no-times mochitest-browser &> test_results/mochitest-browser || true
xvfb-run ./mach --log-no-times mochitest-chrome &> test_results/mochitest-chrome || true
xvfb-run ./mach --log-no-times mochitest-devtools &> test_results/mochitest-devtools || true
xvfb-run ./mach --log-no-times mochitest-plain &> test_results/mochitest-plain || true
xvfb-run ./mach --log-no-times reftest &> test_results/reftest || true
xvfb-run ./mach --log-no-times webapprt-test-chrome &> test_results/webapprt-test-chrome || true
xvfb-run ./mach --log-no-times webapprt-test-content &> test_results/webapprt-test-content || true
./mach --log-no-times webidl-parser-test &> test_results/webidl-parser-test || true
xvfb-run ./mach --log-no-times xpcshell-test &> test_results/xpcshell-test || true
%if %{?system_nss}
rm -f  objdir/dist/bin/certutil
rm -f  objdir/dist/bin/pk12util
%endif

%endif
#---------------------------------------------------------------------

%install
cd %{tarballdir}

# set up our default bookmarks
%{__cp} -p %{default_bookmarks_file} objdir/dist/bin/browser/defaults/profile/bookmarks.html

# Make sure locale works for langpacks
%{__cat} > objdir/dist/bin/browser/defaults/preferences/firefox-l10n.js << EOF
pref("general.useragent.locale", "chrome://global/locale/intl.properties");
EOF

DESTDIR=$RPM_BUILD_ROOT make -C objdir install

%{__mkdir_p} $RPM_BUILD_ROOT{%{_libdir},%{_bindir},%{_datadir}/applications}

desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE20}

# set up the firefox start script
%{__rm} -rf $RPM_BUILD_ROOT%{_bindir}/firefox
%{__cat} %{SOURCE21} > $RPM_BUILD_ROOT%{_bindir}/firefox
%{__chmod} 755 $RPM_BUILD_ROOT%{_bindir}/firefox

%{__install} -p -D -m 644 %{SOURCE23} $RPM_BUILD_ROOT%{_mandir}/man1/firefox.1

%{__rm} -f $RPM_BUILD_ROOT/%{mozappdir}/firefox-config
%{__rm} -f $RPM_BUILD_ROOT/%{mozappdir}/update-settings.ini

for s in 16 22 24 32 48 256; do
    %{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps
    %{__cp} -p browser/branding/official/default${s}.png \
               $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/firefox.png
done

# Install hight contrast icon
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/symbolic/apps
%{__cp} -p %{SOURCE25} \
           $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/symbolic/apps

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/%{name}.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<!--
BugReportURL: https://bugzilla.mozilla.org/show_bug.cgi?id=1071061
SentUpstream: 2014-09-22
-->
<application>
  <id type="desktop">firefox.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <description>
    <p>
      Bringing together all kinds of awesomeness to make browsing better for you.
      Get to your favorite sites quickly – even if you don’t remember the URLs.
      Type your term into the location bar (aka the Awesome Bar) and the autocomplete
      function will include possible matches from your browsing history, bookmarked
      sites and open tabs.
    </p>
    <!-- FIXME: Needs another couple of paragraphs -->
  </description>
  <url type="homepage">http://www.mozilla.org/en-US/</url>
  <screenshots>
    <screenshot type="default">https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/firefox/a.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/firefox/b.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/firefox/c.png</screenshot>
  </screenshots>
  <!-- FIXME: change this to an upstream email address for spec updates
  <updatecontact>someone_who_cares@upstream_project.org</updatecontact>
   -->
</application>
EOF

echo > ../%{name}.lang
%if %{build_langpacks}
# Extract langpacks, make any mods needed, repack the langpack, and install it.
%{__mkdir_p} $RPM_BUILD_ROOT%{langpackdir}
%{__tar} xf %{SOURCE1}
for langpack in `ls firefox-langpacks/*.xpi`; do
  language=`basename $langpack .xpi`
  extensionID=langpack-$language@firefox.mozilla.org
  %{__mkdir_p} $extensionID
  unzip -qq $langpack -d $extensionID
  find $extensionID -type f | xargs chmod 644

  cd $extensionID
  zip -qq -r9mX ../${extensionID}.xpi *
  cd -

  %{__install} -m 644 ${extensionID}.xpi $RPM_BUILD_ROOT%{langpackdir}
  language=`echo $language | sed -e 's/-/_/g'`
  echo "%%lang($language) %{langpackdir}/${extensionID}.xpi" >> ../%{name}.lang
done
%{__rm} -rf firefox-langpacks

# Install langpack workaround (see #707100, #821169)
function create_default_langpack() {
language_long=$1
language_short=$2
cd $RPM_BUILD_ROOT%{langpackdir}
ln -s langpack-$language_long@firefox.mozilla.org.xpi langpack-$language_short@firefox.mozilla.org.xpi
cd -
echo "%%lang($language_short) %{langpackdir}/langpack-$language_short@firefox.mozilla.org.xpi" >> ../%{name}.lang
}

# Table of fallbacks for each language
# please file a bug at bugzilla.redhat.com if the assignment is incorrect
create_default_langpack "bn-IN" "bn"
create_default_langpack "es-AR" "es"
create_default_langpack "fy-NL" "fy"
create_default_langpack "ga-IE" "ga"
create_default_langpack "gu-IN" "gu"
create_default_langpack "hi-IN" "hi"
create_default_langpack "hy-AM" "hy"
create_default_langpack "nb-NO" "nb"
create_default_langpack "nn-NO" "nn"
create_default_langpack "pa-IN" "pa"
create_default_langpack "pt-PT" "pt"
create_default_langpack "sv-SE" "sv"
create_default_langpack "zh-TW" "zh"
%endif # build_langpacks


%{__mkdir_p} $RPM_BUILD_ROOT/%{mozappdir}/browser/defaults/preferences

# System config dir
%{__mkdir_p} $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/pref

# System extensions
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/mozilla/extensions/%{firefox_app_id}
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/mozilla/extensions/%{firefox_app_id}

# Copy over the LICENSE
%{__install} -p -c -m 644 LICENSE $RPM_BUILD_ROOT/%{mozappdir}

# Use the system hunspell dictionaries
%{__rm} -rf ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries
ln -s %{_datadir}/myspell ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries

# Enable crash reporter for Firefox application
%if %{enable_mozilla_crashreporter}
sed -i -e "s/\[Crash Reporter\]/[Crash Reporter]\nEnabled=1/" $RPM_BUILD_ROOT/%{mozappdir}/application.ini
# Add debuginfo for crash-stats.mozilla.com
%{__mkdir_p} $RPM_BUILD_ROOT/%{moz_debug_dir}
%{__cp} objdir/dist/%{symbols_file_name} $RPM_BUILD_ROOT/%{moz_debug_dir}
%endif

%if %{run_tests}
# Add debuginfo for crash-stats.mozilla.com
%{__mkdir_p} $RPM_BUILD_ROOT/test_results
%{__cp} test_results/* $RPM_BUILD_ROOT/test_results
%endif

# Default
%{__cp} %{SOURCE12} ${RPM_BUILD_ROOT}%{mozappdir}/browser/defaults/preferences

# Remove copied libraries to speed up build
rm -f ${RPM_BUILD_ROOT}%{mozappdirdev}/sdk/lib/libmozjs.so
rm -f ${RPM_BUILD_ROOT}%{mozappdirdev}/sdk/lib/libmozalloc.so
rm -f ${RPM_BUILD_ROOT}%{mozappdirdev}/sdk/lib/libxul.so
#---------------------------------------------------------------------

# Moves defaults/preferences to browser/defaults/preferences
%pretrans -p <lua>
require 'posix'
require 'os'
if (posix.stat("%{mozappdir}/browser/defaults/preferences", "type") == "link") then
  posix.unlink("%{mozappdir}/browser/defaults/preferences")
  posix.mkdir("%{mozappdir}/browser/defaults/preferences")
  if (posix.stat("%{mozappdir}/defaults/preferences", "type") == "directory") then
    for i,filename in pairs(posix.dir("%{mozappdir}/defaults/preferences")) do
      os.rename("%{mozappdir}/defaults/preferences/"..filename, "%{mozappdir}/browser/defaults/preferences/"..filename)
    end
    f = io.open("%{mozappdir}/defaults/preferences/README","w")
    if f then
      f:write("Content of this directory has been moved to %{mozappdir}/browser/defaults/preferences.")
      f:close()
    end
  end
end


%preun
# is it a final removal?
if [ $1 -eq 0 ]; then
  %{__rm} -rf %{mozappdir}/components
  %{__rm} -rf %{mozappdir}/extensions
  %{__rm} -rf %{mozappdir}/plugins
  %{__rm} -rf %{langpackdir}
fi

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/firefox
%{mozappdir}/firefox
%{mozappdir}/firefox-bin
%doc %{_mandir}/man1/*
%dir %{_sysconfdir}/%{name}/*
%dir %{_datadir}/mozilla/extensions/*
%dir %{_libdir}/mozilla/extensions/*
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/applications/*.desktop
%dir %{mozappdir}
%doc %{mozappdir}/LICENSE
%{mozappdir}/browser/chrome
%{mozappdir}/browser/chrome.manifest
%dir %{mozappdir}/browser/components
%{mozappdir}/browser/components/*.so
%{mozappdir}/browser/components/components.manifest
%{mozappdir}/browser/defaults/preferences/firefox-redhat-default-prefs.js
%{mozappdir}/browser/features/loop@mozilla.org.xpi
%{mozappdir}/browser/features/e10srollout@mozilla.org.xpi
%{mozappdir}/browser/features/firefox@getpocket.com.xpi
%attr(644, root, root) %{mozappdir}/browser/blocklist.xml
%dir %{mozappdir}/browser/extensions
%{mozappdir}/browser/extensions/*
%if %{build_langpacks}
%dir %{langpackdir}
%endif
%{mozappdir}/browser/omni.ja
%{mozappdir}/browser/icons
%{mozappdir}/run-mozilla.sh
%{mozappdir}/application.ini
%exclude %{mozappdir}/removed-files
%{_datadir}/icons/hicolor/16x16/apps/firefox.png
%{_datadir}/icons/hicolor/22x22/apps/firefox.png
%{_datadir}/icons/hicolor/24x24/apps/firefox.png
%{_datadir}/icons/hicolor/256x256/apps/firefox.png
%{_datadir}/icons/hicolor/32x32/apps/firefox.png
%{_datadir}/icons/hicolor/48x48/apps/firefox.png
%{_datadir}/icons/hicolor/symbolic/apps/firefox-symbolic.svg
%{mozappdir}/webapprt-stub
%dir %{mozappdir}/webapprt
%{mozappdir}/webapprt/omni.ja
%{mozappdir}/webapprt/webapprt.ini
%if %{enable_mozilla_crashreporter}
%{mozappdir}/crashreporter
%{mozappdir}/crashreporter.ini
%{mozappdir}/Throbber-small.gif
%{mozappdir}/browser/crashreporter-override.ini
%endif
%{mozappdir}/*.so
%if %{toolkit_gtk3}
%{mozappdir}/gtk2/*.so
%endif
%{mozappdir}/defaults/pref/channel-prefs.js
%{mozappdir}/dependentlibs.list
%{mozappdir}/dictionaries
%{mozappdir}/omni.ja
%{mozappdir}/platform.ini
%{mozappdir}/plugin-container
%{mozappdir}/gmp-clearkey
%exclude %{_includedir}
%exclude %{_libdir}/firefox-devel-%{version}
%exclude %{_datadir}/idl
%if !%{?system_nss}
%{mozappdir}/libfreebl3.chk
%{mozappdir}/libnssdbm3.chk
%{mozappdir}/libsoftokn3.chk
%endif

#---------------------------------------------------------------------

%changelog
* Mon May 23 2016 Martin Stransky <stransky@redhat.com> - 46.0.1-7
- Rebuilt for new bookmarks (rhbz#1338010)
- Fixed build issue in Gtk3.20 patch

* Fri May 20 2016 Martin Stransky <stransky@redhat.com> - 46.0.1-6
- Updated Gtk3.20 patch - fixed tooltips

* Thu May 19 2016 Martin Stransky <stransky@redhat.com> - 46.0.1-5
- Added a fix for mozbz#1245783 - gcc6.1 crashes in JIT

* Thu May 12 2016 Martin Stransky <stransky@redhat.com> - 46.0.1-4
- Added fix for rhbz#1332821 - Crash on "Select" in "Open with" dialog

* Tue May 10 2016 Martin Stransky <stransky@redhat.com> - 46.0.1-3
- Added patch for rhbz#1332875 - new Samba auth reponse

* Thu May 5 2016 Martin Stransky <stransky@redhat.com> - 46.0.1-2
- Disable dark theme until we support it correctly (mozbz#1216658)

* Tue May 3 2016 Martin Stransky <stransky@redhat.com> - 46.0.1-1
- Updated to 46.0.1

* Mon May 2 2016 Martin Stransky <stransky@redhat.com> - 46.0-6
- Removed gstreamer config as it's no longer used.
  See rhbz#1331496 for details.
- Updated Firefox project URL (rhbz#1329014)

* Thu Apr 28 2016 Martin Stransky <stransky@redhat.com> - 46.0-5
- Added fix for rhbz#1322626 - wrong focused window

* Wed Apr 27 2016 Martin Stransky <stransky@redhat.com> - 46.0-4
- Added fix for rhbz#1315225 - ppc64le/aarch64 build fixes

* Wed Apr 27 2016 Martin Stransky <stransky@redhat.com> - 46.0-3
- Fixed missing langpacks

* Tue Apr 26 2016 Martin Stransky <stransky@redhat.com> - 46.0-2
- Disabled system libicu on Fedora 22/23

* Mon Apr 25 2016 Martin Stransky <stransky@redhat.com> - 46.0-1
- Updated to 46.0 (B5)

* Thu Apr 21 2016 Martin Stransky <stransky@redhat.com> - 45.0.2-5
- Added patch for mozbz#1263145

* Wed Apr 20 2016 Martin Stransky <stransky@redhat.com> - 45.0.2-4
- Updated scrollbar code for Gtk 3.20

* Mon Apr 18 2016 Martin Stransky <stransky@redhat.com> - 45.0.2-2
- Disabled gcc6 null this optimization (rhbz#1328045)

* Mon Apr 11 2016 Martin Stransky <stransky@redhat.com> - 45.0.2-1
- New upstream (45.0.2)

* Tue Apr 5 2016 Martin Stransky <stransky@redhat.com> - 45.0.1-6
- Fixed rhbz#1322669 - Flash widgets are not displayed

* Tue Apr 5 2016 Martin Stransky <stransky@redhat.com> - 45.0.1-5
- Polished gcc6 patches

* Tue Mar 22 2016 Martin Stransky <stransky@redhat.com> - 45.0.1-4
- Fixed rhbz#1321355 - broken flash plugin
- Added /etc/firefox/pref dir for easy configuration

* Mon Mar 21 2016 Martin Stransky <stransky@redhat.com> - 45.0.1-3
- Provide system wide config dir (mozbz#1170092)
- Allow lock preferences from .js files (mozbz#440908)

* Mon Mar 21 2016 Martin Stransky <stransky@redhat.com> - 45.0.1-2
- Fixed rhbz#1293874 - use a Debian patch for disabled extension
  signing

* Wed Mar 16 2016 Martin Stransky <stransky@redhat.com> - 45.0.1-1
- Update to 45.0.1

* Tue Mar 15 2016 Martin Stransky <stransky@redhat.com> - 45.0-5
- Updated gtk3.20 patch

* Fri Mar 4 2016 Martin Stransky <stransky@redhat.com> - 45.0-4
- Update to 45.0 (B2)

* Thu Mar 3 2016 Martin Stransky <stransky@redhat.com> - 45.0-3
- Added run-time fix for JIT (mozbz#1253216)

* Wed Mar 2 2016 Martin Stransky <stransky@redhat.com> - 45.0-2
- Disabled system libvpx on Fedora 22 where is 1.3.0

* Wed Mar 2 2016 Martin Stransky <stransky@redhat.com> - 45.0-1
- Update to 45.0

* Thu Feb 11 2016 Martin Stransky <stransky@redhat.com> - 44.0.2-3
- Added patch for mozbz#1205199

* Thu Feb 11 2016 Martin Stransky <stransky@redhat.com> - 44.0.2-2
- Update to 44.0.2 (B3)

* Wed Feb 10 2016 Martin Stransky <stransky@redhat.com> - 44.0.2-1
- Update to 44.0.2 (B2)

* Mon Feb 8 2016 Martin Stransky <stransky@redhat.com> - 44.0.1-2
- Update to 44.0.1 (B2)

* Fri Feb 5 2016 Martin Stransky <stransky@redhat.com> - 44.0.1-1
- Update to 44.0.1

* Thu Feb  4 2016 Jan Horak <jhorak@redhat.com> - 44.0-6
- Workaround for crash when closing application chooser and Fedora 23
  (rhbz#1291190)

* Tue Feb 2 2016 Martin Stransky <stransky@redhat.com> - 44.0-5
- GCC 6.0 build patch
- Disabled mozilla crashreporter to catch Gtk3 crashes

* Mon Feb 1 2016 Martin Stransky <stransky@redhat.com> - 44.0-4
- Removed pulseaudio hard dependency (rhbz#1303620)

* Tue Jan 26 2016 Ralph Giles <giles@mozilla.com> - 44.0-3
- Medadata update, require pulseaudio

* Mon Jan 25 2016 Martin Stransky <stransky@redhat.com> - 44.0-2
- Update to 44.0 B3

* Thu Jan 21 2016 Jan Horak <jhorak@redhat.com> - 44.0-1
- Update to 44.0

* Thu Jan 14 2016 Martin Stransky <stransky@redhat.com> - 43.0.4-2
- Fixed the progress bar rendering

* Thu Jan 14 2016 Martin Stransky <stransky@redhat.com> - 43.0.4-1
- Update to 43.0.4

* Wed Jan 13 2016 Martin Stransky <stransky@redhat.com> - 43.0.3-5
- Updated progress bars rendering for Gtk 3.20

* Thu Jan 7 2016 Martin Stransky <stransky@redhat.com> - 43.0.3-4
- Added fix for mozbz#1234026 - crashes on XWayland

* Tue Jan 05 2016 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 43.0.3-3
- Fix build on AArch64.

* Mon Jan 4 2016 Martin Stransky <stransky@redhat.com> - 43.0.3-2
- Enabled Skia (rhbz#1282134)

